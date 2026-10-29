# Autonomous Text-to-SQL Agent

An educational AI agent that converts natural-language business questions into SQLite queries, executes them using read-only access, automatically retries after SQL errors, and summarizes the results. A simple Streamlit UI is included, along with an optional chart feature.

## Features

- Natural-language question to SQL using LangChain + Gemini.
- SQLite e-commerce demo database with customers, products, orders, and order items.
- Automatic SQL repair: the model receives the failed SQL and the error message and tries again (up to 3 repairs).
- Read-only SQLite connection (`mode=ro`).
- SQL validation allows only a single `SELECT` or `WITH` query and blocks common write/administrative keywords.
- Natural-language summary of returned rows.
- Bonus: bar chart when the user asks for a chart/graph and the result has suitable columns.
- Streamlit user interface.

## Architecture

1. User submits a question.
2. LangChain sends the schema and question to Gemini.
3. The agent generates a SQL query.
4. The app validates the query and executes it through a read-only SQLite connection.
5. If validation or execution fails, the error is sent back to the model for repair.
6. The result is shown in a table and summarized in plain English.
7. If requested, a bar chart is displayed.

## Requirements

- Python 3.10 or newer
- A Gemini API key
- Internet connection for model requests

## Setup

### 1. Create a virtual environment (recommended)

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the API key

Copy `.env.example` to `.env`, then replace the placeholder with your Gemini API key:

```text
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-3.8-flash
```

Do not upload `.env` or share your API key. The `.gitignore` should exclude `.env`.

### 4. Create the sample database

```bash
python setup_database.py
```

This creates `ecommerce.db` with sample records. The data is fictional and intended for coursework.

### 5. Run the app

```bash
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`.

## Example questions

- What are the top 5 customers by total spending?
- What is the total revenue from completed orders?
- Show monthly revenue.
- Which products have the most units sold?
- Make a bar chart of revenue by product category.

The sample data contains October 2026 dates. The result depends on the generated query and the definition of revenue used. For this demo, revenue should generally be calculated as `order_items.quantity * order_items.unit_price`, joined to `orders`, and filtered to `orders.status = 'completed'` when asking for completed-order revenue.

## Self-correction logic

The app catches SQL validation and database execution errors. It sends the previous SQL and error message to Gemini and asks for a corrected query. It retries up to three times after the first attempt. If all attempts fail, the app displays an error instead of crashing the Streamlit process.

To demonstrate this during a presentation, temporarily change a column name in the SQL-generation prompt or ask a question likely to trigger an incorrect column; then show the self-correction log if the model produces and repairs a failed query. Model behavior is not deterministic, so an error may not occur every time.

## Read-only safeguards

The database is opened with SQLite URI `mode=ro`, which prevents writes through that connection. The app also validates SQL before execution:
- Only one statement is allowed.
- Only `SELECT` or `WITH` queries are allowed.
- Common write and administrative keywords are blocked.
- Results are capped to 200 rows in the UI.
- A SQLite progress handler interrupts some overly expensive queries.

This is a coursework demonstration, not a complete production security boundary. For production, use a database account with read-only permissions, stronger SQL parsing/allow-listing, query timeouts and resource limits, and monitoring. Never connect an LLM agent to a sensitive production database without a security review.

## Project structure

```text
text_to_sql_agent/
├── app.py
├── setup_database.py
├── requirements.txt
├── .env.example
├── README.md
└── ecommerce.db   # created by setup_database.py; don't need to commit if you prefer
```

## Troubleshooting

### `GEMINI_API_KEY is missing`
Create `.env` from `.env.example` and add your API key. Restart Streamlit afterward.

### Model not found / unavailable
Set `GEMINI_MODEL` in `.env` to a model currently available to your Gemini API account. Model availability can vary by account and change over time.

### `Database not found`
Run `python setup_database.py` from the project directory.

### SQL query fails
Check the SQL and the self-correction log. The agent may need a clearer question or a prompt adjustment. The repair limit is intentionally finite to avoid an endless loop.

## Suggested evaluation

Test at least 10 questions. For each question, record:
- Expected answer or SQL result
- Generated SQL
- Whether the query executed
- Whether self-correction was needed
- Whether the final summary matched the result

Include a short table of these tests in your submission/report.

## Limitations

- LLM-generated SQL can be incorrect even when it executes.
- Natural-language date expressions such as “last Friday” need careful date interpretation; specify an exact date for reproducible tests.
- The chart feature uses a simple heuristic to choose a label column and numeric column.
- The app uses fictional demo data and should not be treated as a real business analytics system.
