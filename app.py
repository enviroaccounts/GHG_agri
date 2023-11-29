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

import numpy as np

def create_ghg_emissions_pie_chart(labels, values):
    """Creates a pie chart for GHG emissions data."""

    # Calculate percentages and create custom text labels
    total = sum(values)
    percents = [(v / total * 100) for v in values]
    custom_text = [f"<1%" if 0 < p < 1 else f"{p:.0f}%" for p in percents]

    pie_chart = go.Pie(
        labels=labels,
        values=values,
        textinfo='label+percent',
        hoverinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>%{percent:.0%}<br>Total: %{value}<extra></extra>',
        texttemplate=custom_text  # Use custom text labels
    )

    fig = go.Figure(data=[pie_chart])
    fig.update_layout(
        title={
            'text': "GHG emissions from the agriculture sector by industry",
            'y': 0.08,  # Adjust the vertical position
            'x': 0.5,  # Center the title horizontally
            'xanchor': 'center',
            'yanchor': 'bottom'
        }
    )

    return fig


def setup_ghg_emissions_layout(app, fig_pie_chart):
    """Sets up the layout of the Dash app for GHG emissions visualization."""
    app.layout = html.Div(children=[
        html.Div([
            dcc.Graph(id='ghg-emissions-pie-chart', figure=fig_pie_chart)
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
