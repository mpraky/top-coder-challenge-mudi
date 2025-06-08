#!/usr/bin/env python3
import json
import statistics

# Load test data
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

print("=== DETAILED COMPONENT ANALYSIS ===")

# Look at zero/minimal receipt cases to understand base+mileage
print("\n1. Cases with minimal receipts (< $5) to understand base + mileage:")
minimal_receipts = [c for c in cases if c['input']['total_receipts_amount'] < 5]
print(f"Found {len(minimal_receipts)} cases with < $5 receipts")

for case in sorted(minimal_receipts, key=lambda x: (x['input']['trip_duration_days'], x['input']['miles_traveled']))[:15]:
    inp = case['input']
    exp = case['expected_output']
    days = inp['trip_duration_days']
    miles = inp['miles_traveled']
    receipts = inp['total_receipts_amount']
    
    # If base is $100/day, what's the mileage component?
    base_estimate = days * 100
    mileage_estimate = exp - base_estimate
    rate_per_mile = mileage_estimate / miles if miles > 0 else 0
    
    print(f"{days}d, {miles}mi, ${receipts:.2f}r → ${exp:.2f} | Est mileage: ${mileage_estimate:.2f} (${rate_per_mile:.3f}/mi)")

# Look at zero mileage cases to understand base + receipts
print("\n2. Cases with minimal mileage (< 20 miles) to understand base + receipts:")
minimal_miles = [c for c in cases if c['input']['miles_traveled'] < 20]
print(f"Found {len(minimal_miles)} cases with < 20 miles")

for case in sorted(minimal_miles, key=lambda x: (x['input']['trip_duration_days'], x['input']['total_receipts_amount']))[:15]:
    inp = case['input']
    exp = case['expected_output']
    days = inp['trip_duration_days']
    miles = inp['miles_traveled']
    receipts = inp['total_receipts_amount']
    
    # If base is $100/day and mileage is ~$0.58/mile
    base_estimate = days * 100
    mileage_estimate = miles * 0.58
    receipt_component = exp - base_estimate - mileage_estimate
    receipt_rate = receipt_component / receipts if receipts > 0 else 0
    
    print(f"{days}d, {miles}mi, ${receipts:.2f}r → ${exp:.2f} | Est receipts: ${receipt_component:.2f} ({receipt_rate:.1%})")

# Analyze 5-day bonus
print("\n3. Comparing 4-day vs 5-day vs 6-day trips (similar miles/receipts):")
print("4-day trips:")
four_day = [c for c in cases if c['input']['trip_duration_days'] == 4 and c['input']['miles_traveled'] < 200 and c['input']['total_receipts_amount'] < 100]
for case in four_day[:5]:
    inp = case['input']
    exp = case['expected_output']
    per_day = exp / 4
    print(f"  4d, {inp['miles_traveled']}mi, ${inp['total_receipts_amount']:.2f}r → ${exp:.2f} (${per_day:.2f}/day)")

print("5-day trips:")
five_day = [c for c in cases if c['input']['trip_duration_days'] == 5 and c['input']['miles_traveled'] < 200 and c['input']['total_receipts_amount'] < 100]
for case in five_day[:5]:
    inp = case['input']
    exp = case['expected_output']
    per_day = exp / 5
    print(f"  5d, {inp['miles_traveled']}mi, ${inp['total_receipts_amount']:.2f}r → ${exp:.2f} (${per_day:.2f}/day)")

print("6-day trips:")
six_day = [c for c in cases if c['input']['trip_duration_days'] == 6 and c['input']['miles_traveled'] < 200 and c['input']['total_receipts_amount'] < 100]
for case in six_day[:5]:
    inp = case['input']
    exp = case['expected_output']
    per_day = exp / 6
    print(f"  6d, {inp['miles_traveled']}mi, ${inp['total_receipts_amount']:.2f}r → ${exp:.2f} (${per_day:.2f}/day)")

# Analyze high mileage patterns
print("\n4. High mileage efficiency analysis:")
high_mileage = [c for c in cases if c['input']['miles_traveled'] > 500]
print(f"Found {len(high_mileage)} cases with > 500 miles")

for case in sorted(high_mileage, key=lambda x: x['input']['miles_traveled'] / x['input']['trip_duration_days'])[:10]:
    inp = case['input']
    exp = case['expected_output']
    days = inp['trip_duration_days']
    miles = inp['miles_traveled']
    receipts = inp['total_receipts_amount']
    miles_per_day = miles / days
    
    print(f"{days}d, {miles}mi, ${receipts:.2f}r → ${exp:.2f} | {miles_per_day:.1f} mi/day")
