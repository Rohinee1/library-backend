# LibraryHub API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
All protected endpoints require a JWT token in the `Authorization` header:
```
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

---

## 📋 Table of Contents
1. [Authentication](#authentication)
2. [Books](#books)
3. [Users](#users)
4. [Transactions](#transactions)
5. [Admin](#admin)

---

## Authentication

### Register User
**POST** `/auth/register`

**Request Body:**
```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Success Response (201):**
```json
{
  "message": "User registered successfully",
  "user_id": "507f1f77bcf86cd799439011",
  "member_id": "LIB-20240505120000"
}
```

**Error Response (400/409):**
```json
{
  "error": "Email already registered"
}
```

---

### Login User
**POST** `/auth/login`

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Success Response (200):**
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "full_name": "John Doe",
    "email": "john@example.com",
    "member_id": "LIB-20240505120000",
    "role": "user"
  }
}
```

**Error Response (401):**
```json
{
  "error": "Invalid credentials"
}
```

---

### Validate Token
**GET** `/auth/validate-token`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Success Response (200):**
```json
{
  "valid": true,
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "full_name": "John Doe",
    "email": "john@example.com",
    "member_id": "LIB-20240505120000",
    "role": "user",
    "is_active": true
  }
}
```

---

### Change Password
**POST** `/auth/change-password`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Request Body:**
```json
{
  "old_password": "OldPass123",
  "new_password": "NewPass456"
}
```

**Success Response (200):**
```json
{
  "message": "Password changed successfully"
}
```

---

## Books

### Get All Books
**GET** `/books?page=1&limit=12&category=Fiction&search=great`

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 12)
- `category` (optional): Filter by category
- `search` (optional): Search by title, author, or ISBN
- `available` (optional): true/false for availability filter

**Success Response (200):**
```json
{
  "success": true,
  "books": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "isbn": "978-0743273565",
      "category": "Fiction",
      "description": "A classic novel...",
      "publisher": "Scribner",
      "publication_year": 1925,
      "total_copies": 25,
      "available_copies": 18,
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-05-05T12:00:00"
    }
  ],
  "total": 150,
  "page": 1,
  "limit": 12,
  "total_pages": 13
}
```

---

### Get Book Details
**GET** `/books/{book_id}`

**Success Response (200):**
```json
{
  "success": true,
  "book": {
    "_id": "507f1f77bcf86cd799439011",
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "978-0743273565",
    "category": "Fiction",
    "description": "A classic novel...",
    "publisher": "Scribner",
    "publication_year": 1925,
    "total_copies": 25,
    "available_copies": 18,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-05-05T12:00:00"
  }
}
```

---

### Create Book (Admin Only)
**POST** `/books`

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN
```

**Request Body:**
```json
{
  "title": "New Book",
  "author": "Author Name",
  "isbn": "978-0123456789",
  "category": "Fiction",
  "description": "Book description",
  "publisher": "Publisher",
  "publication_year": 2024,
  "total_copies": 5
}
```

**Success Response (201):**
```json
{
  "success": true,
  "message": "Book created successfully",
  "book_id": "507f1f77bcf86cd799439011"
}
```

---

### Search Books
**GET** `/books/search?q=gatsby`

**Query Parameters:**
- `q` (required): Search query (minimum 2 characters)

**Success Response (200):**
```json
{
  "success": true,
  "results": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "isbn": "978-0743273565",
      "category": "Fiction",
      "available_copies": 18,
      "total_copies": 25
    }
  ],
  "count": 1
}
```

---

### Get Categories
**GET** `/books/categories`

**Success Response (200):**
```json
{
  "success": true,
  "categories": ["Fiction", "Non-Fiction", "Science", "History", "Technology"]
}
```

---

## Users

### Get User Profile
**GET** `/users/profile`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Success Response (200):**
```json
{
  "success": true,
  "user": {
    "_id": "507f1f77bcf86cd799439011",
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "member_id": "LIB-20240505120000",
    "role": "user",
    "is_active": true,
    "books_borrowed": 3,
    "books_reserved": 2,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-05-05T12:00:00"
  }
}
```

---

### Update User Profile
**PUT** `/users/profile`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Request Body:**
```json
{
  "full_name": "John Doe Updated",
  "phone": "9876543210",
  "address": "123 Main St"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Profile updated successfully"
}
```

---

### Get Borrowed Books
**GET** `/users/books/borrowed`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Success Response (200):**
```json
{
  "success": true,
  "books": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "isbn": "978-0743273565",
      "transaction_id": "507f1f77bcf86cd799439022",
      "checkout_date": "2024-04-21T10:30:00",
      "due_date": "2024-05-15T10:30:00"
    }
  ],
  "count": 3
}
```

---

### Get Reserved Books
**GET** `/users/books/reserved`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Success Response (200):**
```json
{
  "success": true,
  "books": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "title": "To Kill a Mockingbird",
      "author": "Harper Lee",
      "isbn": "978-0061120084",
      "reservation_id": "507f1f77bcf86cd799439033",
      "reserved_date": "2024-05-01T10:30:00"
    }
  ],
  "count": 2
}
```

---

### Get User Activity
**GET** `/users/activity`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Success Response (200):**
```json
{
  "success": true,
  "transactions": [
    {
      "_id": "507f1f77bcf86cd799439022",
      "member_id": "507f1f77bcf86cd799439011",
      "book_id": "507f1f77bcf86cd799439011",
      "book_title": "The Great Gatsby",
      "book_author": "F. Scott Fitzgerald",
      "status": "active",
      "created_at": "2024-04-21T10:30:00",
      "due_date": "2024-05-15T10:30:00"
    }
  ],
  "count": 50
}
```

---

### Get User Statistics
**GET** `/users/statistics`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Success Response (200):**
```json
{
  "success": true,
  "statistics": {
    "currently_borrowed": 3,
    "currently_reserved": 2,
    "overdue_books": 0,
    "total_books_read": 45
  }
}
```

---

## Transactions

### Borrow Book
**POST** `/transactions/borrow`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Request Body:**
```json
{
  "book_id": "507f1f77bcf86cd799439011"
}
```

**Success Response (201):**
```json
{
  "success": true,
  "message": "Book borrowed successfully",
  "transaction_id": "507f1f77bcf86cd799439022",
  "due_date": "2024-05-15T10:30:00"
}
```

**Error Response (409):**
```json
{
  "error": "This book is not available"
}
```

---

### Return Book
**POST** `/transactions/return/{transaction_id}`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Book returned successfully"
}
```

---

### Renew Book
**POST** `/transactions/renew/{transaction_id}`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Book renewed successfully",
  "new_due_date": "2024-05-22T10:30:00"
}
```

---

### Reserve Book
**POST** `/transactions/reserve`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Request Body:**
```json
{
  "book_id": "507f1f77bcf86cd799439011"
}
```

**Success Response (201):**
```json
{
  "success": true,
  "message": "Book reserved successfully",
  "reservation_id": "507f1f77bcf86cd799439033",
  "position": 1
}
```

---

### Get Transaction History
**GET** `/transactions/history`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Success Response (200):**
```json
{
  "success": true,
  "transactions": [
    {
      "_id": "507f1f77bcf86cd799439022",
      "member_id": "507f1f77bcf86cd799439011",
      "book_id": "507f1f77bcf86cd799439011",
      "status": "active",
      "created_at": "2024-04-21T10:30:00",
      "due_date": "2024-05-15T10:30:00"
    }
  ],
  "count": 50
}
```

---

### Get Overdue Books
**GET** `/transactions/overdue`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Success Response (200):**
```json
{
  "success": true,
  "books": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "due_date": "2024-05-01T10:30:00",
      "days_overdue": 4
    }
  ],
  "count": 1
}
```

---

## Admin

### Get Dashboard
**GET** `/admin/dashboard`

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN
```

**Success Response (200):**
```json
{
  "success": true,
  "statistics": {
    "total_books": 50234,
    "total_users": 15482,
    "active_members": 12000,
    "active_checkouts": 12543,
    "overdue_books": 342
  },
  "popular_books": [
    {
      "title": "The Great Gatsby",
      "checkouts": 245
    }
  ]
}
```

---

### Get Members
**GET** `/admin/members?page=1&limit=10&status=active`

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN
```

**Query Parameters:**
- `page` (optional): Page number
- `limit` (optional): Items per page
- `status` (optional): 'active' or 'suspended'

**Success Response (200):**
```json
{
  "success": true,
  "members": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "full_name": "John Doe",
      "email": "john@example.com",
      "member_id": "LIB-20240505120000",
      "is_active": true,
      "books_borrowed": 3,
      "created_at": "2024-01-15T10:30:00"
    }
  ],
  "total": 15482,
  "page": 1,
  "total_pages": 1549
}
```

---

### Get Member Details
**GET** `/admin/members/{member_id}`

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN
```

**Success Response (200):**
```json
{
  "success": true,
  "member": {
    "_id": "507f1f77bcf86cd799439011",
    "full_name": "John Doe",
    "email": "john@example.com",
    "member_id": "LIB-20240505120000",
    "is_active": true
  },
  "borrowed_count": 3,
  "reserved_count": 2,
  "transaction_history_count": 20
}
```

---

### Suspend Member
**POST** `/admin/members/{member_id}/suspend`

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Member suspended"
}
```

---

### Activate Member
**POST** `/admin/members/{member_id}/activate`

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Member activated"
}
```

---

### Get Inventory
**GET** `/admin/inventory`

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN
```

**Success Response (200):**
```json
{
  "success": true,
  "low_stock_books": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "title": "The Great Gatsby",
      "available_copies": 2,
      "total_copies": 25
    }
  ],
  "out_of_stock_count": 5,
  "total_books": 50234
}
```

---

### Restock Book
**POST** `/admin/books/{book_id}/restock`

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN
```

**Request Body:**
```json
{
  "quantity": 10
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "10 copies added to inventory"
}
```

---

### Get Transactions
**GET** `/admin/transactions?page=1&limit=20&status=active`

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN
```

**Query Parameters:**
- `page` (optional): Page number
- `limit` (optional): Items per page
- `status` (optional): 'active', 'returned', 'overdue'

**Success Response (200):**
```json
{
  "success": true,
  "transactions": [
    {
      "_id": "507f1f77bcf86cd799439022",
      "member_id": "507f1f77bcf86cd799439011",
      "book_id": "507f1f77bcf86cd799439011",
      "status": "active",
      "created_at": "2024-04-21T10:30:00",
      "due_date": "2024-05-15T10:30:00"
    }
  ],
  "total": 5000,
  "page": 1
}
```

---

### Get Activity Report
**GET** `/admin/reports/activity?days=30`

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN
```

**Query Parameters:**
- `days` (optional): Report period in days (default: 30)

**Success Response (200):**
```json
{
  "success": true,
  "period_days": 30,
  "checkouts": 1250,
  "returns": 1180,
  "new_members": 85
}
```

---

### Get Popular Books Report
**GET** `/admin/reports/popular-books?limit=10`

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN
```

**Query Parameters:**
- `limit` (optional): Number of books to return (default: 10)

**Success Response (200):**
```json
{
  "success": true,
  "popular_books": [
    {
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "checkouts": 245
    },
    {
      "title": "Atomic Habits",
      "author": "James Clear",
      "checkouts": 198
    }
  ]
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message here"
}
```

### Common HTTP Status Codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized (invalid token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `409` - Conflict (e.g., already exists)
- `500` - Server Error

---

## Testing with cURL

### Login Example:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

### Get Books Example:
```bash
curl http://localhost:5000/api/books?page=1&category=Fiction
```

### Borrow Book Example:
```bash
curl -X POST http://localhost:5000/api/transactions/borrow \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "book_id": "507f1f77bcf86cd799439011"
  }'
```

---

## Rate Limiting

Currently, there are no rate limits. For production, implement rate limiting to prevent abuse.

---

## Versioning

Current API Version: **v1**

Future versions will be available at `/api/v2`, etc.

---

**Last Updated:** May 5, 2024
