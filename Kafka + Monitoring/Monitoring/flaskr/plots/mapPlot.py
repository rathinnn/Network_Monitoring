
def updateMap(go,df,px,ACCESS_TOKEN):
    coors = {1:[17.38,78.48], 2:[17.1,79.48], 3:[16.38,78.48], 4:[17.38,79.48]}
    fig = go.Figure(px.scatter_mapbox(
            
            lat = [coors[x][0] for x in df['server_id']],
            lon = [coors[x][1] for x in df['server_id']],
            size= df['count']
           
            
        ))
    
    fig.update_layout(
    mapbox=dict(
        accesstoken=ACCESS_TOKEN,
        
        zoom=6
        )
    )
    return fig
    

    

  
   