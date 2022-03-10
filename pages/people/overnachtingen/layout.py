from dash import html, dcc
import plotly.express as px

from layout.structure.grid import Column, Row


from data.preprocess import FODnacht_df, FODnacht_destoptions, FODnacht_yearoptions

### GENERIC LAYOUT FUNCTIONS ### 
# graph function to add default layout styles?
def get_graph(class_name, **kwargs):
    return html.Div(
        className=class_name + ' plotz-container',
        children = [
            dcc.Graph(**kwargs),
            html.I(className='fa fa-expand')
            ])


### DEFINE DEFAULTS ###
dflt_year = '2020'
dflt_dest = 'Gent'


### DEFINE CONTENT ###
def plottile_staytrend_year(html_id:str, comp_id:str):
    pltdf = FODnacht_df
    pltdf = pltdf.loc[pltdf['Bestemming']==dflt_dest]
    pltdf = pltdf[['Bestemming', 'Jaar', 'Maand', 'Overnachtingen']].groupby(['Bestemming', 'Jaar', 'Maand']).sum().reset_index()
    
    fig = px.line(pltdf, x='Maand', y='Overnachtingen', color='Jaar')
    
    content = html.Div(
                        className=html_id,
                        children = [
                            html.Div(className='tiletitle-topcenter', 
                                      children=['Evolutie aantal overnachtingen per jaar']),
                            get_graph(
                                class_name='',
                                # figure=plots.plot_timeseries_area(ts=ts_crowd_all[ts_crowd_all['source']=='Crowdscan'], x=ts_crowd_all[ts_crowd_all['source']=='Crowdscan'].index, y='crowd_pct', color='zone', datetimerange=dataprep.dflt_daterange), 
                                figure=fig,
                                id=comp_id,
                                #config=plot_config
                                ),
                        
                            ]
                    )
    return content

def plottile_staytrend_origin(html_id:str, comp_id:str):
    pltdf = FODnacht_df
    pltdf = pltdf.loc[(pltdf['Bestemming']==dflt_dest) & (pltdf['Jaar']==dflt_year)]
    pltdf = pltdf[['Herkomstland', 'Jaar', 'Maand', 'Overnachtingen']].groupby(['Herkomstland', 'Jaar', 'Maand']).sum().reset_index()
    pltdf.head()
    fig = px.line(pltdf, x='Maand', y='Overnachtingen', color='Herkomstland')
    
    content = html.Div(
                        className=html_id,
                        children = [
                            html.Div(className='tiletitle-topcenter', 
                                      children=['Evolutie overnachtingen per herkomstland in ' + dflt_year]),
                            get_graph(
                                class_name='',
                                # figure=plots.plot_timeseries_area(ts=ts_crowd_all[ts_crowd_all['source']=='Crowdscan'], x=ts_crowd_all[ts_crowd_all['source']=='Crowdscan'].index, y='crowd_pct', color='zone', datetimerange=dataprep.dflt_daterange), 
                                figure=fig,
                                id=comp_id,
                                #config=plot_config
                                ),
                        
                            ]
                    )
    return content

def plottile_staytrend_motive(html_id:str, comp_id:str):
    pltdf = FODnacht_df
    pltdf = pltdf.loc[(pltdf['Bestemming']==dflt_dest) & (pltdf['Jaar']==dflt_year)]
    pltdf = pltdf[['Motief', 'Jaar', 'Maand', 'Overnachtingen']].groupby(['Motief', 'Jaar', 'Maand']).sum().reset_index()
    pltdf.head()
    fig = px.line(pltdf, x='Maand', y='Overnachtingen', color='Motief')
    
    content = html.Div(
                        className=html_id,
                        children = [
                            html.Div(className='tiletitle-topcenter', 
                                      children=['Evolutie overnachtingen per motief in ' + dflt_year]),
                            get_graph(
                                class_name='',
                                # figure=plots.plot_timeseries_area(ts=ts_crowd_all[ts_crowd_all['source']=='Crowdscan'], x=ts_crowd_all[ts_crowd_all['source']=='Crowdscan'].index, y='crowd_pct', color='zone', datetimerange=dataprep.dflt_daterange), 
                                figure=fig,
                                id=comp_id,
                                #config=plot_config
                                ),
                        
                            ]
                    )
    return content



def filter_dest(html_id:str, comp_id:str):
    content =dcc.RadioItems(id=comp_id, options=FODnacht_destoptions, value=dflt_dest)

    return content

def filter_year(html_id:str, comp_id:str):
    content =dcc.RadioItems(id=comp_id, options=FODnacht_yearoptions, value=dflt_year)

    return content


### BUILD LAYOUT ###
layout = Column(children=[
    Row(children=[
        Column(content=filter_dest(html_id='', comp_id='select_dest')),#, style={'min-height':'100px', 'background-color': 'deeppink'}),
        Column(content=filter_year(html_id='', comp_id='select_year'))
        ]),
    Row(content=plottile_staytrend_year(html_id='', comp_id='plot_staytrend_year'),
        ),
    Row(content=plottile_staytrend_origin(html_id='', comp_id='plot_staytrend_origin')
        ),
    Row(content=plottile_staytrend_origin(html_id='', comp_id='plot_staytrend_motive')
        ),
]).get_layout()
