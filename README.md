# 🔍 BI Data Quality & QA Testing Pipeline

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge)
![QA Score](https://img.shields.io/badge/QA%20Score-91.1%25-blue?style=for-the-badge)

An automated data quality and QA testing pipeline for BI star schema datasets — simulating the kind of quality assurance work performed by BI analysts at FinTech companies before data reaches dashboards and financial reports.

---

## 📊 QA Results Summary

| Metric | Value |
|---|---|
| Tables Tested | 7 |
| Total Checks Run | 45 |
| ✅ Passed | 41 |
| ❌ Failed | 4 |
| **Quality Score** | **91.1%** |

---

## 🧪 Check Categories

### 1. Null / Missing Value Checks
Validates that critical columns contain no null values across all 7 tables.

**Finding:** `days_to_deliver` contains **2,965 nulls (2.98%)**  
**Root cause:** Orders with status `cancelled` or `unavailable` never receive a delivery date — expected behaviour, not a data error. Recommendation: filter by `order_status = 'delivered'` before using this column in KPI calculations.

### 2. Duplicate Primary Key Checks
Ensures no duplicate PKs exist across all dimension and fact tables.

**Result:** ✅ All 5 primary key checks passed — zero duplicates across `order_id`, `customer_id`, `product_id`, `seller_id`.

### 3. Referential Integrity Checks
Validates all foreign key relationships in the star schema — ensures no orphaned records exist between fact and dimension tables.

**Result:** ✅ All 6 FK relationships intact — zero orphaned keys across all joins.

### 4. Outlier Detection
Flags values outside expected business ranges for numeric columns.

**Finding:** `days_to_deliver` has **63 records > 100 days (0.06%)**  
**Recommendation:** Cap at 100 days for dashboard KPIs or flag separately as anomalies for investigation.

### 5. Row Count Validation
Compares loaded row counts against expected baseline to detect data loss during ETL.

| Table | Expected | Actual | Status |
|---|---|---|---|
| fact_orders | 99,441 | 99,441 | ✅ PASS |
| fact_payments | 103,886 | 103,272 | ❌ FAIL (-614) |
| fact_items | 112,650 | 112,650 | ✅ PASS |
| dim_customers | 99,441 | 99,441 | ✅ PASS |
| dim_products | 32,951 | 32,951 | ✅ PASS |
| dim_sellers | 3,095 | 3,095 | ✅ PASS |
| dim_reviews | 99,224 | 98,673 | ❌ FAIL (-551) |

**Root cause — fact_payments (-614):** Some orders have multiple payment records (split payments). The `drop_duplicates()` step in ETL removed these. Recommendation: update deduplication logic to keep all payment rows per order.

**Root cause — dim_reviews (-551):** Some orders received multiple customer reviews. ETL kept only the most recent. Recommendation: document this business rule explicitly.

---

## 🗂️ Data Model Tested

```
fact_orders ──── dim_customers
     │
     ├────────── fact_payments
     │
     ├────────── fact_items ──── dim_products
     │                    └──── dim_sellers
     │
     └────────── dim_reviews
```

---

## ⚙️ How It Works

```python
# Pipeline flow
Load CSVs → Run 5 check categories → Generate QA report

checks/
├── null_checks()          # Missing value detection per column
├── duplicate_pk_checks()  # Primary key uniqueness validation
├── referential_checks()   # FK → PK integrity across all joins
├── outlier_checks()       # Business-range validation for numerics
└── row_count_checks()     # ETL data loss detection
```

---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/gauravbhatia-bit/bi-data-quality-pipeline.git

# 2. Update DATA_PATH in qa_pipeline.py to point to your olist_clean/ folder

# 3. Run
python qa_pipeline.py

# Output: qa_report.md generated automatically
```

**Requirements:** `pandas`, `numpy` (standard data science stack)

---

## 📁 Repository Structure

```
bi-data-quality-pipeline/
├── qa_pipeline.py     # Main QA pipeline script
├── qa_report.md       # Auto-generated QA report (latest run)
└── README.md
```

---

## 📦 Dataset

**Brazilian E-Commerce Public Dataset by Olist**  
Source: [Kaggle — olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)  
Pre-processed using [riverty-style-payments-bi-dashboard](https://github.com/gauravbhatia-bit/riverty-style-payments-bi-dashboard) ETL pipeline.

---

## 👤 Author

**Gaurav Bhatia**  
MSc Data Science, AI & Digital Business — GISMA University, Berlin  
[LinkedIn](https://linkedin.com/in/gaurav-bhatia-5a5a83184) | [GitHub](https://github.com/gauravbhatia-bit)
