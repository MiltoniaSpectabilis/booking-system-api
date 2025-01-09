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

---

## **API Endpoints**

### **Authentication Endpoints**

#### **Register a New User**
- **URL**: `/auth/register`
- **Method**: `POST`
- **Description**: Register a new user.
- **Request Body**:
  ```json
  {
    "username": "string (3-50 chars)",
    "password": "string (min 6 chars)"
  }
  ```
- **Response**:
  ```json
  {
    "id": "integer",
    "username": "string",
    "is_admin": "boolean"
  }
  ```

#### **Login**
- **URL**: `/auth/login`
- **Method**: `POST`
- **Description**: Log in and receive an access token.
- **Request Body**:
  ```json
  {
    "username": "string (3-50 chars)",
    "password": "string (min 6 chars)"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "string (JWT token)"
  }
  ```

---

### **Bookings Endpoints**

#### **Create a New Booking**
- **URL**: `/bookings/`
- **Method**: `POST`
- **Description**: Create a new booking. Non-admin users can only create bookings for themselves.
- **Request Body**:
  ```json
  {
    "user_id": "integer",
    "room_id": "integer",
    "start_time": "string (ISO 8601 datetime)",
    "end_time": "string (ISO 8601 datetime)"
  }
  ```
- **Response**:
  ```json
  {
    "id": "integer",
    "user_id": "integer",
    "room_id": "integer",
    "start_time": "string (ISO 8601 datetime)",
    "end_time": "string (ISO 8601 datetime)"
  }
  ```

#### **Retrieve a Booking by ID**
- **URL**: `/bookings/<int:booking_id>`
- **Method**: `GET`
- **Description**: Retrieve a booking by its ID. Non-admin users can only retrieve their own bookings.
- **Response**:
  ```json
  {
    "id": "integer",
    "user_id": "integer",
    "room_id": "integer",
    "start_time": "string (ISO 8601 datetime)",
    "end_time": "string (ISO 8601 datetime)"
  }
  ```

#### **Retrieve All Bookings for a User**
- **URL**: `/bookings/user/<int:user_id>`
- **Method**: `GET`
- **Description**: Retrieve all bookings for a specific user. Non-admin users can only retrieve their own bookings.
- **Response**:
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

#### **Retrieve All Bookings for a Room (Admin Only)**
- **URL**: `/bookings/room/<int:room_id>`
- **Method**: `GET`
- **Description**: Retrieve all bookings for a specific room. Only accessible by admins.
- **Response**:
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

#### **Retrieve All Bookings (Admin Only)**
- **URL**: `/bookings/`
- **Method**: `GET`
- **Description**: Retrieve all bookings. Only accessible by admins.
- **Response**:
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

#### **Update a Booking**
- **URL**: `/bookings/<int:booking_id>`
- **Method**: `PUT`
- **Description**: Update an existing booking. Non-admin users can only update their own bookings.
- **Request Body**:
  ```json
  {
    "start_time": "string (ISO 8601 datetime, optional)",
    "end_time": "string (ISO 8601 datetime, optional)"
  }
  ```
- **Response**:
  ```json
  {
    "id": "integer",
    "user_id": "integer",
    "room_id": "integer",
    "start_time": "string (ISO 8601 datetime)",
    "end_time": "string (ISO 8601 datetime)"
  }
  ```

#### **Delete a Booking**
- **URL**: `/bookings/<int:booking_id>`
- **Method**: `DELETE`
- **Description**: Delete a booking. Non-admin users can only delete their own bookings.
- **Response**:
  ```json
  {
    "message": "string"
  }
  ```

---

### **Users Endpoints (Admin Only)**

#### **Create a New User**
- **URL**: `/users/`
- **Method**: `POST`
- **Description**: Create a new user. Only accessible by admins.
- **Request Body**:
  ```json
  {
    "username": "string (3-50 chars)",
    "password": "string (min 6 chars)",
    "is_admin": "boolean (optional, default=false)"
  }
  ```
- **Response**:
  ```json
  {
    "id": "integer",
    "username": "string",
    "is_admin": "boolean"
  }
  ```

#### **Retrieve a User by ID**
- **URL**: `/users/<int:user_id>`
- **Method**: `GET`
- **Description**: Retrieve a user by their ID. Only accessible by admins.
- **Response**:
  ```json
  {
    "id": "integer",
    "username": "string",
    "is_admin": "boolean"
  }
  ```

#### **Retrieve All Users**
- **URL**: `/users/`
- **Method**: `GET`
- **Description**: Retrieve all users. Only accessible by admins.
- **Response**:
  ```json
  [
    {
      "id": "integer",
      "username": "string",
      "is_admin": "boolean"
    }
  ]
  ```

---

### **Meeting Rooms Endpoints (Admin Only)**

#### **Create a New Meeting Room**
- **URL**: `/rooms/`
- **Method**: `POST`
- **Description**: Create a new meeting room. Only accessible by admins.
- **Request Body**:
  ```json
  {
    "name": "string (3-100 chars)",
    "capacity": "integer (> 0)",
    "description": "string (optional)"
  }
  ```
- **Response**:
  ```json
  {
    "id": "integer",
    "name": "string",
    "capacity": "integer",
    "description": "string"
  }
  ```

#### **Retrieve a Meeting Room by ID**
- **URL**: `/rooms/<int:room_id>`
- **Method**: `GET`
- **Description**: Retrieve a meeting room by its ID. Only accessible by admins.
- **Response**:
  ```json
  {
    "id": "integer",
    "name": "string",
    "capacity": "integer",
    "description": "string"
  }
  ```

---

## **Error Handling**
- **400 Bad Request**: Invalid input data.
- **401 Unauthorized**: Missing or invalid token.
- **403 Forbidden**: Insufficient permissions.
- **404 Not Found**: Resource not found.
