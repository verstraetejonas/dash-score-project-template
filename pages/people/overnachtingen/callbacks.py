from dash import html, dcc
import plotly.express as px

from dash import Dash, Input, Output, html
from dash.exceptions import PreventUpdate

from data.preprocess import FODnacht_df, FODnacht_destoptions, FODnacht_yearoptions

# Define storage container to share data between callbacks as json



# Define callback functions
def callbacks(app: Dash):
    @app.callback(
        Output('plot_staytrend_year', 'figure'),
        Input('select_dest', 'value'),
        )
    def update_staytrend_year(slct_dest):
        if slct_dest is None:
            raise PreventUpdate
        pltdf = FODnacht_df
        pltdf = pltdf.loc[pltdf['Bestemming']==slct_dest]
        pltdf = pltdf[['Bestemming', 'Jaar', 'Maand', 'Overnachtingen']].groupby(['Bestemming', 'Jaar', 'Maand']).sum().reset_index()
        
        fig = px.line(pltdf, x='Maand', y='Overnachtingen', color='Jaar')
        
        return fig

    @app.callback(
        Output('plot_staytrend_origin', 'figure'),
        Input('select_dest', 'value'),
        Input('select_year', 'value'),
        )
    def update_staytrend_origin(slct_dest, slct_year):
        if slct_year is None or slct_dest is None:
            raise PreventUpdate
        pltdf = FODnacht_df
        pltdf = pltdf.loc[(pltdf['Bestemming']==slct_dest) & (pltdf['Jaar']==slct_year)]
        pltdf = pltdf[['Herkomstland', 'Jaar', 'Maand', 'Overnachtingen']].groupby(['Herkomstland', 'Jaar', 'Maand']).sum().reset_index()
        pltdf.head()
        fig = px.line(pltdf, x='Maand', y='Overnachtingen', color='Herkomstland')
        
        return fig
    
    @app.callback(
        Output('plot_staytrend_motive', 'figure'),
        Input('select_dest', 'value'),
        Input('select_year', 'value'),
        )
    def update_staytrend_motive(slct_dest, slct_year):
        if slct_year is None or slct_dest is None:
            raise PreventUpdate
        pltdf = FODnacht_df
        pltdf = pltdf.loc[(pltdf['Bestemming']==slct_dest) & (pltdf['Jaar']==slct_year)]
        pltdf = pltdf[['Motief', 'Jaar', 'Maand', 'Overnachtingen']].groupby(['Motief', 'Jaar', 'Maand']).sum().reset_index()
        pltdf.head()
        fig = px.line(pltdf, x='Maand', y='Overnachtingen', color='Motief')
        
        return fig