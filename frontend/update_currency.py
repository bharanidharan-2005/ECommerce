import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\utils\currency.js"

content = """export const BASE_CURRENCY = "USD";
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
};

export const formatCurrency = (amount, currency = "INR") => {
    let numericAmount = parseFloat(amount);
    
    // Determine locale based on currency for accurate number formatting
    let locale = 'en-US';
    if (currency === 'INR') locale = 'en-IN';
    else if (currency === 'EUR') locale = 'de-DE';
    else if (currency === 'GBP') locale = 'en-GB';
    else if (currency === 'AED') locale = 'ar-AE';
    else if (currency === 'SGD') locale = 'en-SG';

    return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    }).format(numericAmount);
};

export const formatConvertedCurrency = (amount, fromCurrency = "USD", toCurrency = "INR") => {
    const converted = convertCurrency(amount, fromCurrency, toCurrency);
    return formatCurrency(converted, toCurrency);
};
"""

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated currency.js")
