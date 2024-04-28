from datetime import date
import dash
from dash import html, dcc, callback, Input, Output, State
# from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import csv

# Register the page
dash.register_page(__name__, name='Form', title='Form')

# Define the layout for the form
layout = dbc.Container([
    # create a form to accept the following inputs:
    # Description, Date, Expected Date, Category, Expected Cost (INR), Floor, Class/Lab No
    dbc.Row([
        dbc.Col([
            html.H3(['Enter the details of the maintenance request']),
            html.P([html.B(['Form Overview'])], className='par')
        ], width=12, className='row-titles')
    ]),
    dbc.Row([
        dbc.Col([], width=2),
        dbc.Col([
            html.Form(id='maintenance-form', children=[
                html.Label('Description'),
                dbc.Input(id='description', type='text', className='input-text',
                        #   give it a background color
                            style={'background-color': '#f0f0f0', 'color': 'black'}
                          ),  # Apply custom CSS class

                html.Label('Date'),
                dbc.Input(id='date', type='date', className='input-text'),  # Apply custom CSS class
                html.Label('Expected Date'),
                dbc.Input(id='expected_date', type='date', className='input-text'),  # Apply custom CSS class
                html.Label('Category'),
                dbc.Input(id='category', type='text', className='input-text'),  # Apply custom CSS class
                html.Label('Expected Cost (INR)'),
                dbc.Input(id='expected_cost', type='number', className='input-text'),  # Apply custom CSS class
                html.Label('Floor'),
                dbc.Input(id='floor', type='number', className='input-text'),  # Apply custom CSS class
                html.Label('Class/Lab No'),
                dbc.Input(id='class_lab', type='text', className='input-text'),  # Apply custom CSS class

                html.Br(),
                html.Button('Submit', id='submit-button', type='submit', className='my-button')
            ])
        ], width=8),
        dbc.Col([], width=2)
    ])
])

# Callback to handle form submission
@callback(
    Output('maintenance-form', 'reset'),
    [Input('submit-button', 'n_clicks')],
    [State('description', 'value'),
     State('date', 'value'),
     State('expected_date', 'value'),
     State('category', 'value'),
     State('expected_cost', 'value'),
     State('floor', 'value'),
     State('class_lab', 'value')]
)
def submit_form(n_clicks, description, date, expected_date, category, expected_cost, floor, class_lab):
    if n_clicks:
        # Append form data to a CSV file
        print("Form submitted")

        # print form data   
        print(description, date, expected_date, category, expected_cost, floor, class_lab)
        with open('./data/Building_Maintenance.csv', 'a', newline='') as csvfile:
            fieldnames = ['Description', 'Date', 'Expected Date', 'Category', 'Expected Cost (INR)', 'Floor', 'Class/Lab No', 'Bill URL', 'Is Done']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write header if file is empty
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow({
                'Description': description,
                'Date': date,
                'Expected Date': expected_date,
                'Category': category,
                'Expected Cost (INR)': expected_cost,
                'Floor': floor,
                'Class/Lab No': class_lab,
                'Bill URL': '',
                'Is Done': "No"
            })
        return True
