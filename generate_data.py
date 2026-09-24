import random
from datetime import datetime, timedelta

import pandas as pd

random.seed(42)

products = {
    "Electronics": [("Wireless Headphones", 2499), ("Smart Watch", 3999), ("Bluetooth Speaker", 1799)],
    "Fashion": [("Men's T-Shirt", 799), ("Women's Handbag", 1899), ("Running Shoes", 2499)],
    "Home & Kitchen": [("Water Bottle", 499), ("Coffee Maker", 3499), ("Bedsheet Set", 1299)],
    "Beauty": [("Face Serum", 999), ("Hair Dryer", 1999), ("Perfume", 1499)],
    "Sports": [("Yoga Mat", 899), ("Cricket Bat", 1799), ("Dumbbell Set", 2999)],
}

cities = ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad"]
payment_methods = ["UPI", "Credit Card", "Debit Card", "Cash on Delivery", "Wallet"]

records = []
start_date = datetime(2024, 1, 1)

for order_number in range(1, 5001):
    category, category_products = random.choice(list(products.items()))
    product, price = random.choice(category_products)
    quantity = random.randint(1, 4)
    discount = random.choice([0, 0, 0.05, 0.10, 0.15])
    order_date = start_date + timedelta(days=random.randint(0, 635))

    records.append(
        {
            "Order ID": f"ORD{order_number:05d}",
            "Customer ID": f"CUST{random.randint(1, 800):04d}",
            "Order Date": order_date.date(),
            "City": random.choice(cities),
            "Category": category,
            "Product": product,
            "Unit Price": price,
            "Quantity": quantity,
            "Discount": discount,
            "Sales": round(price * quantity * (1 - discount), 2),
            "Payment Method": random.choice(payment_methods),
            "Delivery Days": random.randint(1, 7),
        }
    )

    df = pd.DataFrame(records)
df.to_csv("ecommerce_sales_data.csv", index=False)

print(f"Created {len(df):,} orders for {df['Customer ID'].nunique():,} customers.")