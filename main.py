from fastmcp import FastMCP   # To import the FastMCP class from the fastmcp module
import os   # To handle file paths
import sqlite3  # To manage the database connection
from typing import Optional # To specify optional parameters in function definitions

DB_PATH = os.path.join(os.path.dirname(__file__), 'expenses.db')  # Define the path to the SQLite database

CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")  # Define the path to the categories JSON file

mcp = FastMCP("ExpenseTracker")  # Create an instance of the FastMCP class


def init_db():
    with sqlite3.connect(DB_PATH) as c:  # Connect to the SQLite database
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               date TEXT NOT NULL,
               amount REAL NOT NULL,
               category TEXT NOT NULL,
               subcategory TEXT DEFAULT '',
               note TEXT DEFAULT ''     
            )
""")
        
# Initialize the database when the script is run
init_db()



# Tool to add an expense to the database
@mcp.tool()
def add_expense(date, amount, category, subcategory="", note=""):
    """ Add a new expense entry to the database with the provided details. """
    with sqlite3.connect(DB_PATH) as c:  # Connect to the SQLite database
        cur = c.execute(
            "INSERT INTO expenses (date, amount, category, subcategory, note) VALUES (?, ?, ?, ?, ?)",
            (date, amount, category, subcategory, note)
        )  # Insert the expense data into the database  
        
        return {"status" : "ok", "id": cur.lastrowid}  # Return a success status and the ID of the newly added expense
    



# Tool to list(or Show) expenses from the database
@mcp.tool()
def list_expenses(start_date,end_date):
    """ List all expense entries from the database."""
    with sqlite3.connect(DB_PATH) as c:  # Connect to the SQLite database
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note 
            FROM expenses 
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """, 
            (start_date, end_date)
        )  # Execute a query to select all expenses
        cols = [d[0] for d in cur.description]  # Get the column names from the query result
        return [dict(zip(cols,r)) for r in cur.fetchall()]  # Return a list of dictionaries representing each expense entry
      



# Tool to summarize expenses by category
@mcp.tool()
def summarize(start_date,end_date,category=None):
    """ Summarize expenses by category" within an inclusive date range. """
    with sqlite3.connect(DB_PATH) as c:  # Connect to the SQLite database
        query = (
            """
            SELECT category, SUM(amount) as total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
            """
        )
        params = [start_date, end_date]

        if category:  # If a specific category is provided, add it to the query
            query += " AND category = ?"
            params.append(category)
        
        query += " GROUP BY category ORDER BY category ASC"  # Group the results by category
        
        cur = c.execute(query, params)  # Execute the query with the provided parameters
        cols = [d[0] for d in cur.description]  # Get the column names from the query result
        return [dict(zip(cols,r)) for r in cur.fetchall()]  # Return a list of dictionaries representing the summarized expenses by category



# Tool to edit an existing expense entry in the database by ID
@mcp.tool()
def edit_expense(
    expense_id: int,
    date: Optional[str] = None,
    amount: Optional[float] = None,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    note: Optional[str] = None,
):
    """
    Update an existing expense.

    Only supplied fields are updated.
    """

    with sqlite3.connect(DB_PATH) as c:

        cur = c.execute(
            """
            SELECT
                id,
                date,
                amount,
                category,
                subcategory,
                note
            FROM expenses
            WHERE id = ?
            """,
            (expense_id,)
        )

        row = cur.fetchone()

        if not row:
            return {
                "status": "error",
                "message": f"Expense ID {expense_id} not found"
            }

        current = {
            "id": row[0],
            "date": row[1],
            "amount": row[2],
            "category": row[3],
            "subcategory": row[4],
            "note": row[5],
        }

        updated_date = date if date is not None else current["date"]
        updated_amount = amount if amount is not None else current["amount"]
        updated_category = category if category is not None else current["category"]
        updated_subcategory = (
            subcategory if subcategory is not None
            else current["subcategory"]
        )
        updated_note = note if note is not None else current["note"]

        c.execute(
            """
            UPDATE expenses
            SET
                date = ?,
                amount = ?,
                category = ?,
                subcategory = ?,
                note = ?
            WHERE id = ?
            """,
            (
                updated_date,
                updated_amount,
                updated_category,
                updated_subcategory,
                updated_note,
                expense_id,
            )
        )

        c.commit()

        return {
            "status": "ok",
            "expense_id": expense_id,
            "updated": {
                "date": updated_date,
                "amount": updated_amount,
                "category": updated_category,
                "subcategory": updated_subcategory,
                "note": updated_note,
            }
        }
    


# Tool to delete an expense entry from the database by ID
@mcp.tool()
def delete_expense(expense_id: int):
    """
    Delete an expense by ID.
    """

    with sqlite3.connect(DB_PATH) as c:

        cur = c.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )

        if cur.rowcount == 0:
            return {
                "status": "error",
                "message": f"Expense ID {expense_id} not found"
            }

        return {
            "status": "ok",
            "deleted_expense_id": expense_id
        }


# Resource to serve the categories JSON file
@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    # Read fresh each time so you can edit the file without restarting
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    mcp.run()  # Run the FastMCP instance to start handling requests
