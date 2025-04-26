# Streamlit application with YAML-based user login, SQLite database, and role-based access control
import streamlit as st
import yaml
import pandas as pd
from sqlalchemy import create_engine, inspect
import os

# ---------- Configuration ----------
USERS_FILE = 'users.yaml'
DB_FILE = 'financial.db'

# ---------- Utility Functions ----------
def load_users(yaml_path=USERS_FILE):
    """
    Load users and permissions from a YAML file.
    YAML structure:
    username:
      password: <plain_text_password>
      permissions:
        table_name:
          view: True/False
          edit: True/False
    """
    if not os.path.exists(yaml_path):
        st.error(f"Users file '{yaml_path}' not found.")
        return {}
    with open(yaml_path) as f:
        users = yaml.safe_load(f)
    return users or {}


def init_db(db_path=DB_FILE):
    """
    Initialize SQLite database and create or update sample tables.
    """
    engine = create_engine(f'sqlite:///{db_path}', connect_args={'check_same_thread': False})

    # Sample dataframes
    dates = pd.date_range(start='2025-01-01', periods=12, freq='M')
    revenue_df = pd.DataFrame({'date': dates, 'amount': [10000, 12000, 11000, 13000, 12500, 14000, 15000, 14500, 15500, 16000, 17000, 18000]})
    expenses_df = pd.DataFrame({'date': dates, 'amount': [8000, 8500, 9000, 9200, 8800, 9400, 9800, 10200, 10000, 10500, 11000, 11500]})
    payroll_df = expenses_df.copy(); payroll_df['amount'] = (payroll_df['amount'] * 0.5).round(2)
    forecasts_df = revenue_df.copy(); forecasts_df['amount'] = (forecasts_df['amount'] * 1.1).round(2)
    balance_df = pd.DataFrame({'date': dates, 'assets': (revenue_df['amount'] * 2).round(2), 'liabilities': (expenses_df['amount'] * 1.2).round(2)})

    tables = {
        'revenue': revenue_df,
        'expenses': expenses_df,
        'payroll': payroll_df,
        'forecasts': forecasts_df,
        'balance_sheet': balance_df
    }

    inspector = inspect(engine)
    if not os.path.exists(db_path):
        for name, df in tables.items():
            df.to_sql(name, engine, index=False)
    else:
        existing = inspector.get_table_names()
        for name, df in tables.items():
            if name not in existing:
                df.to_sql(name, engine, index=False)
    return engine

# ---------- Authentication ----------
def login_form():
    st.title("🔒 Login")
    with st.form('login'):
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        submitted = st.form_submit_button('Login')
        if submitted:
            users = load_users()
            user = users.get(username)
            if user and user.get('password') == password:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['permissions'] = user.get('permissions', {})
                st.success(f"Logged in as {username}")
            else:
                st.error('Invalid username or password')

# ---------- Main Application ----------
def main_app():
    # Logout button with fallback
    if st.sidebar.button("🔓 Logout"):
        for key in ['logged_in', 'username', 'permissions']:
            st.session_state.pop(key, None)
        try:
            st.experimental_rerun()
        except AttributeError:
            st.success("Logged out. Please refresh the page to login again.")
            st.stop()

    engine = init_db()
    username = st.session_state['username']
    permissions = st.session_state.get('permissions', {})

    st.sidebar.title(f"User: {username}")
    available_tables = [tbl for tbl, perm in permissions.items() if perm.get('view')]
    if not available_tables:
        st.warning('No tables available for your user.')
        return
    table = st.sidebar.selectbox('Select table', available_tables)
    perm = permissions.get(table, {})

    df = pd.read_sql_table(table, engine)
    st.subheader(f"Table: {table}")
    st.dataframe(df)

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    if numeric_cols:
        col = st.selectbox('Choose numeric column for line chart', numeric_cols)
        if 'date' in df.columns:
            chart_df = df.set_index('date')[col]
        else:
            chart_df = df[col]
        st.line_chart(chart_df)

    if perm.get('edit'):
        st.markdown('---')
        st.subheader('Edit Data')
        try:
            edited_df = st.data_editor(df, num_rows='dynamic', use_container_width=True)
        except AttributeError:
            st.error("Your Streamlit version does not support data_editor. Please upgrade with 'pip install --upgrade streamlit'.")
            return
        if st.button('Save changes'):
            edited_df.to_sql(table, engine, if_exists='replace', index=False)
            st.success('Table updated successfully!')
    else:
        st.info('Read-only access for this table.')

# ---------- Entry Point ----------
if 'logged_in' not in st.session_state:
    login_form()
else:
    main_app()