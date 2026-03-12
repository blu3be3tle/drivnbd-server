# 🛍️ DrivnBD – Modern Clothing E-Commerce Backend

**DrivnBD** is a production-ready **Django REST Framework** backend powering a full-featured online clothing store. It handles product catalog, user authentication, shopping cart, secure checkout with **SSLCommerz** payment gateway, order management — all deployed serverlessly.

- **Live API**: https://drivnbd-serverside.vercel.app/
- **Interactive Swagger Docs**: https://drivnbd-serverside.vercel.app/api/docs/
- **Companion Frontend (React)**: https://drivnbd-client.vercel.app/
- **License**: MIT

## ✨ Key Features

- RESTful API with **Django 5** + **Django REST Framework**
- **JWT Authentication** (stateless, using `djangorestframework-simplejwt` + `djoser`)
- Custom user model with registration, login, password reset
- Product catalog: categories, stock, featured/new items, filtering & search
- Persistent shopping cart & multi-item orders
- **SSLCommerz** payment gateway integration (Bangladesh-focused)
- **Cloudinary** for optimized product image uploads & CDN delivery
- **PostgreSQL** database (hosted on Supabase)
- Auto-generated **Swagger UI** documentation
- Serverless deployment on **Vercel** (fast cold starts, auto-scaling)
- Production best practices: env vars, WhiteNoise statics, secure config

## 🏗️ Architecture Overview

Modular Django project with clear separation of concerns:

```
drivnbd-server/
├── api/                # Main API router & shared utilities
├── drivnbd/            # Project core: settings.py, wsgi.py (Vercel entrypoint)
├── users/              # Custom User model + auth logic
├── store/              # Product, Category, FeaturedItem models & endpoints
├── order/              # Cart, Order, OrderItem, checkout & payment logic
├── fixtures/           # Sample data (products, categories) – loaddata ready
├── staticfiles/        # Collected static assets (WhiteNoise in prod)
├── .gitignore
├── dockerfile          # Optional Docker support
├── manage.py
├── requirements.txt
├── readme.md
└── vercel.json         # Vercel serverless config
```

### High-Level System Diagram & Data Flow

```
                ┌────────────────────────────┐
                │     Frontend (React SPA)   │
                │   (Cart state, JWT storage)│
                └──────────────┬─────────────┘
                               │ JWT Bearer Token
                               ▼
                ┌────────────────────────────┐
                │     REST API (DRF)         │
                │     /api/ (routers)        │
                └──────────────┬─────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
  ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
  │    users/     │   │    store/     │   │    order/     │
  │ - CustomUser  │   │ - Category    │   │ - Cart        │
  │ - JWT / Djoser│   │ - Product     │   │ - Order       │
  │ - Profiles    │   │ - Featured    │   │ - OrderItem   │
  └───────────────┘   └───────────────┘   └───────┬───────┘
                                                  │
                                                  ▼
                                     ┌────────────────────────────┐
                                     │     PostgreSQL             │
                                     │     (Supabase hosted)      │
                                     └──────────────┬─────────────┘
                                                    │
                                                    ▼
                                     ┌────────────────────────────┐
                                     │     Cloudinary             │
                                     │     (Images + CDN)         │
                                     └────────────────────────────┘

                          Payment Flow (SSLCommerz)
                                     ▲
                                     │ Redirect / Webhook
                                     ▼
                           ┌──────────────────────┐
                           │   SSLCommerz Gateway │
                           └──────────────────────┘
```

**Main Flows Explained**:

1. **Browsing Products** (public)
   - GET `/api/store/products/` → list/filter
   - GET `/api/store/products/{id}/` → detail (with Cloudinary image URLs)

2. **Authentication**
   - POST `/api/auth/users/` → register
   - POST `/api/auth/jwt/create/` → login → access + refresh tokens
   - POST `/api/auth/jwt/refresh/` → refresh access token
   - Protected endpoints require `Authorization: Bearer <access_token>`

3. **Shopping & Checkout**
   - POST `/api/order/cart/add/` → add item (authenticated)
   - GET/PATCH `/api/order/cart/` → view/update cart
   - POST `/api/order/checkout/` → create Order from cart → initiate SSLCommerz session
   - Redirect user to SSLCommerz payment page
   - SSLCommerz webhook/IPN → update Order status (paid/failed)

4. **Order History**
   - GET `/api/order/my-orders/` → list authenticated user's orders

5. **Media Upload**
   - Admin/authorized users upload images → backend sends signed request to Cloudinary
   - Cloudinary returns optimized URL → saved in Product model

## 🛠️ Tech Stack

| Layer             | Technology                          | Purpose                              |
|-------------------|-------------------------------------|--------------------------------------|
| Framework         | Django 5 + DRF                      | API & business logic                 |
| Auth              | simplejwt + djoser                  | JWT tokens & auth endpoints          |
| Database          | PostgreSQL (Supabase)               | Relational storage                   |
| Images            | Cloudinary                          | Upload, optimization, CDN            |
| Payment           | SSLCommerz                          | Secure checkout (Bangladesh)         |
| Docs              | drf-yasg                            | Swagger UI                           |
| Static Files      | WhiteNoise                          | Production static serving            |
| Deployment        | Vercel (serverless Python)          | Zero-ops hosting                     |
| Config            | python-dotenv / env vars            | 12-factor security                   |

## 🚀 Quick Start (Local)

1. Clone & enter directory
   ```bash
   git clone https://github.com/blu3be3tle/drivnbd-server.git
   cd drivnbd-server
   ```

2. Virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/macOS
   # venv\Scripts\activate     # Windows
   ```

3. Install dependencies
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Create `.env` in root (required keys):
   ```env
   SECRET_KEY=your-long-random-secret
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

   DATABASE_URL=postgresql://postgres:[YOUR-PASS]@db.[ref].supabase.co:5432/postgres

   CLOUDINARY_CLOUD_NAME=xxx
   CLOUDINARY_API_KEY=xxx
   CLOUDINARY_API_SECRET=xxx

   EMAIL_HOST_USER=your@gmail.com
   EMAIL_HOST_PASSWORD=app-password
   ```

5. Migrate & create admin
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. (Optional) Load sample data
   ```bash
   python manage.py loaddata fixtures/*.json
   ```

7. Run server
   ```bash
   python manage.py runserver
   ```
   → Swagger: http://127.0.0.1:8000/api/docs/

## 🌐 Vercel Deployment (Serverless)

1. Import repo to Vercel (or connect GitHub)
2. Add **Environment Variables** in Vercel dashboard (all from `.env` above + `DEBUG=False`)
3. Deploy → Vercel uses `vercel.json` → points to `drivnbd/wsgi.py`
4. Done — auto HTTPS, scaling, domain ready

## 📚 API Documentation

- **Swagger UI** → https://drivnbd-serverside.vercel.app/api/docs/
- **ReDoc** (clean alternative) → https://drivnbd-serverside.vercel.app/api/docs/redoc/

Every endpoint includes schemas, examples, auth info.

## 🤝 Contributing

1. Fork → branch (`git checkout -b feature/payment-webhook`)
2. Commit (`git commit -m 'Add SSLCommerz webhook handler'`)
3. Push & open PR

## 📄 License

MIT – see [LICENSE](LICENSE)

---

Built with ❤️ in Dhaka for scalable, beautiful e-commerce.

Happy shopping & coding! 👕✨




```mermaid
architecture-beta
    group frontend(browser)[Frontend (React SPA)]
        service spa(browser)[React App] in frontend

    group api(cloud)[API Layer (DRF)]
        service drf(cloud)[Django REST API] in api

    group backend(cloud)[Backend Apps]
        service users(database)[users/ - CustomUser, JWT] in backend
        service store(database)[store/ - Product, Category] in backend
        service order(database)[order/ - Cart, Order, Payment] in backend

    group data(cloud)[Data & External]
        service db(database)[PostgreSQL (Supabase)] in data
        service cloudinary(database)[Cloudinary (Images + CDN)] in data
        service sslcommerz(database)[SSLCommerz Gateway] in data

    spa:R --> L:drf : JWT Bearer Token
    drf:R --> L:users
    drf:R --> L:store
    drf:R --> L:order
    users:R --> L:db
    store:R --> L:db
    order:R --> L:db
    store:R --> L:cloudinary : Image URLs
    order:R --> L:sslcommerz : Initiate Session + Redirect
    sslcommerz:R --> L:order : IPN/Webhook (status update)