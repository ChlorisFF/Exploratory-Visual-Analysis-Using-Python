import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px

EU_df = pd.read_csv('EU_Electricity_df.csv')

electricity_columns = [
    'biofuel_electricity', 'coal_electricity', 'fossil_electricity',
    'gas_electricity', 'hydro_electricity', 'low_carbon_electricity',
    'nuclear_electricity', 'oil_electricity', 'other_renewable_electricity',
    'renewables_electricity', 'solar_electricity', 'wind_electricity'
]

percentage_columns = [f'{col}_percentage' for col in electricity_columns]

renewable_sources = ['solar_electricity', 'wind_electricity', 'hydro_electricity']

def create_pie_chart(df, selected_country):
    filtered_df = df[df['country'] == selected_country]
    electricity_percentages = filtered_df[percentage_columns].mean()

    fig = px.pie(
        names=electricity_percentages.index.str.replace('_percentage', ''),
        values=electricity_percentages.values,
        title=f'Electricity Generation Distribution in {selected_country}'
    )

    fig.update_layout(
        legend=dict(
            itemclick=False,
            itemdoubleclick=False
        )
    )

    return fig

def create_line_plot(df, selected_country, selected_electricity_type):
    filtered_df = df[df['country'] == selected_country]

    fig = px.line(
        filtered_df,
        x='year',
        y=selected_electricity_type,
        title=f'{selected_electricity_type.replace("_", " ").title()} Trends in {selected_country}',
        labels={'value': 'Electricity Generation (TWh)', 'variable': 'Electricity Type'}
    )

    return fig

def calculate_percentages(df):
    df = df.copy()
    df[electricity_columns] = df[electricity_columns].fillna(0)
    df['total_electricity'] = df[electricity_columns].sum(axis=1)

    for col in electricity_columns:
        df[f'{col}_percentage'] = (df[col] / df['total_electricity']) * 100

    return df

def create_bar_plot(df, selected_year, selected_electricity_type, selected_countries):
    filtered_df = df[df['year'] == selected_year]
    filtered_df = filtered_df[filtered_df['country'].isin(selected_countries)]

    data = []
    for country in selected_countries:
        country_data = filtered_df[filtered_df['country'] == country]
        if not country_data.empty:  # Check if country_data is not empty
            data.append(go.Bar(
                x=[country],
                y=[country_data[selected_electricity_type].values[0]],
                name=country
            ))

    layout = go.Layout(
        title=f'{selected_electricity_type.replace("_", " ").title()} Generation in {selected_year}',
        xaxis=dict(title='Country'),
        yaxis=dict(title='Electricity Generation (TWh)'),
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    return fig

def Run_energy_dashboard_app(EU_df):
    df = calculate_percentages(EU_df)

    app = dash.Dash(__name__)

    countries = df['country'].unique()
    years = df['year'].unique()

    app.layout = html.Div([
        html.H1("Energy Consumption Analytics Dashboard"),

        html.Div([
            html.H2("Electricity Generation Distribution"),
            dcc.Dropdown(
                id='distribution-country-dropdown',
                options=[{'label': country, 'value': country} for country in countries],
                value=countries[0],
                multi=False
            ),
            dcc.Graph(id='electricity-pie-chart'),
        ]),

        html.Div([
            html.H2("Electricity Generation Trends"),
            html.Label("Select Country"),
            dcc.Dropdown(
                id='trends-country-dropdown',
                options=[{'label': country, 'value': country} for country in countries],
                value=countries[0],  # Default value
                multi=False,
                placeholder="Select a country"
            ),
            html.Label("Select Electricity Type"),
            dcc.Dropdown(
                id='electricity-type-dropdown',
                options=[{'label': col.replace('_', ' ').title(), 'value': col} for col in electricity_columns],
                value=electricity_columns[0],
                multi=False,
                placeholder="Select an electricity type"
            ),
            dcc.Graph(id='electricity-line-chart'),
        ]),

        html.Div([
            html.H2("Electricity Generation Comparison"),
            html.Label("Select Year"),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': year, 'value': year} for year in years],
                value=years[0],
                multi=False,
                placeholder="Select a year"
            ),
            html.Label("Select Electricity Type"),
            dcc.Dropdown(
                id='electricity-bar-type-dropdown',
                options=[{'label': col.replace('_', ' ').title(), 'value': col} for col in electricity_columns],
                value=electricity_columns[0],
                multi=False,
                placeholder="Select an electricity type"
            ),
            html.Label("Select Countries"),
            dcc.Dropdown(
                id='bar-countries-dropdown',
                options=[{'label': country, 'value': country} for country in countries],
                value=['Germany', 'France', 'Italy', 'Spain', 'United Kingdom'],
                multi=True,
                placeholder="Select countries"
            ),
            dcc.Graph(id='electricity-bar-plot'),
        ]),

        html.H2("Electricity Generation Comparison"),
        html.Div([
            html.Label("Renewable Energy Production by Source over Time"),
            dcc.Dropdown(
                id='renewable-source-dropdown',
                options=[{'label': source.replace('_', ' ').title(), 'value': source} for source in renewable_sources],
                value=renewable_sources[0],
                multi=False,
                placeholder="Select a renewable energy source"
            ),
            dcc.Graph(id='energy-scatter-plot'),
        ]),

    ])

    @app.callback(
        Output('electricity-pie-chart', 'figure'),
        [Input('distribution-country-dropdown', 'value')]
    )
    def update_distribution_chart(selected_country):
        return create_pie_chart(df, selected_country)

    @app.callback(
        Output('electricity-line-chart', 'figure'),
        [Input('trends-country-dropdown', 'value'),
         Input('electricity-type-dropdown', 'value')]
    )
    def update_trends_chart(selected_country, selected_electricity_type):
        return create_line_plot(df, selected_country, selected_electricity_type)

    @app.callback(
        Output('electricity-bar-plot', 'figure'),
        [Input('year-dropdown', 'value'),
         Input('electricity-bar-type-dropdown', 'value'),
         Input('bar-countries-dropdown', 'value')]
    )
    def update_bar_plot(selected_year, selected_electricity_type, selected_countries):
        return create_bar_plot(df, selected_year, selected_electricity_type, selected_countries)

    @app.callback(
        Output('energy-scatter-plot', 'figure'),
        [Input('renewable-source-dropdown', 'value')]
    )
    def update_scatter_plot(selected_source):
        # Create the scatter plot
        fig = px.scatter(EU_df, x='year', y=selected_source,
                         title=f'Renewable Energy Production ({selected_source.replace("_", " ").title()}) over Time',
                         labels={'year': 'Year', selected_source: 'Energy Production'},
                         hover_data={'year': True, selected_source: True})

        return fig

    if __name__ == '__main__':
        app.run_server(debug=True)


Run_energy_dashboard_app(EU_df)
