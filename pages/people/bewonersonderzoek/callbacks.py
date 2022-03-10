from dash import Dash, Input, Output, html, dash_table
from dash.dash_table.Format import Format, Scheme
from dash.exceptions import PreventUpdate
import plotly.express as px

from storage import container as storage_container

from data.preprocess import TVBewOnd_df_constrresp, \
    TVBewOnd_df_constr, TVBewOnd_cityoptions, TVBewOnd_constroptions

# Define storage container to share data between callbacks as json
storage_container.add_memory_store('store_city')
storage_container.add_memory_store('store_construct')

# Define callback functions
def callbacks(app: Dash):
    # @app.callback(
    #     Output('store_city', 'data'),
    #     Input('select_city', 'value'),
    #     )
    # def store_city(value):
    #     return value

    @app.callback(
        Output('plot_radar', 'figure'),
        Input('select_city', 'value'),
        )
    def update_radar(data_city):
        if data_city is None:
            raise PreventUpdate
        # print(data_city)
        pltdf = TVBewOnd_df_constr
        pltdf = pltdf.loc[pltdf['Stad']==data_city]
        
        fig = px.line_polar(pltdf, r="Score", theta="Construct",
                                color="Jaar", line_close=True,
        #                        color_discrete_sequence=px.colors.sequential.Plasma_r
                            )
        fig.update_traces(fill='toself')
        fig.update_polars(radialaxis=dict(nticks=6, range=[0,5]))
        
        return fig


    @app.callback(
        Output('plot_dist', 'figure'),
        Input('select_construct', 'value'),
        Input('select_city', 'value'),
        )
    def update_dist(slct_constructs, slct_city):
        if slct_constructs is None or slct_city is None:
            raise PreventUpdate

        # print(slct_constructs)
        # print(slct_constructs)
        pltdf = TVBewOnd_df_constrresp
        pltdf = pltdf.loc[(pltdf['Stad']==slct_city) & (pltdf['Construct'].isin(slct_constructs))]
        # pltdf = pltdf.loc(pltdf['Stad']=='Gent')
        fig = px.histogram(pltdf, x="Score", color='Jaar', 
                            barmode='overlay', histnorm='percent', 
                            facet_row='Construct', height=1000)
        fig.update_traces(xbins=dict(start=0.0, end=5.0, size=0.5))
        
        return fig
    

    @app.callback(
        Output('plot_table', 'data'),
        Output('plot_table', 'columns'),
        Input('select_city', 'value'),
        )
    def update_table(slct_city):
        if slct_city is None:
            raise PreventUpdate

        pltdf = TVBewOnd_df_constr
        pltdf = pltdf.loc[pltdf['Stad']==slct_city, ['Jaar', 'Construct', 'Score']]
        pltdf = pltdf.pivot(index='Construct', columns='Jaar', values='Score')
        pltdf = pltdf.reset_index()

        data=pltdf.to_dict('records'),
        columns = [dict(id='Construct',
                        name='Construct'
                        )] + [dict(name=i, id=i, type='numeric',
                                   format=Format(precision=2, scheme=Scheme.fixed)) for i in pltdf.columns[1:]],
                                   
        return data[0], columns[0]

    
