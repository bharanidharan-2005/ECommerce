# ShopVerse — Full-Stack E-Commerce Platform

Django + DRF (JWT) backend • React + Redux Toolkit frontend • PostgreSQL • Stripe payments • Tailwind CSS

## Folder Structure

```
ECommerce/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── config/
│   │   ├── settings.py        # JWT, CORS, DB, S3, Stripe config
│   │   └── urls.py            # API root routes
│   └── apps/
│       ├── accounts/          # Custom User, register/login/profile (JWT)
│       ├── products/          # Category, Product, Review (+ search/filter/pagination)
│       └── orders/            # Order, OrderItem, checkout, Stripe webhook
└── frontend/
    ├── package.json
    ├── tailwind.config.js
    └── src/
        ├── api/axios.js       # Axios instance + auto token refresh
        ├── app/store.js       # Redux store
        ├── features/
        │   ├── auth/          # authSlice (login/register/logout)
        │   ├── products/      # productsSlice (fetch/search/filter)
        │   └── cart/          # cartSlice (persistent via localStorage)
        ├── components/        # Navbar, ProductCard, SkeletonCard, Pagination...
        ├── pages/             # Home, ProductList, ProductDetail, Cart,
        │                      # Checkout (Stripe Elements), Login, Register,
        │                      # Profile (order history), OrderSuccess, 404
        └── utils/
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL running locally (or leave `DATABASE_URL` empty in `.env` for SQLite fallback)

## Backend Setup

```bash
cd ECommerce/backend

# 1. Virtual environment
python -m venv venv
venv\Scripts\activate              # Windows
# source venv/bin/activate         # macOS/Linux

# 2. Dependencies
pip install -r requirements.txt

# 3. Environment variables
copy .env.example .env             # then edit SECRET_KEY, DATABASE_URL, STRIPE keys

# 4. Database
python manage.py makemigrations accounts products orders
python manage.py migrate

# 5. Admin superuser (for /admin dashboard)
python manage.py createsuperuser

# 6. Seed sample data (optional)
python manage.py shell < seed_data.py

# 7. Run
python manage.py runserver         # http://localhost:8000
```

> **Note:** If port 8000 is in use, run the backend on another port (e.g. `python manage.py runserver 8010`) and update `VITE_API_URL` in `frontend/.env` to match.

## Frontend Setup

```bash
cd ECommerce/frontend

npm install
copy .env.example .env             # set VITE_API_URL and VITE_STRIPE_PUBLISHABLE_KEY
npm run dev                        # http://localhost:1234
```

## Stripe Sandbox

1. Create an account at https://dashboard.stripe.com (test mode).
2. Copy **Secret key** -> `backend/.env` as `STRIPE_SECRET_KEY`.
3. Copy **Publishable key** -> `frontend/.env` as `VITE_STRIPE_PUBLISHABLE_KEY`.
4. Test card: `4242 4242 4242 4242`, any future expiry, any CVC.
5. For webhooks in dev: `stripe listen --forward-to localhost:8000/api/orders/stripe/webhook/`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Create account |
| POST | `/api/auth/login/` | Obtain JWT pair |
| POST | `/api/auth/token/refresh/` | Refresh access token |
| GET/PATCH | `/api/auth/me/` | Current user profile |
| GET | `/api/products/?search=&category=&ordering=&page=` | List products |
| GET | `/api/products/:id/` | Product detail + reviews |
| POST | `/api/orders/checkout/` | Create order — routes by `payment_method` (`cod` \| `card` \| `upi_gpay` \| `upi_paytm`) |
| GET | `/api/orders/my/` | User's order history |
| POST | `/api/orders/stripe/webhook/` | Stripe payment events |

## Payment Methods

| Method | Flow |
|---|---|
| **Cash on Delivery** | Order saved as `pending`/unpaid; settled in cash at the door. No gateway needed. |
| **Card** | Stripe PaymentIntent confirmed client-side; webhook marks order paid. Needs real `sk_test_…` keys. |
| **Google Pay / Paytm (UPI)** | Captures the shopper's UPI ID, creates a pending order + collect request. With real gateway credentials (Stripe India UPI or Paytm merchant API) the webhook/callback flips it to `paid`; without keys orders stay pending for manual settlement. |

## Production Notes

- Set `DEBUG=False`, configure `ALLOWED_HOSTS`, strong `SECRET_KEY`.
- Set `DATABASE_URL` to managed Postgres (models include db indexes).
- Set `USE_S3=True` + AWS credentials to serve media from S3.
- Run behind gunicorn/nginx: `gunicorn config.wsgi:application`.
