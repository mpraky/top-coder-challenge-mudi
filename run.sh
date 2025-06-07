#!/bin/bash

# Simplified implementation focused on core patterns from test data analysis
# Based on reverse-engineering the actual behavior from public test cases

python3 - "$@" <<'PY'
import sys
import math

if len(sys.argv) != 4:
    sys.exit("Usage: run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>")

try:
    days = float(sys.argv[1])
    miles = float(sys.argv[2])
    receipts = float(sys.argv[3])
except ValueError:
    sys.exit("Invalid input")

# Enhanced approach with efficiency bonuses for high-intensity trips
def calculate_reimbursement(days, miles, receipts):
    # Base per diem with penalties for very long trips
    if days <= 7:
        base_amount = days * 100.0
    elif days <= 10:
        # Slight penalty for 8-10 day trips
        base_amount = days * 95.0
    elif days <= 13:
        # Bigger penalty for 11-13 day trips
        base_amount = days * 88.0
    else:
        # Heavy penalty for 14+ day trips
        base_amount = days * 80.0
    
    # 5-day bonus
    if days == 5:
        base_amount *= 1.04
    
    # More aggressive tiered mileage
    if miles <= 100:
        mileage_amount = miles * 0.58
    elif miles <= 300:
        mileage_amount = 100 * 0.58 + (miles - 100) * 0.52
    elif miles <= 600:
        mileage_amount = 100 * 0.58 + 200 * 0.52 + (miles - 300) * 0.40
    elif miles <= 1000:
        mileage_amount = 100 * 0.58 + 200 * 0.52 + 300 * 0.40 + (miles - 600) * 0.25
    else:
        # Very high mileage gets penalized heavily
        mileage_amount = 100 * 0.58 + 200 * 0.52 + 300 * 0.40 + 400 * 0.25 + (miles - 1000) * 0.10
    
    # Receipt handling
    if receipts < 40:
        receipt_amount = receipts * -0.8
    elif receipts < 150:
        receipt_amount = receipts * -0.3
    elif receipts < 400:
        receipt_amount = receipts * 0.15
    elif receipts < 800:
        receipt_amount = receipts * 0.45
    elif receipts < 1500:
        receipt_amount = receipts * 0.35
    else:
        receipt_amount = receipts * 0.25
    
    # EFFICIENCY BONUS - this was the missing piece!
    # High-intensity trips get multiplicative bonuses
    if days > 0:
        miles_per_day = miles / days
        
        # Single-day high-mileage trips get special treatment
        if days == 1 and miles > 600:
            efficiency_multiplier = 1.0 + (miles - 600) * 0.0008
            if receipts > 1000:  # Additional boost for high receipts
                efficiency_multiplier *= 1.2
        
        # Multi-day high-intensity trips
        elif miles_per_day > 300 and receipts > 1000:
            efficiency_multiplier = 1.0 + (miles_per_day - 300) * 0.0015
        elif miles_per_day > 200 and receipts > 800:
            efficiency_multiplier = 1.0 + (miles_per_day - 200) * 0.001
        elif miles_per_day > 150:
            efficiency_multiplier = 1.0 + (miles_per_day - 150) * 0.0005
        else:
            efficiency_multiplier = 1.0
    else:
        efficiency_multiplier = 1.0
    
    # Combine components and apply efficiency multiplier
    total = (base_amount + mileage_amount + receipt_amount) * efficiency_multiplier
    
    return total

result = calculate_reimbursement(days, miles, receipts)
print(f"{result:.2f}")
PY
