import mysql.connector
from mysql.connector import Error

#database Connection Configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'product_management_db',
    'user': 'root', 
    'password': 'Lakshman@1'    
}

#Connect to the database
try:
    db = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )
    cursor = db.cursor()
    print(f"Connected to database: {DB_CONFIG['database']}")
except Error as e:
    print(f"Error connecting to MySQL database: {e}")
    # Exit if connection fails, as other functions won't work
    exit(1)


#CRUD Operations for Products

# INSERT
def insert_product(name, description, price, category, stock_quantity, manufacturer, release_date, rating):
    query = """
    INSERT INTO Products (name, description, price, category,stock_quantity, manufacturer, release_date, rating)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (name, description, price, category, stock_quantity, manufacturer, release_date, rating)
    cursor.execute(query, values)
    db.commit()
    print("Product inserted!")

# SELECT ALL
def get_all_products_simple():
    cursor.execute("SELECT * FROM Products")
    results = cursor.fetchall()
    print("All Products")
    for row in results:
        print(row)
    return results # Return results

# SELECT BY ID
def get_product_by_id_simple(product_id):
    query = "SELECT * FROM Products WHERE id = %s"
    cursor.execute(query, (product_id,))
    result = cursor.fetchone()
    if result:
        print(f"Product found: {result}")
    else:
        print(f"Product ID {product_id} not found.")
    return result

# UPDATE
def update_product_title(product_id, new_title):
    query = "UPDATE Products SET name = %s WHERE id = %s"
    values = (new_title, product_id)
    cursor.execute(query, values)
    db.commit()
    if cursor.rowcount > 0:
        print(f"Product ID {product_id} updated!")
    else:
        print(f"Product ID {product_id} not found or no changes made.")

# DELETE
def delete_product_simple(product_id):
    query = "DELETE FROM Products WHERE id = %s"
    cursor.execute(query, (product_id,))
    db.commit()
    if cursor.rowcount > 0:
        print(f"Product ID {product_id} deleted!")
    else:
        print(f"Product ID {product_id} not found.")


#Testing
if __name__ == "__main__":
    print("\nInitial Products")
    get_all_products_simple()

    # Insert a product
    print("\nInserting a new product")
    insert_product(
        "Gaming Headset Pro",
        "High-fidelity sound, noise-cancelling microphone.",
        79.99,
        "Audio",
        50,
        "SoundBlaster",
        "2024-03-10",
        4.6
    )
    get_all_products_simple()

    # Insert another product for testing delete later
    insert_product(
        "Smartwatch Lite",
        "Fitness tracking, notifications, long battery.",
        120.00,
        "Wearables",
        100,
        "WearTech",
        "2023-09-01",
        4.3
    )
    get_all_products_simple()

    print("\nFetching product by ID (e.g., ID 1)")
    get_product_by_id_simple(1)

    print("\nUpdating a product (e.g., ID 1)")
    update_product_title(1, "Gaming Headset Pro Max")
    get_product_by_id_simple(1) # Verify update

    print("\nDeleting a product (e.g., ID 2)")
    delete_product_simple(2)
    get_all_products_simple()

    # Attempt to delete a non-existent product
    delete_product_simple(999)


#Close the cursor and database connection at the very end
print("\nClosing database connection.")
cursor.close()
db.close()
print("Connection closed.")
