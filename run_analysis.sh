#!/bin/bash
# Quick script to run the analysis and generate outputs

echo "Running Stripe Data Analysis..."
echo "================================"
echo ""

# Run the Python analysis script
python scripts/analyze_stripe_data.py

echo ""
echo "================================"
echo "Analysis complete!"
echo ""
echo "To see visualizations:"
echo "1. Open Jupyter: jupyter notebook notebooks/02_stripe_payout_analysis.ipynb"
echo "2. Or visit: http://localhost:8888"
echo ""
