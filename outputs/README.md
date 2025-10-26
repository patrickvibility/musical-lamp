# Stripe Data Analysis Outputs

This directory contains all the generated analysis outputs from your Stripe payout reconciliation data.

## 📊 Available Files

### Summary Report
- **`ANALYSIS_SUMMARY.txt`** - Comprehensive text report with all key metrics, insights, and recommendations

### Visualizations (PNG Charts)

All charts are high-resolution (300 DPI) PNG images:

1. **`01_monthly_revenue_trend.png`**
   - Monthly gross revenue, net revenue, and fees over time
   - Shows overall business growth trajectory

2. **`02_revenue_by_category.png`**
   - Revenue and transaction count by reporting category
   - Breakdown of charges, refunds, disputes, etc.

3. **`03_top_customers.png`**
   - Top 15 customers ranked by total revenue
   - Horizontal bar chart for easy comparison

4. **`04_top_programs.png`**
   - Revenue distribution across top 10 programs
   - Pie chart showing program popularity

5. **`05_payment_methods.png`**
   - Transaction and revenue breakdown by payment method
   - Shows card vs ACH vs other methods

6. **`06_card_brands.png`**
   - Revenue and count by card brand (Visa, Amex, Mastercard, etc.)
   - Dual-axis chart for comprehensive view

7. **`07_day_of_week.png`**
   - Transaction patterns by day of week
   - Identifies busiest days for business

8. **`08_hour_of_day.png`**
   - Transaction patterns by hour (UTC)
   - Shows peak activity times

9. **`09_fee_distribution.png`**
   - Distribution of Stripe fee percentages
   - Histogram with average marked

10. **`10_growth_analysis.png`**
    - Month-over-month revenue growth rate
    - Shows growth trends and patterns

## 📁 Directory Structure

```
outputs/
├── README.md                      (This file)
├── ANALYSIS_SUMMARY.txt           (Full text report)
└── charts/
    ├── 01_monthly_revenue_trend.png
    ├── 02_revenue_by_category.png
    ├── 03_top_customers.png
    ├── 04_top_programs.png
    ├── 05_payment_methods.png
    ├── 06_card_brands.png
    ├── 07_day_of_week.png
    ├── 08_hour_of_day.png
    ├── 09_fee_distribution.png
    └── 10_growth_analysis.png
```

## 🔍 Key Findings

- **Total Revenue**: $4.2M gross ($4.08M net)
- **Peak Month**: August 2025 ($247K)
- **Top Customer**: Amanda Cohen ($116K)
- **Most Popular**: 6 Month Program (4,952 transactions)
- **Average Transaction**: $259.66
- **Fee Rate**: 3.07%

## 📖 How to View

1. **Read the summary**: Open `ANALYSIS_SUMMARY.txt` in any text editor
2. **View charts**: Open PNG files in any image viewer
3. **Share**: All files are ready to share with stakeholders

## 🔄 Regenerating

To regenerate all outputs:
```bash
python scripts/generate_all_charts.py
```

---
Generated: October 26, 2025
