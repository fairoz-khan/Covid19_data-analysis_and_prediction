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
import chart_studio.plotly as py
from world import World_data as wd
# init_notebook_mode(connected=True)

obj_ofind = Inddata()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 
                        'assets/style.css', 
                        'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css']

confirmed_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
deaths_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
recoveries_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
latest_data = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/04-03-2020.csv')
    
cols = confirmed_df.columns[4:]
Countries = list(confirmed_df['Country/Region'].unique())

val_conf = []
val_death = []
val_cured = []
for i in Countries:
    val_conf.append(confirmed_df[confirmed_df['Country/Region']== i][cols[-1]].sum()) 
    val_death.append(deaths_df[deaths_df['Country/Region']== i][cols[-1]].sum()) 
    val_cured.append(recoveries_df[recoveries_df['Country/Region']== i][cols[-1]].sum()) 

confirm_f_data = pd.DataFrame({'Country':Countries, 
                              'value':val_conf})
death_f_data = pd.DataFrame({'Country':Countries, 
                            'value':val_death})
recover_f_data = pd.DataFrame({'Country':Countries, 
                            'value':val_cured})
all_case = pd.DataFrame({'Country':confirm_f_data['Country'],'value':'Confirmed:'+confirm_f_data['value'].apply(lambda x:str(x))
                            +' Cured:'+recover_f_data['value'].apply(lambda x:str(x))+' Death:'+death_f_data['value'].apply(lambda x:str(x))
                        })
                
def show_map():
    data = dict(type='choropleth',
           locations = all_case['Country'],
           locationmode = 'country names',
           z = confirm_f_data['value'],
           reversescale=True,
           text= all_case['value'],
           colorscale='plasma',
           showscale=False)

    layout = dict(width=1500, height=700,
                margin={'l':0,'r':0,'t':0,'b':0},
                geo = dict(
                    showframe = False,
                    projection = {'type':'equirectangular'},
                    showlakes = True,
                    lakecolor = 'rgb(85,173,240)'
                )
            )

    map = go.Figure(data = [data],layout = layout)
    return dcc.Graph(figure=map)


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
                id='World_body',
                children=[
                    html.Div(id='nav', children=obj_ofind.nav_bar()),
                    html.P(className='lablebyme', children="World Map"),
                    html.Div(
                        show_map()
                    ),
                ]
            )

if __name__ == "__main__":
    app.run_server(debug=False, port=8052)