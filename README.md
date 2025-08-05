Exploratory Data Analysis (EDA) Tool

Project Description

This project is an interactive web application for Exploratory Data Analysis (EDA) built using Streamlit. It provides a user-friendly interface for data analysts and data scientists to quickly upload a CSV file, perform initial data cleaning, and generate key visualizations and statistical summaries.

The tool is designed to streamline the initial steps of any data analysis project by offering the following features:

File Upload: Easily upload CSV files directly into the application.

Data Overview: Get an instant summary of the dataset, including the number of rows and columns, data types, and a preview of the first few rows.

Data Cleaning: Interactive options to remove duplicate rows and handle missing values (e.g., remove rows with any or all missing data).

Outlier Detection: Automatically identifies and visualizes outliers in numeric columns using the Interquartile Range (IQR) method.

Univariate Analysis: Analyze single columns to understand their distribution. For numeric columns, it shows a histogram and descriptive statistics. For categorical columns, it displays value counts.

Bivariate Analysis: Explore the relationship between two columns. It generates scatter plots for two numeric columns and box plots for a numeric and a categorical column.

Live Demo
https://auto-eda-tool-galitneu.streamlit.app/

How to Use the Project
To run this project on your local machine, please follow these steps:

1. Prerequisites
Ensure you have Python installed. Then, choose one of the following methods to install the required libraries.

Using Poetry (Recommended)
If you have Poetry installed, navigate to the project directory in your terminal and run the following command. This will create a virtual environment and install all the necessary dependencies from the pyproject.toml and poetry.lock files.

poetry install

Using pip
If you are not using Poetry, you can install the required libraries manually using pip:

pip install streamlit pandas numpy seaborn matplotlib

2. Running the Application
Save the project code as a Python file (e.g., main.py).

Open your terminal or command prompt.

If you used Poetry, first activate the virtual environment by running:

poetry shell

Navigate to the directory where you saved the file.

Run the following command:

streamlit run main.py



3. Using the Tool
Once the application opens in your web browser, use the file uploader to select and upload a CSV file from your computer.

The application will first display a File Overview and Data Cleaning Options.

Choose your desired cleaning options (e.g., remove duplicates) and click the "Apply Cleaning and Analyze" button.

After cleaning, the main analysis interface will appear. Use the Navigation Menu in the sidebar on the left to switch between different analysis views:

General Description: Shows a summary of the cleaned data.

Single Column Analysis: Select a single column to view its statistics and distribution.

Bivariate Analysis: Select two columns to explore their relationship.

File to Execute
The main file to execute is the Python script containing the Streamlit application code. If you saved the code as main.py, this is the file you need to run.

To start the application, run this command in your terminal:

streamlit run main.py
