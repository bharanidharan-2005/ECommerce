import sys
sys.stdout.reconfigure(encoding='utf-8')
import os

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\utils\currency.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

target_rates = '''export const BASE_CURRENCY = "USD";
export const EXCHANGE_RATES = {
    USD: 1,
    INR: 96.10,
    EUR: 0.92,
    GBP: 0.79,
    AED: 3.67,
    SGD: 1.35
};

export const convertCurrency = (amount, fromCurrency = "USD", toCurrency = "INR") => {
    if (fromCurrency === toCurrency) return parseFloat(amount);
    const inUSD = parseFloat(amount) / EXCHANGE_RATES[fromCurrency];
    return inUSD * EXCHANGE_RATES[toCurrency];
};'''

new_rates = '''export const BASE_CURRENCY = "INR";
export const EXCHANGE_RATES = {
    INR: 1,
    USD: 1 / 96.75,
    EUR: 1 / 108.30,
    GBP: 1 / 128.09,
    AED: 1 / 26.34,
    SGD: 1 / 71.90
};

export const convertCurrency = (amount, fromCurrency = "INR", toCurrency = "INR") => {
    if (fromCurrency === toCurrency) return parseFloat(amount);
    const inBase = parseFloat(amount) / EXCHANGE_RATES[fromCurrency];
    return inBase * EXCHANGE_RATES[toCurrency];
};'''

content = content.replace(target_rates, new_rates)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched currency.js with accurate rates')
