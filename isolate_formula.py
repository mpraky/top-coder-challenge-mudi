#!/usr/bin/env python3
import json

# Load test data
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

print("=== ISOLATING BASE + MILEAGE FORMULA ===")
print("Looking at cases with receipts < $20 to minimize receipt impact")

low_receipt_cases = [c for c in cases if c['input']['total_receipts_amount'] < 20]
print(f"Found {len(low_receipt_cases)} cases with receipts < $20")

# Sort by days, then miles
sorted_cases = sorted(low_receipt_cases, key=lambda x: (x['input']['trip_duration_days'], x['input']['miles_traveled']))

current_days = None
for case in sorted_cases:
    inp = case['input']
    exp = case['expected_output']
    days = inp['trip_duration_days']
    miles = inp['miles_traveled']
    receipts = inp['total_receipts_amount']
    
    if days != current_days:
        current_days = days
        print(f"\n--- {days}-DAY TRIPS ---")
    
    # Calculate what mileage rate would work if base is $100/day
    base_estimate = days * 100
    mileage_component = exp - base_estimate
    rate_per_mile = mileage_component / miles if miles > 0 else 0
    
    print(f"  {miles:3d}mi, ${receipts:5.2f}r → ${exp:6.2f} | mileage component: ${mileage_component:5.2f} (${rate_per_mile:.3f}/mi)")

print("\n=== TESTING DIFFERENT BASE RATES ===")
print("Let's see what base rate makes mileage rates most consistent")

for base_rate in [90, 95, 100, 105, 110]:
    print(f"\nTesting base rate: ${base_rate}/day")
    mileage_rates = []
    
    for case in sorted_cases[:10]:  # Just test first 10
        inp = case['input']
        exp = case['expected_output']
        days = inp['trip_duration_days']
        miles = inp['miles_traveled']
        receipts = inp['total_receipts_amount']
        
        base_estimate = days * base_rate
        mileage_component = exp - base_estimate
        rate_per_mile = mileage_component / miles if miles > 0 else 0
        mileage_rates.append(rate_per_mile)
    
    if mileage_rates:
        avg_rate = sum(mileage_rates) / len(mileage_rates)
        print(f"  Average mileage rate: ${avg_rate:.3f}/mi")

print("\n=== TESTING TIERED MILEAGE THEORY ===")
print("Let's see if mileage rates change based on distance tiers")

# Group by mileage ranges
mileage_groups = {
    'low': [c for c in low_receipt_cases if c['input']['miles_traveled'] <= 50],
    'medium': [c for c in low_receipt_cases if 50 < c['input']['miles_traveled'] <= 150],
    'high': [c for c in low_receipt_cases if c['input']['miles_traveled'] > 150]
}

for group_name, group_cases in mileage_groups.items():
    if not group_cases:
        continue
        
    print(f"\n{group_name.upper()} MILEAGE GROUP ({len(group_cases)} cases):")
    
    rates = []
    for case in group_cases:
        inp = case['input']
        exp = case['expected_output']
        days = inp['trip_duration_days']
        miles = inp['miles_traveled']
        
        base_estimate = days * 100
        mileage_component = exp - base_estimate
        rate_per_mile = mileage_component / miles if miles > 0 else 0
        rates.append(rate_per_mile)
        
        if len(rates) <= 5:  # Show first 5 examples
            print(f"  {days}d, {miles}mi → ${rate_per_mile:.3f}/mi")
    
    if rates:
        avg_rate = sum(rates) / len(rates)
        print(f"  Average rate: ${avg_rate:.3f}/mi")
