import pandas as pd
import pyreadstat

##### Set data directory parameters
indir_v = '.\\data\\'
infile_TVBewOnd2021 = 'TVBewOnd_SurveyData_2021.sav'
infile_TVBewOnd2019 = 'TVBewOnd_SurveyData_2019.sav'
infile_TVBewOnd2017 = 'TVBewOnd_SurveyData_2017.sav'
infile_TVBewOnd_mapping = 'TVBewOnd_Meta_columnmappings.xlsx'
infile_FODnacht = "FOD_OvernachtingscijfersPermaand.xlsx"

##### Read data
## TVBewOnd
TVBewOnd_df_2021, TVBewOnd_meta_2021 = pyreadstat.read_sav(indir_v + infile_TVBewOnd2021)
TVBewOnd_df_2019, TVBewOnd_meta_2019 = pyreadstat.read_sav(indir_v + infile_TVBewOnd2019)
TVBewOnd_df_2017, TVBewOnd_meta_2017 = pyreadstat.read_sav(indir_v + infile_TVBewOnd2017)

TVBewOnd_mapping_2021 = pd.read_excel(indir_v + infile_TVBewOnd_mapping, sheet_name='2021', usecols=range(0,6))
TVBewOnd_mapping_2019 = pd.read_excel(indir_v + infile_TVBewOnd_mapping, sheet_name='2019', usecols=range(0,6))
TVBewOnd_mapping_2017 = pd.read_excel(indir_v + infile_TVBewOnd_mapping, sheet_name='2017', usecols=range(0,6))

## FOD overnachtingen
FODnacht_df = pd.read_excel(indir_v + infile_FODnacht, sheet_name='per_maand')

##### Data preparation
## TVBewOnd
# Replace values with value labels
TVBewOnd_dflbl_2021=TVBewOnd_df_2021.copy()
TVBewOnd_dflbl_2019=TVBewOnd_df_2019.copy()
TVBewOnd_dflbl_2017=TVBewOnd_df_2017.copy()

TVBewOnd_datalist = [('2021', TVBewOnd_df_2021, TVBewOnd_dflbl_2021, TVBewOnd_meta_2021, TVBewOnd_mapping_2021), 
            ('2019', TVBewOnd_df_2019, TVBewOnd_dflbl_2019, TVBewOnd_meta_2019, TVBewOnd_mapping_2019), 
            ('2017', TVBewOnd_df_2017, TVBewOnd_dflbl_2017, TVBewOnd_meta_2017, TVBewOnd_mapping_2017)]

# map values to labels
for i, (yr, df, df_lbl, meta, mapping) in enumerate(TVBewOnd_datalist):
    mapdict = meta.variable_value_labels
    statdata = df_lbl
    statmeta = meta
    for colname in statdata.columns:
        if colname in statmeta.variable_value_labels.keys():
            statdata[colname]=statdata[colname].map(mapdict[colname])
    df_lbl =statdata.copy()
    
# Create Analysis tabel with constructs
# TVBewOnd_constructlist = ['Fierheid', 'Economic empowerment', 'Social empowerment', 'Political empowerment', 'Support', 
#               'Positieve impact', 'Negatieve impact', 'Leefbaarheid']
# TVBewOnd_df_constructs = pd.DataFrame(columns = ['Jaar', 'Stad'] + TVBewOnd_constructlist)
# for i, (yr, df, df_lbl, meta, mapping) in enumerate(TVBewOnd_datalist):
#     # constructcols = mapping.loc[(mapping['construct'].isin(TVBewOnd_constructlist)) & (mapping['Type data']=='Constructscore')]
#     constructcols = mapping.loc[(mapping['usage']=='Constructscore')]
#     df_constr = df.loc[:,['Q_stad']+ constructcols.iloc[:,0].tolist()]
#     newcols = ['Stad'] + constructcols.iloc[:,2].tolist()
#     df_constr.columns = newcols
#     df_constr['Jaar'] = yr
#     df_constr['Stad']=df_constr['Stad'].map(meta.variable_value_labels['Q_stad'])  
#     TVBewOnd_df_constructs = pd.concat([TVBewOnd_df_constructs, df_constr])

# TVBewOnd_df_constructs_stacked = TVBewOnd_df_constructs.set_index(['Jaar','Stad' ], append=True)
# TVBewOnd_df_constructs_stacked=TVBewOnd_df_constructs_stacked.stack().to_frame().reset_index().drop('level_0', axis=1)
# TVBewOnd_df_constructs_stacked.columns=['Jaar', 'Stad', 'Construct', 'Gemiddelde']




# Create tabel with all constructitems all respondents
import uuid

TVBewOnd_df_constritems = pd.DataFrame(columns = ['Jaar', 'Stad', 'Vraagcode', 'Vraaglabel', 'Construct', 'Weging', 'Score'])
colname_weging = {'2017': 'weging_final', '2019': 'WegingFinal', '2021': 'Weging'}
for i, (yr, df, df_lbl, meta, mapping) in enumerate(TVBewOnd_datalist):
    constructmapping = mapping.loc[(mapping['usage']=='Constructscore')]
    df_items = df.loc[:,['Q_stad'] + [colname_weging[yr]] + constructmapping.iloc[:,0].tolist()]
    df_items.rename(columns={colname_weging[yr] : 'Weging'}, inplace=True)
    df_items['Q_stad']=df_items['Q_stad'].map(meta.variable_value_labels['Q_stad'])
    df_items['resp_id'] = df_items.index.to_series().map(lambda x: uuid.uuid4())
    df_items = df_items.set_index(['resp_id', 'Q_stad', 'Weging']).stack().to_frame().reset_index()
    df_items.columns = ['resp_id', 'Stad', 'Weging', 'Vraagcode', 'Score']
    df_items['Jaar']=yr
    # map vraaglabeles
    mapdict = mapping.iloc[:,[0,1]]
    mapdict = mapdict.set_index(mapdict.columns[0])
    mapdict = mapdict.to_dict()[mapdict.columns[0]]
    df_items['Vraaglabel']=df_items['Vraagcode'].map(mapdict)
    # map construct
    mapdict = mapping.iloc[:,[0,2]]
    mapdict = mapdict.set_index(mapdict.columns[0])
    mapdict = mapdict.to_dict()[mapdict.columns[0]]
    df_items['Construct']=df_items['Vraagcode'].map(mapdict)
    TVBewOnd_df_constritems = pd.concat([TVBewOnd_df_constritems, df_items])

# Summary table by respondent 
TVBewOnd_df_constrresp= TVBewOnd_df_constritems.groupby(['Stad', 'Jaar','Construct', 'resp_id']).mean().reset_index()

# calculate constructscore summary table
TVBewOnd_df_constr= TVBewOnd_df_constrresp
TVBewOnd_df_constr['Score_Gew']=TVBewOnd_df_constr['Score']*TVBewOnd_df_constr['Weging']
TVBewOnd_df_constr=TVBewOnd_df_constr.groupby(['Stad', 'Jaar','Construct'])
TVBewOnd_df_constr=TVBewOnd_df_constr['Score_Gew'].mean().reset_index()
TVBewOnd_df_constr.rename(columns={'Score_Gew':'Score'}, inplace=True)

# Create city selection list
TVBewOnd_citylist = TVBewOnd_df_constr['Stad'].unique()
TVBewOnd_cityoptions = []
for item in TVBewOnd_citylist:
    TVBewOnd_cityoptions.append({'label':item, 'value':item})

# Create construct selection list
TVBewOnd_constrlist = TVBewOnd_df_constr['Construct'].unique()
TVBewOnd_constroptions = []
for item in TVBewOnd_constrlist:
    TVBewOnd_constroptions.append({'label':item, 'value':item})


## FOD overnachtingen
# Remove calculated records
FODnacht_df['Jaar']=FODnacht_df['Jaar'].astype('str')
FODnacht_df=FODnacht_df[(FODnacht_df['Herkomstland']!='Algemeen totaal') & (FODnacht_df['Herkomstland']!='Totaal buitenland')]

# Create destination lists
FODnacht_destlist = FODnacht_df['Bestemming'].unique()
FODnacht_destoptions = []
for item in FODnacht_destlist:
    FODnacht_destoptions.append({'label':item, 'value':item})

# Create year selection list
FODnacht_yearlist = FODnacht_df['Jaar'].unique()
FODnacht_yearoptions = []
for item in FODnacht_yearlist:
    FODnacht_yearoptions.append({'label':item, 'value':item})