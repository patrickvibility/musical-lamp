import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')

print("="*70)
print("GENERATING STRIPE DATA VISUALIZATIONS")
print("="*70)
print("\nLoading data...")

# Load data
df = pd.read_csv('data/raw/Itemized_payout_reconciliation_USD_2024-01-01_to_2025-10-17_America-Chicago.csv',
                 low_memory=False)

# Convert timestamps
df['created_utc'] = pd.to_datetime(df['created_utc'])
df['created_date'] = df['created_utc'].dt.date
df['created_year'] = df['created_utc'].dt.year
df['created_month'] = df['created_utc'].dt.month
df['created_month_name'] = df['created_utc'].dt.strftime('%Y-%m')
df['created_day_of_week'] = df['created_utc'].dt.day_name()
df['created_hour'] = df['created_utc'].dt.hour
df['fee_percentage'] = (df['fee'] / df['gross'] * 100).round(2)

print(f"✓ Loaded {len(df):,} transactions")
print(f"✓ Generating charts in outputs/charts/...")

# 1. MONTHLY REVENUE TREND
print("\n[1/10] Generating monthly revenue trend...")
monthly = df.groupby('created_month_name').agg({
    'gross': 'sum',
    'fee': 'sum',
    'net': 'sum',
    'balance_transaction_id': 'count'
}).round(2)
monthly.columns = ['Gross Revenue', 'Fees', 'Net Revenue', 'Transactions']

plt.figure(figsize=(16, 8))
x = range(len(monthly))
width = 0.35

plt.bar([i - width/2 for i in x], monthly['Gross Revenue'], width, label='Gross Revenue', color='lightblue', alpha=0.8)
plt.bar([i + width/2 for i in x], monthly['Net Revenue'], width, label='Net Revenue', color='green', alpha=0.8)
plt.plot(x, monthly['Fees'], 'ro-', linewidth=2, markersize=6, label='Fees')

plt.xlabel('Month', fontsize=14, fontweight='bold')
plt.ylabel('Amount ($)', fontsize=14, fontweight='bold')
plt.title('Monthly Revenue Trend: Gross, Net, and Fees', fontsize=16, fontweight='bold')
plt.xticks(x, monthly.index, rotation=45, ha='right')
plt.legend(fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('outputs/charts/01_monthly_revenue_trend.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. REVENUE BY CATEGORY
print("[2/10] Generating revenue by category...")
category_summary = df.groupby('reporting_category').agg({
    'gross': ['sum', 'count']
}).round(2)
category_summary.columns = ['Total Gross', 'Count']
category_summary = category_summary.sort_values('Total Gross', ascending=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

category_summary['Total Gross'].plot(kind='barh', ax=ax1, color='steelblue')
ax1.set_title('Total Revenue by Category', fontsize=14, fontweight='bold')
ax1.set_xlabel('Revenue ($)', fontsize=12)
ax1.grid(axis='x', alpha=0.3)

category_summary['Count'].plot(kind='barh', ax=ax2, color='coral')
ax2.set_title('Transaction Count by Category', fontsize=14, fontweight='bold')
ax2.set_xlabel('Count', fontsize=12)
ax2.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/charts/02_revenue_by_category.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. TOP CUSTOMERS
print("[3/10] Generating top customers chart...")
top_customers = df[df['customer_name'].notna()].groupby('customer_name').agg({
    'gross': 'sum',
    'balance_transaction_id': 'count'
}).round(2)
top_customers.columns = ['Total Revenue', 'Transactions']
top_customers = top_customers.sort_values('Total Revenue', ascending=False).head(15)

plt.figure(figsize=(12, 8))
plt.barh(range(len(top_customers)), top_customers['Total Revenue'], color='steelblue')
plt.yticks(range(len(top_customers)), top_customers.index)
plt.xlabel('Total Revenue ($)', fontsize=12)
plt.title('Top 15 Customers by Revenue', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('outputs/charts/03_top_customers.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. TOP PROGRAMS
print("[4/10] Generating top programs chart...")
programs = df[df['payment_metadata[Program]'].notna()].groupby('payment_metadata[Program]').agg({
    'gross': ['sum', 'count']
}).round(2)
programs.columns = ['Total Revenue', 'Transactions']
programs = programs.sort_values('Total Revenue', ascending=False).head(10)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Revenue pie chart
colors = plt.cm.Set3(range(len(programs)))
ax1.pie(programs['Total Revenue'], labels=programs.index, autopct='%1.1f%%',
        startangle=90, colors=colors)
ax1.set_title('Revenue Distribution by Program (Top 10)', fontsize=14, fontweight='bold')

# Transaction count bar chart
programs['Transactions'].plot(kind='barh', ax=ax2, color='coral')
ax2.set_title('Transaction Count by Program', fontsize=14, fontweight='bold')
ax2.set_xlabel('Transactions', fontsize=12)
ax2.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/charts/04_top_programs.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. PAYMENT METHODS
print("[5/10] Generating payment methods analysis...")
payment_methods = df.groupby('payment_method_type').agg({
    'gross': ['sum', 'count']
}).round(2)
payment_methods.columns = ['Total Revenue', 'Count']
payment_methods = payment_methods.sort_values('Total Revenue', ascending=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.pie(payment_methods['Count'], labels=payment_methods.index, autopct='%1.1f%%', startangle=90)
ax1.set_title('Transactions by Payment Method', fontsize=14, fontweight='bold')

ax2.pie(payment_methods['Total Revenue'], labels=payment_methods.index, autopct='%1.1f%%', startangle=90)
ax2.set_title('Revenue by Payment Method', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('outputs/charts/05_payment_methods.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. CARD BRANDS
print("[6/10] Generating card brands analysis...")
card_data = df[df['card_brand'].notna()]
card_brands = card_data.groupby('card_brand').agg({
    'gross': ['sum', 'count']
}).round(2)
card_brands.columns = ['Total Revenue', 'Count']
card_brands = card_brands.sort_values('Total Revenue', ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))
x = range(len(card_brands))
width = 0.35

ax.bar([i - width/2 for i in x], card_brands['Total Revenue'], width,
       label='Revenue', color='lightblue', alpha=0.8)
ax2 = ax.twinx()
ax2.bar([i + width/2 for i in x], card_brands['Count'], width,
        label='Count', color='coral', alpha=0.8)

ax.set_xlabel('Card Brand', fontsize=12)
ax.set_ylabel('Revenue ($)', fontsize=12, color='blue')
ax2.set_ylabel('Transaction Count', fontsize=12, color='red')
ax.set_title('Revenue and Transaction Count by Card Brand', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(card_brands.index, rotation=45, ha='right')
ax.legend(loc='upper left')
ax2.legend(loc='upper right')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/charts/06_card_brands.png', dpi=300, bbox_inches='tight')
plt.close()

# 7. DAY OF WEEK ANALYSIS
print("[7/10] Generating day of week analysis...")
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dow_analysis = df.groupby('created_day_of_week').agg({
    'gross': ['sum', 'count']
}).round(2)
dow_analysis.columns = ['Total Revenue', 'Count']
dow_analysis = dow_analysis.reindex([d for d in day_order if d in dow_analysis.index])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

dow_analysis['Count'].plot(kind='bar', ax=ax1, color='steelblue')
ax1.set_title('Transactions by Day of Week', fontsize=14, fontweight='bold')
ax1.set_ylabel('Transaction Count', fontsize=12)
ax1.set_xlabel('Day', fontsize=12)
ax1.grid(axis='y', alpha=0.3)
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

dow_analysis['Total Revenue'].plot(kind='bar', ax=ax2, color='coral')
ax2.set_title('Revenue by Day of Week', fontsize=14, fontweight='bold')
ax2.set_ylabel('Revenue ($)', fontsize=12)
ax2.set_xlabel('Day', fontsize=12)
ax2.grid(axis='y', alpha=0.3)
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

plt.tight_layout()
plt.savefig('outputs/charts/07_day_of_week.png', dpi=300, bbox_inches='tight')
plt.close()

# 8. HOUR OF DAY ANALYSIS
print("[8/10] Generating hour of day analysis...")
hour_analysis = df.groupby('created_hour').agg({
    'gross': ['sum', 'count']
}).round(2)
hour_analysis.columns = ['Total Revenue', 'Count']

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(hour_analysis.index, hour_analysis['Count'], marker='o', linewidth=2, markersize=8, color='steelblue')
ax.set_title('Transactions by Hour of Day (UTC)', fontsize=14, fontweight='bold')
ax.set_xlabel('Hour (0-23)', fontsize=12)
ax.set_ylabel('Transaction Count', fontsize=12)
ax.grid(True, alpha=0.3)
ax.set_xticks(range(0, 24))
plt.tight_layout()
plt.savefig('outputs/charts/08_hour_of_day.png', dpi=300, bbox_inches='tight')
plt.close()

# 9. FEE DISTRIBUTION
print("[9/10] Generating fee distribution...")
plt.figure(figsize=(14, 5))
plt.hist(df['fee_percentage'], bins=50, edgecolor='black', alpha=0.7, color='coral')
plt.title('Fee Percentage Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Fee Percentage (%)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.axvline(df['fee_percentage'].mean(), color='red', linestyle='--', linewidth=2,
            label=f'Mean: {df["fee_percentage"].mean():.2f}%')
plt.legend(fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('outputs/charts/09_fee_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 10. GROWTH CHART
print("[10/10] Generating growth chart...")
monthly_sorted = monthly.sort_index()
monthly_sorted['Revenue_Growth_%'] = monthly_sorted['Gross Revenue'].pct_change() * 100

fig, ax1 = plt.subplots(figsize=(14, 6))

ax1.bar(range(len(monthly_sorted)), monthly_sorted['Gross Revenue'], color='lightblue', alpha=0.7, label='Revenue')
ax1.set_xlabel('Month', fontsize=12)
ax1.set_ylabel('Revenue ($)', fontsize=12, color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_xticks(range(len(monthly_sorted)))
ax1.set_xticklabels(monthly_sorted.index, rotation=45, ha='right')

ax2 = ax1.twinx()
ax2.plot(range(len(monthly_sorted)), monthly_sorted['Revenue_Growth_%'],
         color='red', marker='o', linewidth=2, markersize=6, label='Growth %')
ax2.set_ylabel('Growth Rate (%)', fontsize=12, color='red')
ax2.tick_params(axis='y', labelcolor='red')
ax2.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)

plt.title('Monthly Revenue and Growth Rate', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('outputs/charts/10_growth_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n" + "="*70)
print("✓ ALL CHARTS GENERATED SUCCESSFULLY!")
print("="*70)
print("\nCharts saved to: outputs/charts/")
print("\nGenerated files:")
print("  01_monthly_revenue_trend.png")
print("  02_revenue_by_category.png")
print("  03_top_customers.png")
print("  04_top_programs.png")
print("  05_payment_methods.png")
print("  06_card_brands.png")
print("  07_day_of_week.png")
print("  08_hour_of_day.png")
print("  09_fee_distribution.png")
print("  10_growth_analysis.png")
print("\nYou can now view these PNG files in any image viewer!")
print("="*70)
