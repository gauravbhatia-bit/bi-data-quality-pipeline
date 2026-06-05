import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

# ── CONFIG ───────────────────────────────────────────────────────────────────
DATA_PATH = r"C:\Users\gaura\Downloads\olist_clean"
REPORT_PATH = r"C:\Users\gaura\Downloads\olist_clean\qa_report.md"

# Expected schemas: {table: {column: expected_dtype}}
SCHEMAS = {
    "fact_orders":    {"order_id": "object", "customer_id": "object",
                       "order_status": "object", "days_to_deliver": "float64",
                       "purchase_year": "int64", "purchase_month": "int64"},
    "fact_payments":  {"order_id": "object", "payment_type": "object",
                       "payment_value": "float64", "payment_installments": "int64"},
    "fact_items":     {"order_id": "object", "product_id": "object",
                       "seller_id": "object", "price": "float64"},
    "dim_customers":  {"customer_id": "object", "customer_state": "object"},
    "dim_products":   {"product_id": "object", "product_category_name": "object"},
    "dim_sellers":    {"seller_id": "object", "seller_state": "object"},
    "dim_reviews":    {"order_id": "object", "review_score": "int64"},
}

PRIMARY_KEYS = {
    "fact_orders":   "order_id",
    "dim_customers": "customer_id",
    "dim_products":  "product_id",
    "dim_sellers":   "seller_id",
    "dim_reviews":   "order_id",
}

FOREIGN_KEYS = [
    ("fact_payments", "order_id",  "fact_orders",   "order_id"),
    ("fact_items",    "order_id",  "fact_orders",   "order_id"),
    ("fact_items",    "product_id","dim_products",  "product_id"),
    ("fact_items",    "seller_id", "dim_sellers",   "seller_id"),
    ("fact_orders",   "customer_id","dim_customers","customer_id"),
    ("dim_reviews",   "order_id",  "fact_orders",   "order_id"),
]

OUTLIER_CHECKS = {
    "fact_payments": [("payment_value", 0, 15000)],
    "fact_items":    [("price", 0, 10000), ("freight_value", 0, 500)],
    "fact_orders":   [("days_to_deliver", 0, 100)],
    "dim_reviews":   [("review_score", 1, 5)],
}

# ── LOAD TABLES ───────────────────────────────────────────────────────────────
tables = {}
for name in SCHEMAS:
    path = os.path.join(DATA_PATH, f"{name}.csv")
    tables[name] = pd.read_csv(path)
    print(f"✅ Loaded {name}: {len(tables[name]):,} rows")

results = []

def add(table, check, status, detail):
    icon = "✅ PASS" if status else "❌ FAIL"
    results.append({"table": table, "check": check, "status": icon, "detail": detail})
    print(f"  {icon} | {check} | {detail}")

# ── CHECK 1: NULL VALUES ──────────────────────────────────────────────────────
print("\n── NULL CHECKS ──")
for name, df in tables.items():
    for col in SCHEMAS[name]:
        if col in df.columns:
            nulls = df[col].isnull().sum()
            pct = round(nulls / len(df) * 100, 2)
            add(name, f"Null check: {col}", nulls == 0,
                f"{nulls:,} nulls ({pct}%)")

# ── CHECK 2: DUPLICATE PRIMARY KEYS ──────────────────────────────────────────
print("\n── DUPLICATE PK CHECKS ──")
for name, pk in PRIMARY_KEYS.items():
    df = tables[name]
    dupes = df[pk].duplicated().sum()
    add(name, f"Duplicate PK: {pk}", dupes == 0,
        f"{dupes:,} duplicates found")

# ── CHECK 3: REFERENTIAL INTEGRITY ───────────────────────────────────────────
print("\n── REFERENTIAL INTEGRITY CHECKS ──")
for child, fk, parent, pk in FOREIGN_KEYS:
    child_vals  = set(tables[child][fk].dropna().unique())
    parent_vals = set(tables[parent][pk].dropna().unique())
    orphans = len(child_vals - parent_vals)
    add(child, f"FK integrity: {fk} → {parent}.{pk}",
        orphans == 0, f"{orphans:,} orphaned keys")

# ── CHECK 4: OUTLIER DETECTION ────────────────────────────────────────────────
print("\n── OUTLIER CHECKS ──")
for name, checks in OUTLIER_CHECKS.items():
    for col, low, high in checks:
        df = tables[name]
        out = df[(df[col] < low) | (df[col] > high)].shape[0]
        pct = round(out / len(df) * 100, 2)
        add(name, f"Outlier: {col} [{low}-{high}]",
            out == 0, f"{out:,} outliers ({pct}%)")

# ── CHECK 5: ROW COUNT VALIDATION ────────────────────────────────────────────
print("\n── ROW COUNT CHECKS ──")
EXPECTED = {
    "fact_orders": 99441, "fact_payments": 103886,
    "fact_items": 112650, "dim_customers": 99441,
    "dim_products": 32951, "dim_sellers": 3095, "dim_reviews": 99224
}
for name, expected in EXPECTED.items():
    actual = len(tables[name])
    add(name, "Row count validation", actual == expected,
        f"Expected {expected:,} | Got {actual:,}")

# ── GENERATE MARKDOWN REPORT ──────────────────────────────────────────────────
passed = sum(1 for r in results if "PASS" in r["status"])
failed = sum(1 for r in results if "FAIL" in r["status"])
total  = len(results)
score  = round(passed / total * 100, 1)

report = f"""# 🔍 BI Data Quality QA Report
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}  
**Dataset:** Olist Brazilian E-Commerce (Star Schema)  
**Tables Tested:** {len(tables)}  

## 📊 Summary
| Metric | Value |
|---|---|
| Total Checks | {total} |
| ✅ Passed | {passed} |
| ❌ Failed | {failed} |
| Quality Score | **{score}%** |

---

## 📋 Full Results

| Table | Check | Status | Detail |
|---|---|---|---|
"""
for r in results:
    report += f"| `{r['table']}` | {r['check']} | {r['status']} | {r['detail']} |\n"

report += f"""
---

## 🔎 Findings & Recommendations

"""
fails = [r for r in results if "FAIL" in r["status"]]
if fails:
    for f in fails:
        report += f"- **{f['table']} — {f['check']}**: {f['detail']}\n"
else:
    report += "All checks passed. Dataset is clean and ready for BI reporting.\n"

report += "\n---\n*Pipeline built with Python + pandas | Part of BI Data Quality Portfolio*\n"

with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(report)

print(f"\n{'='*50}")
print(f"✅ QA COMPLETE | Score: {score}% | {passed}/{total} checks passed")
print(f"📄 Report saved to: {REPORT_PATH}")