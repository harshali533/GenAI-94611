import csv


with open("products.csv", "r") as file:
    reader = csv.DictReader(file)
    rows = list(reader)


print("PRODUCT DETAILS")
for row in rows:
    print(f"ID: {row['product_id']}, Product_Name: {row['product_name']}, Category: {row['category']}, "
          f"Price: {row['price']}, Quantity: {row['quantity']}")


print("\nTotal number of rows:", len(rows))


count_above_500 = sum(1 for row in rows if float(row["price"]) > 500)
print("Products priced above 500:", count_above_500)


avg_price = sum(float(row["price"]) for row in rows) / len(rows)
print("Average price of all products:", avg_price)


category = input("\nEnter category to search: ").strip().lower()
print(f"\nProducts in category '{category}':")
found = False
for row in rows:
    if row["category"].strip().lower() == category:
        print(f"- {row['product_name']} (Price: {row['price']}, Qty: {row['quantity']})")
        found = True
if not found:
    print("No products found in this category.")


total_qty = sum(int(row["quantity"]) for row in rows)
print("\nTotal quantity in stock:", total_qty)