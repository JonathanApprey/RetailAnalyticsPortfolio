import pandas as pd
import numpy as np
from faker import Faker
import random
import os

fake = Faker()
Faker.seed(42)  # For reproducibility

def generate_customers(n=100):
    """
    Generates synthetic customer data.
    """
    customers = []
    for i in range(n):
        customers.append({
            "customer_id": i + 1,
            "name": fake.name(),
            "email": fake.email(),
            "state": fake.state_abbr(),
            "signup_date": fake.date_between(start_date='-2y', end_date='today')
        })
    return pd.DataFrame(customers)

def generate_products():
    """
    Generates a fixed list of products relevant to camping/RV.
    """
    products = [
        {"product_id": 101, "name": "4-Person Tent", "category": "Camping Gear", "price": 129.99},
        {"product_id": 102, "name": "Sleeping Bag", "category": "Camping Gear", "price": 49.99},
        {"product_id": 103, "name": "Portable Stove", "category": "Camping Gear", "price": 89.99},
        {"product_id": 104, "name": "RV Water Filter", "category": "RV Accessories", "price": 24.99},
        {"product_id": 105, "name": "Leveling Blocks", "category": "RV Accessories", "price": 34.99},
        {"product_id": 106, "name": "Sewer Hose Kit", "category": "RV Accessories", "price": 59.99},
        {"product_id": 107, "name": "Camping Chair", "category": "Camping Gear", "price": 29.99},
        {"product_id": 108, "name": "LED Lantern", "category": "Accessories", "price": 19.99},
        {"product_id": 109, "name": "First Aid Kit", "category": "Accessories", "price": 39.99},
        {"product_id": 110, "name": "Portable Grill", "category": "Camping Gear", "price": 149.99},
    ]
    return pd.DataFrame(products)

def generate_transactions(customers_df, products_df, n=500):
    """
    Generates synthetic transactions linking customers and products.
    """
    transactions = []
    customer_ids = customers_df['customer_id'].tolist()
    product_ids = products_df['product_id'].tolist()
    
    for i in range(n):
        product_id = random.choice(product_ids)
        price = products_df.loc[products_df['product_id'] == product_id, 'price'].values[0]
        
        # Introduce some noise/dirty data (optional, but requested in brief)
        # For now, we'll keep it relatively clean but ensure dates align
        
        transactions.append({
            "order_id": 1000 + i,
            "customer_id": random.choice(customer_ids),
            "product_id": product_id,
            "date": fake.date_between(start_date='-1y', end_date='today'),
            "amount": price, # Simplified: amount is price * 1 (quantity 1)
            "quantity": 1
        })
        
    return pd.DataFrame(transactions)

def generate_web_traffic(customers_df, n=1000):
    """
    Generates synthetic web traffic data.
    """
    traffic = []
    customer_ids = customers_df['customer_id'].tolist()
    # Add None for anonymous users
    user_pool = customer_ids + [None] * (len(customer_ids) * 2) 
    
    pages = ["/home", "/shop/rv", "/shop/camping", "/cart", "/checkout", "/blog/camping-tips"]
    
    for i in range(n):
        path = random.choice(pages)
        converted = False
        if path == "/checkout":
            converted = random.choice([True, False]) # Simple conversion logic
        
        traffic.append({
            "session_id": fake.uuid4(),
            "user_id": random.choice(user_pool),
            "page_path": path,
            "duration_seconds": random.randint(10, 600),
            "converted": converted,
            "timestamp": fake.date_time_between(start_date='-1y', end_date='now')
        })
    return pd.DataFrame(traffic)

def main():
    print("Generating data...")
    customers = generate_customers(200)
    products = generate_products()
    transactions = generate_transactions(customers, products, 1000)
    web_traffic = generate_web_traffic(customers, 2000)
    
    # Introduce data quality issues
    # 1. Duplicates in customers
    customers = pd.concat([customers, customers.sample(5)], ignore_index=True)
    # 2. Null emails
    customers.loc[random.sample(range(len(customers)), 5), 'email'] = None
    
    output_dir = os.path.join(os.path.dirname(__file__), '../data/raw')
    os.makedirs(output_dir, exist_ok=True)
    
    customers.to_csv(os.path.join(output_dir, 'customers.csv'), index=False)
    products.to_csv(os.path.join(output_dir, 'products.csv'), index=False)
    transactions.to_csv(os.path.join(output_dir, 'transactions.csv'), index=False)
    web_traffic.to_csv(os.path.join(output_dir, 'web_traffic.csv'), index=False)
    
    print(f"Data saved to {output_dir}")

if __name__ == "__main__":
    main()
