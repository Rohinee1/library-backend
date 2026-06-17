# LibraryHub - Flask Backend Setup Guide

## 📋 Prerequisites

- Python 3.8 or higher
- MongoDB (local or MongoDB Atlas cloud)
- pip (Python package manager)

---

## 🚀 Installation Steps

### 1. Clone/Download the Project
```bash
cd your-project-directory
```

### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure MongoDB

#### Option A: Local MongoDB
1. Install MongoDB from https://www.mongodb.com/try/download/community
2. Make sure MongoDB service is running
3. Keep the default connection string in `.env`:
   ```
   MONGO_URI=mongodb://localhost:27017/library_db
   ```

#### Option B: MongoDB Atlas (Cloud)
1. Create account at https://www.mongodb.com/cloud/atlas
2. Create a cluster
3. Get connection string (looks like):
   ```
   mongodb+srv://username:password@cluster.mongodb.net/library_db
   ```
4. Update `.env` with your connection string:
   ```
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/library_db
   ```

### 5. Setup Environment Variables
```bash
# Copy example file
cp .env.example .env

# Edit .env with your settings (important: change JWT_SECRET_KEY in production)
```

### 6. Run the Application
```bash
python app.py
```

You should see:
```
✅ Database initialized successfully
 * Running on http://0.0.0.0:5000
```

---

## 🔑 API Endpoints

### Authentication Endpoints (`/api/auth`)
- **POST** `/register` - Register new user
- **POST** `/login` - Login user
- **GET** `/validate-token` - Validate JWT token
- **POST** `/logout` - Logout user
- **POST** `/change-password` - Change password

### Book Endpoints (`/api/books`)
- **GET** `/` - Get all books (with filtering)
- **GET** `/<book_id>` - Get book details
- **POST** `/` - Create new book (Admin only)
- **PUT** `/<book_id>` - Update book (Admin only)
- **DELETE** `/<book_id>` - Delete book (Admin only)
- **GET** `/search?q=query` - Search books
- **GET** `/categories` - Get all categories

### User Endpoints (`/api/users`)
- **GET** `/profile` - Get user profile
- **PUT** `/profile` - Update user profile
- **GET** `/books/borrowed` - Get borrowed books
- **GET** `/books/reserved` - Get reserved books
- **GET** `/activity` - Get user activity
- **GET** `/statistics` - Get user statistics
- **GET** `/notifications/preferences` - Get notification preferences
- **PUT** `/notifications/preferences` - Update notification preferences

### Transaction Endpoints (`/api/transactions`)
- **POST** `/borrow` - Borrow a book
- **POST** `/return/<transaction_id>` - Return a book
- **POST** `/renew/<transaction_id>` - Renew borrowed book
- **POST** `/reserve` - Reserve a book
- **POST** `/cancel-reservation/<reservation_id>` - Cancel reservation
- **GET** `/history` - Get transaction history
- **GET** `/overdue` - Get overdue books

### Admin Endpoints (`/api/admin`)
- **GET** `/dashboard` - Get admin dashboard stats
- **GET** `/members` - Get all members
- **GET** `/members/<member_id>` - Get member details
- **POST** `/members/<member_id>/suspend` - Suspend member
- **POST** `/members/<member_id>/activate` - Activate member
- **GET** `/inventory` - Get inventory overview
- **POST** `/books/<book_id>/restock` - Restock book
- **GET** `/transactions` - Get all transactions
- **POST** `/transactions/<transaction_id>/resolve-overdue` - Resolve overdue
- **GET** `/reports/activity` - Get activity report
- **GET** `/reports/popular-books` - Get popular books

---

## 📝 Example API Usage

### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

### Borrow Book (requires token)
```bash
curl -X POST http://localhost:5000/api/transactions/borrow \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "book_id": "book_id_here"
  }'
```

### Get Books
```bash
curl http://localhost:5000/api/books?page=1&category=Fiction&search=Great
```

---

## 🔐 Security Notes

⚠️ **Important for Production:**

1. **Change JWT_SECRET_KEY** in `.env`:
   ```
   JWT_SECRET_KEY=your-super-secret-key-here
   ```

2. **Use Environment Variables** - Don't hardcode sensitive data

3. **Enable HTTPS** - Use SSL certificates

4. **MongoDB Authentication** - Enable authentication in MongoDB

5. **Rate Limiting** - Add rate limiting for production

6. **CORS Settings** - Configure CORS properly for your frontend domain

---

## 🛠️ Database Schema

### Collections

#### Books
```javascript
{
  _id: ObjectId,
  title: String,
  author: String,
  isbn: String (unique),
  category: String,
  description: String,
  publisher: String,
  publication_year: Number,
  total_copies: Number,
  available_copies: Number,
  created_at: DateTime,
  updated_at: DateTime
}
```

#### Users
```javascript
{
  _id: ObjectId,
  full_name: String,
  email: String (unique),
  password: String (hashed),
  member_id: String (unique),
  phone: String,
  role: String (user/admin),
  is_active: Boolean,
  books_borrowed: Number,
  books_reserved: Number,
  created_at: DateTime,
  updated_at: DateTime,
  last_login: DateTime
}
```

#### Transactions
```javascript
{
  _id: ObjectId,
  member_id: ObjectId,
  book_id: ObjectId,
  status: String (active/returned),
  created_at: DateTime,
  due_date: DateTime,
  returned_at: DateTime,
  is_overdue: Boolean,
  renew_count: Number
}
```

#### Reservations
```javascript
{
  _id: ObjectId,
  member_id: ObjectId,
  book_id: ObjectId,
  status: String (active/cancelled),
  created_at: DateTime,
  position_in_queue: Number
}
```

---

## 🐛 Troubleshooting

### MongoDB Connection Error
```
Error: [Errno 111] Connection refused
```
**Solution**: Make sure MongoDB is running. Check with:
```bash
# Windows: Check Services
# macOS: brew services list
# Linux: sudo systemctl status mongod
```

### Port Already in Use
```
Address already in use
```
**Solution**: Change port in code or kill process:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### JWT Token Invalid
**Solution**: Make sure token is included in Authorization header:
```
Authorization: Bearer YOUR_TOKEN_HERE
```

---

## 📚 Next Steps

1. **Connect Frontend** - Update frontend API URLs to point to this backend
2. **Add Authentication** - Implement JWT token storage in frontend
3. **Test Endpoints** - Use Postman or Insomnia for API testing
4. **Deploy** - Deploy to Heroku, AWS, or your preferred platform

---

## 📞 Support

For issues or questions:
1. Check MongoDB connection
2. Verify JWT token in requests
3. Check browser console for errors
4. Review Flask logs for detailed errors

---

**Happy coding! 🚀**
