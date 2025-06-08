#!/usr/bin/env python3
import json
import statistics

# Load test data
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

# Analyze patterns
print("=== BASIC ANALYSIS ===")
print(f"Total cases: {len(cases)}")

# Group by trip duration
by_days = {}
for case in cases:
    days = case['input']['trip_duration_days']
    if days not in by_days:
        by_days[days] = []
    by_days[days].append(case)

print("\n=== BY TRIP DURATION ===")
for days in sorted(by_days.keys()):
    cases_for_days = by_days[days]
    outputs = [c['expected_output'] for c in cases_for_days]
    avg_output = statistics.mean(outputs)
    avg_per_day = avg_output / days
    print(f"{days} days: {len(cases_for_days)} cases, avg output: ${avg_output:.2f}, avg per day: ${avg_per_day:.2f}")

# Look at simple cases (low mileage, low receipts)
print("\n=== SIMPLE CASES (low miles, low receipts) ===")
simple_cases = [c for c in cases if c['input']['miles_traveled'] <= 100 and c['input']['total_receipts_amount'] <= 20]
print(f"Found {len(simple_cases)} simple cases")

for case in simple_cases[:10]:
    inp = case['input']
    exp = case['expected_output']
    days = inp['trip_duration_days']
    miles = inp['miles_traveled']
    receipts = inp['total_receipts_amount']
    per_day = exp / days
    print(f"{days} days, {miles} miles, ${receipts:.2f} receipts → ${exp:.2f} (${per_day:.2f}/day)")

# Look at 5-day trips specifically
print("\n=== 5-DAY TRIPS ===")
five_day_cases = [c for c in cases if c['input']['trip_duration_days'] == 5]
print(f"Found {len(five_day_cases)} five-day cases")

for case in five_day_cases[:10]:
    inp = case['input']
    exp = case['expected_output']
    miles = inp['miles_traveled']
    receipts = inp['total_receipts_amount']
    per_day = exp / 5
    print(f"5 days, {miles} miles, ${receipts:.2f} receipts → ${exp:.2f} (${per_day:.2f}/day)")

# Look at mileage patterns
print("\n=== MILEAGE ANALYSIS ===")
print("Looking at 1-day trips to isolate mileage effects...")
one_day_low_receipts = [c for c in cases if c['input']['trip_duration_days'] == 1 and c['input']['total_receipts_amount'] <= 20]

for case in sorted(one_day_low_receipts, key=lambda x: x['input']['miles_traveled'])[:15]:
    inp = case['input']
    exp = case['expected_output']
    miles = inp['miles_traveled']
    receipts = inp['total_receipts_amount']
    # Rough estimate: assume $100 base per diem + mileage + small receipt bonus
    estimated_mileage_component = exp - 100 - (receipts * 0.5)  # rough estimate
    rate_per_mile = estimated_mileage_component / miles if miles > 0 else 0
    print(f"{miles} miles, ${receipts:.2f} receipts → ${exp:.2f} (est ${rate_per_mile:.3f}/mile)")
