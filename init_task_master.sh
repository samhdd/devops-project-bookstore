#!/bin/bash

# Task-Master AI initialization script
echo "Initializing Task-Master AI for Bookstore Project..."

# Ensure .vscode directory exists
mkdir -p .vscode

# Check if log directory exists, create if not
if [ ! -d "logs" ]; then
  echo "Creating logs directory..."
  mkdir -p logs
  touch logs/task-master.log
  echo "$(date): Task-Master AI initialized" > logs/task-master.log
fi

# Check for required tools
echo "Checking for required tools..."

# Check for Python
if ! command -v python &> /dev/null; then
  echo "Python is required but not found. Please install Python."
  exit 1
fi

# Check for Node.js
if ! command -v node &> /dev/null; then
  echo "Node.js is required but not found. Please install Node.js."
  exit 1
fi

# Run initial setup tasks
echo "Running initial setup tasks..."

# Install API dependencies
echo "Installing API dependencies..."
cd api && pip install -r requirements.txt
cd ..

# Install UI dependencies
echo "Installing UI dependencies..."
cd ui && npm install
cd ..

# Initialize database
echo "Setting up database..."
cd api && python create_db.py
cd ..

# Test database connection
echo "Testing database connection..."
cd api && python test_db_connection.py
cd ..

# Ensure scripts directory exists
mkdir -p .vscode/scripts
chmod +x .vscode/scripts/generate_prd.sh

# Generate PRD
echo "Generating Product Requirements Document..."
./.vscode/scripts/generate_prd.sh

echo "Task-Master AI has been successfully initialized!"
echo "You can now run tasks using VS Code's Tasks menu or by using the Task-Master AI commands."
