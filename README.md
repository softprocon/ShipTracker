## Ship Tracker Beta

### Overview

This repository contains three Python scripts for tracking ships around oil spills and ranking ships based on their proximity and time of detection. The scripts utilize geospatial data, including ship location data and oil spill trajectory data, to provide insights into ship movements during oil spill events.

### Scripts

#### 1. ship_tracker_beta.py

- **Author**: Ebenezer Agyei-Yeboah
- **Description**: This Python script is designed for tracking ships around oil spills and ranking them based on their proximity and time of detection. It uses various geospatial libraries to perform spatial operations and create visualizations on a map.

#### 2. ship_tracking.py

- **Author**: Ebenezer Agyei-Yeboah
- **Description**: This updated version of the ship tracker script is designed for improved functionality. It includes enhancements such as better map visualization, city markers, and improved data processing.

#### 3. ship_tracker_interactive.ipynb

- **Author**: Ebenezer Agyei-Yeboah
- **Description**: This Jupyter Notebook provides an interactive version of the ship tracker. It allows users to adjust parameters like buffer size, time interval, and selected day using widgets. The script provides real-time visualizations and ship ranking information based on user inputs.

### Usage

To use these scripts, follow these steps:

1. Clone the repository to your local machine.

2. Install the required libraries using `pip install -r requirements.txt`.

3. Run the desired script:

   - For the standalone ship tracker scripts (`ship_tracker_beta.py` or `ship_tracker_september_2023.py`), you can execute them using a Python interpreter. Make sure to provide the necessary input data files as specified in the scripts.

   - For the interactive ship tracker (`ship_tracker_interactive.ipynb`), open it in a Jupyter Notebook environment. You can adjust the parameters using the provided widgets and observe the real-time visualizations.

4. Review the results, including ship rankings and map visualizations, to gain insights into ship movements during oil spill events.

### Data Files

The scripts require specific input data files for ship location data (`.csv`) and oil spill trajectory data (`.geojson`). Ensure that you have these data files in the specified locations or update the file paths in the scripts accordingly.

### Dependencies

The scripts rely on several Python libraries, including NumPy, Matplotlib, GeoPandas, Shapely, and Basemap. The `requirements.txt` file lists the necessary dependencies, which can be installed using `pip` (pip install -r requirements.txt).

### Contributions

Contributions to this repository are welcome. Feel free to submit issues, suggest improvements, or fork the repository and create pull requests with enhancements or bug fixes.

### License

This project is licensed under the MIT License. You are free to use, modify, and distribute the code as per the terms of the license.

---

Please refer to the individual script files for more detailed information about their usage and functionality. Enjoy exploring ship tracking and oil spill analysis with these scripts!