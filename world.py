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
from app import Indian_data as Inddata
from app import generate_table
from makerp import makecnt
# init_notebook_mode(connected=True)

obj_ofind = Inddata()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 
                        'assets/style.css', 
                        'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css']

button_type = ["btn btn-primary", "btn btn-danger", "btn btn-warning"]

def daily_increase(data):
            d = [] 
            for i in range(len(data)):
                if i == 0:
                    d.append(data[0])
                else:
                    d.append(data[i]-data[i-1])
            return d    
x = lambda a:int(str(a).split()[-1])
class World_data:
    confirmed_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    deaths_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    recoveries_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    latest_data = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/04-03-2020.csv')
    
    cols = confirmed_df.columns[4:]
    Countries = list(confirmed_df['Country/Region'].unique())
    country_to_dd = []

    for i in Countries:
        country_to_dd.append({'label':i, 'value':i})

    

    con_casesonday = []
    rec_casesonday = []
    dth_casesonday = []
    for i in cols:
        con_casesonday.append(confirmed_df[i].sum())
        rec_casesonday.append(recoveries_df[i].sum())
        dth_casesonday.append(deaths_df[i].sum())

    


    overtime = pd.DataFrame({'Dates':cols,
                         'cases':con_casesonday
                        })

    overtime_recover = pd.DataFrame({'Dates':cols,
                               'cases': rec_casesonday 
                            })

    overtime_death = pd.DataFrame({'Dates':cols,
                               'cases': dth_casesonday 
                            })

    def barchart_forall(self):
        fig = go.Figure(data=[
            go.Bar(name=f"Confirmed({makecnt(self.overtime.iloc[self.overtime.last_valid_index()]['cases'])})", x=self.overtime.Dates, y=self.overtime.cases, marker_color='green'),
            go.Bar(name=f"Deaths({makecnt(self.overtime_death.iloc[self.overtime_death.last_valid_index()]['cases'])})", x=self.overtime_death.Dates, y=self.overtime_death.cases, marker_color='firebrick'),
            go.Bar(name=f"Cured({makecnt(self.overtime_recover.iloc[self.overtime_recover.last_valid_index()]['cases'])})", x=self.overtime_recover.Dates, y=self.overtime_recover.cases, marker_color='royalblue')
        ])
        # Change the bar mode
        fig.update_layout(autosize=True,
            title="All Cases",
            xaxis_title="Date",
            yaxis_title="Count",
            barmode='relative',
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="black"
            ))
        return dcc.Graph(figure=fig)

    def all_tree_in_col(self):
        fig = make_subplots(rows=1, cols=3, shared_yaxes=True,
                   subplot_titles=("Total confirmed - " + makecnt(self.overtime.iloc[self.overtime.last_valid_index()].cases),
                                    "Total cured - " + makecnt(self.overtime_recover.iloc[self.overtime_recover.last_valid_index()].cases), 
                                   "Total Deaths - " + makecnt(self.overtime_death.iloc[self.overtime_death.last_valid_index()].cases)))
        fig.add_trace(go.Scatter(x=self.overtime.Dates, y=self.overtime.cases, name='Confirm',
                         line=dict(color='royalblue', width=1), mode='lines+markers'), row=1, col=1)
        fig.add_trace(go.Scatter(x=self.overtime_recover.Dates, y=self.overtime_recover.cases, name='Recover',
                         line=dict(color='green', width=1), mode='lines+markers'), row=1, col=2)
        fig.add_trace(go.Scatter(x=self.overtime_death.Dates, y=self.overtime_death.cases, name='Deaths',
                         line=dict(color='firebrick', width=1), mode='lines+markers'), row=1, col=3)

        fig.update_layout(
            title="All Cases",
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

        return dcc.Graph(figure=fig)

    def whole_world_tot(self):
        return(html.Div(children=[
            html.P(className='lablebyme', children=f"Total cases in The World"),
            html.P(className='databyme', children=f"Confirmed count - {makecnt(self.overtime.iloc[self.overtime.last_valid_index()]['cases'])}"),
            html.P(className='databyme', children=f"Cured - {makecnt(self.overtime_recover.iloc[self.overtime_recover.last_valid_index()]['cases'])}", style={'color': 'green',}),
            html.P(className='databyme', children=f"death count - {makecnt(self.overtime_death.iloc[self.overtime_death.last_valid_index()]['cases'])}", style={'color': 'red',})])
        )
    
    def max_amng_countries(self):
        comf_max = self.confirmed_df[self.confirmed_df[self.confirmed_df.columns[-1]].max()==self.confirmed_df[self.confirmed_df.columns[-1]]]
        recv_max = self.recoveries_df[self.recoveries_df[self.recoveries_df.columns[-1]].max()==self.recoveries_df[self.recoveries_df.columns[-1]]]
        death_max = self.deaths_df[self.deaths_df[self.deaths_df.columns[-1]].max()==self.deaths_df[self.deaths_df.columns[-1]]]
        return(html.Div(children=[
            html.P(className='lablebyme', children=f"Maximum among Countries"),
            html.P(className='databyme', children=f"Confirm cases - {makecnt(str(comf_max[comf_max.columns[-1]]).split()[1])} ({str(comf_max['Country/Region']).split()[1]})"),
            html.P(className='databyme', children=f"Cured cases - {makecnt(str(recv_max[recv_max.columns[-1]]).split()[1])} ({str(recv_max['Country/Region']).split()[1]})", style={'color': 'green',}),
            html.P(className='databyme', children=f"Deaths - {makecnt(str(death_max[death_max.columns[-1]]).split()[1])} ({str(death_max['Country/Region']).split()[1]})", style={'color': 'red',}),
        ]))

    def for_selected(self, cntry):
        comf_max = self.confirmed_df[self.confirmed_df['Country/Region']==cntry][self.cols[-1]].sum()
        recv_max = self.recoveries_df[self.recoveries_df['Country/Region']==cntry][self.cols[-1]].sum()
        death_max = self.deaths_df[self.deaths_df['Country/Region']==cntry][self.cols[-1]].sum()
        return(html.Div(children=[
            html.P(className='lablebyme', children=f"Total cases in {cntry}"),
            html.P(className='databyme', children=f"Confirm cases - {makecnt(comf_max)}"),
            html.P(className='databyme', children=f"Cured cases - {makecnt(recv_max)}", style={'color': 'green',}),
            html.P(className='databyme', children=f"Deaths - {makecnt(death_max)}", style={'color': 'red',}),
        ]))

    def indiv_country_cnt(self, country_name, forwt):
        if forwt == 'Cured':
            daily_inc = [self.confirmed_df[self.confirmed_df['Country/Region']==country_name][i].sum() for i in self.cols]
            daily_inc = daily_increase(daily_inc)
        elif forwt == 'Death':
            daily_inc = [self.deaths_df_df[self.deaths_df['Country/Region']==country_name][i].sum() for i in self.cols]
            daily_inc = daily_increase(daily_inc)
        else:
            daily_inc = [self.recoveries_df[self.recoveries_df['Country/Region']==country_name][i].sum() for i in self.cols]
            daily_inc = daily_increase(daily_inc)

        return sum(daily_inc)

    def barcrt_for_country(self, country_name):
        daily_inc = [self.confirmed_df[self.confirmed_df['Country/Region']==country_name][i].sum() for i in self.cols]
        daily_inc = daily_increase(daily_inc)
        fig = px.bar(x=self.cols, y=daily_inc, color= daily_inc, color_continuous_scale=px.colors.sequential.Viridis)

        fig.update_layout(
            title=f"Daily Stats in {country_name} - Total:{makecnt(sum(daily_inc))}",
            xaxis_title="Dates",
            yaxis_title="Count",    
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="black"
            )
        )

        return dcc.Graph(figure=fig)

    # Pie chart operations
    val_conf = pd.DataFrame(columns=['Country','value'], data=confirmed_df[['Country/Region', cols[-1]]].groupby(by='Country/Region'))
    val_conf['value'] = val_conf['value'].apply(x)
    val_death = pd.DataFrame(columns=['Country','value'], data=deaths_df[['Country/Region', cols[-1]]].groupby(by='Country/Region'))
    val_death['value'] = val_death['value'].apply(x)
    val_cured = pd.DataFrame(columns=['Country','value'], data=recoveries_df[['Country/Region', cols[-1]]].groupby(by='Country/Region'))
    val_cured['value'] = val_cured['value'].apply(x) 

    def comp_all_cntry_by_bar(self):
        fig = go.Figure(data=[
            go.Bar(name='Confirmed', x=self.val_conf['Country'], y=self.val_conf['value'], marker_color='green'),
            go.Bar(name='Deaths', x=self.val_death['Country'], y=self.val_death['value'], marker_color='firebrick'),
            go.Bar(name='Recovered', x=self.val_cured['Country'], y=self.val_cured['value'], marker_color='royalblue')
        ])
        fig.update_layout(
            autosize=True,
            title="Country wise cases",
            xaxis_title="Country Name",
            yaxis_title="Count",
            barmode='stack')
        return fig

    def pie_for_all(self, forwt):
        if forwt == 'Cured':
            fig = px.pie(self.val_cured, values='value', names='Country', title=forwt)
        elif forwt == 'Deaths': 
            fig = px.pie(self.val_death, values='value', names='Country', title=forwt)
        else:
            fig = px.pie(self.val_conf, values='value', names='Country', title=forwt)
        
        fig.update_layout(
            autosize=True,
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
            
        return dcc.Graph(figure=fig)    

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

wrld = World_data()
app.layout = html.Div(
                id='World_body',
                children=[
                    html.Div(id='nav', children=obj_ofind.nav_bar()),                
                    # Body of world data analysis
                    html.Div(id='body', 
                        children=[

                            # Cases count
                            html.Div(className='row',
                                children=[
                                    html.Div(className='col-sm-4', children=[
                                        wrld.whole_world_tot(),
                                        html.Div(className='fill_up'),
                                        wrld.max_amng_countries(),
                                    ]),

                                    html.Div(className='col-sm-4',children=[
                                        html.P(className='lablebyme', children=['Select Country']),
                                                dcc.Dropdown(
                                                    id='country_dropdown',
                                                    options=wrld.country_to_dd,
                                                    placeholder='Enter Country name...',
                                                    value='India'
                                                ),
                                                html.Div(className='fill_up'),
                                                html.Div(
                                                    id='per_country_stats'
                                                ),
                                    ]),
                                    html.Div(className='col-sm-4'),
                                ]),
                            html.Div(className='draw_line'),
                            # Visualizaton
                            html.Div(id='All-vis', children=[
                                    html.Div(id='Three_col',
                                        children=[
                                            html.P(className='lablebyme', children="Confirm, Recovery and Death cases over time"),
                                            wrld.all_tree_in_col()]
                                    ),
                                    html.Div(className='draw_line'),
                                    html.Div(id='bar_for_all', children=[
                                        wrld.barchart_forall(),
                                    ]),
                                    html.Div(className='draw_line'),
                                    html.Div(children=[
                                        html.P(className='lablebyme',children='Comaparision between countries'),
                                        dcc.Graph(figure=wrld.comp_all_cntry_by_bar()),
                                    ], style={'marginBottom':'20px'}),
                                    html.Div(className='draw_line'),
                                    html.Div(id='base_country',
                                        children=[
                                            html.Div(className='row',
                                                children=[
                                                    html.Div(id='dd_ctr', className='col-sm-4',
                                                        children=[
                                                            html.P(className='lablebyme', children=['Select Country below']),
                                                            dcc.Dropdown(
                                                                id='country_dd',
                                                                options=wrld.country_to_dd,
                                                                placeholder='Enter Country name...',
                                                                value='India'
                                                            ),
                                                    ]),
                                                    html.Div(id='dploydinc', className='col-sm-8'),
                                            ]),
                                    ]),
                                    html.Div(className='draw_line'),
                                    html.Div(id='pie',children=[
                                        html.P(className='lablebyme', children="Pie Chart for all Countries"),
                                        html.Div(id='buttons', className='row',
                                            children=[
                                                html.Div(className='col-sm-4',
                                                        children=[
                                                            html.Button(obj_ofind.three_type[i], className=button_type[i], id=obj_ofind.three_type[i], n_clicks=0)
                                                        ]         
                                                )for i in range(len(obj_ofind.three_type))
                                        ]),
                                        html.Div(
                                            id='Pie_crt_world'
                                        ),
                                        html.Div(className='draw_line'),
                                    ]),
                            ]),
                        ]),
                ])

# function to display dropdown list
@app.callback(Output('dploydinc', 'children'),
            [Input('country_dd', 'value')])
def update_output(value):
    return(wrld.barcrt_for_country(value))

# function to display dropdown list
@app.callback(Output('per_country_stats', 'children'),
            [Input('country_dropdown', 'value')])
def update_output(value):
    return(wrld.for_selected(value))

# To plot pie charts
@app.callback(Output('Pie_crt_world', 'children'),
              [Input('Cured', 'n_clicks'),
               Input('Deaths', 'n_clicks'),
               Input('Confirmed', 'n_clicks')])
def displayClick(btn1, btn2, btn3):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'Cured' in changed_id:
        return (wrld.pie_for_all('Cured'))
    elif 'Deaths' in changed_id:
        return (wrld.pie_for_all('Deaths'))
    else:
        return (wrld.pie_for_all('Confirmed'))

if __name__ == "__main__":
    app.run_server(debug=False, port=8051)