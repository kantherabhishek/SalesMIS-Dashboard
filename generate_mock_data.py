import random
import datetime
import mysql.connector

def generate_product_name():
    # Generate a random product name
    adjective = random.choice(['Red', 'Blue', 'Green', 'Yellow', 'Black', 'White'])
    noun = random.choice(['Shirt', 'Shoes', 'Hat', 'Watch', 'Bag'])
    return f"{adjective} {noun}"

def generate_price():
    # Generate a random price between 10 and 1000
    return round(random.uniform(10, 1000), 2)

def create_invoice_id():
    return "INV" + str(random.randint(1000, 9999))

def create_branch():
    return chr(random.randint(65, 71))  # ASCII values for A to G

def get_random_indian_city():
    cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Ahmedabad", "Pune", "Surat", "Jaipur"]
    return random.choice(cities)

def get_random_customer_type():
    return random.choice(["Member", "Non-Member"])

def get_random_gender():
    return random.choice(["Male", "Female"])

def get_random_category():
    product_category = ["Textile Cat A", "Textile Cat B", "Textile Cat C", "Textile Cat D", "Textile Cat E", "Textile Cat F", "Textile Cat G", "Textile Cat H", "Textile Cat I", "Textile Cat J"]
    return random.choice(product_category)


def get_random_unit_price():
    return random.randint(100, 500000)

def get_random_quantity():
    return random.randint(1, 10)

def calculate_tax(unit_price):
    return unit_price * 0.18

def calculate_total(unit_price, quantity, tax):
    return unit_price * quantity + tax

def get_random_date():
    start_date = datetime.datetime(2022, 1, 1)
    end_date = datetime.datetime(2022, 12, 31)
    random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime("%Y-%m-%d")

def get_random_time():
    return datetime.time(random.randint(9, 18), random.randint(0, 59)).strftime("%H:%M")

def get_random_payment():
    return random.choice(["Cash", "eWallet"])

def calculate_cost_of_goods_sold(unit_price):
    return random.uniform(0.8, 0.85) * unit_price

def calculate_gross_margin_percentage(cost_of_goods_sold, total_amount):
    return (total_amount - cost_of_goods_sold) / total_amount * 100

def calculate_gross_income(cost_of_goods_sold, quantity):
    return cost_of_goods_sold * quantity

def get_random_stratification_rating():
    return random.randint(1, 5)


# Connect to the MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="test"
)

# Create the sales and products tables if they don't exist
mycursor = mydb.cursor()
mycursor.execute("SHOW TABLES LIKE 'sales'")
sales_table_exists = mycursor.fetchone()
mycursor.execute("SHOW TABLES LIKE 'products'")
products_table_exists = mycursor.fetchone()

if not sales_table_exists:
    mycursor.execute('''
        CREATE TABLE sales (
            id INT AUTO_INCREMENT PRIMARY KEY,
            invoice_id VARCHAR(255),
            branch VARCHAR(1),
            city VARCHAR(255),
            customer_type VARCHAR(255),
            gender VARCHAR(255),
            product_line VARCHAR(255),
            unit_price DECIMAL(10, 2),
            quantity INT,
            tax DECIMAL(10, 2),
            total_amount DECIMAL(10, 2),
            date DATE,
            time TIME,
            payment VARCHAR(255),
            cost_of_goods_sold DECIMAL(10, 2),
            gross_margin_percentage DECIMAL(10, 2),
            gross_income DECIMAL(10, 2),
            stratification_rating INT
        )
    ''')

if not products_table_exists:
    mycursor.execute('''
        CREATE TABLE products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_line VARCHAR(255),
            product_category VARCHAR(100),
            product_tax DECIMAL(2, 2),
            product_cogs DECIMAL(2, 2)
        )
    ''')

# Check if there is data in the sales and products tables
mycursor.execute("SELECT COUNT(*) FROM sales")
sales_data_count = mycursor.fetchone()[0]
mycursor.execute("SELECT COUNT(*) FROM products")
products_data_count = mycursor.fetchone()[0]

# Insert mock data into the products table if there is no data
if products_data_count == 0:
    # Generate 20 textile products with random names and categories
    products_data = []
    for _ in range(20):
        product_name = generate_product_name()
        product_category = get_random_category()
        product_tax = round(random.uniform(0.01, 0.20), 2)
        product_cogs = round(random.uniform(0.50, 0.80), 2)
        product_data = (product_name, product_category, product_tax, product_cogs)
        products_data.append(product_data)

    # Insert the products data into the products table
    insert_query = "INSERT INTO products (product_line, product_category, product_tax, product_cogs) VALUES (%s, %s, %s, %s)"
    mycursor.executemany(insert_query, products_data)
    mydb.commit()

# Insert mock data into the sales table if there is no data
if sales_data_count == 0:
    # Generate 1000 mock sales invoices
    data_set = []
    for _ in range(1000):
        invoice = {
            "invoice_id": "INV" + str(random.randint(1000, 9999)),
            "branch": chr(random.randint(65, 71)),  # ASCII values for A to G
            "city": random.choice(["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Ahmedabad", "Pune", "Surat", "Jaipur"]),
            "customer_type": random.choice(["Member", "Non-Member"]),
            "gender": random.choice(["Male", "Female"]),
            "product_line": get_random_category(),
            "unit_price": random.randint(100, 500000),
            "quantity": random.randint(1, 10),
            "tax": 0,
            "total_amount": 0,
            "date": get_random_date(),
            "time": get_random_time(),
            "payment": random.choice(["Cash", "eWallet"]),
            "cost_of_goods_sold": 0,
            "gross_margin_percentage": 0,
            "gross_income": 0,
            "stratification_rating": random.randint(1, 5)
        }
        invoice["tax"] = calculate_tax(invoice["unit_price"])
        invoice["total_amount"] = calculate_total(
            invoice["unit_price"], invoice["quantity"], invoice["tax"]
        )
        invoice["cost_of_goods_sold"] = calculate_cost_of_goods_sold(invoice["unit_price"])
        invoice["gross_margin_percentage"] = calculate_gross_margin_percentage(
            invoice["cost_of_goods_sold"], invoice["total_amount"]
        )
        invoice["gross_income"] = calculate_gross_income(
            invoice["cost_of_goods_sold"], invoice["quantity"]
        )
        data_set.append(invoice)

    # Insert the mock data into the sales table
    sql = "INSERT INTO sales (invoice_id, branch, city, customer_type, gender, product_line, unit_price, quantity, tax, total_amount, date, time, payment, cost_of_goods_sold, gross_margin_percentage, gross_income, stratification_rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = [
        (
            invoice["invoice_id"], invoice["branch"], invoice["city"], invoice["customer_type"],
            invoice["gender"], invoice["product_line"], invoice["unit_price"], invoice["quantity"],
            invoice["tax"], invoice["total_amount"], invoice["date"], invoice["time"], invoice["payment"],
            invoice["cost_of_goods_sold"], invoice["gross_margin_percentage"], invoice["gross_income"],
            invoice["stratification_rating"]
        ) for invoice in data_set
    ]
    mycursor.executemany(sql, values)
    mydb.commit()
