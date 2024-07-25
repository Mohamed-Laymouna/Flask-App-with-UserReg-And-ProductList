# Flask App with User Registration and Product List

## Overview

This project is a RESTful API built with Flask, designed to handle user registration and manage a product list. It leverages Flask-SQLAlchemy for database interactions and Flask-Smorest for API management.

## Features

- **User Registration**: Allows users to register with their name, phone, email, and password.
- **Product Management**: Manage a list of products with details like name, price, quantity, and owner.
- **API Endpoints**: Well-structured endpoints for handling user and product data.

## Technologies Used

- Flask
- Flask-SQLAlchemy
- Flask-Smorest

## Project Structure

```
Flask-App-with-UserReg-And-ProductList/
├── app.py
├── db.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── product.py
├── resources/
│   ├── __init__.py
│   ├── user.py
│   └── product.py
├── instance/
│   └── config.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository**:
   ```sh
   git clone https://github.com/Mohamed-Laymouna/Flask-App-with-UserReg-And-ProductList.git
   cd Flask-App-with-UserReg-And-ProductList
   ```

2. **Create a virtual environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```sh
   flask run
   ```

## Usage

- **User Registration**: `POST /register`
  - Request Body: `{"name": "Name", "phone": "Phone", "email": "Email", "password": "Password"}`
- **Product Management**:
  - `GET /products`: Get a list of products.
  - `POST /products`: Add a new product.
  - `PUT /products/<product_id>`: Update an existing product.
  - `DELETE /products/<product_id>`: Delete a product.

## Contributing

Contributions are welcome! Please create a pull request or open an issue to discuss your ideas.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact [Mohamed Laymouna](https://github.com/Mohamed-Laymouna).
