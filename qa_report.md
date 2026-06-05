# 🔍 BI Data Quality QA Report
**Generated:** 2026-06-06 05:15  
**Dataset:** Olist Brazilian E-Commerce (Star Schema)  
**Tables Tested:** 7  

## 📊 Summary
| Metric | Value |
|---|---|
| Total Checks | 45 |
| ✅ Passed | 41 |
| ❌ Failed | 4 |
| Quality Score | **91.1%** |

---

## 📋 Full Results

| Table | Check | Status | Detail |
|---|---|---|---|
| `fact_orders` | Null check: order_id | ✅ PASS | 0 nulls (0.0%) |
| `fact_orders` | Null check: customer_id | ✅ PASS | 0 nulls (0.0%) |
| `fact_orders` | Null check: order_status | ✅ PASS | 0 nulls (0.0%) |
| `fact_orders` | Null check: days_to_deliver | ❌ FAIL | 2,965 nulls (2.98%) |
| `fact_orders` | Null check: purchase_year | ✅ PASS | 0 nulls (0.0%) |
| `fact_orders` | Null check: purchase_month | ✅ PASS | 0 nulls (0.0%) |
| `fact_payments` | Null check: order_id | ✅ PASS | 0 nulls (0.0%) |
| `fact_payments` | Null check: payment_type | ✅ PASS | 0 nulls (0.0%) |
| `fact_payments` | Null check: payment_value | ✅ PASS | 0 nulls (0.0%) |
| `fact_payments` | Null check: payment_installments | ✅ PASS | 0 nulls (0.0%) |
| `fact_items` | Null check: order_id | ✅ PASS | 0 nulls (0.0%) |
| `fact_items` | Null check: product_id | ✅ PASS | 0 nulls (0.0%) |
| `fact_items` | Null check: seller_id | ✅ PASS | 0 nulls (0.0%) |
| `fact_items` | Null check: price | ✅ PASS | 0 nulls (0.0%) |
| `dim_customers` | Null check: customer_id | ✅ PASS | 0 nulls (0.0%) |
| `dim_customers` | Null check: customer_state | ✅ PASS | 0 nulls (0.0%) |
| `dim_products` | Null check: product_id | ✅ PASS | 0 nulls (0.0%) |
| `dim_products` | Null check: product_category_name | ✅ PASS | 0 nulls (0.0%) |
| `dim_sellers` | Null check: seller_id | ✅ PASS | 0 nulls (0.0%) |
| `dim_sellers` | Null check: seller_state | ✅ PASS | 0 nulls (0.0%) |
| `dim_reviews` | Null check: order_id | ✅ PASS | 0 nulls (0.0%) |
| `dim_reviews` | Null check: review_score | ✅ PASS | 0 nulls (0.0%) |
| `fact_orders` | Duplicate PK: order_id | ✅ PASS | 0 duplicates found |
| `dim_customers` | Duplicate PK: customer_id | ✅ PASS | 0 duplicates found |
| `dim_products` | Duplicate PK: product_id | ✅ PASS | 0 duplicates found |
| `dim_sellers` | Duplicate PK: seller_id | ✅ PASS | 0 duplicates found |
| `dim_reviews` | Duplicate PK: order_id | ✅ PASS | 0 duplicates found |
| `fact_payments` | FK integrity: order_id → fact_orders.order_id | ✅ PASS | 0 orphaned keys |
| `fact_items` | FK integrity: order_id → fact_orders.order_id | ✅ PASS | 0 orphaned keys |
| `fact_items` | FK integrity: product_id → dim_products.product_id | ✅ PASS | 0 orphaned keys |
| `fact_items` | FK integrity: seller_id → dim_sellers.seller_id | ✅ PASS | 0 orphaned keys |
| `fact_orders` | FK integrity: customer_id → dim_customers.customer_id | ✅ PASS | 0 orphaned keys |
| `dim_reviews` | FK integrity: order_id → fact_orders.order_id | ✅ PASS | 0 orphaned keys |
| `fact_payments` | Outlier: payment_value [0-15000] | ✅ PASS | 0 outliers (0.0%) |
| `fact_items` | Outlier: price [0-10000] | ✅ PASS | 0 outliers (0.0%) |
| `fact_items` | Outlier: freight_value [0-500] | ✅ PASS | 0 outliers (0.0%) |
| `fact_orders` | Outlier: days_to_deliver [0-100] | ❌ FAIL | 63 outliers (0.06%) |
| `dim_reviews` | Outlier: review_score [1-5] | ✅ PASS | 0 outliers (0.0%) |
| `fact_orders` | Row count validation | ✅ PASS | Expected 99,441 | Got 99,441 |
| `fact_payments` | Row count validation | ❌ FAIL | Expected 103,886 | Got 103,272 |
| `fact_items` | Row count validation | ✅ PASS | Expected 112,650 | Got 112,650 |
| `dim_customers` | Row count validation | ✅ PASS | Expected 99,441 | Got 99,441 |
| `dim_products` | Row count validation | ✅ PASS | Expected 32,951 | Got 32,951 |
| `dim_sellers` | Row count validation | ✅ PASS | Expected 3,095 | Got 3,095 |
| `dim_reviews` | Row count validation | ❌ FAIL | Expected 99,224 | Got 98,673 |

---

## 🔎 Findings & Recommendations

- **fact_orders — Null check: days_to_deliver**: 2,965 nulls (2.98%)
- **fact_orders — Outlier: days_to_deliver [0-100]**: 63 outliers (0.06%)
- **fact_payments — Row count validation**: Expected 103,886 | Got 103,272
- **dim_reviews — Row count validation**: Expected 99,224 | Got 98,673

---
*Pipeline built with Python + pandas | Part of BI Data Quality Portfolio*
