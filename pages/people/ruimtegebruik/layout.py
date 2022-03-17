from dash import html, dcc
import plotly.express as px

from layout.structure.grid import Column, Row
from components.tiles import pagetitletile, subtitletile, infotile, filtertile, plottile, tile

from data.preprocess import ts_celluse_daily_hex
from data.analyse import cluster_celluse

### GENERIC LAYOUT FUNCTIONS ### 
# graph function to add default layout styles?



### DEFINE PAGE DEFAULTS ###
# dflt_constructs = ['Fierheid', 'Leesbaarheid', 'Support']
# dflt_city = 'Gent'
dflt_select={'profile':['Inwoner', 'Pendelaar'], 'period':['academiejaar'],
                'celltype':['visit_cell','working_cell','study_cell'], 'staytype':['visit']}

pagetitle = 'Ruimtegebruik'
pageinfo = ('Gentgebruikers gebruiken de stad Gent op heel wat verschillende manieren: om te leven, te werken, te studeren of te bezoeken. '
             'Op deze pagina wordt elke zone van de stad getypeerd op basis van het ruimtegebruik. '
             'Via clustering kunnen de zones worden gegroepeerd in clusters met gelijkaardig ruimtegebruik. '
             'Filter de gewenste periode en het gewenste gebruikersprofiel en klik op de knop. '
             ' Zo analyseer je hoe de stad wordt gebruikt. ')

### 
prox_ts_celluse_daily_hex_clust = cluster_celluse(df=ts_celluse_daily_hex, measure='count', 
                                                  select={'profile':dflt_select['profile']}, datetimerange=None, 
                                                  sampleidx='cell', clusterattrs=['dagvdweek',  'profile', 'celltype'],
                                                  n_clust=1)

### DEFINE CONTENT ###
# def filter_period(comp_id:str):
#     filtercomp =dcc.Checklist(
#         id=comp_id, 
#         className='text-uppercase',
#         options=TVBewOnd_constroptions, 
#         value=dflt_constructs,
#         labelStyle={'margin-right': '0.5rem'},
#         inputStyle={'margin-right': '0.25rem'}
#         )
#     content = filtertile(children=[
#         html.Label('Selecteer construct(en):'),
#         filtercomp])
#     return content

def filter_user(comp_id:str):
    content = ''
    return content

def filter_staytype(comp_id:str):
    content = ''
    return content

def filter_dayofweek(comp_id:str):
    content = ''
    return content


### BUILD LAYOUT ###
layout = Column(children=[
    Row(content=pagetitletile(pagetitle)),
    Row(content=infotile(pageinfo)),
    Row(children=[
        Column(children=[
            Row(content=subtitletile('Filter data voor clustering')),
            ]),
        Column(children=[
            Row(content=subtitletile('Cluster zones op basis van ruimtegebruik')),
            ])
        ])
    
    
    
    
    
    # Row(children=[
    #     Column(content=filter_city(comp_id='select_city')),
    #     Column(content=filter_construct(comp_id='select_construct'))
    #     ]),
    # Row(children=[
    #     Column(children=[
    #         Row(content=plottile_radar(comp_id='plot_radar'),
    #             ),
    #         Row(content=plottile_table(comp_id='plot_table')
    #             ),
    #         ]),
    #     Column(children=[
    #         Row(content=plottile_dist(comp_id='plot_dist'))
    #         ])
    #     ])
]).get_layout()
