from dash import html, dcc, dash_table
from dash.dash_table.Format import Format, Scheme
import plotly.express as px

from layout.structure.grid import Column, Row

from data.preprocess import TVBewOnd_df_constrresp, \
    TVBewOnd_df_constr, TVBewOnd_cityoptions, TVBewOnd_constroptions

### GENERIC LAYOUT FUNCTIONS ### 

# graph function to add default layout styles?
def get_graph(class_name, **kwargs):
    return html.Div(
        className=class_name + ' plotz-container',
        children = [
            dcc.Graph(**kwargs),
            html.I(className='fa fa-expand')
            ])

# get tile function to add default tile layout with title

# # import from components?
# def get_content_with_id(html_id: str):
#     return html.Div([
#         html.H1("GDP viewer"),
#         html.Hr(),
#         dcc.Graph(id=html_id),
#         dcc.Slider(
#             id=f'{html_id}-slider',
#             min=dataframe()['year'].min(),
#             max=dataframe()['year'].max(),
#             value=dataframe()['year'].min(),
#             marks={str(year): str(year) for year in dataframe()['year'].unique()},
#             step=None
#         )
#     ])


### DEFINE DEFAULTS ###
dflt_constructs = ['Fierheid', 'Leesbaarheid', 'Support']
dflt_city = 'Gent'


### DEFINE CONTENT ###
def plottile_radar(html_id:str, comp_id:str):
    pltdf = TVBewOnd_df_constr
    pltdf = pltdf.loc[pltdf['Stad']==dflt_city]
    
    fig = px.line_polar(pltdf, r="Score", theta="Construct",
                            color="Jaar", line_close=True,
    #                        color_discrete_sequence=px.colors.sequential.Plasma_r
                        )
    fig.update_traces(fill='toself')
    fig.update_polars(radialaxis=dict(nticks=6, range=[0,5]))
    
    content = html.Div(
                        className=html_id,
                        children = [
                            html.Div(className='tiletitle-topcenter', 
                                      children=['Evolutie hoofdconcepten']),
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

def plottile_dist(html_id:str, comp_id:str):
    pltdf = TVBewOnd_df_constrresp
    pltdf = pltdf.loc[(pltdf['Stad']==dflt_city) & (pltdf['Construct'].isin(dflt_constructs))]
    fig = px.histogram(pltdf, x="Score", color='Jaar', 
                       barmode='overlay', histnorm='percent', 
                       facet_row='Construct', height=1000)
    fig.update_traces(xbins=dict(start=0.75, end=5.25, size=0.5))
    
    content = html.Div(
                        className=html_id,
                        children = [
                            html.Div(className='tiletitle-topcenter', 
                                      children=['Evolutie hoofdconcepten']),
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

def plottile_table(html_id:str, comp_id:str):
    pltdf = TVBewOnd_df_constr
    pltdf = pltdf.loc[pltdf['Stad']==dflt_city, ['Jaar', 'Construct', 'Score']]
    pltdf = pltdf.pivot(index='Construct', columns='Jaar', values='Score')
    pltdf = pltdf.reset_index()
    
    # conditionalstyling = ([
    #         {
    #             'if': {
    #                 'filter_query': '{{{}}} > {}'.format(col, value),
    #                 'column_id': col
    #             },
    #             'backgroundColor': '#3D9970',
    #             'color': 'white'
    #         } for (col, value) in pltdf.iloc[:,1:].max().iteritems()
    #     ] +
    #     [
    #         {
    #             'if': {
    #                 'filter_query': '{{{}}} <= {}'.format(col, value),
    #                 'column_id': col
    #             },
    #             'backgroundColor': '#FE4136',
    #             'color': 'white'
    #         } for (col, value) in pltdf.iloc[:,1:].median().iteritems()
    #     ] +
    #     [
    #         {
    #             'if': {
    #                 'filter_query': '{{{}}} <= {}'.format(col, value),
    #                 'column_id': col
    #             },
    #             'backgroundColor': '#FF4136',
    #             'color': 'white'
    #         } for (col, value) in pltdf.iloc[:,1:].min().iteritems()
    #     ]
    #     )
    
    content= html.Div(className=html_id,
                      children = [
                          dash_table.DataTable(
                              id=comp_id,
                              data=pltdf.to_dict('records'),
                              columns = [dict(id='Construct', 
                                              name='Construct'
                                              )] + [dict(name=i, id=i, type='numeric', 
                                                         format=Format(precision=2, scheme=Scheme.fixed)) for i in pltdf.columns[1:]],
                              # style_data_conditional=conditionalstyling
                              )
                          ])
    
    return content

def filter_city(html_id:str, comp_id:str):
    content =dcc.RadioItems(id=comp_id, options=TVBewOnd_cityoptions, value=dflt_city)

    return content

def filter_construct(html_id:str, comp_id:str):
    content =dcc.Checklist(id=comp_id, options=TVBewOnd_constroptions, value=dflt_constructs)

    return content



### BUILD LAYOUT ###
layout = Column(children=[
    Row(children=[
        Column(content=filter_city(html_id='', comp_id='select_city')),
        Column(content=filter_construct(html_id='', comp_id='select_construct'))
        ]),
    Row(children=[
        Column(children=[
            Row(content=plottile_radar(html_id='', comp_id='plot_radar'),
                ),
            Row(content=plottile_table(html_id='', comp_id='plot_table')
                ),
            ]),
        Column(children=[
            Row(content=plottile_dist(html_id='', comp_id='plot_dist'))
            ])
        ])
]).get_layout()


        



