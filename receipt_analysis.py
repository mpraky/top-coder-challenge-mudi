#!/usr/bin/env python3
import json

# Load test data
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

print("=== SYSTEMATIC RECEIPT ANALYSIS ===")
print("Let's examine if receipts actually can cause NEGATIVE adjustments")

# Look at pairs of similar cases with different receipt amounts
print("\nLooking for cases with similar days/miles but different receipts:")

# Group by days and approximate miles
grouped = {}
for case in cases:
    days = case['input']['trip_duration_days'] 
    miles = case['input']['miles_traveled']
    miles_bucket = (miles // 50) * 50  # Round to nearest 50
    
    key = (days, miles_bucket)
    if key not in grouped:
        grouped[key] = []
    grouped[key].append(case)

# Find groups with multiple cases
for key, group in grouped.items():
    if len(group) >= 3:  # At least 3 cases
        days, miles_bucket = key
        print(f"\n{days} days, ~{miles_bucket} miles ({len(group)} cases):")
        
        # Sort by receipt amount
        sorted_group = sorted(group, key=lambda x: x['input']['total_receipts_amount'])
        
        for case in sorted_group[:5]:  # Show first 5
            inp = case['input']
            exp = case['expected_output']
            receipts = inp['total_receipts_amount']
            miles = inp['miles_traveled']
            
            print(f"  {miles}mi, ${receipts:.0f}r → ${exp:.0f}")
        
        # Check if higher receipts lead to lower reimbursements
        if len(sorted_group) >= 2:
            lowest_receipt = sorted_group[0]
            highest_receipt = sorted_group[-1]
            
            if highest_receipt['expected_output'] < lowest_receipt['expected_output']:
                print(f"  ⚠️  Higher receipts (${highest_receipt['input']['total_receipts_amount']:.0f}) → LOWER reimbursement!")

print("\n=== RECEIPT PENALTY ANALYSIS ===")
print("Let's see if there are clear receipt penalty thresholds")

# Look for receipt amounts where reimbursement suddenly drops
receipt_impacts = []

for case in cases:
    inp = case['input']
    exp = case['expected_output']
    days = inp['trip_duration_days']
    miles = inp['miles_traveled']
    receipts = inp['total_receipts_amount']
    
    # Calculate base + mileage estimate
    base = days * 100
    if miles <= 60:
        mileage = miles * 0.39
    elif miles <= 120:
        mileage = 60 * 0.39 + (miles - 60) * 0.67
    else:
        mileage = 60 * 0.39 + 60 * 0.67 + (miles - 120) * 0.62
    
    receipt_impact = exp - base - mileage
    
    receipt_impacts.append((receipts, receipt_impact, case))

# Sort by receipt amount and look for patterns
sorted_impacts = sorted(receipt_impacts, key=lambda x: x[0])

print(f"\nReceipt amount vs Impact on reimbursement:")
print("Receipt Amount | Impact | Case")
print("---------------|--------|-----")

for i in range(0, len(sorted_impacts), len(sorted_impacts)//20):  # Sample every 5%
    receipts, impact, case = sorted_impacts[i]
    inp = case['input']
    print(f"${receipts:8.0f}   | ${impact:6.0f} | {inp['trip_duration_days']}d, {inp['miles_traveled']}mi")

# Look for sudden drops
print("\n=== LOOKING FOR PENALTY THRESHOLDS ===")
current_bucket = 0
bucket_size = 100

bucket_impacts = []
for receipts, impact, case in sorted_impacts:
    bucket = int(receipts // bucket_size) * bucket_size
    bucket_impacts.append((bucket, impact))

# Group by bucket and calculate averages
bucket_averages = {}
for bucket, impact in bucket_impacts:
    if bucket not in bucket_averages:
        bucket_averages[bucket] = []
    bucket_averages[bucket].append(impact)

print("Receipt Range | Avg Impact | Count")
print("-------------|-----------|------")
for bucket in sorted(bucket_averages.keys())[:15]:  # First 15 buckets
    impacts = bucket_averages[bucket]
    avg_impact = sum(impacts) / len(impacts)
    print(f"${bucket:4.0f}-${bucket+bucket_size-1:4.0f}  | ${avg_impact:8.0f} | {len(impacts):4d}")
