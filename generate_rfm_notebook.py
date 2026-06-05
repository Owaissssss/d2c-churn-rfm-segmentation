import json

rfm_notebook_json = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Capstone Part 2: RFM Behavioral Segmentation & Risk Integration\n",
                "**Course**: IITP AI Course Capstone\n",
                "**Project Repository**: `d2c-churn-rfm-segmentation`\n\n",
                "### Objective:\n",
                "Engineers robust RFM features using transactional profiles on or before the 2025-09-30 snapshot limit, blends behavioral risk flags, assigns segments, and exports data files."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n\n",
                "sns.set_theme(style='whitegrid')\n",
                "print('Part 2 dependencies loaded cleanly.')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Load Data and Isolate Pre-Snapshot Transactions\n",
                "We enforce strict leakage boundaries by filtering out records past 2025-09-30."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "orders = pd.read_csv('orders.csv')\n",
                "customers = pd.read_csv('customers.csv')\n",
                "support = pd.read_csv('support_tickets.csv')\n\n",
                "orders_cleaned = orders[~orders['order_id'].str.endswith('_DUP')].copy()\n",
                "orders_cleaned['order_date'] = pd.to_datetime(orders_cleaned['order_date'])\n",
                "snapshot_date = pd.to_datetime('2025-09-30')\n\n",
                "hist_orders = orders_cleaned[orders_cleaned['order_date'] <= snapshot_date].copy()\n",
                "print(f'Safe transactions for modeling: {hist_orders.shape[0]}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. RFM Feature Engineering\n",
                "We compute core customer metrics: Recency, Frequency, and Monetary values."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "rfm = hist_orders.groupby('customer_id').agg(\n",
                "    last_date=('order_date', 'max'),\n",
                "    frequency=('order_id', 'count'),\n",
                "    monetary=('gross_amount', 'sum')\n",
                ").reset_index()\n\n",
                "rfm['recency'] = (snapshot_date - rfm['last_date']).dt.days\n",
                "rfm = rfm.drop(columns=['last_date'])\n",
                "print(rfm.head())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Integrating Non-RFM Operational Risk Signals\n",
                "We supplement our profiles with support complaints and return rates per customer."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "ticket_counts = support[pd.to_datetime(support['ticket_date']) <= snapshot_date].groupby('customer_id').size().reset_index(name='ticket_count')\n",
                "return_metrics = hist_orders.groupby('customer_id')['returned'].mean().reset_index(name='return_rate')\n\n",
                "master_df = pd.merge(customers[['customer_id']], rfm, on='customer_id', how='left').fillna({'recency': 999, 'frequency': 0, 'monetary': 0})\n",
                "master_df = pd.merge(master_df, ticket_counts, on='customer_id', how='left').fillna({'ticket_count': 0})\n",
                "master_df = pd.merge(master_df, return_metrics, on='customer_id', how='left').fillna({'return_rate': 0.0})\n",
                "print(master_df.describe())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Cohort Segmentation Definition\n",
                "We define 5 distinct behavioral blocks using custom tier limits."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "def segment_customer(row):\n",
                "    if row['frequency'] == 0:\n",
                "        return 'Dormant Unconverted'\n",
                "    if row['recency'] <= 45 and row['frequency'] >= 5:\n",
                "        return 'Champions'\n",
                "    if row['recency'] > 90 and row['monetary'] > 2000:\n",
                "        return 'At-Risk High-Value'\n",
                "    if row['ticket_count'] >= 2 and row['return_rate'] > 0.3:\n",
                "        return 'High-Value Unhappy'\n",
                "    if row['recency'] <= 60 and row['frequency'] <= 2:\n",
                "        return 'New Shoppers'\n",
                "    return 'Regular Value Core'\n\n",
                "master_df['segment_name'] = master_df.apply(segment_customer, axis=1)\n",
                "print(master_df['segment_name'].value_counts())\n\n",
                "master_df.to_csv('segments.csv', index=False)\n",
                "print('segments.csv generated successfully.')"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"}
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

with open("rfm_segmentation.ipynb", "w", encoding="utf-8") as f:
    json.dump(rfm_notebook_json, f, indent=2)
print("SUCCESS: rfm_segmentation.ipynb setup completed.")