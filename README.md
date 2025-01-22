# **Booking System API Documentation**

This API provides functionality for managing users, meeting rooms, and bookings. It supports role-based access control, where non-admin users can only access their own data, and admins have full access.

---

## **Table of Contents**
1. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Running the Application](#running-the-application)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
   - [Authentication](#authentication-endpoints)
   - [Bookings](#bookings-endpoints)
   - [Users](#users-endpoints)
   - [Meeting Rooms](#meeting-rooms-endpoints)
4. [Error Handling](#error-handling)
5. [Examples](#examples)
6. [Contributing](#contributing)
7. [License](#license)

---

## **Getting Started**

### **Prerequisites**
- Python 3.8+
- MySQL Server
- `pip` for installing dependencies

### **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/MiltoniaSpectabilis/booking-system-api.git
   cd booking-system-api
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:
   ```plaintext
   DATABASE_URL=mysql+mysqlconnector://user:password@localhost/your_database_name
   SECRET_KEY=your_secret_key
   ```

### **Running the Application**
Start the Flask development server:
```bash
python -m app.main
```

The API will be available at `http://127.0.0.1:5000`.

---

## **Authentication**
All endpoints (except `/auth/register` and `/auth/login`) require a valid JWT token in the `Authorization` header.

Example:
```http
Authorization: Bearer <access_token>
```

### **First User Admin Policy**

- The first user to register in the system automatically receives admin privileges
- Subsequent users are created as non-admin unless explicitly granted admin rights by an existing admin
- This ensures there's always at least one administrative account in the system

---

## **API Endpoints**

### **Authentication Endpoints**

### Register User
Creates a new user account in the system.

**Endpoint:** `POST /api/auth/register`

**Request Body:**
```json
{
    "username": "string (3-50 chars)",
    "password": "string (min 6 chars)"
}
```

**Response:** `201 Created`
```json
{
    "id": "integer",
    "username": "string",
    "is_admin": "boolean"
}
```

### Login
Authenticates a user and provides an access token.

**Endpoint:** `POST /api/auth/login`

**Request Body:**
```json
{
    "username": "string (3-50 chars)",
    "password": "string (min 6 chars)"
}
```

**Response:** `200 OK`
```json
{
    "access_token": "string (JWT)"
}
```

## Bookings

### Create Booking
Creates a new room booking.

**Endpoint:** `POST /api/bookings/`

**Request Body:**
```json
{
    "user_id": "integer",
    "room_id": "integer",
    "start_time": "string (ISO 8601 datetime)",
    "end_time": "string (ISO 8601 datetime)"
}
```

**Response:** `201 Created`
```json
{
    "id": "integer",
    "user_id": "integer",
    "room_id": "integer",
    "start_time": "string (ISO 8601 datetime)",
    "end_time": "string (ISO 8601 datetime)"
}
```

### Get Booking by ID
Retrieves details of a specific booking.

**Endpoint:** `GET /api/bookings/{id}`

**Response:** `200 OK`
```json
{
    "id": "integer",
    "user_id": "integer",
    "room_id": "integer",
    "start_time": "string (ISO 8601 datetime)",
    "end_time": "string (ISO 8601 datetime)"
}
```

### Get User Bookings
Retrieves all bookings for a specific user.

**Endpoint:** `GET /api/bookings/user/{user_id}`

**Response:** `200 OK`
```json
[
    {
        "id": "integer",
        "user_id": "integer",
        "room_id": "integer",
        "start_time": "string (ISO 8601 datetime)",
        "end_time": "string (ISO 8601 datetime)"
    }
]
```

### Get Room Bookings (Admin Only)
Retrieves all bookings for a specific room.

**Endpoint:** `GET /api/bookings/room/{room_id}`

**Response:** `200 OK`
```json
[
    {
        "id": "integer",
        "user_id": "integer",
        "room_id": "integer",
        "start_time": "string (ISO 8601 datetime)",
        "end_time": "string (ISO 8601 datetime)"
    }
]
```

### Update Booking
Updates an existing booking's time slots.

**Endpoint:** `PUT /api/bookings/{id}`

**Request Body:**
```json
{
    "start_time": "string (ISO 8601 datetime, optional)",
    "end_time": "string (ISO 8601 datetime, optional)"
}
```

**Response:** `200 OK`
```json
{
    "id": "integer",
    "user_id": "integer",
    "room_id": "integer",
    "start_time": "string (ISO 8601 datetime)",
    "end_time": "string (ISO 8601 datetime)"
}
```

### Delete Booking
Removes a booking from the system.

**Endpoint:** `DELETE /api/bookings/{id}`

**Response:** `204 No Content`

## Users (Admin Only)

### Create User
Creates a new user account (admin access required).

**Endpoint:** `POST /api/users/`

**Request Body:**
```json
{
    "username": "string (3-50 chars)",
    "password": "string (min 6 chars)",
    "is_admin": "boolean (optional)"
}
```

**Response:** `201 Created`
```json
{
    "id": "integer",
    "username": "string",
    "is_admin": "boolean"
}
```

### Get User by ID
Retrieves user details by ID.

**Endpoint:** `GET /api/users/{id}`

**Response:** `200 OK`
```json
{
    "id": "integer",
    "username": "string",
    "is_admin": "boolean"
}
```

### Get All Users
Retrieves a list of all users.

**Endpoint:** `GET /api/users/`

**Response:** `200 OK`
```json
[
    {
        "id": "integer",
        "username": "string",
        "is_admin": "boolean"
    }
]
```

### Update User
Updates user information.

**Endpoint:** `PUT /api/users/{id}`

**Request Body:**
```json
{
    "username": "string (3-50 chars, optional)",
    "is_admin": "boolean (optional)"
}
```

**Response:** `200 OK`
```json
{
    "id": "integer",
    "username": "string",
    "is_admin": "boolean"
}
```

### Delete User
Removes a user from the system.

**Endpoint:** `DELETE /api/users/{id}`

**Response:** `204 No Content`

## Meeting Rooms (Admin Only)

### Create Room
Creates a new meeting room.

**Endpoint:** `POST /api/rooms/`

**Request Body:**
```json
{
    "name": "string (3-100 chars)",
    "capacity": "integer (>0)",
    "description": "string (optional)"
}
```

**Response:** `201 Created`
```json
{
    "id": "integer",
    "name": "string",
    "capacity": "integer",
    "description": "string"
}
```

### Get Room by ID
Retrieves room details by ID.

**Endpoint:** `GET /api/rooms/{id}`

**Response:** `200 OK`
```json
{
    "id": "integer",
    "name": "string",
    "capacity": "integer",
    "description": "string"
}
```

### Get All Rooms
Retrieves a list of all meeting rooms.

**Endpoint:** `GET /api/rooms/`

**Response:** `200 OK`
```json
[
    {
        "id": "integer",
        "name": "string",
        "capacity": "integer",
        "description": "string"
    }
]
```

### Update Room
Updates room information.

**Endpoint:** `PUT /api/rooms/{id}`

**Request Body:**
```json
{
    "name": "string (3-100 chars, optional)",
    "capacity": "integer (>0, optional)",
    "description": "string (optional)"
}
```

**Response:** `200 OK`
```json
{
    "id": "integer",
    "name": "string",
    "capacity": "integer",
    "description": "string"
}
```

### Delete Room
Removes a room from the system.

**Endpoint:** `DELETE /api/rooms/{id}`

**Response:** `204 No Content`

## Status Codes

The API uses standard HTTP response codes to indicate the success or failure of requests:

| Code | Status | Description |
|------|---------|------------|
| 200 | OK | Successful GET/PUT operations |
| 201 | Created | Successful resource creation |
| 204 | No Content | Successful deletions |
| 400 | Bad Request | Invalid request parameters/body |
| 401 | Unauthorized | Missing/invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Booking conflict or duplicate data |
| 500 | Server Error | Internal server issues |

---
