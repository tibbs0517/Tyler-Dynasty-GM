"""
Launcher for transaction analysis.

This file exists so GitHub Actions can simply run:

    python analyze_transactions.py

The real implementation lives in:
    scripts/analyze_transactions.py
"""

from scripts.analyze_transactions import main


if __name__ == "__main__":
    main()
