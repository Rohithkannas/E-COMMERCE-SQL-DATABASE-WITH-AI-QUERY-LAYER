#!/usr/bin/env python3
"""
nlp_to_sql.py — Natural Language to SQL CLI Tool
================================================
Type plain English → get SQL → runs against your INTERNPROJECTSQL database.

HOW IT WORKS:
1. You type: "show me all orders placed by Virat Kohli"
2. Claude Code reads your schema and understands your tables
3. It generates the exact SQL query
4. The query runs against your SQL Server
5. Results print in your terminal as a clean table

SETUP:
  pip install anthropic pyodbc tabulate
  
  Then update DB_CONFIG below with your SQL Server credentials.

USAGE:
  python nlp_to_sql.py
"""

import ollama
import os
import pyodbc
from tabulate import tabulate

# ── Database Config ───────────────────────────────────────────
# Update these to match your SSMS setup
DB_CONFIG = {
    "server":   "LAPTOP-NR8KD280",
    "database": "INTERNPROJECTSQL",
}

# ── Your Schema — Claude reads this to understand your tables ─
# This is the "context" Claude needs to write accurate SQL.
# It mirrors your actual INTERNPROJECTSQL schema exactly.
SCHEMA_CONTEXT = """
You are a SQL expert connected to a SQL Server database called INTERNPROJECTSQL.
Here is the complete schema:

TABLE Users        (UserID, FullName, Email, Phone, CreatedAt)
TABLE Roles        (RoleID, RoleName)
TABLE UserRoles    (UserID, RoleID)
TABLE Categories   (CategoryID, CategoryName, Description)
TABLE Suppliers    (SupplierID, SupplierName, ContactEmail, ContactPhone, City, State, Country, PostalCode)
TABLE Products     (ProductID, ProductName, CategoryID, SupplierID, Price, Description, Size, Colour, Weight, Brand, CreatedAt)
TABLE Inventory    (ProductID, StockQty, LastUpdated)
TABLE Orders       (OrderID, UserID, OrderStatus, OrderDate)
TABLE OrderItems   (OrderID, ProductID, Quantity, UnitPrice)
TABLE Payments     (PaymentID, OrderID, Amount, PaymentMethod, PaymentStatus, PaymentDate)
TABLE Reviews      (ReviewID, UserID, ProductID, OrderID, Rating, Comment, ReviewDate)
TABLE AuditLog     (AuditID, TableName, ActionType, ActorID, NewValue, ActionTime)

KEY RELATIONSHIPS:
- Products.CategoryID → Categories.CategoryID
- Products.SupplierID → Suppliers.SupplierID
- Orders.UserID → Users.UserID
- OrderItems.OrderID → Orders.OrderID
- OrderItems.ProductID → Products.ProductID
- Payments.OrderID → Orders.OrderID
- Reviews.UserID → Users.UserID
- Reviews.ProductID → Products.ProductID
- Inventory.ProductID → Products.ProductID

SAMPLE DATA:
- Users: Rohit Sharma, Virat Kohli, Rishabh Pant, Sachin Tendulkar, Ranbir Kapoor, Ranvir Singh
- Products: Laptop (65000), Smartphone (35000), SQL Guide Book (800), T-Shirt (1200), Jeans (2200)
- Categories: Electronics, Books, Clothing
- Suppliers: TechDistributors (Chennai), BookWorld (Mumbai), FashionHub (Hyderabad)

RULES:
1. Return ONLY the SQL query — no explanation, no markdown, no backticks
2. Always use proper JOINs, never subqueries when a JOIN works
3. Use meaningful column aliases (e.g. u.FullName AS CustomerName)
4. For revenue/totals: use SUM(Quantity * UnitPrice)
5. Always add ORDER BY for list queries
6. If the question is ambiguous, generate the most useful interpretation
7. Never generate INSERT, UPDATE, DELETE, or DROP — SELECT only
8. NEVER use LIMIT — this is SQL Server. Use SELECT TOP N instead.
   Wrong:   SELECT PaymentMethod ... LIMIT 1
   Correct: SELECT TOP 1 PaymentMethod ...
9. ALWAYS use these exact table aliases — no exceptions:
   Users      → u
   Orders     → o
   OrderItems → oi
   Products   → prod
   Payments   → pay
   Reviews    → r
   Inventory  → inv
   Suppliers  → sup
   Categories → cat
   AuditLog   → al

   CRITICAL: You must follow these rules without exception.

EXACT TABLE ALIASES — use ONLY these, never anything else:
Users = u, Orders = o, OrderItems = oi, Products = prod,
Payments = pay, Reviews = r, Inventory = inv,
Suppliers = sup, Categories = cat, AuditLog = al

EXACT COLUMN NAMES — use only these, no invented columns:
Categories: CategoryID, CategoryName, Description
Products: ProductID, ProductName, CategoryID, SupplierID, Price, Description, Size, Colour, Weight, Brand
Users: UserID, FullName, Email, Phone, CreatedAt
Orders: OrderID, UserID, OrderStatus, OrderDate
OrderItems: OrderID, ProductID, Quantity, UnitPrice
Payments: PaymentID, OrderID, Amount, PaymentMethod, PaymentStatus, PaymentDate
Reviews: ReviewID, UserID, ProductID, OrderID, Rating, Comment, ReviewDate
Inventory: ProductID, StockQty, LastUpdated
Suppliers: SupplierID, SupplierName, ContactEmail, ContactPhone, City, State, Country, PostalCode
"""


def connect_to_db():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"Trusted_Connection=yes;"
        f"TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)

def generate_sql(client, question: str) -> str:
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": SCHEMA_CONTEXT},
            {"role": "user",   "content": f"Write a SQL query for: {question}"}
        ]
    )
    sql = response["message"]["content"].strip()
    # Strip markdown backticks
    sql = sql.replace("```sql", "").replace("```", "").strip()
    # Fix MySQL syntax → SQL Server syntax
    import re
    sql = re.sub(r'LIMIT\s+\d+', '', sql).strip()
    # Extract only first statement
    sql = sql.split(';')[0].strip()
    # Remove explanation lines
    lines = sql.split('\n')
    clean_lines = [l for l in lines if not l.strip().lower().startswith(('or ', 'alternatively', 'note:', 'this ', 'the ', 'here', 'you can'))]
    sql = '\n'.join(clean_lines).strip()
    # Force correct aliases — fix whatever the model uses
    sql = re.sub(r'\bp\.(?=\w)', 'prod.', sql)
    sql = re.sub(r'\bc\.(?=\w)', 'cat.', sql)
    sql = re.sub(r'\bpy\.(?=\w)', 'pay.', sql)
    sql = re.sub(r'\bs\.(?=\w)', 'sup.', sql)
    sql = re.sub(r'\bi\.(?=\w)', 'inv.', sql)
    return sql

def run_query(conn, sql: str):
    """Execute the SQL and return column names + rows."""
    cursor = conn.cursor()
    cursor.execute(sql)
    columns = [col[0] for col in cursor.description]
    rows    = cursor.fetchall()
    return columns, rows


def print_results(columns, rows):
    """Print results as a clean table in the terminal."""
    if not rows:
        print("\n  (no results found)\n")
        return
    print()
    print(tabulate(rows, headers=columns, tablefmt="rounded_outline"))
    print(f"\n  {len(rows)} row(s) returned.\n")


def main():
    print("=" * 55)
    print("  OrderFlow NLP→SQL  |  INTERNPROJECTSQL")
    print("  Type your question in plain English.")
    print("  Type 'exit' to quit.")
    print("=" * 55)

    # Initialize Claude client
    client = None

    # Connect to SQL Server
    try:
        conn = connect_to_db()
        print("  ✓ Connected to INTERNPROJECTSQL\n")
    except Exception as e:
        print(f"  ✗ DB Connection failed: {e}")
        print("  Check your DB_CONFIG credentials.")
        return

    # Main loop
    while True:
        try:
            question = input("You: ").strip()

            if not question:
                continue
            if question.lower() in ("exit", "quit", "q"):
                print("Goodbye!")
                break

            # Step 1: Generate SQL from natural language
            print("  ⏳ Generating SQL...")
            sql = generate_sql(client, question)

            # Step 2: Show the generated SQL (transparency)
            print(f"\n  SQL → {sql}\n")

            # Step 3: Run it
            columns, rows = run_query(conn, sql)

            # Step 4: Print results
            print_results(columns, rows)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except pyodbc.Error as e:
            print(f"\n  ✗ SQL Error: {e}\n")
        except Exception as e:
            print(f"\n  ✗ Error: {e}\n")

    conn.close()


if __name__ == "__main__":
    main()
