# Intership_Project
Streamlit Financial Dashboard

A simple Streamlit application that provides:

User Authentication via a YAML file (users.yaml)

Role-Based Access Control allowing users to view or edit specific tables

Local SQLite Database (financial.db) pre-populated with sample financial tables

Interactive Data Exploration with Pandas DataFrame display and line charts

In-App Data Editing using Streamlit’s st.data_editor

Features

Login / Logout

Credentials and permissions managed in users.yaml

Secure session handling with Streamlit’s session_state

Database Initialization

Automatically creates or updates tables for:

revenue

expenses

payroll

forecasts

balance_sheet

Detects missing tables in existing DB and adds them on startup

Role-Based Table Access

Each user has view and edit flags per table

Sidebar controls reflect available tables and permissions

Data Visualization

Line charts for any numeric column (dates auto-indexed)

In-App Editing

Editable DataFrame component

Changes written back to the database on save

Getting Started

Prerequisites

Python 3.8+

pip package manager

Installation

Clone the repository

git clone https://github.com/yourusername/streamlit-financial-dashboard.git
cd streamlit-financial-dashboard

Install dependencies

pip install streamlit pandas sqlalchemy pyyaml

Configuration

users.yaml

Create a users.yaml file in the project root:

alice:
  password: password123
  permissions:
    revenue:
      view: true
      edit: true
    expenses:
      view: true
      edit: false
    payroll:
      view: true
      edit: true
    forecasts:
      view: true
      edit: true
    balance_sheet:
      view: true
      edit: true

bob:
  password: secret456
  permissions:
    revenue:
      view: true
      edit: false
    expenses:
      view: false
      edit: false
    payroll:
      view: true
      edit: false
    forecasts:
      view: true
      edit: false
    balance_sheet:
      view: false
      edit: false

Database

No manual setup is needed. On first run, the app will create financial.db in the project root with the five sample tables. On subsequent runs, any missing tables will be added automatically.

Running the App

streamlit run streamlit_app.py

Open your browser at the provided local URL (usually http://localhost:8501/).

Log in with one of the usernames/passwords defined in users.yaml.

Use the sidebar to navigate tables and log out.

Project Structure

├── financial.db          # SQLite database (auto-generated)
├── streamlit_app.py      # Main application script
├── users.yaml            # User credentials & permissions
└── README.md             # This file

Customization

Add New Tables: Modify init_db() in streamlit_app.py to include additional DataFrames or load from CSV.

Password Hashing: Replace plain-text passwords with hashed values and update the login logic.

Visualization Types: Extend the UI to include bar charts, scatter plots, or other Streamlit components.

License

MIT License © 2025 Jean Alvarez
