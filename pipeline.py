"""
Part 2 - Sales Data Pipeline
"""

import pandas as pd

from solution import add_virtual_column


df = pd.read_csv("data/sales.csv")
# ==================================================
# DATA EXPLORATION
# ==================================================
df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
)

# print(df.dtypes)

df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
df["discount"] = pd.to_numeric(df["discount"], errors="coerce") 
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

#duplicates = df[df.duplicated(keep=False)]
#print(f"Duplicates: {len(duplicates)}")
#print(
#    duplicates.sort_values("order_id")
#)

df = df.drop_duplicates()

# ==================================================
# ORDER ID
# ==================================================

#print(df["order_id"].isnull().sum())
#print(df["order_id"].duplicated().sum())
#invalid_ids = df[
#    ~df["order_id"].str.match(r"^SO-\d+$", na=False)
#]
#print(invalid_ids)

df = df[df["order_id"] != "Order ID"]
df = df[df["order_id"] != "TOTAL"]

# ==================================================
# REGION
# ==================================================

#print(sorted(df["region"].unique()))
#regions_before = df["region"].copy()

df["region"] = (
    df["region"]
    .str.strip()
    .str.title()
)

#affected_regions = (regions_before != df["region"]).sum()
#print(f"Affected rows: {affected_regions}")

# ==================================================
# PRODUCT
# ==================================================

#print(df["product"].isnull().sum())
#print(sorted(df["product"].unique()))
#print(df["product"].value_counts())

# ==================================================
# QUANTITY
# ==================================================

#print(df["quantity"].describe())
#print(df.nsmallest(10, "quantity"))
#print(df.nlargest(10, "quantity"))

# ==================================================
# UNIT PRICE
# ==================================================

#print(df["unit_price"].describe())
#print(df[df["unit_price"].isna()])
#print(df[df["unit_price"] <= 0])
#print(
#    df.groupby("product")["unit_price"]
#    .nunique()
#)

def fill_price(group):
    price = group.mode()[0]
    return group.fillna(price)

df["unit_price"] = (
    df.groupby("product")["unit_price"]
    .transform(fill_price)
)

# ==================================================
# DISCOUNT
# ==================================================

#print(df["discount"].describe())
#print(df[df["discount"] < 0])
#print(df[df["discount"].isna()])
#line_value = df["quantity"] * df["unit_price"]
#invalid_discounts = df[
#    df["discount"] > line_value
#]
#print(invalid_discounts)

df["discount"] = df["discount"].fillna(0)

# ==================================================
# ORDER DATE
# ==================================================

print(df["order_date"].isna().sum())

print(
    df[df["order_date"].isna()]
)

df = add_virtual_column(
    df,
    "quantity * unit_price - discount",
    "revenue"
)

revenue_by_region = (
    df.groupby("region")["revenue"]
    .sum()
    .reset_index()
)

revenue_by_region.to_csv(
    "data/revenue_by_region.csv",
    index=False
)

check = pd.read_csv("data/revenue_by_region.csv")

print(check)
