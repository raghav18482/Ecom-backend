# Hoodie Store API

A complete FastAPI backend for an e-commerce hoodie store with Supabase PostgreSQL integration.

## Features

- **FastAPI** framework with async/await support
- **Supabase PostgreSQL** database integration
- **JWT Authentication** with secure password hashing
- **RESTful API** endpoints for products, orders, and profiles
- **CORS** support for frontend integration
- **Docker** support for easy deployment
- **Comprehensive error handling** and logging

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user info

### Products
- `GET /api/v1/products` - List all products (with filters)
- `GET /api/v1/products/{id}` - Get specific product
- `POST /api/v1/products` - Create product (admin)
- `PUT /api/v1/products/{id}` - Update product (admin)
- `DELETE /api/v1/products/{id}` - Delete product (admin)

### Orders
- `POST /api/v1/orders` - Create new order
- `GET /api/v1/orders/{id}` - Get specific order
- `GET /api/v1/orders/user/{user_id}` - Get user's orders
- `PUT /api/v1/orders/{id}/status` - Update order status (admin)
- `PUT /api/v1/orders/{id}` - Update order (admin)

### Profiles
- `GET /api/v1/profiles/{user_id}` - Get user profile
- `PUT /api/v1/profiles/{user_id}` - Update user profile
- `POST /api/v1/profiles` - Create user profile

## Quick Start

### 1. Environment Setup

Copy the example environment file:
```bash
cp env.example .env
```

Update the `.env` file with your Supabase credentials:
```env
DATABASE_URL=postgresql://your-supabase-connection-string
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-anon-key
JWT_SECRET_KEY=your-secret-key
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Database Migrations

The application will automatically create tables on startup, or you can run the seed script:

```bash
python seed.py
```

### 4. Start the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 5. View API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database Schema

### Products Table
- `id` (UUID, Primary Key)
- `name` (Text, Not Null)
- `description` (Text)
- `price` (Numeric)
- `stock` (Integer)
- `images` (Text Array)
- `color` (Text)
- `size` (Text Array)
- `material` (Text)
- `fit_type` (Text)
- `gender` (Text)
- `category` (Text)
- `rating` (Numeric)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

### Orders Table
- `id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key)
- `total_amount` (Numeric)
- `payment_status` (Text)
- `order_status` (Text)
- `shipping_address` (Text)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

### Order Items Table
- `id` (UUID, Primary Key)
- `order_id` (UUID, Foreign Key)
- `product_id` (UUID, Foreign Key)
- `quantity` (Integer)
- `price` (Numeric)

### Profiles Table
- `id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key)
- `full_name` (Text)
- `phone` (Text)
- `address` (Text)
- `created_at` (Timestamp)

## Deployment

### Using Docker

1. Build the Docker image:
```bash
docker build -t hoodie-store-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 --env-file .env hoodie-store-api
```

### Using Render/Railway

1. Connect your GitHub repository
2. Set environment variables in the deployment platform
3. Deploy using the Dockerfile

## Development

### Project Structure

```
Backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py
│   │   │   │   ├── products.py
│   │   │   │   ├── orders.py
│   │   │   │   └── profiles.py
│   │   │   └── api.py
│   │   └── dependencies.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/
│   │   ├── auth.py
│   │   ├── product.py
│   │   ├── order.py
│   │   └── profile.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── product_service.py
│   │   ├── order_service.py
│   │   └── profile_service.py
│   └── main.py
├── requirements.txt
├── Dockerfile
├── seed.py
└── README.md
```

### Adding New Features

1. Create models in `app/models/`
2. Create services in `app/services/`
3. Create endpoints in `app/api/v1/endpoints/`
4. Add routes to `app/api/v1/api.py`

## Testing

The API includes comprehensive error handling and validation. Test the endpoints using:

- Swagger UI at `/docs`
- Postman collection
- curl commands

Example curl command:
```bash
curl -X GET "http://localhost:8000/api/v1/products" \
  -H "accept: application/json"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
