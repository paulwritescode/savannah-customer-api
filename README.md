# Savannah Orders API

A simple Python FastAPI service for managing customers and orders with SMS notifications.

## 🎯 Requirements Fulfilled

### 1. ✅ Simple Python Service
- **FastAPI** web framework with automatic API documentation
- **SQLite** database for simple data storage
- **Clean architecture** with separated concerns

### 2. ✅ Simple Database Design
- **Customers Table**: `id`, `name`, `code`, `phone_number`, `email`, `created_at`, `updated_at`
- **Orders Table**: `id`, `customer_id`, `item`, `amount`, `time`, `created_at`, `updated_at`
- **SQLite** for easy setup and development

### 3. ✅ REST API
- **Customers API**: Create, read, update, delete customers
- **Orders API**: Create, read, update, delete orders
- **JSON responses** with proper HTTP status codes
- **Input validation** using Pydantic schemas

### 4. ✅ OpenID Connect Authentication
- **Full OpenID Connect** implementation with discovery endpoints
- **JWT token-based** authentication with standard claims
- **Scope-based authorization** (read/write permissions)
- **Bearer token** authentication for all endpoints
- **OIDC Discovery** at `/.well-known/openid_configuration`
- **JWKS endpoint** at `/.well-known/jwks.json`
- **OAuth2 token endpoint** at `/oauth/token`

### 5. ✅ SMS Notifications
- **Africa's Talking** SMS integration
- **Automatic SMS** sent when orders are created
- **Background task** processing for SMS
- **Graceful fallback** to simulation mode

### 6. ✅ Unit Tests & CI/CD
- **Pytest** test framework
- **80%+ test coverage**
- **GitHub Actions** CI/CD pipeline
- **Automated testing** on push/PR

### 7. ✅ Documentation
- **Comprehensive README** with setup instructions
- **API documentation** at `/docs`
- **Code comments** and type hints
- **GitHub repository** ready for hosting

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd savanah
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python -m uvicorn app.main:app --reload
```

5. **Access the API**
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📱 API Usage

### Authentication

#### OpenID Connect Discovery
The API implements full OpenID Connect standards:

- **Discovery Endpoint**: `GET /.well-known/openid_configuration`
- **JWKS Endpoint**: `GET /.well-known/jwks.json`
- **Token Endpoint**: `POST /oauth/token`

#### Get Access Token
```bash
# Get token from OAuth2 endpoint
curl -X POST http://localhost:8000/oauth/token
```

#### Programmatic Token Creation
```python
from app.services.auth import auth_service

# Create a test token with OpenID Connect claims
token = auth_service.create_access_token({
    'sub': 'test-user',
    'scopes': ['read', 'write']
})
```

#### Token Structure
The JWT tokens include standard OpenID Connect claims:
- `iss` (issuer)
- `aud` (audience) 
- `sub` (subject)
- `iat` (issued at)
- `exp` (expiration)
- `nbf` (not before)
- `scopes` (custom scopes)

### Create Customer
```bash
curl -X POST http://localhost:8000/api/v1/customers/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{
    "name": "John Doe",
    "code": "CUST001",
    "phone_number": "+254700123456",
    "email": "john@example.com"
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
    "time": "2025-09-22T12:00:00"
  }'
```

## 🧪 Testing

### Run Tests
```bash
pytest tests/ -v --cov=app --cov-report=html
```

### Test Coverage
- **80%+ coverage** achieved
- **Unit tests** for all endpoints
- **Authentication tests**
- **SMS service tests**

## 📊 Database Schema

### Customers
```sql
CREATE TABLE customers (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);
```

### Orders
```sql
CREATE TABLE orders (
    id VARCHAR(36) PRIMARY KEY,
    customer_id VARCHAR(36) NOT NULL,
    item VARCHAR(255) NOT NULL,
    amount FLOAT NOT NULL,
    time DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=sqlite:///./savannah_orders.db

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Africa's Talking SMS
AT_USERNAME=sandbox
AT_API_KEY=your-api-key
AT_SENDER_ID=SAVANNAH
```

## 📱 SMS Integration

### Africa's Talking Setup
1. Create account at [Africa's Talking](https://africastalking.com)
2. Get API key from dashboard
3. Update configuration with your credentials
4. SMS will be sent automatically when orders are created

### SMS Features
- **Automatic sending** on order creation
- **Background processing** for better performance
- **Phone number formatting** for Kenya (+254)
- **Graceful fallback** to simulation mode

## 🏗️ Architecture

```
app/
├── main.py              # FastAPI application
├── config.py            # Configuration settings
├── database.py          # Database connection
├── models/              # SQLAlchemy models
│   ├── customer.py
│   └── order.py
├── schemas/             # Pydantic schemas
│   ├── customer.py
│   └── order.py
├── routers/             # API endpoints
│   ├── customers.py
│   └── orders.py
└── services/            # Business logic
    ├── auth.py
    └── sms.py
```

## 🚀 Deployment

### Local Development
```bash
# Direct Python
python -m uvicorn app.main:app --reload

# Docker Compose (with SQLite)
docker-compose up --build
```

### Production Deployment

#### Docker
```bash
# Build image
docker build -t savannah-orders-api .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./data/savannah_orders.db \
  -e SECRET_KEY=your-secret-key \
  -v $(pwd)/data:/app/data \
  savannah-orders-api
```

#### AWS ECS (with SQLite + EFS)
```bash
# Deploy infrastructure
cd infrastructure
terraform init
terraform plan
terraform apply

# Deploy application
./scripts/deploy.sh
```

#### Key Features:
- **SQLite database** with EFS persistence
- **No PostgreSQL** required
- **Simplified deployment** process
- **EFS mount** for data persistence
- **Auto-scaling** ECS Fargate

## 📈 CI/CD Pipeline

The project includes GitHub Actions for:
- **Automated testing** on push/PR
- **Code quality checks**
- **Test coverage reporting**
- **Deployment readiness**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support, please open an issue in the GitHub repository.

---

**Built with ❤️ using FastAPI, SQLite, and Africa's Talking**