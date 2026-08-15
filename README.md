<div align="center">

# 🛒 DA-04 — E-commerce Funnel Analytics

### Python · Pandas · Event Analytics · Funnel Conversion · Drop-off · User Journeys · CI

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Event_Analytics-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Testing](https://img.shields.io/badge/Tests-pytest-0A9EDC?style=for-the-badge)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

**A reproducible event-level analytics case study that measures how users move from visit to purchase, where they drop out, and which segments show the strongest friction.**

</div>

---

## 🎯 Business Problem

Top-line conversion hides where a customer journey breaks. Growth and product teams need to know which funnel transition loses the most users, whether friction differs by device or acquisition channel, and which paths deserve investigation or experimentation.

DA-04 adds a new skill layer to the portfolio: **event instrumentation thinking, session-level funnel construction, conversion diagnostics, behavioral segmentation, and journey analysis**.

## 🗺️ Canonical Funnel

```text
Visit
  ↓
Product View
  ↓
Add to Cart
  ↓
Checkout
  ↓
Purchase
```

The project calculates both **stage-to-stage conversion** and **visit-to-stage conversion**, so local friction and end-to-end performance are visible at the same time.

## ❓ Business Questions

1. What is the overall visit-to-purchase conversion rate?
2. Which stage has the largest drop-off?
3. How many users bounce before viewing a product?
4. Where do cart users abandon the journey?
5. Does mobile convert differently from desktop or tablet?
6. Which acquisition channels deliver stronger purchase intent?
7. Which channel-stage combinations show the highest friction?
8. What share of sessions end at each journey outcome?
9. Do segment differences suggest UX or traffic-quality hypotheses?
10. Which funnel problems should be prioritized for experimentation?

## 🔬 What the Code Demonstrates

`event-level data` · sessionization grain · ordered funnel logic · pivot tables · stage reach flags · step conversion · end-to-end conversion · drop-off · device/channel segmentation · journey outcomes · reproducible synthetic data · pytest · GitHub Actions

## 🏗️ Data & Analytical Grains

Raw data is **one row per event**. The analytical layer pivots events to **one row per session** with binary stage indicators. This grain change is crucial: funnel denominators must count sessions consistently rather than raw event rows.

See [`docs/ANALYSIS_PLAYBOOK.md`](docs/ANALYSIS_PLAYBOOK.md) for definitions and interpretation guardrails.

## 📁 Repository Structure

```text
.
├── README.md
├── requirements.txt
├── docs/
│   └── ANALYSIS_PLAYBOOK.md
├── src/
│   ├── __init__.py
│   ├── generate_data.py
│   ├── analytics.py
│   └── run_analysis.py
├── tests/
│   └── test_funnel.py
└── .github/workflows/
    └── python-ci.yml
```

## 🚀 Run Locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -q
python -m src.run_analysis
```

The pipeline generates **12,000 sessions** of deterministic event data, analytical tables, friction diagnostics, an executive summary, and portfolio-ready charts.

## 🧪 Validation & Reproducibility

Automated tests verify that event IDs are unique, timestamps are ordered within sessions, the funnel is monotonically decreasing, purchase implies every prior stage, segmented funnels reconcile to overall totals, and journey outcomes cover the full session population.

GitHub Actions recreates the Python environment, runs all tests, executes the full analysis, and verifies the expected CSV and PNG deliverables.

> Synthetic data is used for methodology and reproducibility. Segment differences are designed for analytical diagnosis and are not evidence about a real company.

## 💼 Portfolio Progression

**DA-01:** EDA & visualization  
**DA-02:** advanced SQL & business analytics  
**DA-03:** customer behavior & retention analytics  
**DA-04:** event-level funnel & journey analytics

This project adds the product/growth analytics layer: **Events → Sessions → Funnel → Friction → Hypothesis → Experiment**.

---

<div align="center">

### Visit → Engage → Cart → Checkout → Purchase

**DA-04 in the Data Analytics portfolio roadmap**

</div>
