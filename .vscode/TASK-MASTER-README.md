# Task-Master AI for Bookstore Project

This document provides information on how to use Task-Master AI for automating tasks in the Bookstore project.

## Overview

Task-Master AI is configured to automate common development tasks and improve workflow efficiency for the Bookstore application. It automates database setup, dependency management, and scheduled product updates.

## Available Tasks

The following tasks are available:

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

## Automation Rules

Task-Master AI includes the following automation rules:

1. **PRD Generation**: Automatically generates a Product Requirements Document on project startup
2. **Database Setup**: Automatically runs database setup and tests connection on project startup
3. **Dependency Management**: Automatically installs dependencies when requirements.txt or package.json changes
4. **Product Updates**: Runs product updates on a daily schedule
5. **PRD Updates**: Automatically updates the PRD when code changes are made to UI or API files

## Getting Started

1. Initialize Task-Master AI by running:
   ```
   ./init_task_master.sh
   ```

2. Open the project in VS Code to use the configured tasks:
   - Press `Ctrl+Shift+P` and type "Tasks: Run Task" to see available tasks
   - Use the Tasks menu in VS Code to run specific tasks
   - The default build task (`Ctrl+Shift+B`) will start the full application

## Configuration Files

- `.vscode/tasks.json`: Contains task definitions
- `.vscode/task-master.json`: Contains Task-Master AI configuration
- `logs/task-master.log`: Contains Task-Master AI execution logs
- `docs/product_requirements_document.md`: The generated PRD
- `docs/prd_template.md`: Template used for PRD generation

## Customization

You can customize Task-Master AI by editing the `.vscode/task-master.json` file to add new automation rules, change schedules, or modify notification settings.
