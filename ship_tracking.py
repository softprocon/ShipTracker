"""
ship_tracker_beta.py
Author: Ebenezer Agyei-Yeboah
Description: A Python script for tracking ships around oil spills and ranking ships.
Date: September 2023
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pandas import read_csv, to_datetime, Timedelta, set_option
import geopandas as gpd
from shapely.geometry import MultiPoint
import datetime as dt
from scipy.spatial import cKDTree

set_option('display.max_rows', None)

def oil_tracker(oil_path, ship_gdf, time_interval, buffer_size, selected_day=None):
    fig, ax = plt.subplots(figsize=(14, 8))
    m = Basemap(projection='merc',
                ax=ax,
                llcrnrlat=-14.25,
                urcrnrlat=-10.25,
                llcrnrlon=-40,
                urcrnrlon=-33,
                epsg=4326 ,
                resolution='f'
                )
    
   # Read shapefiles for cities
    br_admin = gpd.read_file('./data/BR_Municipios_2020.shp')
    br_admin_filtered = br_admin.cx[-39.5:-32.5, -14.25:10.5]
    br_admin_filtered.plot(ax=ax, color="white", linewidth=1, edgecolor='#c3c3d6', facecolor="none")
    
    affected_cities = gpd.read_file(f'./data/bahia_coast_cities1.geojson')
    affected_cities = affected_cities.to_crs(epsg=4326)
    for x, y, label in zip(affected_cities.geometry.centroid.x, affected_cities.geometry.centroid.y, affected_cities['NM_MUN']):
        plt.text(x-0.1, y, label, fontsize=8, ha='right', va='center')
    plt.scatter(affected_cities.geometry.centroid.x, affected_cities.geometry.centroid.y, marker='.', color='blue', s=30, label='City Marker')

    m.drawparallels(np.arange(-14.25, -10.25, 0.5), labels=[1, 0, 0, 0], fontsize=10, labelstyle='+/-', linewidth=0.1)
    m.drawmeridians(np.arange(-40, -33, 1), labels=[1, 1, 0, 1], fontsize=10, labelstyle='+/-', linewidth=0.1)
        
    nA = np.array(list(ship_gdf.geometry.apply(lambda x: (x.x, x.y))))
    nB = np.array(list(oil_path.geometry.apply(lambda x: (x.x, x.y))))
    btree = cKDTree(nB)
    distance, idx = btree.query(nA, k=1)
    oil_path_nearest = oil_path.iloc[idx.squeeze()].reset_index(drop=True)
    ship_gdf['distance'] = distance.squeeze()
    ship_gdf['distance'] = round(ship_gdf['distance'] * 111, 2)

    buffer_size_deg = round(buffer_size/111, 2)
    tra_buffer_gdf = gpd.GeoDataFrame(geometry=oil_path['geometry'].buffer(buffer_size_deg, resolution=16), crs='EPSG:4326') 
    within_buffered_area = ship_gdf[ship_gdf['distance'] <= buffer_size]
    within_buffered_area['day'] = within_buffered_area['dh'].dt.day
    
    time_interval_minutes = time_interval / 2
    oil_path['day'] = oil_path['time'].dt.day
    time_interval = Timedelta(minutes=time_interval)
    reference_times = oil_path.groupby('day')['time'].min()
    filtered_dfs = within_buffered_area.groupby('day').apply(
        lambda df: df[(df['dh'] >= reference_times.loc[df['day'].iloc[0]] - time_interval / 2) &
                      (df['dh'] < reference_times.loc[df['day'].iloc[0]] + time_interval / 2)]
    )

    oil_centroids = oil_path.groupby('day')['geometry'].apply(lambda x: MultiPoint(x.tolist()).centroid)

    # Calculate the time difference between the ship's timestamp and the oil spill timestamp
    oil_times = oil_path.groupby('day')['time'].min()
    filtered_dfs['time_diff'] = filtered_dfs.apply(lambda row: (row['dh'] - oil_times[row['day']]).total_seconds() / 60, axis=1)  # time difference in minutes
    unique_filtered_dfs = filtered_dfs.drop_duplicates()

    # Ranking ships in time and distance
    normalized_distance = unique_filtered_dfs['distance'] / unique_filtered_dfs['distance'].max()
    normalized_time = abs(unique_filtered_dfs['time_diff']) / abs(unique_filtered_dfs['time_diff']).max()
    unique_filtered_dfs = unique_filtered_dfs.copy()
    unique_filtered_dfs['Score'] = (1 + 99 * (normalized_distance + normalized_time)).astype(int)
    lowest_rank_indices = unique_filtered_dfs.groupby(['mmsi', 'nome_navio'])['Score'].idxmin()
    unique_filtered_dfs = unique_filtered_dfs.loc[lowest_rank_indices]
    unique_filtered_dfs['Ship_rank'] = unique_filtered_dfs['Score'].rank(method='min').astype(int)
    unique_filtered_dfs.sort_values(by='Ship_rank', ascending=True, inplace=True)
    ship_ranking = unique_filtered_dfs
    # ship_ranking.to_csv('./ranking.csv', index=False)
    
    ### Plotting data to map
    start_date = oil_path['time'].min()
    end_date = oil_path['time'].max()
    ax.set_title(f'{start_date.strftime("%d-%b-%Y")} to {end_date.strftime("%d-%b-%Y")}', fontsize=10)

    ax.set_xlabel('Longitude', labelpad=20, fontsize=10)
    ax.set_ylabel('Latitude', labelpad=40, fontsize=10)

    tra_buffer_gdf.plot(ax=ax, linewidth=2, color='#00242e')
    oil_path.plot(ax=ax, color='#4efaff')
    ship_ranking.plot(ax=ax, c='#b00000', marker='o', markersize=50, linewidth=1, edgecolor='black')
    
    print(ship_ranking.drop(['geometry', 'day'], axis=1))
    plt.show()
    
    # return ship_ranking

# plt.show()
# Arguements
ship_data = read_csv(f'./data/tanker_csv.csv')
ship_gdf = gpd.GeoDataFrame(ship_data, crs='EPSG:4326', geometry=gpd.points_from_xy(ship_data['lon'], ship_data['lat']))
ship_gdf['dh'] = to_datetime(ship_gdf['dh'], format="%Y-%m-%d %H:%M:%S", errors='coerce')

oil_path = gpd.read_file(f'./data/Traj_Backw_CI-Auto_NC-Auto.geojson')
selected_day = 21
time_interval = 30
buffer_size = 10
oil_tracker(oil_path, ship_gdf, time_interval, buffer_size)