# Stadium Management System

A comprehensive web application for managing stadium bookings, events, and ticket sales.

## Features

- Role-based access control (Admin, Organizer, Customer)
- Event scheduling and management
- Stadium booking system
- Online ticket booking
- User authentication and authorization
- Responsive design with Bootstrap

## Prerequisites

- Python 3.8 or higher
- MySQL Server
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd stadium-management
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=mysql://username:password@localhost/stadium_management_db
```

5. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

6. Run the application:
```bash
flask run
```

## Project Structure

```
stadium_management/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── static/
│   └── templates/
├── migrations/
├── .env
├── config.py
├── requirements.txt
└── run.py
```

## User Roles

1. Admin
   - Manage stadiums
   - Approve/reject bookings
   - View all users and events

2. Organizer
   - Book stadiums
   - Create and manage events
   - View booking history

3. Customer
   - Browse events
   - Book tickets
   - View ticket history

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 