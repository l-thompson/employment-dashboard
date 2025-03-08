# Employment Dashboard
An interactive web dashboard visualizing U.S. employment data from the 2021 County Business Patterns.

## Overview
- **Objective**: Explore establishment counts and payroll by employment size and legal form.
- **Data**: U.S. Census Bureau County Business Patterns (2021).
- **Tools**: Python, Flask, pandas, Plotly.

## Features
- Bar chart: Number of establishments by employment size.
- Pie chart: Annual payroll distribution by legal form.

## Setup
1. Clone the repo: `git clone https://github.com/yourusername/employment-dashboard`
2. Install dependencies: `pip install flask pandas plotly`
3. Run the app: `python app.py`
4. Visit `http://127.0.0.1:5000` in your browser.

## Files
- `app.py`: Flask application.
- `templates/index.html`: HTML template for the dashboard.
- `cbp_2021.csv`: Dataset (source: U.S. Census Bureau).