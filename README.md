# D2C Customer Churn Intelligence — Part 2: RFM Segmentation & Retention Strategy

## Student & Course Information
* **Student Name:** Mohammad Owais
* **Registration Number:** iitp_aiml_2506198
* **Email:** zkzonfamily@gmail.com
* **Course:** IIT Patna AI/ML Course Capstone

This repository contains **Part 2** of the 4-part D2C Personal-Care Churn Intelligence Capstone Project. It implements an empirical, data-driven behavioral segmentation model using Recency, Frequency, and Monetary (RFM) metrics calculated from pre-snapshot transactions, integrates multi-source non-RFM risk factors, and outlines a targeted operational retention strategy.

## Project Structure
* `requirements.txt`: Project dependency declarations ensuring matching environment installations.
* `rfm_segmentation.ipynb`: Clean Jupyter notebook executing raw transaction filtering, customer feature calculation, feature merging, and cohort grouping.
* `segments.csv`: Exported data tracking customer IDs alongside their explicit segment names, recency spans, frequencies, monetary footprints, support log volumes, and return rates.
* `retention_strategy.md`: Business action framework presenting quantified segment sizes, specific campaign playbooks, and priority-driven budget distributions.
* `manual_review_cases.md`: Deep-dive log auditing 10 unique customer edge cases with conflicting behavioral signals and custom operational directions.

## Segment Configuration Summary
Based on the absolute data profile limits enforced prior to the snapshot cutoff date (`2025-09-30`), the 2,400 active customer rows are mapped into 5 core cohorts:
1. **Regular Value Core**: Consistent baseline buyers forming the stable middle layer of our brand sales.
2. **New Shoppers**: Recent first-time purchasers acquired within the last 60 days who require onboarding retention setup.
3. **At-Risk High-Value**: High historical spenders who have crossed the 90-day transaction inactivity wall.
4. **Champions**: Elite high-frequency purchasers with active, recent touchpoints.
5. **High-Value Unhappy**: Top-tier spenders showing critical operational friction via product returns and high customer-care complaints.

## Environment Setup & Execution Instructions

1. Ensure your terminal has initialized your isolated virtual environment (`venv`).
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt