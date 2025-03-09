# U.S. Employment Insights Dashboard (2021)

This project provides an interactive dashboard to explore U.S. employment data for the year 2021, sourced from the County Business Patterns (CBP) dataset. The dashboard visualizes key metrics such as the number of establishments, number of employees, and annual payroll, broken down by employment size and legal form of organization (LFO).

## Features

- **Visualizations**:
  - **Establishments by Employment Size**: A bar chart showing the number of establishments across different employment size categories (e.g., "<5", "5-9", ..., "1,000+").
  - **Payroll Distribution by Legal Form**: A pie chart displaying the distribution of annual payroll across different legal forms (e.g., C-Corporations, S-Corporations).
  - **Employees by Employment Size**: A bar chart illustrating the number of employees in each employment size category.
  - **Establishments by Legal Form**: A pie chart showing the distribution of establishments by legal form.
  - **Payroll by Employment Size and Legal Form**: A stacked bar chart detailing annual payroll across employment sizes, segmented by legal form.

- **Data Adjustments**:
  - Excludes the "All establishments" category from bar and stacked bar charts to focus on specific size ranges.
  - Converts payroll data from thousands of dollars to actual dollars for clarity (e.g., "Annual Payroll ($)" instead of "Annual Payroll ($1,000)").
  - Uses shortened labels for better readability (e.g., "C-Corporations" instead of "C-corporations and other corporate legal forms of organization").
  - Fixes Y-axis ordering in bar charts to ensure values increase from bottom to top with proportional spacing.

- **Styling**:
  - Uses the `plotly_white` template for a light background, improving readability.
  - Ensures high-contrast text (black) for titles, labels, and legends.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>