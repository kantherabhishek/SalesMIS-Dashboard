import mysql.connector
import datetime
import dash
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Group
from dash import Dash, dcc, html, Input, Output, State
from dash_table import DataTable


# MySQL connection details
host = "localhost"
user = "root"
password = "root"
database = "my_sales"

# Establish MySQL connection
conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
cursor = conn.cursor()

# Fetch sales data from the MySQL database
sales_query = "SELECT * FROM sales"
cursor.execute(sales_query)
sales_data = cursor.fetchall()
sales_columns = [desc[0] for desc in cursor.description]
sales = pd.DataFrame(sales_data, columns=sales_columns)

# Fetch products data from the MySQL database
products_query = "SELECT * FROM products"
cursor.execute(products_query)
products_data = cursor.fetchall()
products_columns = [desc[0] for desc in cursor.description]
products = pd.DataFrame(products_data, columns=products_columns)

# Calculate the daily sales count
daily_sales_number = (
    sales["invoice_id"].groupby(sales["date"]).nunique().rename("Number of sales")
)

# Create a line chart for daily sales count
figure_daily_sales_number = px.line(
    daily_sales_number, title="Daily number of sales"
).update_layout(title_font_size=30)

# Calculate the 7-day moving average of daily revenue
m7d_mean_revenue = (
    sales["total_amount"].groupby(sales["date"]).sum().rolling(7, min_periods=7).mean()
)

# Create a line chart for 7-day moving average of daily revenue
figure_m7d_mean_revenue = px.line(
    m7d_mean_revenue, title="7-day moving average of daily revenue"
).update_layout(title_font_size=30)

# Create a pie chart for revenue distribution by product line
figure_product_line = px.pie(
    sales.groupby("product_line")["total_amount"].sum().reset_index(),
    names="product_line",
    values="total_amount",
    title="Product lines ratio"
).update_layout(title_font_size=30)

# Create a bar chart for revenue breakdown by city
figure_revenue_bycity = px.bar(
    sales.groupby("city")["total_amount"].sum().reset_index(),
    x="city",
    y="total_amount",
    title="Revenue by city"
).update_layout(title_font_size=30)

# Create a revenue breakdown table
sums = (
    sales[["total_amount", "tax", "cost_of_goods_sold", "gross_income"]]
    .sum()
    .rename("Value")
    .reset_index()
    .rename(columns={"index": "Item"})
)

sums_datatable = html.Div(
    [
        html.P(),
        html.Label(
            "Revenue breakdown",
            style={"font-size": "30px", "color": "grey"},
        ),
        html.P(),
        DataTable(
            data=sums.to_dict("records"),
            columns=[{"name": col, "id": col} for col in ["Item", "Value"]],
        ),
    ]
)



# Create the Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

view_sales_content = dbc.Card(
    dbc.CardBody(
        [
            html.H4("View Sales Data"),
            DataTable(
                id="view-sales-data",
                data=sales.to_dict("records"),
                sort_action='native',
                columns=[
                    {"name": col, "id": col}
                    for col in sales_columns
                ],
                style_data={
                    "whiteSpace": "normal",
                    "height": "auto",
                    "maxHeight": "none",
                },
                style_cell={"textAlign": "left"},
                style_table={"overflowY": "scroll"},
                page_size=20,
                editable=False,  # Disable editing for the table
                row_deletable=True,  # Enable row deletion
            ),
        ]
    )
)



view_product_line_content = dbc.Card(
    dbc.CardBody(
        [
            html.H4("View Product Line"),
            DataTable(
                id="view-product-line",
                data=products.to_dict("records"),
                sort_action='native',
                columns=[
                    {"name": col, "id": col}
                    for col in products_columns
                ],
                style_data={
                    "whiteSpace": "normal",
                    "height": "auto",
                    "maxHeight": "none",
                },
                style_cell={"textAlign": "left"},
                style_table={"overflowY": "scroll"},
                page_size=20,
                editable=False,  # Disable editing for the table
                row_deletable=True,  # Enable row deletion
                tooltip_duration=None,
            ),
        ]
    )
)


# Add Sales tab content
add_sales_content = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Add Sales"),
            html.Label("Invoice ID"),
            dbc.Input(id="invoice-id-input", type="text", placeholder="Enter Invoice ID"),
            html.Label("Branch"),
            dbc.Select(
                id="branch-select",
                options=[
                    {"label": "A", "value": "A"},
                    {"label": "B", "value": "B"},
                    {"label": "C", "value": "C"},
                    {"label": "D", "value": "D"},
                    {"label": "E", "value": "E"},
                    {"label": "F", "value": "F"},
                    {"label": "G", "value": "G"},
                ],
                placeholder="Select Branch",
            ),
            html.Label("City"),
            dbc.Select(
                id="city-select",
                options=[
                    {"label": "Kolkata", "value": "Kolkata"},
                    {"label": "Delhi", "value": "Delhi"},
                    {"label": "Pune", "value": "Pune"},
                    {"label": "Mumbai", "value": "Mumbai"},
                    {"label": "Chennai", "value": "Chennai"},
                    {"label": "Bangalore", "value": "Bangalore"},
                ],
                placeholder="Select City",
            ),
            html.Label("Customer Type"),
            dbc.Select(
                id="customer-type-select",
                options=[
                    {"label": "Member", "value": "Member"},
                    {"label": "Non-Member", "value": "Non-Member"},
                ],
                placeholder="Select Customer Type",
            ),
            html.Label("Gender"),
            dbc.Select(
                id="gender-select",
                options=[
                    {"label": "Male", "value": "Male"},
                    {"label": "Female", "value": "Female"},
                    {"label": "Other", "value": "Other"},
                ],
                placeholder="Select Gender",
            ),
            html.Label("Product Line"),
            dcc.Dropdown(
                id="product-line-dropdown",
                options=[
                    {"label": row, "value": row} for row in products["product_line"].unique() if row is not None
                ],
                placeholder="Select Product Line",
            ),
            html.Label("Unit Price"),
            dbc.Input(id="unit-price-input", type="number", placeholder="Enter Unit Price"),
            html.Label("Quantity"),
            dbc.Input(id="quantity-input", type="number", placeholder="Enter Quantity"),
            html.Label("Payment"),
            dbc.Select(
                id="payment-select",
                options=[
                    {"label": "eWallet", "value": "eWallet"},
                    {"label": "Cash", "value": "Cash"},
                    {"label": "Credit Card", "value": "Credit Card"},
                ],
                placeholder="Select Payment",
            ),
            html.Label("Customer Satisfaction"),
            dbc.Select(
                id="customer-satisfaction-select",
                options=[
                    {"label": "1", "value": "1"},
                    {"label": "2", "value": "2"},
                    {"label": "3", "value": "3"},
                    {"label": "4", "value": "4"},
                    {"label": "5", "value": "5"},
                ],
                placeholder="Select Customer Satisfaction",
            ),html.P(""),
            dbc.Button("Submit", id="submit-sales-btn", color="primary", className="mr-2"),
        ]
    )
)


# Add Sales tab content
add_porduct_line_content = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Add Product Line"),
            html.Label("Product Line"),
            dbc.Input(id="product-line-input", type="text", placeholder="Enter Product Line"),
            html.Label("Product Category"),
            dbc.Input(id="product-category-input", type="text", placeholder="Enter Product Category"),
            html.Label("Product Tax"),
            dbc.Input(id="product-tax-input", type="number", placeholder="Enter tax amount  eg. for 10% use 0.1"),
            html.Label("Product COGS (% of total amount)"),
            dbc.Input(id="product-cogs-input", type="number", placeholder="Enter COGS eg. for 62% use 0.62"),
            html.P(""),
            dbc.Button("Submit", id="submit-product-btn", color="primary", className="mr-2"),
        ]
    )
)



# Create the tabs
tabs = dbc.Tabs(
    [
        dbc.Tab(label="Sales KPIs", children=[
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(figure=figure_product_line),
                        width=4
                    ),
                    dbc.Col(
                        dcc.Graph(figure=figure_revenue_bycity),
                        width=4
                    ),
                    dbc.Col(
                        sums_datatable,
                        width=4
                    ),
                ],
                justify="center",
                align="center",
                style={"padding": "20px"},
            ),
            dcc.Graph(figure=figure_daily_sales_number),
            dcc.Graph(figure=figure_m7d_mean_revenue),
        ]),
        dbc.Tab(label="Add Sales", children=[
            add_sales_content,
        ]),
        dbc.Tab(label="View Sales Data", children=[
            view_sales_content,
        ]),
        dbc.Tab(label="Add Product Line", children=[
            add_porduct_line_content,
        ]),
        dbc.Tab(label="View Product Line", children=[
            view_product_line_content,
        ]),
    ],
    id="tabs",
    active_tab="Sales KPIs",
)


# Create the layout
app.layout = html.Div(
    [
        html.H1(
        children='Welcome to Sales MIS Dashboard',
        style={
            'textAlign': 'center'
        }
    ),
        tabs,
    ],
    style={"margin": "auto", "max-width": "100%"},
)

# Submit sales form
@app.callback(
    Output("invoice-id-input", "value"),
    Output("branch-select", "value"),
    Output("city-select", "value"),
    Output("customer-type-select", "value"),
    Output("gender-select", "value"),
    Output("product-line-dropdown", "value"),
    Output("unit-price-input", "value"),
    Output("quantity-input", "value"),
    Output("payment-select", "value"),
    Output("customer-satisfaction-select", "value"),
    [
        Input("submit-sales-btn", "n_clicks"),
    ],
    [
        State("invoice-id-input", "value"),
        State("branch-select", "value"),
        State("city-select", "value"),
        State("customer-type-select", "value"),
        State("gender-select", "value"),
        State("product-line-dropdown", "value"),
        State("unit-price-input", "value"),
        State("quantity-input", "value"),
        State("payment-select", "value"),
        State("customer-satisfaction-select", "value"),
    ],
)


def submit_sales_form(
    n_clicks, invoice_id, branch, city, customer_type, gender, product_line, unit_price, quantity, payment, customer_satisfaction
):
    if n_clicks:
        # Calculate tax and total amount
        tax_query = f"SELECT product_tax FROM products WHERE product_line = '{product_line}'"
        cursor.execute(tax_query)
        tax_result = cursor.fetchone()
        if tax_result is not None:
            tax = tax_result[0]
            total_amount = (unit_price * quantity) + (unit_price * quantity * tax)

            # Calculate cost of goods sold and gross income
            cogs_query = f"SELECT product_cogs FROM products WHERE product_line = '{product_line}'"
            cursor.execute(cogs_query)
            cogs_result = cursor.fetchone()
            if cogs_result is not None:
                cogs = cogs_result[0]
                cost_of_goods_sold = total_amount * cogs
                gross_income = cost_of_goods_sold * quantity

                # Insert sales record into the MySQL database
                insert_query = f"""
                INSERT INTO sales (invoice_id, branch, city, customer_type, gender, product_line, unit_price, quantity, tax,
                total_amount, date, time, payment, cost_of_goods_sold, gross_margin_percentage, gross_income,
                stratification_rating)
                VALUES ('{invoice_id}', '{branch}', '{city}', '{customer_type}', '{gender}', '{product_line}',
                {unit_price}, {quantity}, {tax}, {total_amount}, CURDATE(), CURTIME(), '{payment}', {cost_of_goods_sold},
                100 - ({cost_of_goods_sold} / {total_amount} * 100), {gross_income}, '{customer_satisfaction}')
                """
                cursor.execute(insert_query)
                conn.commit()

                # Show success message
                print("Sales record added successfully!")

                return "", None, None, None, None, None, None, None, None, None
            else:
                print(f"No cost of goods sold found for product line: {product_line}")
        else:
            print(f"No tax found for product line: {product_line}")

    return invoice_id, branch, city, customer_type, gender, product_line, unit_price, quantity, payment, customer_satisfaction


# Submit Products form
@app.callback(
    Output("product-line-input", "value"),
    Output("product-category-input", "value"),
    Output("product-tax-input", "value"),
    Output("product-cogs-input", "value"),
    [
        Input("submit-product-btn", "n_clicks"),
    ],
    [
        State("product-line-input", "value"),
        State("product-category-input", "value"),
        State("product-tax-input", "value"),
        State("product-cogs-input", "value"),
    ],
)

def submit_products_form(
    n_clicks, product_line, product_category, product_tax, product_cogs
):
    if n_clicks:
        # Calculate tax and total amount
        product_query = f"INSERT INTO products (product_line, product_category, product_tax, product_cogs) VALUES ('{product_line}', '{product_category}', {product_tax}, {product_cogs})"
        cursor.execute(product_query)
        conn.commit()
        print("Sales record added successfully!")

        return "", None, None, None
    return product_line, product_category, product_tax, product_cogs

# Handle row deletion in the sales table
@app.callback(
    Output("view-product-line", "data"),
    [Input("view-product-line", "data_previous")],
    [State("view-product-line", "data")],
)
def delete_sales_row(previous_data, current_data):
    if previous_data and current_data and len(previous_data) > len(current_data):
        # Identify the deleted rows by comparing the lengths of previous and current data
        deleted_ids = set(d["id"] for d in previous_data) - set(d["id"] for d in current_data)
        if deleted_ids:
            # Filter out the deleted rows
            products_filtered = [row for row in current_data if row["id"] not in deleted_ids]
            
            # Delete the rows from the SQL Server database
            conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
            cursor = conn.cursor()
            for deleted_id in deleted_ids:
                delete_query = "DELETE FROM products WHERE id = %s"
                cursor.execute(delete_query, (deleted_id,))
            conn.commit()
            cursor.close()
            conn.close()
            
            return products_filtered

    return current_data

# Handle row deletion in the sales table
@app.callback(
    Output("view-sales-data", "data"),
    [Input("view-sales-data", "data_previous")],
    [State("view-sales-data", "data")],
)
def delete_sales_row(previous_data, current_data):
    if previous_data and current_data and len(previous_data) > len(current_data):
        # Identify the deleted rows by comparing the lengths of previous and current data
        deleted_ids = set(d["id"] for d in previous_data) - set(d["id"] for d in current_data)
        if deleted_ids:
            # Filter out the deleted rows
            sales_filtered = [row for row in current_data if row["id"] not in deleted_ids]
            
            # Delete the rows from the SQL Server database
            conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
            cursor = conn.cursor()
            for deleted_id in deleted_ids:
                delete_query = "DELETE FROM sales WHERE id = %s"
                cursor.execute(delete_query, (deleted_id,))
            conn.commit()
            cursor.close()
            conn.close()
            
            return sales_filtered

    return current_data

# Run the Dash application
if __name__ == "__main__":
    app.run_server(debug=True)
