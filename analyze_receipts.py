#!/usr/bin/env python3
import json

# Load test data
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

print("=== HIGH RECEIPT ANALYSIS ===")
print("Understanding how large receipt amounts are processed")

# Get cases with high receipts
high_receipt_cases = [c for c in cases if c['input']['total_receipts_amount'] > 500]
print(f"Found {len(high_receipt_cases)} cases with receipts > $500")

print("\nSample high-receipt cases:")
for case in sorted(high_receipt_cases, key=lambda x: x['input']['total_receipts_amount'])[:15]:
    inp = case['input']
    exp = case['expected_output']
    days = inp['trip_duration_days']
    miles = inp['miles_traveled']
    receipts = inp['total_receipts_amount']
    
    # Calculate base + mileage using our current understanding
    base = days * 100
    
    # Mileage using current tiers
    if miles <= 60:
        mileage = miles * 0.39
    elif miles <= 120:
        mileage = 60 * 0.39 + (miles - 60) * 0.67
    else:
        mileage = 60 * 0.39 + 60 * 0.67 + (miles - 120) * 0.62
    
    # What's left must be receipt processing
    receipt_component = exp - base - mileage
    receipt_rate = receipt_component / receipts if receipts > 0 else 0
    
    print(f"{days}d, {miles}mi, ${receipts:.0f}r → ${exp:.0f} | receipt part: ${receipt_component:.0f} ({receipt_rate:.1%})")

print("\n=== MEDIUM RECEIPT ANALYSIS ===")
# Get cases with medium receipts (50-500)
medium_receipt_cases = [c for c in cases if 50 <= c['input']['total_receipts_amount'] <= 500]
print(f"Found {len(medium_receipt_cases)} cases with receipts $50-500")

print("\nSample medium-receipt cases:")
for case in sorted(medium_receipt_cases, key=lambda x: x['input']['total_receipts_amount'])[:15]:
    inp = case['input']
    exp = case['expected_output']
    days = inp['trip_duration_days']
    miles = inp['miles_traveled']
    receipts = inp['total_receipts_amount']
    
    # Calculate base + mileage
    base = days * 100
    if miles <= 60:
        mileage = miles * 0.39
    elif miles <= 120:
        mileage = 60 * 0.39 + (miles - 60) * 0.67
    else:
        mileage = 60 * 0.39 + 60 * 0.67 + (miles - 120) * 0.62
    
    receipt_component = exp - base - mileage
    receipt_rate = receipt_component / receipts if receipts > 0 else 0
    
    print(f"{days}d, {miles}mi, ${receipts:.0f}r → ${exp:.0f} | receipt part: ${receipt_component:.0f} ({receipt_rate:.1%})")

print("\n=== RECEIPT RATE BY AMOUNT ===")
# Group all cases by receipt amount ranges
receipt_ranges = [
    (0, 20, "Very low"),
    (20, 100, "Low"), 
    (100, 300, "Medium"),
    (300, 800, "High"),
    (800, 99999, "Very high")
]

for min_r, max_r, label in receipt_ranges:
    range_cases = [c for c in cases if min_r <= c['input']['total_receipts_amount'] < max_r]
    if not range_cases:
        continue
        
    print(f"\n{label} receipts (${min_r}-${max_r}): {len(range_cases)} cases")
    
    rates = []
    for case in range_cases[:10]:  # Sample first 10
        inp = case['input']
        exp = case['expected_output']
        days = inp['trip_duration_days']
        miles = inp['miles_traveled']
        receipts = inp['total_receipts_amount']
        
        base = days * 100
        if miles <= 60:
            mileage = miles * 0.39
        elif miles <= 120:
            mileage = 60 * 0.39 + (miles - 60) * 0.67
        else:
            mileage = 60 * 0.39 + 60 * 0.67 + (miles - 120) * 0.62
        
        receipt_component = exp - base - mileage
        receipt_rate = receipt_component / receipts if receipts > 0 else 0
        rates.append(receipt_rate)
    
    if rates:
        avg_rate = sum(rates) / len(rates)
        print(f"  Average receipt reimbursement rate: {avg_rate:.1%}")
