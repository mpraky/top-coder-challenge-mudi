#!/bin/bash

# Simple baseline implementation for the reimbursement calculator
# Uses a linear formula derived from the public_cases.json data via
# least squares regression. This is not expected to perfectly match
# the legacy system but serves as a deterministic baseline.

python3 - "$@" <<'PY'
import sys

if len(sys.argv) != 4:
    sys.exit("Usage: run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>")

try:
    d = float(sys.argv[1])
    m = float(sys.argv[2])
    r = float(sys.argv[3])
except ValueError:
    sys.exit("Invalid input")

# Coefficients learned with linear regression on the public dataset
coef_days = 50.05048622
coef_miles = 0.44564529
coef_receipts = 0.38286076
intercept = 266.7076805

result = coef_days * d + coef_miles * m + coef_receipts * r + intercept
print(f"{result:.2f}")
PY
