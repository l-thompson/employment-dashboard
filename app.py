from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)

# Load and process the data
def load_data():
    df = pd.read_csv('cbp_2021.csv')
    # Convert numeric columns, handling commas
    df['Annual payroll ($1,000) (PAYANN)'] = pd.to_numeric(df['Annual payroll ($1,000) (PAYANN)'].str.replace(',', ''), errors='coerce')
    df['Number of establishments (ESTAB)'] = pd.to_numeric(df['Number of establishments (ESTAB)'].str.replace(',', ''), errors='coerce')
    df['Number of employees (EMP)'] = pd.to_numeric(df['Number of employees (EMP)'].str.replace(',', ''), errors='coerce')
    # Convert payroll to actual dollars
    df['Annual payroll ($) (PAYANN)'] = df['Annual payroll ($1,000) (PAYANN)'] * 1000
    # Filter for "All establishments" under LFO for size breakdowns
    df_all = df[df['Meaning of Legal form of organization code (LFO_LABEL)'] == 'All establishments']
    return df_all, df

# Mapping for shorter LFO labels
LFO_LABEL_MAPPING = {
    'C-corporations and other corporate legal forms of organization': 'C-Corporations',
    'S-corporations': 'S-Corporations',
    'Individual proprietorships': 'Individual Proprietorships',
    'Partnerships': 'Partnerships',
    'Non-profit': 'Non-Profit',
    'Government': 'Government',
    'Other noncorporate legal forms of organization': 'Other Noncorporate'
}

# Mapping for shorter employment size labels
EMPSZES_LABEL_MAPPING = {
    'All establishments': 'All',
    'Establishments with less than 5 employees': '<5',
    'Establishments with 5 to 9 employees': '5-9',
    'Establishments with 10 to 19 employees': '10-19',
    'Establishments with 20 to 49 employees': '20-49',
    'Establishments with 50 to 99 employees': '50-99',
    'Establishments with 100 to 249 employees': '100-249',
    'Establishments with 250 to 499 employees': '250-499',
    'Establishments with 500 to 999 employees': '500-999',
    'Establishments with 1,000 employees or more': '1,000+'
}

# Generate Plotly charts
def create_charts(df_all, df_full):
    # 1. Bar Chart: Number of establishments by employment size
    bar_estab_df = df_all[df_all['2017 NAICS code (NAICS2017)'] == '00'].copy()
    bar_estab_df = bar_estab_df[bar_estab_df['Meaning of Employment size of establishments code (EMPSZES_LABEL)'] != 'All establishments']
    bar_estab_df['Meaning of Employment size of establishments code (EMPSZES_LABEL)'] = bar_estab_df['Meaning of Employment size of establishments code (EMPSZES_LABEL)'].map(EMPSZES_LABEL_MAPPING)
    bar_estab_fig = px.bar(
        bar_estab_df,
        x='Meaning of Employment size of establishments code (EMPSZES_LABEL)',
        y='Number of establishments (ESTAB)',
        title='Establishments by Employment Size (2021)',
        labels={'Number of establishments (ESTAB)': 'Establishments', 
                'Meaning of Employment size of establishments code (EMPSZES_LABEL)': 'Employment Size'},
        height=400,
        color_discrete_sequence=['#1f77b4'],
        template='plotly_white'  # Use light theme
    )
    bar_estab_fig.update_layout(
        xaxis={'tickangle': 45, 'categoryorder': 'array', 'categoryarray': ['<5', '5-9', '10-19', '20-49', '50-99', '100-249', '250-499', '500-999', '1,000+']},
        yaxis={'autorange': True, 'type': 'linear', 'range': [0, bar_estab_df['Number of establishments (ESTAB)'].max() * 1.1]},
        margin=dict(t=50, b=50, l=50, r=50),
        font=dict(color='black')  # Ensure text is dark for contrast
    )

    # 2. Pie Chart: Annual payroll by legal form
    lfo_payroll_df = df_full[
        (df_full['2017 NAICS code (NAICS2017)'] == '00') &
        (df_full['Meaning of Legal form of organization code (LFO_LABEL)'] != 'All establishments')
    ].groupby('Meaning of Legal form of organization code (LFO_LABEL)')['Annual payroll ($) (PAYANN)'].sum().reset_index()
    lfo_payroll_df['Meaning of Legal form of organization code (LFO_LABEL)'] = lfo_payroll_df['Meaning of Legal form of organization code (LFO_LABEL)'].map(LFO_LABEL_MAPPING)
    pie_payroll_fig = px.pie(
        lfo_payroll_df,
        values='Annual payroll ($) (PAYANN)',
        names='Meaning of Legal form of organization code (LFO_LABEL)',
        title='Payroll Distribution by Legal Form (2021)',
        height=400,
        color_discrete_sequence=px.colors.qualitative.Set2,
        template='plotly_white'  # Use light theme
    )
    pie_payroll_fig.update_traces(textposition='inside', textinfo='percent+label')
    pie_payroll_fig.update_layout(font=dict(color='black'))  # Ensure text is dark for contrast

    # 3. Bar Chart: Number of employees by employment size
    bar_emp_df = df_all[df_all['2017 NAICS code (NAICS2017)'] == '00'].copy()
    bar_emp_df = bar_emp_df[bar_emp_df['Meaning of Employment size of establishments code (EMPSZES_LABEL)'] != 'All establishments']
    bar_emp_df['Meaning of Employment size of establishments code (EMPSZES_LABEL)'] = bar_emp_df['Meaning of Employment size of establishments code (EMPSZES_LABEL)'].map(EMPSZES_LABEL_MAPPING)
    bar_emp_fig = px.bar(
        bar_emp_df,
        x='Meaning of Employment size of establishments code (EMPSZES_LABEL)',
        y='Number of employees (EMP)',
        title='Employees by Employment Size (2021)',
        labels={'Number of employees (EMP)': 'Employees', 
                'Meaning of Employment size of establishments code (EMPSZES_LABEL)': 'Employment Size'},
        height=400,
        color_discrete_sequence=['#ff7f0e'],
        template='plotly_white'  # Use light theme
    )
    bar_emp_fig.update_layout(
        xaxis={'tickangle': 45, 'categoryorder': 'array', 'categoryarray': ['<5', '5-9', '10-19', '20-49', '50-99', '100-249', '250-499', '500-999', '1,000+']},
        yaxis={'autorange': True, 'type': 'linear', 'range': [0, bar_emp_df['Number of employees (EMP)'].max() * 1.1]},
        margin=dict(t=50, b=50, l=50, r=50),
        font=dict(color='black')  # Ensure text is dark for contrast
    )

    # 4. Pie Chart: Number of establishments by legal form
    lfo_estab_df = df_full[
        (df_full['2017 NAICS code (NAICS2017)'] == '00') &
        (df_full['Meaning of Legal form of organization code (LFO_LABEL)'] != 'All establishments')
    ].groupby('Meaning of Legal form of organization code (LFO_LABEL)')['Number of establishments (ESTAB)'].sum().reset_index()
    lfo_estab_df['Meaning of Legal form of organization code (LFO_LABEL)'] = lfo_estab_df['Meaning of Legal form of organization code (LFO_LABEL)'].map(LFO_LABEL_MAPPING)
    pie_estab_fig = px.pie(
        lfo_estab_df,
        values='Number of establishments (ESTAB)',
        names='Meaning of Legal form of organization code (LFO_LABEL)',
        title='Establishments by Legal Form (2021)',
        height=400,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        template='plotly_white'  # Use light theme
    )
    pie_estab_fig.update_traces(textposition='inside', textinfo='percent+label')
    pie_estab_fig.update_layout(font=dict(color='black'))  # Ensure text is dark for contrast

    # 5. Stacked Bar Chart: Annual payroll by employment size and LFO
    stacked_df = df_full[
        (df_full['2017 NAICS code (NAICS2017)'] == '00') &
        (df_full['Meaning of Legal form of organization code (LFO_LABEL)'] != 'All establishments') &
        (df_full['Meaning of Employment size of establishments code (EMPSZES_LABEL)'] != 'All establishments')
    ].copy()
    stacked_df['Meaning of Legal form of organization code (LFO_LABEL)'] = stacked_df['Meaning of Legal form of organization code (LFO_LABEL)'].map(LFO_LABEL_MAPPING)
    stacked_df['Meaning of Employment size of establishments code (EMPSZES_LABEL)'] = stacked_df['Meaning of Employment size of establishments code (EMPSZES_LABEL)'].map(EMPSZES_LABEL_MAPPING)
    stacked_fig = px.bar(
        stacked_df,
        x='Meaning of Employment size of establishments code (EMPSZES_LABEL)',
        y='Annual payroll ($) (PAYANN)',
        color='Meaning of Legal form of organization code (LFO_LABEL)',
        title='Payroll by Employment Size and Legal Form (2021)',
        labels={'Annual payroll ($) (PAYANN)': 'Annual Payroll ($)', 
                'Meaning of Employment size of establishments code (EMPSZES_LABEL)': 'Employment Size'},
        height=500,
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.D3,
        template='plotly_white'  # Use light theme
    )
    stacked_fig.update_layout(
        xaxis={'tickangle': 45, 'categoryorder': 'array', 'categoryarray': ['<5', '5-9', '10-19', '20-49', '50-99', '100-249', '250-499', '500-999', '1,000+']},
        yaxis={'autorange': True, 'type': 'linear'},
        margin=dict(t=50, b=50, l=50, r=50),
        font=dict(color='black')  # Ensure text is dark for contrast
    )

    # Convert to HTML
    return (
        pio.to_html(bar_estab_fig, full_html=False),
        pio.to_html(pie_payroll_fig, full_html=False),
        pio.to_html(bar_emp_fig, full_html=False),
        pio.to_html(pie_estab_fig, full_html=False),
        pio.to_html(stacked_fig, full_html=False)
    )

@app.route('/')
def dashboard():
    df_all, df_full = load_data()
    bar_estab, pie_payroll, bar_emp, pie_estab, stacked_payroll = create_charts(df_all, df_full)
    return render_template(
        'index.html',
        bar_estab=bar_estab,
        pie_payroll=pie_payroll,
        bar_emp=bar_emp,
        pie_estab=pie_estab,
        stacked_payroll=stacked_payroll
    )

if __name__ == '__main__':
    app.run(debug=False, port=5000)