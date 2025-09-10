# Personal Finance Manager API

A comprehensive REST API for managing personal finances built with FastAPI, Firebase Authentication, and Google Firestore.

## 🚀 Features

- **User Authentication**: Firebase Authentication with JWT tokens
- **Transaction Management**: Full CRUD operations for financial transactions
- **User Profiles**: Manage user profile information
- **Filtering & Querying**: Filter transactions by type, date range, and category
- **Data Validation**: Pydantic models for request/response validation
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation
- **Security**: JWT-based authentication middleware

## 📋 Requirements

- Python 3.11+
- Firebase project with Authentication and Firestore enabled
- Firebase Admin SDK service account key

## 🛠️ Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd finance-api
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install fastapi uvicorn firebase-admin pydantic[email]
   ```

4. **Setup Firebase**:

   - Create a Firebase project at https://console.firebase.google.com
   - Enable Authentication and Firestore
   - Generate a service account key:
     - Go to Project Settings > Service Accounts
     - Click "Generate new private key"
     - Save the JSON file as `serviceAccountKey.json` in the project root

5. **Environment Setup** (Optional):
   Create a `.env` file for any additional configuration if needed.

## 🏃‍♂️ Running the Application

1. **Start the development server**:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## 📚 API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login user (returns auth instructions)

### Users

- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update current user profile

### Transactions

- `POST /transactions` - Create a new transaction
- `GET /transactions` - Get user's transactions (with optional filters)
- `GET /transactions/{id}` - Get specific transaction
- `PUT /transactions/{id}` - Update transaction
- `DELETE /transactions/{id}` - Delete transaction

### Query Parameters for GET /transactions:

- `type`: Filter by "income" or "expense"
- `start_date`: Filter transactions from this date
- `end_date`: Filter transactions until this date
- `category`: Filter by category

## 🔐 Authentication

This API uses Firebase Authentication with JWT tokens. Here's how to authenticate:

1. **Register/Login**: Use the `/auth/register` endpoint or Firebase client SDK
2. **Get Token**: Obtain JWT token from Firebase client
3. **Make Requests**: Include token in Authorization header:
   ```
   Authorization: Bearer <your-jwt-token>
   ```

### Client-Side Authentication Example (JavaScript):

```javascript
import { initializeApp } from 'firebase/app';
import { getAuth, signInWithEmailAndPassword } from 'firebase/auth';

const firebaseConfig = {
  // Your config
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Login
const { user } = await signInWithEmailAndPassword(auth, email, password);
const token = await user.getIdToken();

// Use token in API requests
fetch('http://localhost:8000/transactions', {
  headers: {
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
});
```

## 📊 Data Models

### User

```json
{
  "id": "string",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2023-01-01T00:00:00Z"
}
```

### Transaction

```json
{
  "id": "string",
  "user_id": "string",
  "type": "income|expense",
  "amount": 100.5,
  "category": "food",
  "date": "2023-01-01T00:00:00Z",
  "description": "Grocery shopping"
}
```

## 🗄️ Database Structure

### Firestore Collections:

#### users

```
users/{userId}
├── email: string
├── name: string (optional)
└── created_at: timestamp
```

#### transactions

```
transactions/{transactionId}
├── user_id: string
├── type: "income" | "expense"
├── amount: number
├── category: string
├── date: timestamp
└── description: string (optional)
```

## 🚀 Production Deployment

1. **Update CORS settings** in `main.py` for your domain
2. **Set environment variables** for production
3. **Use production Firebase project**
4. **Deploy using your preferred method** (Docker, Heroku, GCP, etc.)

### Docker Deployment:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔧 Development

### Project Structure:

```
finance-api/
├── main.py                 # FastAPI app entry point
├── serviceAccountKey.json  # Firebase service account key
├── config/
│   └── firebase.py        # Firebase configuration
├── middleware/
│   └── auth.py           # Authentication middleware
├── models/
│   ├── user.py           # User data models
│   └── transaction.py    # Transaction data models
├── routers/
│   ├── auth.py          # Authentication endpoints
│   ├── user.py          # User endpoints
│   └── transaction.py   # Transaction endpoints
├── services/
│   ├── user_service.py      # User business logic
│   └── transaction_service.py # Transaction business logic
└── utils/
    └── exceptions.py    # Error handlers
```

### Adding New Features:

1. Define models in `models/`
2. Create service functions in `services/`
3. Add router endpoints in `routers/`
4. Include router in `main.py`

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions, please create an issue in the repository.
