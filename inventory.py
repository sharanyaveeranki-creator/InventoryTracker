import sqlite3

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
quantity INTEGER NOT NULL,
price REAL NOT NULL
)
""")
conn.commit()

def add_product():
	name = input("Enter product name: ")
	quantity = int(input("Enter quantity: "))
	price = float(input("Enter price: "))


	cursor.execute(
    	"INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
    	(name, quantity, price)
	)
	conn.commit()
	print("Product added successfully!")


def view_products():
	cursor.execute("SELECT * FROM products")
	products = cursor.fetchall()


	if not products:
    		print("No products found.")
    		return

	print("\nID | Name | Quantity | Price")
	print("-" * 45)

	for product in products:
    		print(f"{product[0]} | {product[1]} | {product[2]} | ₹{product[3]:.2f}")


def search_product():
	product_id = input("Enter product ID to search: ")


	cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
	product = cursor.fetchone()

	if product:
    		print("\nProduct Found!")
    		print("ID:", product[0])
    		print("Name:", product[1])
    		print("Quantity:", product[2])
    		print("Price: ₹{:.2f}".format(product[3]))
	else:
    		print("Product not found.")

def update_product():
	product_id = input("Enter product ID to update: ")


	cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
	product = cursor.fetchone()

	if product:
    		print("Current quantity:", product[2])
    		print("Current price:", product[3])

    		quantity = int(input("Enter new quantity: "))
    		price = float(input("Enter new price: "))

    		cursor.execute(
        		"UPDATE products SET quantity = ?, price = ? WHERE id = ?",
        		(quantity, price, product_id)
    		)
    		conn.commit()
    		print("Product updated successfully!")
	else:
    		print("Product not found.")

def delete_product():
	product_id = input("Enter product ID to delete: ")


	cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
	product = cursor.fetchone()

	if product:
    		cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    		conn.commit()
    		print("Product deleted successfully!")
	else:
    		print("Product not found.")


def low_stock_alert():
	cursor.execute("SELECT * FROM products WHERE quantity < 5")
	products = cursor.fetchall()


	if products:
    		print("\nLOW STOCK PRODUCTS")
    		for product in products:
        		print(f"{product[1]} - Quantity: {product[2]}")
	else:
    		print("No low-stock products.")


def total_inventory_value():
	cursor.execute("SELECT SUM(quantity * price) FROM products")
	total = cursor.fetchone()[0]


	if total is None:
    		total = 0

	print(f"Total Inventory Value: ₹{total:.2f}")


try:
    while True:
        print("\n===== INVENTORY TRACKER =====")
        print("1. Add Product")
        print("2. View Products")
        print("3. Search Product")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. Low Stock Alert")
        print("7. Total Inventory Value")
        print("8. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                add_product()
            elif choice == "2":
                view_products()
            elif choice == "3":
                search_product()
            elif choice == "4":
                update_product()
            elif choice == "5":
                delete_product()
            elif choice == "6":
                low_stock_alert()
            elif choice == "7":
                total_inventory_value()
            elif choice == "8":
                print("Thank you for using Inventory Tracker!")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter numbers correctly.")

finally:
    conn.close()