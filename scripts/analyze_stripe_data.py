import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load the data
print("Loading Stripe payout reconciliation data...")
df = pd.read_csv('data/raw/Itemized_payout_reconciliation_USD_2024-01-01_to_2025-10-17_America-Chicago.csv')

print(f"\n{'='*60}")
print(f"STRIPE PAYOUT RECONCILIATION ANALYSIS")
print(f"{'='*60}")
print(f"\nDataset: {len(df):,} transactions")
print(f"Date Range: 2024-01-01 to 2025-10-17")
print(f"Currency: USD")

# Basic info
print(f"\n{'='*60}")
print("DATASET STRUCTURE")
print(f"{'='*60}")
print(f"Total columns: {len(df.columns)}")
print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# Column names
print(f"\n{'='*60}")
print("COLUMN NAMES")
print(f"{'='*60}")
for i, col in enumerate(df.columns, 1):
    print(f"{i}. {col}")

# Missing values
print(f"\n{'='*60}")
print("MISSING VALUES (Top 20 columns with missing data)")
print(f"{'='*60}")
missing = df.isnull().sum()
missing = missing[missing > 0].sort_values(ascending=False).head(20)
if len(missing) > 0:
    for col, count in missing.items():
        pct = (count / len(df)) * 100
        print(f"{col}: {count:,} ({pct:.1f}%)")
else:
    print("No missing values found!")

# Data types
print(f"\n{'='*60}")
print("DATA TYPES")
print(f"{'='*60}")
dtype_counts = df.dtypes.value_counts()
for dtype, count in dtype_counts.items():
    print(f"{dtype}: {count} columns")

# Convert timestamps
print(f"\n{'='*60}")
print("CONVERTING TIMESTAMPS...")
print(f"{'='*60}")
df['created_utc'] = pd.to_datetime(df['created_utc'])
df['available_on_utc'] = pd.to_datetime(df['available_on_utc'])
df['automatic_payout_effective_at_utc'] = pd.to_datetime(df['automatic_payout_effective_at_utc'])

# Extract date components
df['created_date'] = df['created_utc'].dt.date
df['created_year'] = df['created_utc'].dt.year
df['created_month'] = df['created_utc'].dt.month
df['created_day_of_week'] = df['created_utc'].dt.day_name()
df['created_hour'] = df['created_utc'].dt.hour

print("✓ Timestamps converted and date components extracted")

# Financial Analysis
print(f"\n{'='*60}")
print("FINANCIAL SUMMARY")
print(f"{'='*60}")
total_gross = df['gross'].sum()
total_fees = df['fee'].sum()
total_net = df['net'].sum()
avg_transaction = df['gross'].mean()
median_transaction = df['gross'].median()

print(f"Total Gross Revenue: ${total_gross:,.2f}")
print(f"Total Stripe Fees: ${total_fees:,.2f}")
print(f"Total Net Revenue: ${total_net:,.2f}")
print(f"Average Transaction: ${avg_transaction:,.2f}")
print(f"Median Transaction: ${median_transaction:,.2f}")
print(f"Fee Rate: {(total_fees/total_gross*100):.2f}%")

# Reporting categories
print(f"\n{'='*60}")
print("REPORTING CATEGORIES")
print(f"{'='*60}")
if 'reporting_category' in df.columns:
    category_summary = df.groupby('reporting_category').agg({
        'gross': ['sum', 'count', 'mean']
    }).round(2)
    category_summary.columns = ['Total Gross', 'Count', 'Avg Amount']
    category_summary = category_summary.sort_values('Total Gross', ascending=False)
    print(category_summary)

# Payment methods
print(f"\n{'='*60}")
print("PAYMENT METHODS")
print(f"{'='*60}")
if 'payment_method_type' in df.columns:
    payment_methods = df['payment_method_type'].value_counts()
    for method, count in payment_methods.items():
        pct = (count / len(df)) * 100
        print(f"{method}: {count:,} ({pct:.1f}%)")

# Card brands (if card payments)
print(f"\n{'='*60}")
print("CARD BRANDS")
print(f"{'='*60}")
if 'card_brand' in df.columns:
    card_brands = df['card_brand'].value_counts()
    for brand, count in card_brands.head(10).items():
        if pd.notna(brand):
            pct = (count / len(df)) * 100
            print(f"{brand}: {count:,} ({pct:.1f}%)")

# Top customers
print(f"\n{'='*60}")
print("TOP 10 CUSTOMERS BY REVENUE")
print(f"{'='*60}")
if 'customer_name' in df.columns:
    top_customers = df.groupby('customer_name').agg({
        'gross': 'sum',
        'balance_transaction_id': 'count'
    }).round(2)
    top_customers.columns = ['Total Revenue', 'Transaction Count']
    top_customers = top_customers.sort_values('Total Revenue', ascending=False).head(10)
    print(top_customers)

# Programs analysis (from metadata)
print(f"\n{'='*60}")
print("PROGRAMS ANALYSIS")
print(f"{'='*60}")
if 'payment_metadata[Program]' in df.columns:
    programs = df['payment_metadata[Program]'].value_counts().head(10)
    print("Top Programs:")
    for program, count in programs.items():
        if pd.notna(program):
            print(f"{program}: {count:,} transactions")

# Monthly revenue
print(f"\n{'='*60}")
print("MONTHLY REVENUE BREAKDOWN")
print(f"{'='*60}")
monthly = df.groupby(['created_year', 'created_month']).agg({
    'gross': 'sum',
    'fee': 'sum',
    'net': 'sum',
    'balance_transaction_id': 'count'
}).round(2)
monthly.columns = ['Gross Revenue', 'Fees', 'Net Revenue', 'Transactions']
monthly.index.names = ['Year', 'Month']
print(monthly)

# Save summary
print(f"\n{'='*60}")
print("SAVING PROCESSED DATA")
print(f"{'='*60}")
df.to_csv('data/processed/transactions_processed.csv', index=False)
print("✓ Saved to: data/processed/transactions_processed.csv")

# Save monthly summary
monthly.to_csv('data/processed/monthly_summary.csv')
print("✓ Saved to: data/processed/monthly_summary.csv")

print(f"\n{'='*60}")
print("ANALYSIS COMPLETE!")
print(f"{'='*60}")
print("\nNext steps:")
print("1. Open notebooks/01_transaction_analysis.ipynb for detailed analysis")
print("2. Run visualizations for revenue trends")
print("3. Analyze customer segments and program performance")
