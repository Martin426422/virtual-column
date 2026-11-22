import pandas as pd

from solution import add_virtual_column


# Revenue calculation test

df = pd.DataFrame({
    "quantity": [2, 3],
    "unit_price": [100, 50],
    "discount": [10, 5]
})

result = add_virtual_column(
    df,
    "quantity * unit_price - discount",
    "revenue"
)

assert result["revenue"].tolist() == [190, 145]

print("Revenue test passed.")

# Invalid column test

result = add_virtual_column(
    df,
    "quantity * missing_column",
    "revenue"
)

assert result.empty

print("Invalid column test passed.")

# Empty column name test

result = add_virtual_column(
    df,
    "quantity * unit_price",
    ""
)

assert result.empty

print("Empty column name test passed.")


# Invalid expression test

result = add_virtual_column(
    df,
    "quantity +",
    "revenue"
)

assert result.empty

print("Invalid expression test passed.")

# Invalid label naming convention test

result = add_virtual_column(
    df,
    "quantity1 + quantity",
    "revenue"
)

assert result.empty

print("Invalid label naming convention test passed.")