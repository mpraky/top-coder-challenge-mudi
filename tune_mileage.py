#!/usr/bin/env python3
import json

# Load test data
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

# Get low receipt cases
low_receipt_cases = [c for c in cases if c['input']['total_receipts_amount'] < 20]

print("=== PRECISE MILEAGE RATE CALCULATION ===")
print("For each case, calculate exact mileage rate needed (assuming $100/day base + small receipt bonus)")

for case in sorted(low_receipt_cases, key=lambda x: x['input']['miles_traveled']):
    inp = case['input']
    exp = case['expected_output']
    days = inp['trip_duration_days']
    miles = inp['miles_traveled']
    receipts = inp['total_receipts_amount']
    
    # Assume base is $100/day
    base = days * 100
    
    # Assume small receipt bonus (rough estimate)
    if receipts < 5:
        receipt_bonus = 0
    else:
        receipt_bonus = receipts * 0.25  # rough estimate
    
    # Calculate what mileage rate would be needed
    remaining = exp - base - receipt_bonus
    needed_rate = remaining / miles if miles > 0 else 0
    
    print(f"{miles:3d}mi, {days}d, ${receipts:5.2f}r → ${exp:6.2f} | Need ${needed_rate:.3f}/mi")

print("\n=== FINDING OPTIMAL TIERED RATES ===")
# Let's try to find the best tier boundaries and rates

# Sort by miles
sorted_by_miles = sorted(low_receipt_cases, key=lambda x: x['input']['miles_traveled'])

print("Testing different tier configurations:")

# Configuration 1: 0-60, 60-120, 120+
print("\nConfig 1: 0-60, 60-120, 120+")
tier1_cases = [c for c in low_receipt_cases if c['input']['miles_traveled'] <= 60]
tier2_cases = [c for c in low_receipt_cases if 60 < c['input']['miles_traveled'] <= 120]
tier3_cases = [c for c in low_receipt_cases if c['input']['miles_traveled'] > 120]

for tier_name, tier_cases in [("Tier1 (0-60)", tier1_cases), ("Tier2 (60-120)", tier2_cases), ("Tier3 (120+)", tier3_cases)]:
    if not tier_cases:
        continue
    
    rates = []
    for case in tier_cases:
        inp = case['input']
        exp = case['expected_output']
        days = inp['trip_duration_days']
        miles = inp['miles_traveled']
        receipts = inp['total_receipts_amount']
        
        base = days * 100
        receipt_bonus = 0 if receipts < 5 else receipts * 0.25
        remaining = exp - base - receipt_bonus
        needed_rate = remaining / miles if miles > 0 else 0
        rates.append(needed_rate)
    
    if rates:
        avg_rate = sum(rates) / len(rates)
        print(f"  {tier_name}: {len(tier_cases)} cases, avg rate: ${avg_rate:.3f}/mi")

# Test our current implementation on these cases
print("\n=== TESTING CURRENT IMPLEMENTATION ===")
import subprocess

print("Case -> Expected | Current | Error")
for case in sorted_by_miles[:10]:
    inp = case['input']
    exp = case['expected_output']
    days = inp['trip_duration_days']
    miles = inp['miles_traveled']
    receipts = inp['total_receipts_amount']
    
    # Run our current implementation
    result = subprocess.run(['./run.sh', str(days), str(miles), str(receipts)], 
                          capture_output=True, text=True, cwd='.')
    current = float(result.stdout.strip()) if result.stdout.strip() else 0
    error = abs(current - exp)
    
    print(f"{days}d,{miles}mi,${receipts:.2f} -> ${exp:.2f} | ${current:.2f} | ${error:.2f}")
