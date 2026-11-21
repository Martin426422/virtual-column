# CloudFide Recruitment Task

This repository contains my solution for the CloudFide Junior Data Engineer recruitment task.

## Repository Status

Project initialization phase.

The repository will contain:

- Part 1: Virtual column implementation
- Part 2: Sales data quality pipeline
- Unit tests
- Documentation describing assumptions and design decisions

## Approach

Although the task description starts with the virtual column implementation,
I began with the sales dataset analysis. The revenue calculation requirements
helped define what the virtual column function should support.

### Duplicate records

Affected rows: 10 rows (5 duplicate pairs)

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

Validation performed:
- checked for missing values
- checked for invalid date formats

Result:
No issues were found in the order_date column.

## Author

Martin Karwacki