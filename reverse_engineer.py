#!/usr/bin/env python3
import json

# Load test data
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

print("=== REVERSE ENGINEERING APPROACH ===")
print("Let's work backwards from known outputs to understand the formula")

# Test a few specific simple cases
test_cases = [
    (3, 93, 1.42, 364.51),
    (1, 55, 3.60, 126.06), 
    (2, 13, 4.67, 203.52),
    (1, 47, 17.97, 128.91),
    (3, 88, 5.78, 380.37)
]

print("\nAnalyzing simple cases:")
for days, miles, receipts, expected in test_cases:
    print(f"\n{days} days, {miles} miles, ${receipts:.2f} receipts → ${expected:.2f}")
    
    # Try different base assumptions
    # Assumption 1: Simple base + mileage + receipts
    base_100 = days * 100
    mileage_58 = miles * 0.58
    remaining = expected - base_100 - mileage_58
    receipt_rate = remaining / receipts if receipts > 0 else 0
    print(f"  If base=$100/day, mileage=$0.58/mi: remaining=${remaining:.2f} ({receipt_rate:.1%} of receipts)")
    
    # Assumption 2: Different base rate
    base_120 = days * 120  
    remaining2 = expected - base_120 - mileage_58
    receipt_rate2 = remaining2 / receipts if receipts > 0 else 0
    print(f"  If base=$120/day, mileage=$0.58/mi: remaining=${remaining2:.2f} ({receipt_rate2:.1%} of receipts)")

# Look for patterns in 5-day trips
print("\n=== 5-DAY TRIP ANALYSIS ===")
five_day_cases = [c for c in cases if c['input']['trip_duration_days'] == 5]
print(f"Analyzing first 10 of {len(five_day_cases)} five-day cases:")

for case in five_day_cases[:10]:
    inp = case['input']
    exp = case['expected_output']
    days = inp['trip_duration_days']
    miles = inp['miles_traveled']
    receipts = inp['total_receipts_amount']
    
    # Standard calculation
    base_std = 5 * 100
    mileage_std = miles * 0.58
    remaining = exp - base_std - mileage_std
    
    # With 5-day bonus
    base_bonus = 5 * 100 * 1.15  # 15% bonus
    remaining_bonus = exp - base_bonus - mileage_std
    
    print(f"  {miles}mi, ${receipts:.2f}r → ${exp:.2f}")
    print(f"    Standard base: remaining=${remaining:.2f}")
    print(f"    With 15% bonus: remaining=${remaining_bonus:.2f}")

# Look at 1-day trips to isolate the formula
print("\n=== 1-DAY TRIP ANALYSIS ===")
one_day_cases = [c for c in cases if c['input']['trip_duration_days'] == 1]
print(f"Analyzing first 15 of {len(one_day_cases)} one-day cases:")

for case in sorted(one_day_cases, key=lambda x: x['input']['miles_traveled'])[:15]:
    inp = case['input']
    exp = case['expected_output']
    miles = inp['miles_traveled']
    receipts = inp['total_receipts_amount']
    
    print(f"  {miles}mi, ${receipts:.2f}r → ${exp:.2f}")
    
    # If we assume base is $100 + some mileage rate + some receipt processing
    remaining_after_base = exp - 100
    if miles > 0:
        implied_mileage_rate = (remaining_after_base - receipts * 0.5) / miles  # rough estimate
        print(f"    After $100 base & rough receipt est: ${implied_mileage_rate:.3f}/mi")
