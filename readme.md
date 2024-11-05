Here’s a template for your `README.md` file, covering the main aspects of the project:

---

# Warehouse Manager Server

This repository contains the backend server for the **Warehouse Management System** (WMS), which helps manage inventory, products, and financial reports for a warehouse. The backend is built using Flask and MongoDB, with user authentication and role-based access control.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [API Endpoints](#api-endpoints)
- [Authentication and Authorization](#authentication-and-authorization)
- [License](#license)

## Features

- **User Roles**: Admin and Customer roles with access control
- **Inventory Management**: CRUD operations for products
- **Financial Reports**: Summaries of sales data and inventory costs
- **Authentication**: Secure JWT-based authentication

## Tech Stack

- **Backend Framework**: Flask
- **Database**: MongoDB
- **Authentication**: Flask-JWT-Extended and Flask-Bcrypt for secure password hashing
- **API Testing**: Tested using Insomnia

## Setup and Installation

### Prerequisites

- Python 3.6 or higher
- MongoDB (local or hosted, e.g., MongoDB Atlas)
- Git

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bises7/warehouse_manager_server.git
   cd warehouse_manager_server
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the root directory and add the following variables:
     ```plaintext
     SECRET_KEY=<your_secret_key>
     JWT_SECRET_KEY=<your_jwt_secret_key>
     MONGO_URI=<your_mongo_db_uri>
     ```

5. **Run the server**:
   ```bash
   python app.py
   ```

   The server will run at `http://127.0.0.1:5000`.

## API Endpoints

### Authentication

- **Register** (Admin and Customer):
  - `POST /auth/register`
  - Request body:
    ```json
    {
      "username": "string",
      "password": "string",
      "role": "string" // "admin" or "customer"
    }
    ```

- **Login**:
  - `POST /auth/login`
  - Request body:
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```

### Product Management (Admin only for create, update, delete)

- **Add Product**: `POST /products/add`
- **Get All Products**: `GET /products/`
- **Get Product by ID**: `GET /products/<product_id>`
- **Update Product**: `PUT /products/update/<product_id>`
- **Delete Product**: `DELETE /products/delete/<product_id>`

### Reports (Admin only)

- **Sales Report**: `GET /reports/sales`
- **Inventory Cost Report**: `GET /reports/inventory`
- **Sales by Date Range**: `POST /reports/sales_by_date`

## Authentication and Authorization

- **JWT** is used for secure authentication.
- **Admin Role**: Can perform all CRUD operations and access financial reports.
- **Customer Role**: Can only view product details.

### Usage of Access Token
Add the JWT token to the `Authorization` header for routes that require authentication:
```plaintext
Authorization: Bearer <JWT_TOKEN>
```

## License

This project is licensed under the MIT License.

---

Feel free to adjust any section as needed, especially URLs and any custom instructions based on your specific setup. This `README.md` provides a solid overview for anyone using or contributing to the project. Let me know if you’d like any additional sections or adjustments!