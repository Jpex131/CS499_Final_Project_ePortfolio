import base64
import pandas as pd
from jupyter_plotly_dash import JupyterDash
from dash import dcc, html, dash_table as dt, Input, Output
import dash_leaflet as dl
from CRUDmodule import AnimalShelter  # Ensure this is updated with enhancements

# Initialize AnimalShelter instance
username = "yourUsername"  # Update with actual username
password = "yourPassword"  # Update with actual password
shelter = AnimalShelter(username, password)

# Encode Grazioso Salvare’s logo image
image_filename = 'Grazioso_Salvare_Logo.png'  # Make sure this file is in your directory
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode()

app = JupyterDash('AnimalShelter')

# Dashboard Layout
app.layout = html.Div([
    html.Div([
        html.Center(html.B(html.H1('Grazioso Salvare Dashboard'))),
        html.Center(html.Img(src=f'data:image/png;base64,{encoded_image}', style={'height':'10%', 'width':'10%'})),
    ]),
    html.Hr(),
    html.Div([
        html.Label("Filter Options"),
        dcc.Dropdown(
            id='filter-dropdown',
            options=[
                {'label': 'Water Rescue', 'value': 'water'},
                {'label': 'Mountain/Wilderness Rescue', 'value': 'mountain'},
                {'label': 'Disaster Rescue', 'value': 'disaster'},
                {'label': 'Custom Query', 'value': 'custom'},
            ],
            value='water',  # Default value
        ),
        dcc.Textarea(
            id='custom-query-input',
            placeholder='Enter your custom MongoDB query here...',
            style={'width': '100%', 'height': 100, 'display': 'none'},
        ),
    ]),
    html.Hr(),
    dt.DataTable(
        id='datatable',
        columns=[],  # Columns will be dynamically generated based on the data
        style_table={'height': '400px', 'overflowY': 'auto'},
        page_size=10,
    ),
    html.Hr(),
    html.Div(id='geospatial-visualization-container', children=[
        dl.Map(
            center=[39.50, -98.35],  # Center of the map (e.g., central USA)
            zoom=4,
            children=[dl.TileLayer()],
            style={'width': '1000px', 'height': '500px'},
            id='geospatial-visualization',
        ),
    ]),
])

@app.callback(
    Output('custom-query-input', 'style'),
    [Input('filter-dropdown', 'value')]
)
def show_hide_custom_query_input(value):
    if value == 'custom':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    [Output('datatable', 'data'), Output('datatable', 'columns')],
    [Input('filter-dropdown', 'value'), Input('custom-query-input', 'value')]
)
def update_datatable(filter_value, custom_query):
    if filter_value == 'custom' and custom_query:
        # Assuming custom_query is a string representation of a MongoDB query dictionary
        try:
            query = eval(custom_query)  # WARNING: Using eval() is generally unsafe
            data = list(shelter.read(query))
        except Exception as e:
            return [], [{"name": "Error", "id": "error"}]
    else:
        # Implement predefined queries based on filter_value
        data = []  # Placeholder for data fetched based on predefined filters
    df = pd.DataFrame(data)
    columns = [{"name": i, "id": i} for i in df.columns]
    return df.to_dict('records'), columns

@app.callback(
    Output('geospatial-visualization', 'children'),
    [Input('datatable', 'data')]
)
def update_geospatial_visualization(rows):
    markers = [
        dl.Marker(position=[row['location_lat'], row['location_long']], children=[
            dl.Tooltip(row['name']),  # Assuming 'name' is a key in your data
            dl.Popup([
                html.H6(row['name']),
                html.P(f"Additional details here")
            ])
        ])
        for row in rows if 'location_lat' in row and 'location_long' in row
    ]
    return [dl.TileLayer()] + markers
S
# Add more logic as needed for complete functionality

if __name__ == '__main__':
    app.run_server(debug=True)
