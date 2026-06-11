# 💸 Expense Tracker MCP Server

A lightweight Model Context Protocol (MCP) server built with FastMCP and SQLite that enables AI assistants such as Claude to manage personal expenses through natural language.

The server provides tools for adding, listing, updating, deleting, and summarizing expenses while storing all data locally in a SQLite database.

---

## 📚 Table of Contents

- [🔍 Overview](#-overview)
- [✨ Features](#-features)
- [📁 Project Structure](#-project-structure)
- [⚙️ Requirements](#️-requirements)
- [🚀 Installation](#-installation)
- [▶️ Running the Server](#️-running-the-server)
- [🔌 Claude Desktop Integration](#-claude-desktop-integration)
- [🛠️ Available Tools](#️-available-tools)
  - [add_expense](#add_expense)
  - [list_expenses](#list_expenses)
  - [summarize](#summarize)
  - [edit_expense](#edit_expense)
  - [delete_expense](#delete_expense)
- [📦 Available Resources](#-available-resources)
- [🏷️ Expense Categories](#️-expense-categories)
- [🗄️ Database Schema](#️-database-schema)
- [💬 Example Claude Prompts](#-example-claude-prompts)
- [🧑‍💻 Development](#-development)
- [📄 License](#-license)

---

## 🔍 Overview

Expense Tracker MCP Server exposes a set of MCP tools that allow AI assistants to interact directly with your expense data.

Instead of manually maintaining spreadsheets or expense apps, you can simply talk to Claude and ask it to:

- Record a new expense
- Update an incorrect entry
- Delete unwanted records
- Show expenses for a specific period
- Summarize spending by category
- View available categories and subcategories

All expense records are stored locally in SQLite, ensuring that your financial data remains under your control.

---

## ✨ Features

- Local-first SQLite storage
- FastMCP-powered MCP server
- Add new expenses with categories and notes
- View expenses within custom date ranges
- Generate category-wise spending summaries
- Update existing expense records
- Remove incorrect or duplicate entries
- Configurable categories via JSON
- Automatic category reload without restart
- Simple Python codebase for customization
- Compatible with Claude Desktop and other MCP clients

---

## 📁 Project Structure

```text
expense-tracker-mcp/
├── main.py
├── expenses.db
├── categories.json
├── pyproject.toml
└── README.md
```

| File | Description |
|--------|-------------|
| `main.py` | MCP server implementation |
| `expenses.db` | SQLite database |
| `categories.json` | Expense categories and subcategories |
| `pyproject.toml` | Project dependencies |
| `README.md` | Project documentation |

---

## ⚙️ Requirements

| Requirement | Version |
|------------|---------|
| Python | 3.10+ |
| FastMCP | Latest |
| SQLite | Included with Python |

---

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/expense-tracker-mcp.git
cd expense-tracker-mcp
```

### Install Dependencies

Using uv:

```bash
uv sync
```

Or using pip:

```bash
pip install fastmcp
```

---

## ▶️ Running the Server

Using uv:

```bash
uv run main.py
```

Using Python:

```bash
python main.py
```

The SQLite database is created automatically on first startup.

---

## 🔌 Claude Desktop Integration

Add the following configuration to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "expense-tracker": {
      "command": "uv",
      "args": ["run", "main.py"],
      "cwd": "/absolute/path/to/expense-tracker-mcp"
    }
  }
}
```

Restart Claude Desktop after updating the configuration.

---

## 🛠️ Available Tools

### add_expense

Create a new expense record.

| Parameter | Type | Required |
|------------|------|----------|
| date | string | Yes |
| amount | float | Yes |
| category | string | Yes |
| subcategory | string | No |
| note | string | No |

#### Example

```text
Add an expense - cab ride to dehli last sunday fare was 500Rs.

Request

{
  "date": "2026-06-07",
  "note": "Cab ride to Delhi",
  "amount": "500",
  "category": "Transport",
  "subcategory": "Cab"
}
Response

{"status":"ok","id":1}
```

---

### list_expenses

Retrieve all expenses within a specified date range.

| Parameter | Type | Required |
|------------|------|----------|
| start_date | string | Yes |
| end_date | string | Yes |

#### Example

```text
Show my expenses of May.
```

---

### summarize

Generate category-wise spending totals.

| Parameter | Type | Required |
|------------|------|----------|
| start_date | string | Yes |
| end_date | string | Yes |
| category | string | No |

#### Example

```text
Summarize my expenses for June 2026.
```

---

### edit_expense

Update an existing expense record.

Only supplied fields are modified.

| Parameter | Type | Required |
|------------|------|----------|
| expense_id | integer | Yes |
| date | string | No |
| amount | float | No |
| category | string | No |
| subcategory | string | No |
| note | string | No |

#### Example

```text
Update expense ID 5.

Change amount to 1200 and note to "Weekly groceries".
```

---

### delete_expense

Delete an expense by ID.

| Parameter | Type | Required |
|------------|------|----------|
| expense_id | integer | Yes |

#### Example

```text
Delete expense ID 5.
```

---

## 📦 Available Resources

### expense://categories

Returns all configured categories and subcategories from `categories.json`.

This resource is loaded fresh on every request, allowing you to modify categories without restarting the server.

#### Example

```text
Show all available expense categories.
```

---

## 🏷️ Expense Categories

The server includes a structured category system designed to cover most personal and professional spending scenarios.

Each expense consists of:

- **Category** → High-level classification
- **Subcategory** → More specific spending type

### Example

```text
Category: food
Subcategory: groceries
```

### Available Categories

| Category | Examples |
|-----------|----------|
| food | groceries, dining_out, snacks |
| transport | fuel, cab_ride_hailing, tolls |
| housing | rent, furnishing, repairs |
| utilities | electricity, internet, mobile_phone |
| health | medicines, doctor_consultation |
| education | books, courses, workshops |
| entertainment | movies, games, streaming |
| shopping | clothing, electronics, accessories |
| subscriptions | SaaS, cloud services, newsletters |
| travel | flights, hotels, local_transport |
| business | hosting, ads, contractor_payments |
| investments | stocks, mutual_funds, crypto |
| personal_care | salon, cosmetics, hygiene |
| family_kids | school_fees, toys, events |
| gifts_donations | gifts, charity, festivals |
| finance_fees | brokerage, bank_charges |
| home | kitchenware, repairs, cleaning |
| pet | food, vet, grooming |
| taxes | income_tax, gst |
| misc | uncategorized, other |

### Customizing Categories

All categories are defined in:

```text
categories.json
```

You can:

- Add new categories
- Add new subcategories
- Rename existing entries
- Remove unused categories

Changes become available immediately without restarting the server.

---

## 🗄️ Database Schema

```sql
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT DEFAULT '',
    note TEXT DEFAULT ''
);
```

---

## 💬 Example Claude Prompts

### Add Expense

```text
I spent ₹450 on groceries today.
```

### List Expenses

```text
Show all expenses from 2026-06-01 to 2026-06-30.
```

### Summarize Expenses

```text
How much did I spend this month by category?
```

### Update Expense

```text
Update expense ID 3.

Change amount to ₹900 and note to "Weekly grocery shopping".
```

### Delete Expense

```text
Delete expense ID 3.
```

### View Categories

```text
What expense categories are available?
```

---

## 🧑‍💻 Development

Run the server locally:

```bash
uv run main.py
```

Database file:

```text
expenses.db
```

Category configuration:

```text
categories.json
```

The project is intentionally simple and easy to extend. New tools, resources, reports, analytics, and integrations can be added with minimal changes.

---

## 📄 License

MIT License

You are free to use, modify, and distribute this project in accordance with the license terms.
