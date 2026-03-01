# 🛒 E-Commerce Database Management System

A fully normalized relational database system built using **Microsoft SQL Server (T-SQL)**, simulating the backend data infrastructure of an e-commerce platform. This project covers end-to-end database design including schema creation, data insertion, stored procedures, triggers, views, and role-based access control.

Now features an **AI-powered NLP-to-SQL Chatbot** using **Ollama** for natural language querying!

---

## 📁 Project Structure

| File / Folder | Description |
|---------------|-------------|
| `SQL/Creation.sql` | Database creation and recovery configuration |
| `SQL/Schemas.sql` | Table definitions with constraints and relationships |
| `SQL/Insert_Data.sql` | Sample data population for all tables |
| `SQL/Views.sql` | Aggregate views for reporting and analytics |
| `SQL/Stored_Procedures.sql` | Reusable procedures for user and order management |
| `SQL/Triggers.sql` | Automated triggers for inventory and audit logging |
| `SQL/Securities.sql` | Role-based access control (RBAC) configuration |
| `ChatbotAI/nlp_to_sql.py` | **[NEW]** NLP-to-SQL CLI tool using Ollama (Llama 3.2) |
| `ERDs/` | Entity Relationship Diagrams for the database |

---

## 🤖 AI Chatbot (NLP to SQL)

The project includes an intelligent interface that allows you to query your database using plain English. 

### How it Works:
1. **Natural Language Input**: Type a query like *"Show me the total revenue from Laptops"*.
2. **AI Reasoning**: The tool uses **Ollama (Llama 3.2)** to analyze the database schema and generate a precise T-SQL query.
3. **Execution**: The generated SQL runs securely against your SQL Server.
4. **Presentation**: Results are formatted into a clean, readable table in your terminal.

---

## ⚙️ Features

### ✅ Data Modeling & Normalization
- Fully normalized schema (3NF) with clearly defined primary keys, foreign keys, and unique constraints.
- `IDENTITY` columns for auto-incrementing primary keys.

### ✅ AI Integration (New!)
- **NLP Interpretation**: Converts complex English questions into multi-join SQL queries.
- **Dynamic Context**: The AI is "aware" of your specific table names, relationships, and sample data.

### ✅ Database Logic
- **Stored Procedures**: `AddUser`, `AddOrder`, `SearchProducts`.
- **Triggers**: Real-time inventory updates and audit logging.
- **Views**: `SalesSummary`, `CustomerOrderOverview`, `ProductPerformanceView`.

---

## 🚀 Getting Started

### Prerequisites
- Microsoft SQL Server (2019 or later) & SSMS.
- **Python 3.8+** (for the Chatbot).
- **Ollama** installed locally (https://ollama.com).

### 1. Database Setup
Run the SQL scripts in the `SQL/` folder in this order:
1. `Creation.sql`
2. `Schemas.sql`
3. `Insert_Data.sql`
4. `Views.sql`, `Stored_Procedures.sql`, `Triggers.sql`, `Securities.sql`.

### 2. Chatbot Setup (Ollama)
1. Install dependencies:
   ```bash
   pip install ollama pyodbc tabulate
   ```
2. Pull the required AI model:
   ```bash
   ollama pull llama3.2
   ```
3. Update `DB_CONFIG` in `ChatbotAI/nlp_to_sql.py` with your server name.

---

## 📊 Sample Queries (NLP)

Once the chatbot is running (`python ChatbotAI/nlp_to_sql.py`), you can ask:

- *"Who are our top 5 customers by order volume?"*
- *"Which products are currently low on stock (less than 10 units)?"*
- *"Show me the total sales for each category this month."*
- *"Find all reviews for 'Laptop' with a rating higher than 4."*

---

## 🧱 Tech Stack

| Layer | Technology |
|-------|------------|
| **Database** | Microsoft SQL Server (T-SQL) |
| **AI Engine** | Ollama (Llama 3.2 Model) |
| **Logic Layer** | Python 3.x |
| **Interface** | CLI (Python / Tabulate) |
| **Tools** | SSMS, ODBC Driver 17 |

---

## 👤 Author

Developed by **Rohith Kanna S** as part of an e-commerce database engineering project.
