# BrewByte Cafe ☕

A full-stack online cafe ordering and management system built using Python, Django REST Framework, and PostgreSQL.

## Overview

BrewByte Cafe is an online cafe management platform that allows customers to explore food menus, add items to their cart, apply discount coupons, place orders, and make payments through a simulated payment workflow.

The system also supports restaurant reservations, inventory tracking, and order management.

## Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT
- **API Testing:** Postman
- **Frontend:** React (Planned)

## Features

- User Registration and Authentication
- JWT-based Authorization
- Food Categories and Menu Management
- Shopping Cart Management
- Order Placement and Order History
- Order Status Management
- Table Reservations
- Inventory Management
- Coupon Validation and Discount Calculation
- Checkout API
- Payment Simulation

## Project Structure

- users/ – User authentication
- menu/ – Food categories and menu items
- orders/ – Cart and order management
- reservations/ – Table reservations
- inventory/ – Stock management
- coupons/ – Discount coupon management
- checkout/ – Checkout and price calculation
- payments/ – Payment processing simulation

## Setup Instructions

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies using 'pip install -r requirements.txt'.
4. Configure environment variables and PostgreSQL database settings.
5. Run database migrations.
6. Start the Django development server.

## API Testing

APIs are tested using Postman.

## Project Status

Backend development is in progress. React frontend development and real payment gateway integration are planned.

## Future Enhancements

- React-based responsive frontend
- Real payment gateway integration
- Improved order tracking
- Automated testing
- Deployment to a cloud platform
