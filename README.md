# CloudFide Recruitment Task

This repository contains my solution for the CloudFide Junior Data Engineer recruitment task.

## Repository Contents

- Part 1: Virtual column implementation
- Part 2: Sales data quality pipeline
- Unit tests
- Documentation describing assumptions and design decisions

## Project Structure

Recruitment Task
│
├── data
│   ├── sales.csv
│   └── revenue_by_region.csv
│
├── my_test.py
├── test_virtual_column.py
├── pipeline.py
├── solution.py
├── README.md
└── requirements.txt

## Approach

Although the task description starts with the virtual column implementation,
I began with the sales dataset analysis. The revenue calculation requirements
helped define what the virtual column function should support.

## Part 2 - Data Analysis & Pipeline

### Duplicate records

Affected rows: 10 (5 duplicate pairs)

Examples:
- SO-10305
- SO-10822
- SO-10966
- SO-11240
- SO-11405

Resolution:
After verification, all duplicate records were exact copies.
The duplicate copies were removed using `drop_duplicates()`.

### Invalid non-transaction rows

Affected rows: 2

Examples:
- Repeated header row ("Order ID")
- Summary row ("TOTAL")

Resolution:
These rows do not represent actual sales transactions and were removed before revenue calculations.

### Inconsistent region names

Affected rows: 15

Examples:
- west
- WEST
-  North

Resolution:
Region names were standardized using string trimming and title casing
to ensure consistent aggregation by region.

### Product

Affected rows: 0

Validation performed:
- checked for missing values
- checked for inconsistent naming

Result:
No data quality issues were found in the product column.

### Negative quantities

Affected rows: 6

Examples:
- SO-10779
- SO-10515
- SO-11011
- SO-11289
- SO-10421
- SO-11445

Analysis:
Negative quantities may represent returns or order corrections.
The dataset does not provide enough business context to classify them as invalid.

Resolution:
Negative quantities were preserved and included in revenue calculations.

### Missing unit prices

Affected rows: 11

Analysis:
A distinct value analysis (`nunique`) confirmed that each product
has exactly one unit price in the dataset.

Resolution:
Missing prices were filled using the price associated with the same product.

Result:
All 11 missing values were successfully restored.

### Missing discount values

Affected rows: 959

Analysis:
According to the task specification, an empty discount means that no discount was applied.

Resolution:
Missing discount values were replaced with 0 using fillna(0).

### Order Date

Affected rows: 0

Validation performed:
- checked for missing values
- checked for invalid date formats

Result:
No issues were found in the order_date column.

## Part 1 - Virtual Column

Implemented `add_virtual_column()` function which:

- accepts a pandas DataFrame,
- evaluates arithmetic expressions based on existing columns,
- creates a new virtual column,
- returns an empty DataFrame when an expression cannot be evaluated.

### Example

```python
add_virtual_column(
    df,
    "quantity * unit_price - discount",
    "revenue"
)
```
### Implementation Details

The solution uses the pandas `DataFrame.eval()` expression engine,
allowing arithmetic expressions to be evaluated directly against
DataFrame columns.

## Assumptions

- Empty discount values represent no discount and were replaced with 0.
- Negative quantities were preserved because they may represent returns or corrections.
- Missing unit prices were restored using prices associated with identical products.
- Revenue is calculated as:
  
  revenue = quantity * unit_price - discount

## Usage

Run the pipeline:

```bash
python pipeline.py
```

Output:
data/revenue_by_region.csv

### Run tests

```bash
python run_tests.py
```

## Results

The pipeline successfully:

- cleaned and standardized the sales dataset,
- generated a revenue column using `add_virtual_column()`,
- aggregated total revenue by region,
- exported the results to `data/revenue_by_region.csv`.

## Author

Martin Karwacki