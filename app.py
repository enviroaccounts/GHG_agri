from dash import Dash, html, dcc
import pandas as pd
import plotly.graph_objects as go

def load_ghg_emissions_data():
    """Loads greenhouse gas emissions data."""
    return pd.read_csv("static/data/GHG_emissions_Agri_Industry.csv")

def prepare_ghg_emissions_chart_data(data_df):
    """Prepares data for the GHG emissions pie chart."""
    # GHG emissions data start from the 'Total fertiliser emissions' column
    ghg_emissions_data = data_df.iloc[0, 2:-1]
    labels = ghg_emissions_data.index.tolist()
    values = []
    for value in ghg_emissions_data.values:
        if isinstance(value, str):
            value = float(value.replace(',', '').strip())
        values.append(value)
    return labels, values

def create_ghg_emissions_pie_chart(labels, values):
    """Creates a pie chart for GHG emissions data."""
    return go.Figure(data=[go.Pie(labels=labels, values=values)])

def setup_ghg_emissions_layout(app, fig_pie_chart):
    """Sets up the layout of the Dash app for GHG emissions visualization."""
    app.layout = html.Div(children=[
        html.Div([
            dcc.Graph(id='ghg-emissions-pie-chart', figure=fig_pie_chart)
        ]),
        html.Div([  
            html.H3(id='ghg-emissions-pie-chart-description', children='GHG Emissions from the Agriculture Sector by Industry.')
        ])
    ], id='ghg-emissions-pie-chart-layout')

def create_app():
    """Creates and configures the Dash app."""
    app = Dash(__name__)

    # Load and prepare data
    data_df = load_ghg_emissions_data()
    labels, values = prepare_ghg_emissions_chart_data(data_df)

    # Create pie chart
    fig_pie_chart = create_ghg_emissions_pie_chart(labels, values)

    # Setup layout
    setup_ghg_emissions_layout(app, fig_pie_chart)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run_server(debug=True, host='0.0.0.0', port=8050)
