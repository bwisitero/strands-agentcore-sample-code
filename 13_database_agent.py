"""
Demo 13: SQL Database Agent (Natural Language to SQL)
Goal: Query databases using natural language with an intelligent agent

Key Teaching Points:
- Converting natural language to SQL queries
- Safe database operations with agents
- Schema awareness and query validation
- Real-world data analysis use cases
"""

import sqlite3
from strands import Agent, tool
from typing import List, Dict, Any
import json


# Initialize SQLite database with sample data
def setup_database():
    """Create a sample e-commerce database with products and orders."""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            customer_name TEXT NOT NULL,
            order_date DATE NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    # Clear existing data
    cursor.execute('DELETE FROM orders')
    cursor.execute('DELETE FROM products')

    # Insert sample products
    products = [
        (1, 'Laptop Pro', 'Electronics', 1299.99, 15),
        (2, 'Wireless Mouse', 'Electronics', 29.99, 100),
        (3, 'USB-C Cable', 'Accessories', 19.99, 200),
        (4, 'Desk Chair', 'Furniture', 299.99, 25),
        (5, 'Monitor 27"', 'Electronics', 399.99, 30),
        (6, 'Keyboard Mechanical', 'Electronics', 149.99, 45),
        (7, 'Desk Lamp', 'Furniture', 59.99, 60),
        (8, 'Notebook Set', 'Stationery', 12.99, 150),
    ]
    cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?, ?)', products)

    # Insert sample orders
    orders = [
        (1, 1, 2, 'Alice Johnson', '2025-10-01'),
        (2, 2, 5, 'Bob Smith', '2025-10-01'),
        (3, 5, 1, 'Alice Johnson', '2025-10-02'),
        (4, 4, 3, 'Carol White', '2025-10-02'),
        (5, 1, 1, 'David Brown', '2025-10-03'),
        (6, 6, 2, 'Alice Johnson', '2025-10-03'),
        (7, 3, 10, 'Bob Smith', '2025-10-04'),
        (8, 7, 4, 'Eve Davis', '2025-10-04'),
    ]
    cursor.executemany('INSERT INTO orders VALUES (?, ?, ?, ?, ?)', orders)

    conn.commit()
    conn.close()
    print("✅ Database setup complete!")


@tool
def get_database_schema() -> str:
    """Get the database schema to understand available tables and columns."""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    schema_info = []

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        column_info = [f"{col[1]} ({col[2]})" for col in columns]
        schema_info.append(f"Table: {table_name}\nColumns: {', '.join(column_info)}")

    conn.close()
    return "\n\n".join(schema_info)


@tool
def execute_sql_query(query: str) -> str:
    """
    Execute a SELECT SQL query and return results as JSON.
    Only SELECT queries are allowed for safety.
    """
    # Safety check - only allow SELECT queries
    if not query.strip().upper().startswith('SELECT'):
        return "Error: Only SELECT queries are allowed for safety reasons."

    try:
        conn = sqlite3.connect('ecommerce.db')
        cursor = conn.cursor()

        cursor.execute(query)
        rows = cursor.fetchall()

        # Get column names
        columns = [description[0] for description in cursor.description]

        # Convert to list of dictionaries
        results = [dict(zip(columns, row)) for row in rows]

        conn.close()

        if not results:
            return "Query executed successfully but returned no results."

        return json.dumps(results, indent=2)

    except sqlite3.Error as e:
        return f"SQL Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def get_table_sample(table_name: str, limit: int = 5) -> str:
    """Get a sample of rows from a specific table to understand the data."""
    try:
        conn = sqlite3.connect('ecommerce.db')
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {table_name} LIMIT ?", (limit,))
        rows = cursor.fetchall()

        # Get column names
        columns = [description[0] for description in cursor.description]

        # Convert to list of dictionaries
        results = [dict(zip(columns, row)) for row in rows]

        conn.close()

        return json.dumps(results, indent=2)

    except sqlite3.Error as e:
        return f"SQL Error: {str(e)}"


# Create database agent with SQL tools
database_agent = Agent(
    tools=[get_database_schema, execute_sql_query, get_table_sample],
    system_prompt="""You are a SQL database expert assistant. You help users query databases using natural language.

When a user asks a question:
1. First, use get_database_schema to understand the database structure
2. Optionally use get_table_sample to see example data
3. Write an appropriate SQL query to answer their question
4. Use execute_sql_query to run the query
5. Interpret and present the results in a clear, human-readable format

Always explain what query you're running and why. Present results in a clear, formatted way."""
)


def main():
    """Run the database agent demo."""
    print("=" * 60)
    print("🗄️  SQL Database Agent Demo")
    print("=" * 60)
    print()

    # Setup database
    setup_database()
    print()

    # Example queries
    queries = [
        "What products do we have in stock?",
        "Show me all orders placed by Alice Johnson",
        "What's the total revenue from all orders?",
        "Which product category has the most sales?",
        "List the top 3 most expensive products",
    ]

    for i, query in enumerate(queries, 1):
        print(f"\n📊 Query {i}: {query}")
        print("-" * 60)
        response = database_agent(query)
        print(response)
        print()

    print("\n" + "=" * 60)
    print("✨ Demo complete! Database saved as 'ecommerce.db'")
    print("=" * 60)


if __name__ == "__main__":
    main()


"""
Usage Instructions:

1. Install required packages (already included with strands):
   uv add strands

2. Run the demo:
   python demo_13_database_agent.py

3. Try your own queries:
   python -c "from demo_13_database_agent import database_agent;
   print(database_agent('How many electronics do we have in stock?'))"

Features Demonstrated:
- Natural language to SQL conversion
- Schema discovery and understanding
- Safe query execution (SELECT only)
- Result formatting and interpretation
- Multi-table queries and aggregations

Example Questions You Can Ask:
- "What's our total inventory value?"
- "Who are our top customers by order count?"
- "What products are low on stock (less than 20)?"
- "Show me orders from the last 3 days"
- "What's the average price of electronics?"

Production Considerations:
- Add user authentication and access control
- Implement query result caching
- Add support for database views
- Implement rate limiting
- Add query explanation and optimization
- Support for multiple databases (PostgreSQL, MySQL, etc.)
- Add data visualization capabilities

Database Schema:
- products: id, name, category, price, stock
- orders: id, product_id, quantity, customer_name, order_date
"""

'''Sample output

emil@Franklins-MacBook-Pro strands-agentcore-demo % uv run demo_13_database_agent.py 
============================================================
🗄️  SQL Database Agent Demo
============================================================

✅ Database setup complete!


📊 Query 1: What products do we have in stock?
------------------------------------------------------------
I'll help you find what products are in stock. Let me start by examining the database structure to understand how product and inventory information is organized.
Tool #1: get_database_schema
Great! I can see there's a `products` table with a `stock` column that should show inventory levels. Let me get a sample of the data to better understand the structure:
Tool #2: get_table_sample
Perfect! Now I'll query for all products that have stock available (stock > 0):
Tool #3: execute_sql_query
## Products Currently in Stock

Here are all the products we currently have available in inventory, organized by category:

### **Accessories**
- **USB-C Cable** - $19.99 (200 units in stock)

### **Electronics**
- **Keyboard Mechanical** - $149.99 (45 units in stock)
- **Laptop Pro** - $1,299.99 (15 units in stock)
- **Monitor 27"** - $399.99 (30 units in stock)
- **Wireless Mouse** - $29.99 (100 units in stock)

### **Furniture**
- **Desk Chair** - $299.99 (25 units in stock)
- **Desk Lamp** - $59.99 (60 units in stock)

### **Stationery**
- **Notebook Set** - $12.99 (150 units in stock)

**Summary**: We currently have **8 different products** in stock with a total combined inventory of **625 units**. The highest stock levels are for USB-C Cables (200 units) and Notebook Sets (150 units), while the Laptop Pro has the lowest stock at 15 units.## Products Currently in Stock

Here are all the products we currently have available in inventory, organized by category:

### **Accessories**
- **USB-C Cable** - $19.99 (200 units in stock)

### **Electronics**
- **Keyboard Mechanical** - $149.99 (45 units in stock)
- **Laptop Pro** - $1,299.99 (15 units in stock)
- **Monitor 27"** - $399.99 (30 units in stock)
- **Wireless Mouse** - $29.99 (100 units in stock)

### **Furniture**
- **Desk Chair** - $299.99 (25 units in stock)
- **Desk Lamp** - $59.99 (60 units in stock)

### **Stationery**
- **Notebook Set** - $12.99 (150 units in stock)

**Summary**: We currently have **8 different products** in stock with a total combined inventory of **625 units**. The highest stock levels are for USB-C Cables (200 units) and Notebook Sets (150 units), while the Laptop Pro has the lowest stock at 15 units.



📊 Query 2: Show me all orders placed by Alice Johnson
------------------------------------------------------------
I'll search for all orders placed by Alice Johnson. Let me query the orders table to find her orders.
Tool #4: execute_sql_query
Now let me get the product details for these orders to show what items Alice Johnson ordered:
Tool #5: execute_sql_query
## Orders Placed by Alice Johnson

Here are all the orders placed by Alice Johnson, listed from most recent to oldest:

### **Order #6** - October 3, 2025
- **Product**: Keyboard Mechanical
- **Quantity**: 2 units
- **Unit Price**: $149.99
- **Total**: $299.98

### **Order #3** - October 2, 2025
- **Product**: Monitor 27"
- **Quantity**: 1 unit
- **Unit Price**: $399.99
- **Total**: $399.99

### **Order #1** - October 1, 2025
- **Product**: Laptop Pro
- **Quantity**: 2 units
- **Unit Price**: $1,299.99
- **Total**: $2,599.98

---

**Summary**: Alice Johnson has placed **3 orders** totaling **$3,299.95** over a 3-day period (October 1-3, 2025). Her largest single order was for 2 Laptop Pro units worth $2,599.98.## Orders Placed by Alice Johnson

Here are all the orders placed by Alice Johnson, listed from most recent to oldest:

### **Order #6** - October 3, 2025
- **Product**: Keyboard Mechanical
- **Quantity**: 2 units
- **Unit Price**: $149.99
- **Total**: $299.98

### **Order #3** - October 2, 2025
- **Product**: Monitor 27"
- **Quantity**: 1 unit
- **Unit Price**: $399.99
- **Total**: $399.99

### **Order #1** - October 1, 2025
- **Product**: Laptop Pro
- **Quantity**: 2 units
- **Unit Price**: $1,299.99
- **Total**: $2,599.98

---

**Summary**: Alice Johnson has placed **3 orders** totaling **$3,299.95** over a 3-day period (October 1-3, 2025). Her largest single order was for 2 Laptop Pro units worth $2,599.98.



📊 Query 3: What's the total revenue from all orders?
------------------------------------------------------------
I'll calculate the total revenue from all orders by summing up the value of each order (quantity × price).
Tool #6: execute_sql_query
Let me also get a breakdown by order to show you the details:
Tool #7: execute_sql_query
## Total Revenue Summary

### **Overall Revenue**
- **Total Revenue**: $6,089.72
- **Total Orders**: 8 orders
- **Total Items Sold**: 28 units

### **Revenue Breakdown by Order**

**October 4, 2025:**
- Order #7 (Bob Smith): USB-C Cable × 10 = $199.90
- Order #8 (Eve Davis): Desk Lamp × 4 = $239.96

**October 3, 2025:**
- Order #5 (David Brown): Laptop Pro × 1 = $1,299.99
- Order #6 (Alice Johnson): Keyboard Mechanical × 2 = $299.98

**October 2, 2025:**
- Order #3 (Alice Johnson): Monitor 27" × 1 = $399.99
- Order #4 (Carol White): Desk Chair × 3 = $899.97

**October 1, 2025:**
- Order #1 (Alice Johnson): Laptop Pro × 2 = $2,599.98
- Order #2 (Bob Smith): Wireless Mouse × 5 = $149.95

### **Key Insights**
- The highest single order was Alice Johnson's purchase of 2 Laptop Pro units ($2,599.98)
- Average order value: $761.22
- Alice Johnson is the top customer with 3 orders totaling $3,299.95 (54% of total revenue)
- Electronics category generates the most revenue, primarily from laptop sales## Total Revenue Summary

### **Overall Revenue**
- **Total Revenue**: $6,089.72
- **Total Orders**: 8 orders
- **Total Items Sold**: 28 units

### **Revenue Breakdown by Order**

**October 4, 2025:**
- Order #7 (Bob Smith): USB-C Cable × 10 = $199.90
- Order #8 (Eve Davis): Desk Lamp × 4 = $239.96

**October 3, 2025:**
- Order #5 (David Brown): Laptop Pro × 1 = $1,299.99
- Order #6 (Alice Johnson): Keyboard Mechanical × 2 = $299.98

**October 2, 2025:**
- Order #3 (Alice Johnson): Monitor 27" × 1 = $399.99
- Order #4 (Carol White): Desk Chair × 3 = $899.97

**October 1, 2025:**
- Order #1 (Alice Johnson): Laptop Pro × 2 = $2,599.98
- Order #2 (Bob Smith): Wireless Mouse × 5 = $149.95

### **Key Insights**
- The highest single order was Alice Johnson's purchase of 2 Laptop Pro units ($2,599.98)
- Average order value: $761.22
- Alice Johnson is the top customer with 3 orders totaling $3,299.95 (54% of total revenue)
- Electronics category generates the most revenue, primarily from laptop sales



📊 Query 4: Which product category has the most sales?
------------------------------------------------------------
I'll analyze sales by product category to see which one has generated the most revenue and volume.
Tool #8: execute_sql_query
Let me also get a detailed breakdown of which specific products were sold in each category:
Tool #9: execute_sql_query
## Product Category Sales Analysis

### **Sales by Category (Ranked by Revenue)**

### 🥇 **1st Place: Electronics**
- **Total Revenue**: $4,749.89 (77.9% of total sales)
- **Units Sold**: 11 units
- **Number of Orders**: 5 orders
- **Average Order Value**: $949.98

**Electronics Breakdown:**
- Laptop Pro: 3 units sold = $3,899.97 (82% of Electronics revenue)
- Monitor 27": 1 unit sold = $399.99
- Keyboard Mechanical: 2 units sold = $299.98
- Wireless Mouse: 5 units sold = $149.95

### 🥈 **2nd Place: Furniture**
- **Total Revenue**: $1,139.93 (18.7% of total sales)
- **Units Sold**: 7 units
- **Number of Orders**: 2 orders
- **Average Order Value**: $569.97

**Furniture Breakdown:**
- Desk Chair: 3 units sold = $899.97 (79% of Furniture revenue)
- Desk Lamp: 4 units sold = $239.96

### 🥉 **3rd Place: Accessories**
- **Total Revenue**: $199.90 (3.3% of total sales)
- **Units Sold**: 10 units
- **Number of Orders**: 1 order
- **Average Order Value**: $199.90

**Accessories Breakdown:**
- USB-C Cable: 10 units sold = $199.90

### **Key Insights**
- **Electronics dominates** with nearly 78% of total revenue, primarily driven by high-value laptop sales
- **Furniture** has the highest volume per category (7 units) but lower revenue due to mid-range pricing
- **Accessories** has high unit sales (10 units) but low revenue due to lower-priced items
- **Laptop Pro** is the single best-selling product by revenue ($3,899.97)

**Winner: Electronics category has the most sales by revenue!**## Product Category Sales Analysis

### **Sales by Category (Ranked by Revenue)**

### 🥇 **1st Place: Electronics**
- **Total Revenue**: $4,749.89 (77.9% of total sales)
- **Units Sold**: 11 units
- **Number of Orders**: 5 orders
- **Average Order Value**: $949.98

**Electronics Breakdown:**
- Laptop Pro: 3 units sold = $3,899.97 (82% of Electronics revenue)
- Monitor 27": 1 unit sold = $399.99
- Keyboard Mechanical: 2 units sold = $299.98
- Wireless Mouse: 5 units sold = $149.95

### 🥈 **2nd Place: Furniture**
- **Total Revenue**: $1,139.93 (18.7% of total sales)
- **Units Sold**: 7 units
- **Number of Orders**: 2 orders
- **Average Order Value**: $569.97

**Furniture Breakdown:**
- Desk Chair: 3 units sold = $899.97 (79% of Furniture revenue)
- Desk Lamp: 4 units sold = $239.96

### 🥉 **3rd Place: Accessories**
- **Total Revenue**: $199.90 (3.3% of total sales)
- **Units Sold**: 10 units
- **Number of Orders**: 1 order
- **Average Order Value**: $199.90

**Accessories Breakdown:**
- USB-C Cable: 10 units sold = $199.90

### **Key Insights**
- **Electronics dominates** with nearly 78% of total revenue, primarily driven by high-value laptop sales
- **Furniture** has the highest volume per category (7 units) but lower revenue due to mid-range pricing
- **Accessories** has high unit sales (10 units) but low revenue due to lower-priced items
- **Laptop Pro** is the single best-selling product by revenue ($3,899.97)

**Winner: Electronics category has the most sales by revenue!**



📊 Query 5: List the top 3 most expensive products
------------------------------------------------------------
I'll query the products table to find the top 3 most expensive products based on their price.
Tool #10: execute_sql_query
## Top 3 Most Expensive Products

### 🥇 **1st Place: Laptop Pro**
- **Price**: $1,299.99
- **Category**: Electronics
- **Stock**: 15 units available

### 🥈 **2nd Place: Monitor 27"**
- **Price**: $399.99
- **Category**: Electronics  
- **Stock**: 30 units available

### 🥉 **3rd Place: Desk Chair**
- **Price**: $299.99
- **Category**: Furniture
- **Stock**: 25 units available

### **Key Observations**
- The **Laptop Pro** is significantly more expensive than other products, costing over 3x more than the second most expensive item
- **Electronics dominate** the high-end price range (2 out of 3 top products)
- All three products have healthy stock levels available
- There's a notable price gap: $1,299.99 → $399.99 → $299.99## Top 3 Most Expensive Products

### 🥇 **1st Place: Laptop Pro**
- **Price**: $1,299.99
- **Category**: Electronics
- **Stock**: 15 units available

### 🥈 **2nd Place: Monitor 27"**
- **Price**: $399.99
- **Category**: Electronics  
- **Stock**: 30 units available

### 🥉 **3rd Place: Desk Chair**
- **Price**: $299.99
- **Category**: Furniture
- **Stock**: 25 units available

### **Key Observations**
- The **Laptop Pro** is significantly more expensive than other products, costing over 3x more than the second most expensive item
- **Electronics dominate** the high-end price range (2 out of 3 top products)
- All three products have healthy stock levels available
- There's a notable price gap: $1,299.99 → $399.99 → $299.99



============================================================
✨ Demo complete! Database saved as 'ecommerce.db'
============================================================'''