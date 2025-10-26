# Stripe Transaction Data Analysis

This project analyzes Stripe transaction data to extract insights about payments, revenue, and customer behavior.

## Project Structure

```
musical-lamp/
├── data/
│   ├── raw/          <- Upload your Stripe export files here
│   └── processed/    <- Cleaned and transformed data
├── notebooks/        <- Jupyter notebooks for analysis
├── scripts/          <- Python scripts for data processing
├── sql/              <- SQL queries (if using a database)
└── docs/             <- Documentation
```

## Getting Started

### 1. Upload Your Data

**Place your Stripe transaction export file here:**
```
data/raw/transactions.csv
```

Supported formats:
- CSV (recommended)
- JSON
- Excel (.xlsx)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Analysis

Open the Jupyter notebook:
```bash
jupyter notebook notebooks/01_transaction_analysis.ipynb
```

## Common Stripe Transaction Fields

- `id` - Unique transaction ID
- `amount` - Amount in cents
- `currency` - Currency code (USD, EUR, etc.)
- `created` - Timestamp
- `customer` - Customer ID
- `status` - Payment status (succeeded, failed, etc.)
- `description` - Transaction description
- `fee` - Stripe fee amount
- `net` - Net amount after fees

## Security Notes

- Never commit actual Stripe data to git
- Keep API keys in `.env` file (not tracked)
- The `.gitignore` is configured to exclude sensitive data

## Need Help?

Check the example notebook in `notebooks/` for common analysis patterns.
