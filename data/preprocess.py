import pandas as pd
import geopandas as gpd
import pyreadstat
import uuid

######!!!====== TVBewOnd =====!!!######
##### Set data directory parameters
indir_v = '.\\data\\input\\'
infile_TVBewOnd2021 = 'TVBewOnd_SurveyData_2021.sav'
infile_TVBewOnd2019 = 'TVBewOnd_SurveyData_2019.sav'
infile_TVBewOnd2017 = 'TVBewOnd_SurveyData_2017.sav'
infile_TVBewOnd_mapping = 'TVBewOnd_Meta_columnmappings.xlsx'

##### Read data
TVBewOnd_df_2021, TVBewOnd_meta_2021 = pyreadstat.read_sav(indir_v + infile_TVBewOnd2021)
TVBewOnd_df_2019, TVBewOnd_meta_2019 = pyreadstat.read_sav(indir_v + infile_TVBewOnd2019)
TVBewOnd_df_2017, TVBewOnd_meta_2017 = pyreadstat.read_sav(indir_v + infile_TVBewOnd2017)

TVBewOnd_mapping_2021 = pd.read_excel(indir_v + infile_TVBewOnd_mapping, sheet_name='2021', usecols=range(0,6))
TVBewOnd_mapping_2019 = pd.read_excel(indir_v + infile_TVBewOnd_mapping, sheet_name='2019', usecols=range(0,6))
TVBewOnd_mapping_2017 = pd.read_excel(indir_v + infile_TVBewOnd_mapping, sheet_name='2017', usecols=range(0,6))



##### Data preparation
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
    


# Create tabel with all constructitems all respondents
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


######!!!====== FOD overnachtingen =====!!!######
##### Set data directory parameters
indir_v = '.\\data\\input\\'
infile_FODnacht = "FOD_OvernachtingscijfersPermaand.xlsx"

##### Read data
FODnacht_df = pd.read_excel(indir_v + infile_FODnacht, sheet_name='per_maand')


# Remove calculated records
FODnacht_df['Jaar']=FODnacht_df['Jaar'].astype('str')
FODnacht_df=FODnacht_df[(FODnacht_df['Herkomstland']!='Algemeen totaal') & (FODnacht_df['Herkomstland']!='Totaal buitenland')]

##### Data preparation
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



######!!!====== proximus profile data 2020 (students) =====!!!######
##### Set data directory parameters
root = '.\\'
indir = root + 'data\\input\\'
# infile_timeslots = 'prox_timeslots.csv'
# infile_staytime = 'prox_staytimecategory.csv'
infile_users_hourly = 'prox_users_hourly.csv'
infile_users_daily = 'prox_users_daily.csv'
infile_celluse_daily = 'prox_celluse_daily.csv'
infile_proxcells = 'ref_proxcells.shp'
infile_hexcells = 'ref_hexcells.shp'
infile_proxhex = 'ref_cellmapping_proxhex.shp'
infile_calendar = 'prox_calendar.csv'
infile_profiles='ref_profiles.csv'
infile_period = 'ref_period.csv'

##### Read data
df_calendar = pd.read_csv(indir + infile_calendar,';')
# ts_users_hourly = pd.read_csv(indir + infile_users_hourly,';')
# ts_users_daily = pd.read_csv(indir + infile_users_daily,';')
# ts_celluse_daily = pd.read_csv(indir + infile_celluse_daily,';')
ts_users_hourly_hex = pd.read_csv(indir + infile_users_hourly.replace('.csv', '_hex_dev.csv'),';',dtype=str)
ts_users_daily_hex = pd.read_csv(indir + infile_users_daily.replace('.csv', '_hex.csv'),';', dtype=str)
ts_celluse_daily_hex = pd.read_csv(indir + infile_celluse_daily.replace('.csv', '_hex.csv'),';', dtype=str)
gdf_proxcells = gpd.read_file(indir + infile_proxcells)
gdf_hexcells = gpd.read_file(indir + infile_hexcells)
# gdf_proxhex = gpd.read_file(indir + infile_proxhex)
df_profiles=pd.read_csv(indir + infile_profiles,';')
# df_period = pd.read_csv(indir + infile_period,';')   


##### Data preparation
# rename attributes
gdf_proxcells=gdf_proxcells.rename(columns={'tacs':'cell'})
gdf_hexcells=gdf_hexcells.rename(columns={'hexid':'cell'})
df_calendar=df_calendar.rename(columns={'category_nl':'period'})

# prep function
def prep_proxdata2020(df, df_profiles, df_calendar, freq, types_dict = {'count': float, 'count_extrapolated': float}):
    # Set attribute types
    for col, col_type in types_dict.items():
        df[col] = df[col].astype(col_type)
    # Join profile names
    df = df.merge(df_profiles, how='left', left_on='profile', right_on='profile_code')
    
    # # Extrapolate counts
    # marketshares= {'Kotstudent': 0.27, 'default':0.38}
    # df=extrapolate(prepdata, 'count', 'count_extrapolated', 'profile', marketshares)
    
    if freq=='hourly':
        # format timestamp
        df['timestamp'] = df['date'] + ' ' + df['time']
        df['timestamp'] =  pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S')
        df.drop('period', axis=1)
    elif freq == 'daily':
        # format timestamp
        df['timestamp'] =  pd.to_datetime(df['date'], format='%Y-%m-%d')
    # Join period names
    df = df.merge(df_calendar[['date','period']], how='left', left_on='date', right_on='date')

    # set timeseries index
    df = df.set_index(['timestamp'])
    return df

# ts_users_hourly = prep_proxdata2020(ts_users_hourly, df_profiles, df_calendar, freq='hourly', types_dict = {'count': float, 'count_extrapolated': float})
# ts_users_daily = prep_proxdata2020(ts_users_daily, df_profiles, df_calendar, freq='daily', types_dict = {'count': float, 'count_extrapolated': float})
# ts_celluse_daily = prep_proxdata2020(ts_celluse_daily, df_profiles, df_calendar, freq='daily', types_dict = {'count': float, 'count_extrapolated': float})
ts_users_hourly_hex = prep_proxdata2020(ts_users_hourly_hex, df_profiles, df_calendar, freq='hourly', types_dict = {'count': float, 'count_extrapolated': float})
ts_users_daily_hex = prep_proxdata2020(ts_users_daily_hex, df_profiles, df_calendar, freq='daily', types_dict = {'count': float, 'count_extrapolated': float})
ts_celluse_daily_hex = prep_proxdata2020(ts_celluse_daily_hex, df_profiles, df_calendar, freq='daily', types_dict = {'count': float, 'count_extrapolated': float})
    
ts_users_hourly_hex =ts_users_hourly_hex[['cell', 'profile_code', 'profile', 'profile_name', 'profile_order', 'period_y', 'count', 'count_extrapolated']].rename(columns={'period_y':'period'})
ts_users_hourly_hex['cl']=0
ts_celluse_daily_hex['cl']=0
ts_users_daily_hex['cl']=0
ts_celluse_daily_hex['dayofweek']=ts_celluse_daily_hex.index.dayofweek
ts_celluse_daily_hex['dagvdweek'] = ts_celluse_daily_hex['dayofweek'].map({0:'Ma', 1:'Di', 2:'Wo', 3:'Do', 4:'Vr', 5:'Za', 6:'Zo'})


## Calculate surface area
gdf_proxcells['area']=gdf_proxcells.geometry.area 


# Get datetime indexes
datetimeindex = ts_users_hourly_hex.index.values
datetimerange = [datetimeindex.min(),datetimeindex.max()]
datetimerange = [str(pd.Timestamp(x)) for x in datetimerange]
dateindex = pd.date_range(start=datetimerange[0], end=datetimerange[1], freq='D')
weekindex=dateindex[dateindex.dayofweek==0]
monthindex= pd.date_range(start=datetimerange[0], end=datetimerange[1], freq='MS')
datetimeindexes= {'datetime': datetimeindex, 
                  'date': dateindex.strftime("%Y-%m-%d").tolist(),
                  'week': weekindex.strftime("%Y-%m-%d").tolist(),
                  'month': monthindex.strftime("%Y-%m-%d").tolist()}

## List of used profiles
profileoptions =pd.DataFrame(ts_users_hourly_hex['profile_name'].unique(), columns=['profile'])
profileoptions = profileoptions.merge(df_profiles, 'left', left_on='profile', right_on='profile_name')
profileoptions = profileoptions.sort_values(['profile_order'])
#profileoptions = list(profileoptions.profile_name)
profileoptions = list(map(dict,map(lambda t: zip(('label','value'),t), zip(profileoptions['profile_name'], profileoptions['profile_code']))))






######!!!====== data =====!!!######
##### Set data directory parameters
##### Read data
##### Data preparation