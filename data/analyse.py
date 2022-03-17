import pandas as pd
import geopandas as gpd

from sklearn import cluster
from sklearn.preprocessing import scale


######!!!============================ Analysis functions ============================######

def cluster_celluse(df, measure='count', select=None, datetimerange=None, sampleidx = 'cell', clusterattrs=None, n_clust=5, aggrfunc='mean' ):
    # Filter data
    if select is None:
        select = {}
    # Filter data
    for key in select.keys():
        df = df[df[key].isin(select[key])]
    if datetimerange:
        df = df.loc[datetimerange[0]:datetimerange[1],:]
    if clusterattrs is None:
        clusterattrs=list(df.columns)
        clusterattrs.remove(measure)
        
    # Prep data for visualisation 
    if aggrfunc=='mean':
        df = df.loc[:,clusterattrs + [sampleidx, measure]].groupby(by=clusterattrs + [sampleidx]).mean()
        df = df.unstack([0,1,2])
        df = df.fillna(0)
        df = df.droplevel(level=0, axis=1)

    # Standardize a dataset along any axis, Center to the mean and component wise scale to unit variance.
    df_clust = pd.DataFrame(scale(df), index=df.index, columns=df.columns).rename(lambda x: str(x))
    
    # Apply clustering on scaled df
    km5 = cluster.KMeans(n_clusters=n_clust)
    km5cls = km5.fit(df_clust)
    # print(len(km5cls.labels_))
    
    df["cl"] = km5cls.labels_
                    
    return df
