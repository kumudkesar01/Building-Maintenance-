from datetime import date
import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import csv
import requests
import base64


dash.register_page(__name__, name='Project Management', title='Form')

def get_descriptions():
    descriptions = []
    with open('./data/Building_Maintenance.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            descriptions.append(row['Description'])
    return descriptions

def get_bill_url(description):
    with open('./data/Building_Maintenance.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Description'] == description:
                return row['Bill URL']
    return []

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3(['Project Management']),
            dbc.Row([
                dbc.Col([
                    html.Button('Create Project', id='create-project-btn', className='my-button'),
                ],
                  ),
                dbc.Col([
                    html.Button('Edit Project', id='edit-project-btn', className='my-button'),
                ], ),
                dbc.Col([
                    html.Button('Bill View/Upload', id='bill-upload-btn', className='my-button'),
                ], ),
            ],
            justify='center',
            ),
            html.Div(id='update-success-message') ,
            html.Div(id='content-section')
        ])
    ],
    ),
],

style={
    "margin-left": "5rem",
    "margin-right": "5rem",
    "width": "90%"
}
)

@callback(
    Output('content-section', 'children'),
    [Input('create-project-btn', 'n_clicks'),
     Input('edit-project-btn', 'n_clicks'),
     Input('bill-upload-btn', 'n_clicks')]
)
def update_content(create_clicks, edit_clicks, bill_clicks):
    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'create-project-btn':
            return create_project_form()
        elif button_id == 'edit-project-btn':
            return edit_project_form()
        elif button_id == 'bill-upload-btn':
            return bill_upload_section()

def create_project_form():
    return html.Form(id='maintenance-form', children=[
                html.Label('Description'),
                dbc.Input(id='description', type='text', className='input-text',
                            style={'background-color': '#f0f0f0', 'color': 'black'}
                          ),
                html.Label('Date'),
                dbc.Input(id='date', type='date', className='input-text'),
                html.Label('Expected Date'),
                dbc.Input(id='expected_date', type='date', className='input-text'),
                html.Label('Category'),
                dbc.Input(id='category', type='text', className='input-text'),
                html.Label('Expected Cost (INR)'),
                dbc.Input(id='expected_cost', type='number', className='input-text'),
                html.Label('Floor'),
                dbc.Input(id='floor', type='number', className='input-text'),
                html.Label('Class/Lab No'),
                dbc.Input(id='class_lab', type='text', className='input-text'),

                html.Br(),
                html.Button('Submit', id='submit-button', type='submit', className='my-button')
            ])

def edit_project_form():
    return html.Div([
        html.Label('Select Description'),
        dcc.Dropdown(
            id='description-dropdown',
            options=[{'label': desc, 'value': desc} for desc in get_descriptions()],
            value=get_descriptions()[0],
            className='input-text'
        ),
        html.Div(id='edit-form-content'),
        html.Br(),
    ])

@callback(
    Output('edit-form-content', 'children'),
    [Input('description-dropdown', 'value')]
)
def load_edit_form_data(description):
    if description:
        with open('./data/Building_Maintenance.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Description'] == description:
                    return create_project_form_with_data(row)

def create_project_form_with_data(data):
    return html.Div([
        html.Form(id='maintenance-form-update', children=[
             html.Label('Description'),
        dbc.Input(id='description', type='text', value=data['Description'], className='input-text', style={'background-color': '#f0f0f0', 'color': 'black'}),  
        html.Label('Date'),
        dbc.Input(id='date', type='date', value=data['Date'], className='input-text'),  
        html.Label('Expected Date'),
        dbc.Input(id='expected_date', type='date', value=data['Expected Date'], className='input-text'),  
        html.Label('Category'),
        dbc.Input(id='category', type='text', value=data['Category'], className='input-text'),  
        html.Label('Expected Cost (INR)'),
        dbc.Input(id='expected_cost', type='number', value=data['Expected Cost (INR)'], className='input-text'),  
        html.Label('Floor'),
        dbc.Input(id='floor', type='number', value=data['Floor'], className='input-text'),  
        html.Label('Class/Lab No'),
        dbc.Input(id='class_lab', type='text', value=data['Class/Lab No'], className='input-text'),  
        html.Br(),
        html.Button('Update', id='update-button', type='submit', className='my-button', style={'font-size': '16px', 'padding': '10px 20px'}),
        ])
    ])


@callback(
    [Output('maintenance-form-update', 'reset'),
     Output('update-success-message', 'children')],
    [Input('update-button', 'n_clicks')],
    [State('description', 'value'),
     State('date', 'value'),
     State('expected_date', 'value'),
     State('category', 'value'),
     State('expected_cost', 'value'),
     State('floor', 'value'),
     State('class_lab', 'value')]
)
def update_form(n_clicks, description, date, expected_date, category, expected_cost, floor, class_lab):
    if n_clicks:
        with open('./data/Building_Maintenance.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            for index, row in enumerate(rows):
                if row['Description'] == description:
                    rows[index] = {
                        'Description': description,
                        'Date': date,
                        'Expected Date': expected_date,
                        'Category': category,
                        'Expected Cost (INR)': expected_cost,
                        'Floor': floor,
                        'Class/Lab No': class_lab,
                        'Bill URL': row['Bill URL'],
                        'Is Done': "No"
                    }
        with open('./data/Building_Maintenance.csv', 'w', newline='') as csvfile:
            fieldnames = ['Description', 'Date', 'Expected Date', 'Category', 'Expected Cost (INR)', 'Floor', 'Class/Lab No', 'Bill URL', 'Is Done']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        # return create_project_form()
        return True, dbc.Alert("Update successful!", color="success")
    return None, None

# Function to create the bill upload section
def bill_upload_section():
    return html.Div([
        html.Br(),
        dcc.Dropdown(
            id='description-dropdown',
            options=[{'label': desc, 'value': desc} for desc in get_descriptions()],
            placeholder='Select a description...'
        ),
        html.Div(id='output-bill-images'),
        dcc.Upload(
            id='upload-bill',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px 0'
            },
            multiple=False
        ),
        html.Div(id='output-bill-upload')
    ])

# Callback to update bill images based on selected description
@callback(
    Output('output-bill-images', 'children'),
    [Input('description-dropdown', 'value')]
)
def update_bill_images(description):
    if description:
        urls = get_bill_url(description)
        if urls:
            urls = urls.split('|')
            if len(urls) == 1:
                return html.Div(html.Img(src=urls[0], style={'width': '100%'}), style={"margin": '10px'})
            else:
                return html.Div(
                    [
                        html.Div(html.Img(src=url, style={'width': '100%', }), style={'display': 'inline-block', "margin": '10px'})
                        for url in urls
                    ]
                )
        else:
            return html.Div([html.P('No images available for this description.')])

# Callback to handle bill upload
@callback(
    Output('output-bill-upload', 'children'),
    [Input('upload-bill', 'contents'),
     Input('upload-bill', 'filename'),
     Input('description-dropdown', 'value')]
)
def update_output(contents, filename, selected_description):
    if contents is not None and selected_description:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        url = upload_bill_to_api(decoded, filename)
        if url:
            # Append the URL to the CSV for the selected description
            append_url_to_csv(selected_description, url)
            return html.Div([
                html.P('Bill uploaded successfully!')
            ])
        else:
            return html.Div([
                html.P('Error uploading bill!')
            ])

# API call for uploading bill
def upload_bill_to_api(contents, filename):
    try:
        api = 'http://127.0.0.1:3001/upload_bill'
        files = {'image': (filename, contents)}
        response = requests.post(api, files=files)
        return response.json()['url']
    except Exception as e:
        print(e)
        return None

# Function to append URL to CSV for the selected description
def append_url_to_csv(description, url):
    with open('./data/Building_Maintenance.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        for index, row in enumerate(rows):
            if row['Description'] == description:
                # Append the URL to the list
                if row['Bill URL']:
                    row['Bill URL'] = row['Bill URL'] + '|' + url
                else:
                    row['Bill URL'] = url
    with open('./data/Building_Maintenance.csv', 'w', newline='') as csvfile:
        fieldnames = ['Description', 'Date', 'Expected Date', 'Category', 'Expected Cost (INR)', 'Floor', 'Class/Lab No', 'Bill URL', 'Is Done']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

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
    if not n_clicks:
        return None
    if not all([description, date, expected_date, category, expected_cost, floor, class_lab]):
        return False
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