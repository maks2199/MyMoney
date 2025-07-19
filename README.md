# MyMoney

MyMoney is a personal finance analytics tool for visualizing and analyzing your expenses. It supports importing bank transaction data, categorizing expenses, and displaying interactive charts.

The app is working with the data from T-Bank for now, but can be expandable.

![](docs/screen1.jpg)

## Features

- Import transactions from Excel or CSV files
- Categorize and group expenses
- Interactive dashboards with Streamlit and Plotly
- Planned vs actual expense tracking
- Database integration (MySQL, Directus)

## Getting Started

### Backend (Python)

1. Install dependencies:
   ```sh
   pip install streamlit pandas altair plotly mysql-connector-python python-dotenv
   ```
2. Run the Streamlit app:
   ```sh
   streamlit run main.py
   ```

## Configuration

- Expense categories: [`configs/mapCategories.json`](configs/mapCategories.json)
- Planned expenses: [`configs/plannedExpenses.json`](configs/plannedExpenses.json)
- Excluded categories: [`configs/excludedCategories.json`](configs/excludedCategories.json)

## Import to Directus

To sync transactions with Directus, configure `.env` and run:

```sh
python import_to_directus.py
```
