#!/usr/bin/env python3
"""
Run delivery test using URLs from previous stress test
"""

import json
import os
import sys
import glob

sys.path.insert(0, os.path.dirname(__file__))

from delivery_test import run_delivery_test

# Find latest stress test results
results_files = sorted(glob.glob('./results/stress_test_*.json'))
if not results_files:
    print("No stress test results found!")
    sys.exit(1)

latest = results_files[-1]
print(f"Using URLs from: {latest}")

with open(latest) as f:
    data = json.load(f)

# Get successful URLs with good scores
urls = [
    r['url'] for r in data['results']
    if r.get('success') and r.get('total_score') and r['total_score'] > 50
]

print(f"Found {len(urls)} valid URLs")

# Run delivery test on first 100
urls = urls[:100]
run_delivery_test(urls, workers=8, output_dir='./test_pdfs')
