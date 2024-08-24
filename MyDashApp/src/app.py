from optparse import Values
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.subplots as sp

# Read data
df = pd.read_csv("https://raw.githubusercontent.com/rxgerdxdger/rbtn22/main/22RBTN_updated.csv")

# Get available columns for dropdown (excluding LOC, BREEDER, YEAR, BLK, ENTRY & PLOT)
available_columns = [col for col in df.columns if col not in ['LOC', 'BREEDER', 'YEAR', 'BLK', 'ENTRY', 'PLOT','(G)']]

# Function to update pie figure
def update_pie_figure(selected_column):
    breeders = df['BREEDER'].unique()
    values = [df[df['BREEDER'] == breeder][selected_column].mean() for breeder in breeders]

    pie_fig = go.Figure(data=[go.Pie(
        labels=breeders,
        values=values,
        hole=0.2,
        textinfo='value',
        textposition='inside',
        insidetextorientation='radial',
        texttemplate='%{value:.2f}'  # Format the value with 2 decimal places
    )])

    pie_fig.update_layout(
        title_text=f"Mean {selected_column}",
        title_x=0.5,
        height=400,
        width=400,
        margin=dict(l=50, r=50, b=50, t=100),
        legend_title="Breeder"
    )
    return pie_fig

# Function to update box figure
def update_box_figure(selected_column):
    box_fig = go.Figure(data=[go.Box(x=df['BREEDER'], y=df[selected_column], notched=True, marker=dict(color='green'))])
    
    #Customize the layout
    box_fig.update_layout(
        title_text="Box Plot of " + selected_column,
        title_x=0.5,  # Center the title
        height=900,  # Adjust height as needed
        xaxis_title="Breeder",
        yaxis_title=selected_column,
        margin=dict(l=50, r=50, b=50, t=100)  # Adjust margins as needed
    )
    return box_fig

# Function to update scatter figure
def update_scatter_figure(selected_column):
    scatter_fig = go.Figure()

    # Create a scatter trace for each unique BLK value
    for blk_value, df_group in df.groupby('BLK'):
        scatter_fig.add_trace(go.Scatter(
            x=df_group['BREEDER'],
            y=df_group[selected_column],
            mode='markers',
            marker=dict(
                color=df_group['ENTRY'],
                size=10,  # Adjust marker size as needed
                symbol=blk_value,  # Assign a symbol based on BLK value
                opacity=0.9
            ),
            name=f"BLK {blk_value}"
        ))

    # Customize the layout
    scatter_fig.update_layout(
        title=f"{selected_column} by Breeder, Colored by ENTRY, Shaped by BLK",
        xaxis_title="Breeder",
        yaxis_title=selected_column,
        legend_title="BLK",
        coloraxis=dict(colorbar=dict(title="ENTRY")),
        height=900,
    )

    return scatter_fig

# Function to update table figure
def update_table_figure(selected_column):
    grouped_data = df.groupby(['BREEDER', 'ENTRY', 'BLK'])[selected_column].mean().reset_index()
    grouped_data = grouped_data.sort_values(by=selected_column, ascending=False)
    table_fig = go.Figure(data=[go.Table(
    header= "Table Summary",
        values=Values,
        hole=0.3,
        textinfo='value',
        textposition='inside',
        insidetextorientation='radial',
        texttemplate='%{value:.2f}'  # Format the value with 2 decimal places
    )])

    pie_fig.update_layout(
        title_text=f"Mean {selected_column}",
        title_x=0.5,
        height=400,
        width=400,
        margin=dict(l=50, r=50, b=50, t=100),
        legend_title="Breeder"
    )
    return pie_fig

# Function to update box figure
def update_box_figure(selected_column):
    box_fig = go.Figure(data=[go.Box(x=df['BREEDER'], y=df[selected_column], notched=True, marker=dict(color='green'))])
    
    #Customize the layout
    box_fig.update_layout(
        title_text="Box Plot of " + selected_column,
        title_x=0.5,  # Center the title
        height=900,  # Adjust height as needed
        xaxis_title="Breeder",
        yaxis_title=selected_column,
        margin=dict(l=50, r=50, b=50, t=100)  # Adjust margins as needed
    )
    return box_fig

# Function to update scatter figure
def update_scatter_figure(selected_column):
    scatter_fig = go.Figure()

    # Create a scatter trace for each unique BLK value
    for blk_value, df_group in df.groupby('BLK'):
        scatter_fig.add_trace(go.Scatter(
            x=df_group['BREEDER'],
            y=df_group[selected_column],
            mode='markers',
            marker=dict(
                color=df_group['ENTRY'],
                size=10,  # Adjust marker size as needed
                symbol=blk_value,  # Assign a symbol based on BLK value
                opacity=0.9
            ),
            name=f"BLK {blk_value}"
        ))

    # Customize the layout
    scatter_fig.update_layout(
        title=f"{selected_column} by Breeder, Colored by ENTRY, Shaped by BLK",
        xaxis_title="Breeder",
        yaxis_title=selected_column,
        legend_title="BLK",
        coloraxis=dict(colorbar=dict(title="ENTRY")),
        height=900,
    )

    return scatter_fig

# Function to update table figure
def update_table_figure(selected_column):
    grouped_data = df.groupby(['BREEDER', 'ENTRY', 'BLK'])[selected_column].mean().reset_index()
    grouped_data = grouped_data.sort_values(by=selected_column, ascending=False)
    table_fig = go.Figure(data=[go.Table(
        header=dict(values=['Breeder', 'Entry', 'Blk', selected_column]),
        cells=dict(values=[grouped_data['BREEDER'], grouped_data['ENTRY'], grouped_data['BLK'], grouped_data[selected_column]])
    )])
#Customize the layout
    table_fig.update_layout(
        title_text="Table Summary",
        title_x=0.5,  # Center the title
        height=400,  # Adjust height as needed
        margin=dict(l=50, r=50, b=50, t=100)  # Adjust margins as needed
    )
    return table_fig

# Function to update max value pie figure
def update_max_value_pie_figure(selected_column):
    max_data = df.groupby('BREEDER')[selected_column].max().reset_index()
    max_value_pie_fig = go.Figure(data=[go.Pie(
        labels=max_data['BREEDER'],
        values=max_data[selected_column],
        hole=0.2,
        textinfo='value',
        textposition='inside',
        insidetextorientation='radial',
        texttemplate='%{value:.2f}'  # Format the value with 2 decimal places
    )])
    max_value_pie_fig.update_layout(
        title_text=f"Max {selected_column}",
         title_x=0.5,
        height=400,
        width=400,
        margin=dict(l=50, r=50, b=50, t=100),
        legend_title="Breeder"
      # ... other layout options ...
  )
    # Add hover data
    max_value_pie_fig.update_traces(
        customdata=max_data[['BREEDER', selected_column]].values,
        hovertemplate="Breeder: %{customdata[0]}<br>Max Value: %{customdata[1]}"
        
    )
   #max_value_pie_fig.update_traces(customdata=max_data[['BLK', 'ENTRY']].values)

    return max_value_pie_fig

# Initial figures
pie_fig = update_pie_figure(available_columns[0])
box_fig = update_box_figure(available_columns[0])
scatter_fig = update_scatter_figure(available_columns[0])
table_fig = update_table_figure(available_columns[0])
max_value_pie_fig = update_max_value_pie_figure(available_columns[0])

# Dropdown component
dropdown = dcc.Dropdown(
    id="selected-column",
    options=[{'label': col, 'value': col} for col in available_columns],
    value=available_columns[0]  # Set initial selected value
)

app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.JOURNAL,
    "https://codepen.io/chriddyp/pen/bWLwgP.css"])
server = app.server 


app.layout = html.Div([
    html.H1("Analytics Dashboard of 2022 RBTN Data", style={"textAlign": "center", "fontFamily": "Arial"}),
    dropdown,
    dcc.Graph(id="max-value-pie-graph", figure=max_value_pie_fig),
    
    dcc.Graph(id="pie-graph", figure=pie_fig),
    dcc.Graph(id="box-graph", figure=box_fig),
    dcc.Graph(id="scatter-graph", figure=scatter_fig),
    dcc.Graph(id="table-graph", figure=table_fig)
])
# Callbacks
@app.callback(
    Output("pie-graph", "figure"),
    Input("selected-column", "value")
)
def update_pie_graph(selected_column):
    return update_pie_figure(selected_column)

@app.callback(
    Output("box-graph", "figure"),
    Input("selected-column", "value")
)
def update_box_graph(selected_column):
    return update_box_figure(selected_column)

@app.callback(
    Output("scatter-graph", "figure"),
    Input("selected-column", "value")
)
def update_scatter_graph(selected_column):
    return update_scatter_figure(selected_column)

@app.callback(
    Output("table-graph", "figure"),
    Input("selected-column", "value")
)
def update_table_graph(selected_column):
    return update_table_figure(selected_column)

@app.callback(
    Output("max-value-pie-graph", "figure"),
    Input("selected-column", "value")
)
def update_max_value_pie_graph(selected_column):
    return update_max_value_pie_figure(selected_column)

if __name__ == "__main__":
    app.run_server(debug=True)