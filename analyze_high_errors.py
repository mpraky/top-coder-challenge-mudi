#!/usr/bin/env python3

import json

# High-error cases from the evaluation
high_error_cases = [
    {"case": 996, "days": 1, "miles": 1082, "receipts": 1809.49, "expected": 446.94, "got": 1567.23, "error": 1120.29},
    {"case": 684, "days": 8, "miles": 795, "receipts": 1645.99, "expected": 644.69, "got": 1502.25, "error": 857.56},
    {"case": 548, "days": 8, "miles": 482, "receipts": 1411.49, "expected": 631.81, "got": 1488.82, "error": 857.01},
    {"case": 520, "days": 14, "miles": 481, "receipts": 939.99, "expected": 877.17, "got": 1683.40, "error": 806.23},
    {"case": 367, "days": 11, "miles": 740, "receipts": 1171.99, "expected": 902.09, "got": 1695.20, "error": 793.11}
]

print("🔍 Analysis of High-Error Cases:")
print("=" * 50)

for case in high_error_cases:
    print(f"\nCase {case['case']}:")
    print(f"  Trip: {case['days']} days, {case['miles']} miles, ${case['receipts']:.2f} receipts")
    print(f"  Expected: ${case['expected']:.2f}")
    print(f"  Our result: ${case['got']:.2f}")
    print(f"  Error: ${case['error']:.2f}")
    
    # Calculate efficiency metrics
    miles_per_day = case['miles'] / case['days']
    receipts_per_day = case['receipts'] / case['days']
    
    print(f"  Efficiency: {miles_per_day:.1f} miles/day, ${receipts_per_day:.1f} receipts/day")
    
    # Analyze what might be wrong
    if case['receipts'] > 1000 and case['days'] <= 8:
        print(f"  ⚠️  High receipts ({case['receipts']}) for short trip - may be over-rewarded")
    
    if case['miles'] > 1000 and case['days'] == 1:
        print(f"  ⚠️  Very high single-day mileage - efficiency bonus may be too aggressive")
    
    if case['days'] >= 11:
        print(f"  ⚠️  Long trip penalty may not be strong enough")

print("\n📊 Pattern Analysis:")
print("=" * 50)

# Look for patterns
high_receipt_cases = [c for c in high_error_cases if c['receipts'] > 1000]
single_day_cases = [c for c in high_error_cases if c['days'] == 1]
long_trip_cases = [c for c in high_error_cases if c['days'] >= 10]

print(f"High receipts (>$1000): {len(high_receipt_cases)}/5 cases")
print(f"Single day trips: {len(single_day_cases)}/5 cases")
print(f"Long trips (10+ days): {len(long_trip_cases)}/5 cases")

if high_receipt_cases:
    print(f"\nHigh receipt cases avg expected: ${sum(c['expected'] for c in high_receipt_cases)/len(high_receipt_cases):.2f}")
    print(f"High receipt cases avg our result: ${sum(c['got'] for c in high_receipt_cases)/len(high_receipt_cases):.2f}")

print("\n💡 Recommendations:")
print("1. Cap or reduce efficiency bonuses for very high receipts")
print("2. Add stronger penalties for single-day extreme mileage")
print("3. Review receipt handling for amounts >$1000")
print("4. Strengthen long-trip penalties")
