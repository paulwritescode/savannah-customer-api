# Savannah Orders API

A simple Python FastAPI service for managing customers and orders with automatic SMS notifications.

## ✅ Requirements Fulfilled

1. **Simple Python Service** - FastAPI with SQLite database
2. **Simple Database Design** - Customers and Orders tables
3. **REST API** - Full CRUD operations for customers and orders
4. **OpenID Connect Authentication** - JWT-based auth with OIDC discovery
5. **SMS Notifications** - Automatic SMS via Africa's Talking when orders are created
6. **Unit Tests & CI/CD** - 85% test coverage with GitHub Actions
7. **Documentation** - Complete setup and API documentation

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

1. **Clone and setup**
```bash
git clone <repository-url>
cd savanah
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Run the application**
```bash
python -m uvicorn app.main:app --reload
```

3. **Access the API**
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📱 API Usage

### Authentication

Get an access token:
```bash
curl -X POST http://localhost:8000/oauth/token
```

Use the token in API requests:
```bash
curl -H "Authorization: Bearer <your-token>" http://localhost:8000/api/v1/customers/
```

### Create Customer
```bash
curl -X POST http://localhost:8000/api/v1/customers/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{
    "name": "John Doe",
    "code": "CUST001",
    "phone_number": "+254700123456"
  }'
```

### Create Order (triggers SMS)
```bash
curl -X POST http://localhost:8000/api/v1/orders/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{
    "customer_id": "customer-id",
    "item": "iPhone 15",
    "amount": 120000.00,
    "time": "2025-01-22T12:00:00"
  }'
```

## 🧪 Testing

### Run Tests
```bash
pytest tests/ -v --cov=app --cov-report=html
```

### Test Coverage
- **85% coverage** achieved
- **Unit tests** for all endpoints
- **Authentication tests**
- **SMS service tests**

## 📊 Database Schema

**Customers**: `id`, `name`, `code`, `phone_number`, `email`, `created_at`, `updated_at`

**Orders**: `id`, `customer_id`, `item`, `amount`, `time`, `created_at`, `updated_at`

SQLite database automatically created on first run.

## 🔧 Configuration

Environment variables (all optional, defaults provided):
```bash
DATABASE_URL=sqlite:///./savannah_orders.db
SECRET_KEY=your-secret-key
AT_USERNAME=sandbox
AT_API_KEY=your-api-key
```

## 📱 SMS Integration

### Africa's Talking Setup
1. Create account at [Africa's Talking](https://africastalking.com)
2. Get API key from dashboard
3. Update `AT_API_KEY` in config
4. SMS sent automatically when orders are created

### SMS Features
- **Automatic sending** on order creation
- **Background processing** for performance
- **Phone number formatting** for Kenya (+254)
- **Graceful fallback** to simulation mode

## 🏗️ Architecture

Simple structure with clear separation:
- `app/main.py` - FastAPI application
- `app/models/` - Database models (Customer, Order)
- `app/routers/` - API endpoints
- `app/services/` - Business logic (Auth, SMS)
- `tests/` - Unit tests

## 🚀 Deployment

### Local Development
```bash
python -m uvicorn app.main:app --reload
```

### Docker
```bash
docker build -t savannah-orders-api .
docker run -p 8000:8000 savannah-orders-api
```

### Docker Compose
```bash
docker-compose up --build
```

## 📈 CI/CD Pipeline

GitHub Actions workflow includes:
- **Automated testing** on push/PR
- **Code quality checks** with flake8
- **Test coverage** reporting
- **Docker build** testing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

**Built with ❤️ using FastAPI, SQLite, and Africa's Talking**