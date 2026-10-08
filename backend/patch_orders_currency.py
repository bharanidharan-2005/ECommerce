# -*- coding: utf-8 -*-
import sys
import re

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\orders\views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'def get_converted_amount\(.*?\).*?return int\(total_price_usd \* 100\), "usd"', re.DOTALL)

new_func = '''def get_converted_amount(total_price_inr: float, currency_code: str) -> tuple:
    """
    Convert INR amount to target currency using fixed exchange rates.
    Returns (converted_amount_in_cents, currency_code).
    """
    # Base INR
    rates = {
        "INR": 1.0,
        "USD": 96.75,
        "EUR": 108.30,
        "GBP": 128.09
    }
    
    code = currency_code.upper()
    if code not in rates:
        code = "INR"
    
    # 1 USD = 96.75 INR -> USD = INR / 96.75
    converted = total_price_inr / rates[code]
    
    return int(converted * 100), code.lower()'''

if pattern.search(content):
    content = pattern.sub(new_func, content, count=1)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Patched backend get_converted_amount successfully.')
else:
    print('Could not find pattern')
