# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
# extra lauch counts added
launch_counts = spacex_df.groupby('Launch Site').size().reset_index(name='Total Launches')
spacex_df = spacex_df.merge(launch_counts, on='Launch Site')
# Create Dash app
app = dash.Dash(__name__)

# -------------------------
# App Layout
# -------------------------
app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
    ),

    # TASK 1: Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    html.Br(),

    # TASK 2: Pie chart
    dcc.Graph(id='success-pie-chart'),

    html.Br(),

    html.P("Payload range (Kg):"),
dcc.RangeSlider(
    id='payload-slider',
    min=min_payload,
    max=max_payload,
    step=100,
    marks={
        0: '0',
        2500: '2500',
        5000: '5000',
        7500: '7500',
        10000: '10000'
    },
    value=[min_payload, max_payload]
),
    # Placeholder for Task 3 (to add later)
    # dcc.RangeSlider(...),

    # Placeholder for Task 4
    dcc.Graph(id='success-payload-scatter-chart')
])

# -------------------------
# TASK 2: Pie chart callback
# -------------------------
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Site',
            hover_data=['Total Launches']
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs Failure for site {entered_site}',
            color='class',
            color_discrete_map={
                1: 'green',
                0: 'red'
            }
        )
    return fig

        # return the outcomes piechart for a selected site
                                #html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)




                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                #html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                #])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)

def update_scatter(site, payload_range):
    low, high = payload_range


# Filter by payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    # Filter by site if needed
    if site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == site]

    # Create scatter plot
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload vs Launch Success'
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
