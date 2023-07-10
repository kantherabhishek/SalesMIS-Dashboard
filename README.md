# Sales MIS Dashboard
The Sales MIS Dashboard is a Python-based web application that provides small business owners with a comprehensive tool to track sales data, visualize key metrics, and make data-driven decisions. This repository contains the code and resources necessary to set up the Sales MIS Dashboard on your local machine.

# Features
  1. Visualize daily sales count, 7-day moving average of daily revenue, revenue distribution by product line, and revenue breakdown by city.
  2. Add new sales records and view existing sales data.
  3. Add new product lines and view existing product line data.

# Installation
  ## Prerequisites
    Python 3.x
    MySQL server (Make sure you have the necessary credentials to connect to the database)
  ## Setup
  1. Clone this repository to your local machine.
  2. Install the required Python libraries by running the following command:
      <code>pip install -r requirements.txt</code>
  3. Import the mock data into the MySQL database:
   #
     python generate_mock_data.py
  4. Create a new database named my_sales in your MySQL server.
  5. Import the sales.csv and products.csv files located in the data directory into the my_sales database. These files contain sample data to populate the sales and products tables respectively.

# Configuration
  ## Open the app.py file in a text editor and modify the following variables with your MySQL database connection details:
    host = "localhost"
    user = "root"
    password = "root"
    database = "my_sales"
# Running the Application
To start the Sales MIS Dashboard, run the following command in your terminal:
    <code>python app.py</code>

The application will be accessible at http://localhost:8050/.

# Usage
1. Sales KPIs: View the line charts representing the daily sales count, 7-day moving average of daily revenue, pie chart showing revenue distribution by product line, and bar chart illustrating revenue breakdown by city.
1. Add Sales: Fill in the required fields to add new sales records.
View Sales Data: Browse and filter existing sales data.
3. Add Product Line: Enter details to add new product lines.
4. View Product Line: Explore and manage existing product line data.

# Contributing
Contributions are welcome! If you have any suggestions, improvements, or bug fixes, please open an issue or submit a pull request.

# License
This project is licensed under the MIT License.

# Acknowledgments
The Sales MIS Dashboard is built using the Dash framework.

The data provided in the sales.csv and products.csv files is for demonstration purposes and can be replaced with actual data for real-world usage.
