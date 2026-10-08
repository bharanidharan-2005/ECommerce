export const BASE_CURRENCY = "INR";
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
