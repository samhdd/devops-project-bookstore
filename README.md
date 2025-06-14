# 📚 DevOps Bookstore Project

A full-stack e-commerce application for a bookstore specializing in Russian literature, featuring a Flask API backend and React frontend. This project is set up with Task-Master AI for automated DevOps workflows.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-19.0.0-blue.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.2.3-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-blue.svg)](https://www.postgresql.org/)

## ✨ Features

- Browse books by category with interactive filtering
- View featured books on the beautifully designed homepage
- Detailed product pages with comprehensive book information
- User-friendly shopping cart with real-time updates
- Responsive design for desktop and mobile devices
- Complete authentication system with JWT-based security
- User registration, login, and profile management
- Password reset functionality with token-based verification
- Role-based authorization (admin/customer)
- Task-Master AI integration for DevOps automation
- Automated Product Requirements Document generation
- PostgreSQL integration with complete database schema
- Environment-based configuration for development flexibility
- Automated database initialization and seeding

## 🔄 Recent Updates

- **Task-Master AI Integration**: Automated DevOps workflows and task management
- **PRD Generation**: Automated Product Requirements Document generation
- **PostgreSQL Database**: Enhanced data persistence and reliability with complete database schema
- **Image Handling**: Improved image loading with direct database URL usage
- **API Enhancements**: New endpoints for image diagnostics and direct image serving
- **UI Improvements**: Optimized React components and responsive design
- **DevOps Automation**: Enhanced startup scripts and environment management

## 📂 Project Structure

```
devops-project-bookstore/
├── .vscode/            # VS Code configuration and Task-Master AI setup
├── api/                # Flask API backend
│   ├── __pycache__/    # Python cache files
│   ├── config.py       # API configuration
│   ├── create_db.py    # Database setup script
│   ├── db_setup.sql    # SQL schema definitions
│   ├── main.py         # Main API entry point
│   ├── README.md       # API documentation
│   ├── requirements.txt # Python dependencies
│   ├── test_db_connection.py # Database connectivity test
│   └── update_products.py # Product data update script
├── docs/               # Project documentation
│   └── product_requirements_document.md # PRD
├── logs/               # Application and task logs
├── ui/                 # React frontend
│   ├── public/         # Static assets and HTML
│   │   └── images/     # Image resources
│   ├── src/            # React source code
│   │   ├── assets/     # Frontend assets
│   │   ├── components/ # Reusable UI components
│   │   ├── pages/      # Application pages
│   │   └── utils/      # Utility functions
│   ├── package.json    # Frontend dependencies
│   ├── README.md       # Frontend documentation
│   └── server.js       # Development server
├── init_task_master.sh # Task-Master AI initialization
├── LICENSE             # Project license
├── README.md           # This file
├── start_clean.sh      # Clean startup script
└── start.sh            # Application startup script
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher
- Node.js 18.x or higher
- PostgreSQL 14 or higher
- VS Code (for Task-Master AI integration)

### Initial Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/devops-project-bookstore.git
   cd devops-project-bookstore
   ```

2. Initialize Task-Master AI (recommended):
   ```bash
   chmod +x init_task_master.sh
   ./init_task_master.sh
   ```
   This will:
   - Set up Task-Master AI configuration
   - Install API and UI dependencies
   - Initialize the database
   - Generate the Product Requirements Document

3. Environment Configuration:
   - The project uses environment variables for configuration
   - Database settings can be customized in `api/config.py`
   - Default values are provided for development environments

4. Database Setup:
   - PostgreSQL is configured automatically by the startup scripts
   - Tables are created according to the schema in `api/db_setup.sql`
   - Initial product data is seeded via `api/update_products.py`

### Running the Application

#### Option 1: Using Task-Master AI (Recommended)

In VS Code, press `Ctrl+Shift+B` or run the "Start Full Application" task from the Tasks menu.

#### Option 2: Using the Start Script

```bash
chmod +x start.sh
./start.sh
```

#### Option 3: Running Components Separately

**Backend (Flask API):**
```bash
cd api
python main.py
```

**Frontend (React):**
```bash
cd ui
npm start
```

### Access the Application

- **Frontend:** http://localhost:3000
- **API:** http://localhost:5000/api

## 🔌 API Endpoints

The Flask API (`main.py`) provides a complete REST interface with PostgreSQL integration:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/categories` | GET | Retrieve all book categories |
| `/api/categories/:id` | GET | Get details for a specific category |
| `/api/categories/:id/products` | GET | Get all products in a specific category |
| `/api/products/:id` | GET | Get detailed information for a specific product |
| `/api/products/featured` | GET | Get a list of featured products for homepage |
| `/api/cart` | GET | Retrieve current cart contents |
| `/api/cart/add` | POST | Add a new item to the shopping cart |
| `/api/cart/update` | PUT | Update quantity of an item in the cart |
| `/api/cart/remove/:id` | DELETE | Remove an item from the cart |
| `/api/cart/checkout` | POST | Process checkout and clear cart |
| `/api/images/books/:filename` | GET | Serve book cover images directly |
| `/api/debug/images` | GET | Debug endpoint for image loading issues |
| `/api/auth/register` | POST | Register a new user |
| `/api/auth/login` | POST | Authenticate a user and return a token |
| `/api/auth/profile` | GET | Get the authenticated user's profile |
| `/api/auth/password-reset` | POST | Request a password reset |
| `/api/auth/password-reset/confirm` | POST | Confirm and set a new password |

### API Implementation Features
- Full CRUD operations for categories, products, and cart items
- User authentication and authorization
- Password reset functionality
- Database connection management with psycopg2
- Comprehensive error handling and logging
- Image serving capabilities with proper content types

## 🖼️ Image Loading System

The application uses a robust image loading approach:

1. **URL Normalization**: The API normalizes image URLs before sending to frontend
2. **Direct Database URLs**: Frontend accepts direct image URLs from database
3. **Fallback System**: Multi-tier fallback to ensure images display properly:
   - Direct database URL → Local public folder → Default placeholder image
4. **Lazy Loading**: Images load progressively as user scrolls for better performance

## ⚙️ Task-Master AI

This project includes Task-Master AI for DevOps automation:

### Available Tasks

- **Start API Server**: Runs the backend API server
- **Start UI Server**: Runs the frontend UI server
- **Setup Database**: Creates and initializes the database
- **Test Database Connection**: Verifies database connectivity
- **Update Products**: Updates product data in the database
- **Install API Dependencies**: Installs Python dependencies for the API
- **Install UI Dependencies**: Installs Node.js dependencies for the UI
- **Start Full Application**: Starts both API and UI servers in sequence
- **Generate PRD**: Creates or updates the Product Requirements Document
- **Task-Master: Status Check**: Shows the current status of Task-Master AI

### Automation Rules

1. **PRD Generation**: Automatically generates a Product Requirements Document on project startup
2. **Database Setup**: Automatically runs database setup and tests connection on project startup
3. **Dependency Management**: Automatically installs dependencies when requirements.txt or package.json changes
4. **Product Updates**: Runs product updates on a daily schedule
5. **PRD Updates**: Automatically updates the PRD when code changes are made to UI or API files

To learn more, see [Task-Master AI README](./.vscode/TASK-MASTER-README.md)

## 🗃️ PostgreSQL Implementation

The application features a robust PostgreSQL implementation with the following components:

### Database Configuration
- **Environment-based Configuration**: Database connection details are managed through `config.py` with environment-specific settings
- **Connection Pooling**: Efficient database connection management to optimize performance
- **Error Handling**: Comprehensive error management for database operations

### Database Schema
- **Categories Table**: Hierarchical book categorization system
- **Products Table**: Complete book information storage including authors, prices, and descriptions
- **Cart Items Table**: Persistent shopping cart with user associations
- **Foreign Key Relationships**: Properly designed relationships for data integrity

### Automation
- **Automated Setup**: Database creation via `create_db.py`
- **Schema Management**: Table creation and updates through SQL scripts
- **Data Seeding**: Initial product catalog population with `update_products.py`
- **Migration Support**: Infrastructure for schema updates and data management

## 🧑‍💻 Development

### Backend Development

1. Install Python dependencies:
   ```bash
   cd api
   pip install -r requirements.txt
   ```

2. Run the backend in development mode:
   ```bash
   python main.py
   ```

3. Test database connection:
   ```bash
   python test_db_connection.py
   ```

4. Database Management:
   ```bash
   # Create or reset the database
   python create_db.py
   
   # Update product catalog
   python update_products.py
   
   # Check database schema
   python check_db_schema.py
   ```

5. The backend implements:
   - PostgreSQL connection pooling
   - Environment-based configuration
   - Comprehensive error handling
   - Schema management and migration support

### Frontend Development

1. Install Node.js dependencies:
   ```bash
   cd ui
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

3. Build for production:
   ```bash
   npm run build
   ```

## 📊 Project Documentation

The project includes comprehensive documentation:

- **Product Requirements Document**: Located at `docs/product_requirements_document.md`
- **API Documentation**: Available in the API README at `api/README.md`
- **Task-Master AI Guide**: Available at `.vscode/TASK-MASTER-README.md`

## 🤝 Contributing

We welcome contributions to the DevOps Bookstore Project! Here's how you can contribute:

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the terms found in the LICENSE file in the root directory.

---

*Last Updated: June 14, 2025*

## 🛠️ DevOps Automation

The project includes several automation scripts to simplify development and deployment:

### Startup Scripts

- **start.sh**: Complete application startup automation
  - PostgreSQL service management
  - Process cleanup and monitoring
  - Virtual environment management
  - Sequential service startup

- **start_clean.sh**: Fresh start with clean environment
  - Removes temporary files
  - Resets database if needed
  - Reinitializes environment

### Development Environment Features

- Properly configured `.gitignore` for Python/Node.js projects
- Requirements files for dependency management
- Environment variable configuration
- Database initialization and seeding scripts
