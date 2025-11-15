#!/usr/bin/env python3
"""
Dummy Sales Data Generator for Umami Wholesale Inc.
Generates 3 years of daily sales data (2022-2024) for data analysis demo.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Product catalog: 8 categories with 2-3 products each
PRODUCTS = {
    "Soy Sauce": [
        {"name": "Kikkoman Soy Sauce 1L", "base_price": 8.99, "base_quantity": 150},
        {"name": "Yamasa Soy Sauce 500ml", "base_price": 5.49, "base_quantity": 120},
    ],
    "Miso": [
        {"name": "Marukome Miso 1kg", "base_price": 12.99, "base_quantity": 80},
        {"name": "Hikari Miso 500g", "base_price": 7.99, "base_quantity": 100},
    ],
    "Rice": [
        {"name": "Koshihikari Rice 10kg", "base_price": 45.99, "base_quantity": 50},
        {"name": "Calrose Rice 5kg", "base_price": 22.99, "base_quantity": 70},
        {"name": "Jasmine Rice 20lb", "base_price": 35.99, "base_quantity": 60},
    ],
    "Noodles": [
        {"name": "Instant Ramen 24-pack", "base_price": 18.99, "base_quantity": 200},
        {"name": "Udon Noodles 5-pack", "base_price": 8.99, "base_quantity": 150},
        {"name": "Soba Noodles 10-pack", "base_price": 15.99, "base_quantity": 120},
    ],
    "Seasonings": [
        {"name": "Mirin 500ml", "base_price": 6.99, "base_quantity": 90},
        {"name": "Cooking Sake 750ml", "base_price": 9.99, "base_quantity": 80},
        {"name": "Dashi Stock Pack", "base_price": 11.99, "base_quantity": 100},
    ],
    "Frozen Foods": [
        {"name": "Gyoza 50-count", "base_price": 14.99, "base_quantity": 110},
        {"name": "Edamame 2kg", "base_price": 12.99, "base_quantity": 130},
    ],
    "Snacks": [
        {"name": "Pocky Assorted 12-pack", "base_price": 16.99, "base_quantity": 180},
        {"name": "Rice Crackers Mix 1kg", "base_price": 13.99, "base_quantity": 140},
        {"name": "Mochi Assorted 20-pack", "base_price": 19.99, "base_quantity": 100},
    ],
    "Beverages": [
        {"name": "Green Tea 24-bottles", "base_price": 22.99, "base_quantity": 160},
        {"name": "Ramune 12-pack", "base_price": 14.99, "base_quantity": 120},
    ],
}

# Regions with distribution weights
REGIONS = {
    "West Coast": 0.40,
    "East Coast": 0.30,
    "Midwest": 0.15,
    "South": 0.15,
}

# Customer types with distribution weights
CUSTOMER_TYPES = {
    "Restaurant": 0.50,
    "Retail Store": 0.30,
    "Online": 0.20,
}

# Date range
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2024, 12, 31)


def get_seasonality_factor(date, category):
    """
    Calculate seasonality factor based on month and category.
    Returns multiplier for base quantity.
    """
    month = date.month

    # January: New Year demand (+30% for rice, soy sauce, noodles)
    if month == 1:
        if category in ["Rice", "Soy Sauce", "Noodles"]:
            return 1.30
        return 1.15

    # July-August: Summer demand (+25% for frozen foods, beverages)
    elif month in [7, 8]:
        if category in ["Frozen Foods", "Beverages"]:
            return 1.25
        return 1.05

    # November-December: Holiday demand (+35% for snacks, beverages)
    elif month in [11, 12]:
        if category in ["Snacks", "Beverages"]:
            return 1.35
        return 1.20

    # Spring promotion (March-May): +10% across the board
    elif month in [3, 4, 5]:
        return 1.10

    else:
        return 1.0


def get_trend_factor(date, region, customer_type):
    """
    Calculate growth trend factor based on year, region, and customer type.
    Returns multiplier for base quantity.
    """
    year = date.year
    years_since_start = year - 2022

    # Base annual growth: +10%
    base_growth = 1 + (years_since_start * 0.10)

    # South region: Higher growth (+15% annually)
    if region == "South":
        base_growth = 1 + (years_since_start * 0.15)

    # Online customer type: Rapid growth (+25% annually)
    if customer_type == "Online":
        online_growth = 1 + (years_since_start * 0.25)
        return base_growth * online_growth / 1.5  # Adjust to avoid extreme values

    return base_growth


def get_anomaly_factor(date):
    """
    Detect special events and return anomaly multiplier.
    """
    # 2022-03: COVID-19 restrictions lifted, restaurant demand surge
    if date.year == 2022 and date.month == 3:
        return 1.40

    # 2023-06: Supply chain issue, temporary shortage
    if date.year == 2023 and date.month == 6:
        return 0.70

    # 2024-02: Japanese food festival, sales spike
    if date.year == 2024 and date.month == 2:
        return 1.50

    return 1.0


def is_promotion_day(date):
    """
    Determine if the date is a promotion day (1-2 times per month).
    Returns True for approximately 5-8 days per month.
    """
    # Use date hash to create deterministic but varied promotion days
    day_hash = hash(date.strftime("%Y-%m-%d"))
    return (day_hash % 5) == 0  # Approximately 20% of days = 6 days/month


def get_promotion_factor():
    """
    Return promotion effect multiplier (+20-40%).
    """
    return random.uniform(1.20, 1.40)


def calculate_cost_of_goods(unit_price):
    """
    Calculate COGS assuming 60% margin (COGS = 60% of unit price).
    """
    return round(unit_price * 0.60, 2)


def generate_sales_data():
    """
    Generate complete sales dataset.
    """
    print("Generating dummy sales data for Umami Wholesale Inc...")
    print(f"Date range: {START_DATE.date()} to {END_DATE.date()}")

    data = []
    date = START_DATE

    # Generate data for each day
    while date <= END_DATE:
        day_of_week = date.strftime("%A")
        month = date.month
        quarter = (month - 1) // 3 + 1
        year = date.year

        anomaly_factor = get_anomaly_factor(date)
        is_promo = is_promotion_day(date)
        promo_factor = get_promotion_factor() if is_promo else 1.0

        # For each category and product
        for category, products in PRODUCTS.items():
            seasonality = get_seasonality_factor(date, category)

            for product in products:
                product_name = product["name"]
                base_price = product["base_price"]
                base_quantity = product["base_quantity"]

                # For each region
                for region, region_weight in REGIONS.items():
                    # For each customer type
                    for customer_type, customer_weight in CUSTOMER_TYPES.items():

                        # Calculate quantity with all factors
                        trend = get_trend_factor(date, region, customer_type)

                        # Combine all factors
                        quantity_multiplier = (
                            seasonality * trend * anomaly_factor *
                            promo_factor * region_weight * customer_weight
                        )

                        # Add random variation (±20%)
                        random_factor = random.uniform(0.80, 1.20)
                        quantity_multiplier *= random_factor

                        # Calculate final quantity (ensure integer)
                        quantity_sold = max(1, int(base_quantity * quantity_multiplier))

                        # Price varies slightly (±5%)
                        price_variation = random.uniform(0.95, 1.05)
                        unit_price = round(base_price * price_variation, 2)

                        # Calculate totals
                        total_sales = round(quantity_sold * unit_price, 2)
                        cost_of_goods = round(quantity_sold * calculate_cost_of_goods(unit_price), 2)

                        # Create record
                        record = {
                            "date": date.strftime("%Y-%m-%d"),
                            "product_category": category,
                            "product_name": product_name,
                            "region": region,
                            "customer_type": customer_type,
                            "quantity_sold": quantity_sold,
                            "unit_price": unit_price,
                            "total_sales": total_sales,
                            "cost_of_goods": cost_of_goods,
                            "promotion_flag": is_promo,
                            "day_of_week": day_of_week,
                            "month": month,
                            "quarter": quarter,
                            "year": year,
                        }

                        data.append(record)

        # Progress indicator
        if date.day == 1:
            print(f"  Processing: {date.strftime('%Y-%m')}...")

        date += timedelta(days=1)

    # Create DataFrame
    df = pd.DataFrame(data)

    print(f"\nDataset generated successfully!")
    print(f"Total records: {len(df):,}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Total sales: ${df['total_sales'].sum():,.2f}")
    print(f"Average daily sales: ${df.groupby('date')['total_sales'].sum().mean():,.2f}")

    return df


def save_data(df, output_path):
    """
    Save DataFrame to CSV file.
    """
    df.to_csv(output_path, index=False)
    print(f"\nData saved to: {output_path}")
    print(f"File size: {round(os.path.getsize(output_path) / 1024 / 1024, 2)} MB")


def display_sample_statistics(df):
    """
    Display sample statistics for verification.
    """
    print("\n" + "="*60)
    print("SAMPLE STATISTICS")
    print("="*60)

    print("\nProduct Categories:")
    print(df.groupby('product_category')['total_sales'].sum().sort_values(ascending=False))

    print("\nRegions:")
    print(df.groupby('region')['total_sales'].sum().sort_values(ascending=False))

    print("\nCustomer Types:")
    print(df.groupby('customer_type')['total_sales'].sum().sort_values(ascending=False))

    print("\nYearly Sales:")
    print(df.groupby('year')['total_sales'].sum())

    print("\nPromotion Impact:")
    promo_avg = df[df['promotion_flag'] == True]['total_sales'].mean()
    non_promo_avg = df[df['promotion_flag'] == False]['total_sales'].mean()
    print(f"  Average sales (with promotion): ${promo_avg:.2f}")
    print(f"  Average sales (no promotion): ${non_promo_avg:.2f}")
    print(f"  Promotion lift: {((promo_avg / non_promo_avg - 1) * 100):.1f}%")

    print("\n" + "="*60)


if __name__ == "__main__":
    import os

    # Set output path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_path = os.path.join(project_root, "data", "raw", "umami_sales_2022_2024.csv")

    # Generate data
    df = generate_sales_data()

    # Display statistics
    display_sample_statistics(df)

    # Save to CSV
    save_data(df, output_path)

    print("\n✅ Dummy data generation completed successfully!")
    print(f"\nNext steps:")
    print("1. Review the generated data: data/raw/umami_sales_2022_2024.csv")
    print("2. Start Phase 1 analysis using Skill(data-scientist)")
