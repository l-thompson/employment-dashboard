from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Load and process the data
def load_data():
    df = pd.read_csv('cbp_2021.csv')
    # Filter for "All establishments" under LFO to avoid double-counting by LFO
    df_all = df[df['Meaning of Legal form of organization code (LFO_LABEL)'] == 'All establishments']
    return df_all

# Generate Plotly charts
def create_charts(df):
    # Bar chart: Number of establishments by employment size (all sectors)
    bar_fig = px.bar(
        df[df['2017 NAICS code (NAICS2017)'] == '00'],
        x='Meaning of Employment size of establishments code (EMPSZES_LABEL)',
        y='Number of establishments (ESTAB)',
        title='Number of Establishments by Employment Size (2021)',
        labels={'Number of establishments (ESTAB)': 'Establishments', 
                'Meaning of Employment size of establishments code (EMPSZES_LABEL)': 'Employment Size'},
        height=400
    )
    bar_fig.update_layout(xaxis={'tickangle': 45})

    # Pie chart: Total annual payroll by legal form (all sectors, all sizes)
    lfo_df = df[df['Meaning of Employment size of establishments code (EMPSZES_LABEL)'] == 'All establishments']
    pie_fig = px.pie(
        lfo_df[lfo_df['2017 NAICS code (NAICS2017)'] == '00'],
        values='Annual payroll ($1,000) (PAYANN)',
        names='Meaning of Legal form of organization code (LFO_LABEL)',
        title='Annual Payroll Distribution by Legal Form (2021)',
        height=400
    )

    # Convert figures to HTML
    bar_html = pio.to_html(bar_fig, full_html=False)
    pie_html = pio.to_html(pie_fig, full_html=False)
    return bar_html, pie_html

@app.route('/')
def dashboard():
    df = load_data()
    bar_chart, pie_chart = create_charts(df)
    return render_template('index.html', bar_chart=bar_chart, pie_chart=pie_chart)

if __name__ == '__main__':
    app.run(debug=True)