import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
from plotly.subplots import make_subplots
cf.go_online()
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import seaborn as sns
from makerp import makecnt 
# init_notebook_mode(connected=True)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 
                        'assets/style.css', 
                        'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css']

button_type = ["btn btn-primary", "btn btn-danger", "btn btn-warning"]
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

class Indian_data:
    df = pd.read_csv('covid_19_india.csv', index_col='Sno')
    df.Date = pd.to_datetime(df.Date, format='%d/%m/%y')
    df = df.dropna()

    date_table = df.groupby(['Date', 'State/UnionTerritory']).sum().reset_index().set_index('Date')
    total = date_table.loc[date_table.last_valid_index()].sum()
    confirmed_count = int(total.Confirmed)
    death_count = int(total.Deaths)
    cured_count = int(total.Cured)

    today_states = date_table.loc[date_table.last_valid_index()].reset_index()
    max_confrim = today_states[today_states.Confirmed == today_states.Confirmed.max()]
    max_deaths = today_states[today_states.Deaths == today_states.Deaths.max()]
    max_cured = today_states[today_states.Cured == today_states.Cured.max()]

    date_group = df.groupby(['Date']).sum()
    date_group.reset_index(inplace=True)

    date_group.sort_values('Date',inplace=True)

    states = list(date_table['State/UnionTerritory'].unique())

    dummy = pd.DataFrame()
    dummy['State'] = df['State/UnionTerritory'].unique() 
    colors =sns.color_palette("viridis", 33).as_hex()

    states_to_dropdown = []

    for i in states:
        states_to_dropdown.append({'label':i, 'value':i})

    three_type = list(date_table.columns[1:])
    def all_tree_in_col(self):
        fig = make_subplots(rows=1, cols=3, shared_yaxes=True, 
                    subplot_titles=("Total deaths - " + makecnt(self.death_count),"Total confirmed - " + makecnt(self.confirmed_count),"Total cured - " + makecnt(self.cured_count)))
        fig.add_trace(go.Scatter(x=self.date_group.Date, y=self.date_group.Deaths, name='Deaths',
                                line=dict(color='firebrick', width=1), mode='lines+markers'), row=1, col=1)
        fig.add_trace(go.Scatter(x=self.date_group.Date, y=self.date_group.Confirmed, name = 'Confirmed',
                                line=dict(color='royalblue', width=1), mode='lines+markers',), row=1, col=2)
        fig.add_trace(go.Scatter(x=self.date_group.Date, y=self.date_group.Cured, name='Cured',
                                line=dict(color='green', width=1), mode='lines+markers',), row=1, col=3)

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Count",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="black"
            )
        )

        fig.update_xaxes(ticks="inside")
        fig.update_yaxes(ticks="inside", col=1)

        return fig

    def all_combined_data(self):
        fig_all = go.Figure(data=[
        go.Bar(name='Confirmed', x=self.date_group.Date, y=self.date_group.Confirmed, marker_color='green'),
        go.Bar(name='Deaths', x=self.date_group.Date, y=self.date_group.Deaths, marker_color='firebrick'),
        go.Bar(name='Cured', x=self.date_group.Date, y=self.date_group.Cured, marker_color='royalblue')])
        # Change the bar mode
        fig_all.update_layout(autosize=True, height=600,
            title="All Cases",
            xaxis_title="Date",
            yaxis_title="Count",
            barmode='relative',
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="black"
            ))
        return fig_all

    def bar_for_all(self, forwt):
        fig = px.bar(self.date_group, x='Date', y=forwt, color='Confirmed', color_continuous_scale=px.colors.sequential.Viridis)

        fig.update_layout(
            title=f"{forwt} cases",    
            font=dict(family="Times New Roman, monospace", size=18, color="black"),
        )
        return dcc.Graph(figure=fig)

    def all_states(self):
        fig = go.Figure(data=[
            go.Bar(name='Confirmed', x=self.date_table.loc[self.date_table.last_valid_index()]['State/UnionTerritory'], y=self.date_table.loc[self.date_table.last_valid_index()].Confirmed, marker_color='green'),
            go.Bar(name='Deaths', x=self.date_table.loc[self.date_table.last_valid_index()]['State/UnionTerritory'], y=self.date_table.loc[self.date_table.last_valid_index()].Deaths, marker_color='firebrick'),
            go.Bar(name='Cured', x=self.date_table.loc[self.date_table.last_valid_index()]['State/UnionTerritory'], y=self.date_table.loc[self.date_table.last_valid_index()].Cured, marker_color='royalblue')
        ])
        # Change the bar mode
        fig.update_layout(
            autosize=True,
            height=600,
            title="State wise cases",
            xaxis_title="States",
            yaxis_title="Count",
            barmode='stack',
        )
        return fig

    def ind_stats(self, state):
        stats = self.today_states[self.today_states['State/UnionTerritory']== state]
        s_data = [state, 
                    str(stats['Confirmed']).split()[1], 
                    str(stats['Cured']).split()[1],
                    str(stats['Deaths']).split()[1]]
        return s_data
        
    def pie_for_all(self, forwt):
        fig = px.pie(self.date_table.loc[self.date_table.last_valid_index()], values=forwt, names='State/UnionTerritory', title=forwt)
        
        fig.update_layout(
            autosize=True,
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        return dcc.Graph(figure=fig)

    def animate_bar_chart(self):
        frames = []
        grouped = self.df[self.df['Date'] > '2020/03'][['Date', 'State/UnionTerritory', 'Confirmed', 'Deaths', 'Cured']].groupby(['Date'])    
        for name, group in iter(grouped):
            merged = pd.merge(group, self.dummy, how='outer', left_on='State/UnionTerritory', right_on='State')        
            merged.fillna(0, inplace=True)
            merged.sort_values('State', inplace=True)
            frames.append(go.Frame(data = [go.Bar(x = merged['State'].tolist(), y=merged['Confirmed'].tolist(), marker_color=self.colors)], 
                                layout=go.Layout(title='Confirmed cases - '+group.Date.iloc[0].strftime('%Y-%m-%d'))))
            fig = go.Figure(
            data = [go.Bar(x = merged['State'].tolist(), y = [0] * len(merged['State'].tolist()))],
            frames=frames, 
            layout=go.Layout(
                autosize=True,
                xaxis=dict(type='category'),
                yaxis=dict(range=[0, 3500], autorange=True),            
                title="Confirmed cases",
                xaxis_title="State",
                yaxis_title="Count",
                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(label="Play",
                                method="animate",
                                args=[None])])]))

        return dcc.Graph(figure=fig)
                                       
    def nav_bar(self):
        return html.Nav(className='navbar navbar-expand-sm row', 
                    children=[
                        html.Div(className='col-sm-1'),
                        html.Div(className='col-sm-1',
                            children=[html.Img(id='icon', src='assets/corona.jpeg')]
                        ),
                        html.Div(id='Heading', className='col-sm-4',
                            children="Covid19 Data Analysis and Visualization"
                        ),
                        html.Div(className='col-sm-3'),
                        html.Ul(className='navbar-nav col-sm-3', children=[
                            html.Li(className="nav-item active",
                                children=[html.A(className="nav-link", href="http://127.0.0.1:8050/", children=[html.P("India")]),]
                            ),
                            html.Li(className="nav-item active",
                                children=[html.A(className="nav-link", href="http://127.0.0.1:8051/", children=[html.P("World")]),]
                            ),
                            html.Li(className="nav-item active",
                                children=[html.A(className="nav-link", href="http://127.0.0.1:8052/", children=[html.P("Map")])]
                            ),
                        ])
                    ]),

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
indian = Indian_data()

app.layout = html.Div(
                children=[
                    html.Div(id='nav', children=indian.nav_bar()),
                    html.Div(id="body", 
                                children=[
                                    # Cases count
                                    html.Div(id="Text_info", className="row", 
                                        children=[
                                            html.Div(className="col-sm-4", children=[
                                            html.P(className='lablebyme', children=["Total cases in India"]),
                                            html.P(className='databyme', children=f"Confirmed count - {makecnt(indian.confirmed_count)}"),
                                            html.P(className='databyme', children=f"Cured - {makecnt(indian.cured_count)}", style={'color': 'green',}),
                                            html.P(className='databyme', children=f"death count - {makecnt(indian.death_count)}", style={'color': 'red',}),
                                            html.Div(className='fill_up'),
                                            html.P(className='lablebyme', children=["Maximum Cases Among Indian States"]),
                                            html.P(className='databyme', children=f"Confirm cases - {makecnt(indian.max_confrim.Confirmed.iloc[0])} ({indian.max_confrim['State/UnionTerritory'].iloc[0]})"),
                                            html.P(className='databyme', children=f"Cured cases - {makecnt(indian.max_cured.Cured.iloc[0])} ({indian.max_cured['State/UnionTerritory'].iloc[0]})", style={'color': 'green',}),
                                            html.P(className='databyme', children=f"Deaths - {makecnt(indian.max_deaths.Deaths.iloc[0])} ({indian.max_deaths['State/UnionTerritory'].iloc[0]})", style={'color': 'red',}),
                                            ]),
                                            html.Div(className='col-sm-4', children=[
                                                html.P(className='lablebyme', children=['Select State']),
                                                dcc.Dropdown(
                                                    id='state_dropdown',
                                                    options=indian.states_to_dropdown,
                                                    placeholder='Enter State name...',
                                                    value='Karnataka'
                                                ),
                                                html.Div(className='fill_up'),
                                                html.Div(
                                                    id='state_ind_stats'
                                            ),]
                                            ),
                                            html.Div(className='col-sm-4', 
                                                children=[
                                                    
                                                ]
                                            ),
                                    ]),
                                    html.Div(className='draw_line'),
                                    # Data visualization
                                    html.Div(
                                        id='All-vis',
                                        children=[
                                            html.P(className='lablebyme', children="Confirm, Recovery and Death cases over time"),
                                            html.Div(id="Whole_country", children = [dcc.Graph(
                                                                                id='all_three_cols',
                                                                                figure=indian.all_tree_in_col()),
                                                                                html.Div(className='draw_line'),
                                                                            html.P(className='lablebyme', children=["Confirm, Recovery and Death cases using bar plot"]),
                                                                            dcc.Graph(
                                                                                id='all-case-bar',
                                                                                figure=indian.all_combined_data()),
                                                                                html.Div(className='draw_line'),
                                                                        html.P(className='lablebyme', children=["Bar chart to Cured, Deaths, and Confirmed cases"]),
                                                                        html.Div(className='row', children=[
                                                                            html.Div(className='col-sm-4', children=[
                                                                                    html.Button(indian.three_type[i], className=button_type[i], id=indian.three_type[i]+str(i), n_clicks=0)
                                                                            ])for i in range(len(indian.three_type))
                                                                        ]),  
                                                                        html.Div(id='bar_for_all'),
                                                                    ]
                                                    ),
                                            html.Div(className='draw_line'),
                                            # Statewise bar plot analysis
                                            html.Div(id="State_wise",
                                                    children=[
                                                        html.P(className='lablebyme', children="Indian State wise Analysis"),
                                                        dcc.Graph(
                                                            id="all_states_in_one",
                                                            figure=indian.all_states()
                                                        ),
                                                    ]),
                                            html.Div(className='draw_line'),
                                            # pie chart for all states
                                            html.P(className='lablebyme', children=["Pie chart for all Indian States"]),
                                            html.Div(className='row',
                                                children=[                    
                                                    html.Div(className='col-sm-4',
                                                        children=[
                                                            html.Button(indian.three_type[i], className=button_type[i], id=indian.three_type[i], n_clicks=0)
                                                        ]         
                                                )for i in range(len(indian.three_type))
                                            ]),
                                            # html.Div(className='draw_line'),
                                            # pie charts through button
                                            html.Div(
                                                id='Pie_by_but'
                                            ),
                                            # Animation plot
                                                # html.Div(
                                                #   children=[html.P(className='lablebyme', children=["Corond19 Confirm cases overtime (Animation Plot)"]),
                                                #           html.Button("Animation Plot", className=button_type[0], id='animation', n_clicks=0),
                                                #           Animation bar
                                                #             html.Div(id='show_animation')
                                                #             ],),
                                                    
                                                ]),
                                        ]),
                                ])

# Dropdown box to select States in india
@app.callback(Output('state_ind_stats', 'children'),
            [Input('state_dropdown', 'value')])
def update_output(value):
    data = indian.ind_stats(value)
    return (html.P(className='lablebyme', children=f"Total cases in {data[0]}"),
            html.P(className='databyme', children=f"Confirmed count - {makecnt(data[1])}"),
            html.P(className='databyme', children=f"Cured - {makecnt(data[2])}", style={'color': 'green',}),
            html.P(className='databyme', children=f"death count - {makecnt(data[3])}", style={'color': 'red',}))

# Three buttons for bar charts
@app.callback(Output('bar_for_all', 'children'),
              [Input('Cured0', 'n_clicks'),
               Input('Deaths1', 'n_clicks'),
               Input('Confirmed2', 'n_clicks')])
def displayClick(btn1, btn2, btn3):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'Cured' in changed_id:
        msg = html.Div(children=[indian.bar_for_all('Cured')])
    elif 'Deaths' in changed_id:
        msg = html.Div(children=[indian.bar_for_all('Deaths')])
    else:
        msg = html.Div(children=indian.bar_for_all('Confirmed'))
    return msg
 
#Three buttons in indian data analysis to display pie charts
@app.callback(Output('Pie_by_but', 'children'),
              [Input('Cured', 'n_clicks'),
               Input('Deaths', 'n_clicks'),
               Input('Confirmed', 'n_clicks')])
def displayClick(btn1, btn2, btn3):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'Cured' in changed_id:
        msg = html.Div(children=[indian.pie_for_all('Cured')])
    elif 'Deaths' in changed_id:
        msg = html.Div(children=[indian.pie_for_all('Deaths')])
    else:
        msg = html.Div(children=indian.pie_for_all('Confirmed'))
    return msg

# Function to animation plot
# @app.callback(Output('show_animation', 'children'),
#             [Input('animation', 'value')])
# def update_output(value):
#     return (indian.animate_bar_chart())
if __name__ == '__main__':
    app.run_server(debug=True)