#!/bin/bash
# Simplified Bookstore application startup script

set -e  # Exit on any error

echo "Starting Bookstore Application..."

# Kill any existing application processes
echo "Stopping any existing processes..."
pkill -f "python.*main.py" || true
pkill -f "npm.*start" || true
sleep 2

# Check if PostgreSQL is running
echo "Checking PostgreSQL service..."
if ! pgrep -x "postgres" > /dev/null; then
    echo "Starting PostgreSQL service..."
    sudo service postgresql start
    sleep 3
fi

# Ensure Node.js/npm is in PATH (for systems where it's not in sudo PATH)
if ! command -v npm &> /dev/null; then
    # Try to find npm in common locations or use a configurable fallback path
    FALLBACK_NPM_PATH=${FALLBACK_NPM_PATH:-"/versions/node/v22.15.1/bin/npm"}
    COMMON_LOCATIONS=("/usr/local/bin/npm" "/usr/bin/npm" "$FALLBACK_NPM_PATH")

    for location in "${COMMON_LOCATIONS[@]}"; do
        if [ -f "$location" ]; then
            export PATH="$(dirname "$location"):$PATH"
            echo "Added Node.js to PATH from $location"
            break
        fi
    done

    if ! command -v npm &> /dev/null; then
        echo "ERROR: npm not found. Please ensure Node.js is installed."
        echo "You may need to install Node.js or set FALLBACK_NPM_PATH."
        exit 1
    fi
fi

# Setup Python API
echo "Setting up API..."
cd /home/sam/devops-project-bookstore/api

# Create and activate virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Setup database
echo "Setting up database..."
python create_db.py
PGPASSWORD=postgres psql -h localhost -U postgres -d bookstore -f db_setup.sql -v ON_ERROR_STOP=1 || echo "Database schema already exists"
python update_products.py
python check_db_schema.py

# Set environment variables for API
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=bookstore
export DB_USER=postgres
export DB_PASSWORD=postgres

# Start API server in background
echo "Starting API server..."
python main.py &
API_PID=$!
echo "API server started with PID: $API_PID"

# Wait for API to be ready
sleep 3

# Setup and start React frontend
echo "Setting up UI..."
cd /home/sam/devops-project-bookstore/ui

# Install npm dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing React dependencies..."
    npm install
fi

# Set environment variables for React
export REACT_APP_API_URL=http://localhost:5000
export BROWSER=none  # Prevent auto-opening browser

# Start React development server
echo "Starting React development server..."
npm start &
UI_PID=$!
echo "React development server started with PID: $UI_PID"

# Wait for React to fully start
sleep 5

echo ""
echo "Application started successfully!"
echo "API is running at http://localhost:5000"
echo "Frontend is running at http://localhost:3000"
echo ""

# Try to open browser
if command -v xdg-open &> /dev/null; then
    echo "Opening frontend in your browser..."
    xdg-open http://localhost:3000 &
fi

echo "Press Ctrl+C to stop both servers"

# Function to cleanup processes on exit
cleanup() {
    echo ""
    echo "Stopping all services..."
    kill $API_PID $UI_PID 2>/dev/null || true
    wait $API_PID $UI_PID 2>/dev/null || true
    echo "All services stopped."
}

# Trap signals to cleanup properly
trap cleanup INT TERM EXIT

# Wait for both processes
wait $API_PID $UI_PID
