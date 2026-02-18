# Personal Finance Tracker API

A production-ready, asynchronous REST API built with **FastAPI** and **MongoDB**. This application provides comprehensive financial management, featuring advanced aggregations, full-text search, and ACID-compliant category management.

##  Features
- **Transaction Management**: Full CRUD for income and expenses with strict Pydantic v2 validation.
- **Advanced Filtering**: Simultaneous filtering by category, date range, type, and tags.
- **Monthly Insights**: Advanced MongoDB aggregation pipelines for detailed financial health reports.
- **Search & Discovery**: Full-text search across titles and descriptions using MongoDB Text Indexes.
- **Atomic Category Deletion**: Uses MongoDB sessions (transactions) to safely reassign transactions to "uncategorized" and log an audit trail when a category is removed.
- **Programmatic Indexing**: All database indexes are automatically verified and created on application startup.

##  Tech Stack
- **Python**: v3.13
- **Framework**: FastAPI
- **Database**: MongoDB (Motor Driver for Async support)
- **Validation**: Pydantic v2
- **Dependency Management**: Poetry

---

## Schema Design & Justifications

### 1. Transactions Collection
- **Date Storage**: Stored as native `datetime` objects to allow high-performance range queries and native aggregation operators ($month, $year).
- **Category Denormalization**: Stored as a string name. This reduces the need for `$lookup` joins in the most common "List Transactions" view, significantly improving read performance.
- **Tags**: Stored as an array of strings with a multikey index to support efficient "contains" filtering.

### 2. Categories Collection
- **Uniqueness**: The `name` field is unique to prevent logic collisions (e.g., having two "Food" categories).
- **Normalization**: Names are converted to lowercase via Pydantic validators before storage to ensure consistent querying.

---

##  Indexing Strategy
Indexes are created programmatically on startup within `db1_.py`.

| Index Key | Collection | Type | Purpose |
| :--- | :--- | :--- | :--- |
| `date: -1` | `transactions` | Single Field | Optimizes chronological listing and "latest first" views. |
| `{ category: 1, date: -1 }` | `transactions` | Compound | Speeds up category-specific filtering combined with date sorting. |
| `{ type: 1, date: -1 }` | `transactions` | Compound | Optimizes reports filtered by Income/Expense type. |
| `{ title: "text", description: "text" }` | `transactions` | Text | Powers the full-text search across financial descriptions. |
| `name: 1` | `categories` | Unique | Enforces data integrity at the database level. |

---

##  Project Structure
```text
Personal-Finance-Tracker-Api/
├── api_/                       # API Routing & Controllers
│   ├── __init__.py
│   └── api_.py                 # Endpoint definitions & Aggregation logic
├── db_/                        # Database Layer
│   ├── __init__.py
│   └── db1_.py                 # MongoDB Connection & Index Initialization
├── models/                     # Pydantic Schemas (V2)
│   ├── __init__.py
│   ├── category.py             # Category Request/Response models
│   └── transaction.py          # Transaction Request/Response models
├── .env                        # Environment Variables (MONGO_URI)
├── .gitignore                  # Git exclusion rules
├── main.py                     # App entry point & FastAPI setup
├── poetry.lock                 # Poetry dependency lock
├── pyproject.toml              # Project metadata & dependencies
└── README.md                   # Project documentation
