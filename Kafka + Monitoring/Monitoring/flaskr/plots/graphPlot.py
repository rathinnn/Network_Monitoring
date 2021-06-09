
def updateMethod(px,df):
    #df = tdf.sort("Date")
    
    fig = px.pie(df,values = 'count', names = 'method')

    return fig

def updateStatus(px,df):
    #df = tdf.sort("Date")
    
    fig = px.pie(df,values = 'count', names = 'status')

    return fig
    
def updateSearch(px,df):
    
    df = df.head(4)
    fig = px.bar(df,x = 'url',y = 'count')

    fig.update_layout(
        title = "Most Requests for Websites",
        )
    
    return fig

def updateTotal(px,df):
    
    
    fig = px.bar(df,x = 'server_id',y = 'count')

    fig.update_layout(
        title = 'Total Requests',
       )
    
    
    
    return fig

def updateBlocked(px,df):
    
    fig = px.bar(df,x = 'server_id',y = 'count')

    fig.update_layout(
        title = "Requests Blocked",
        xaxis={'categoryorder':'category ascending'})
    
    
    
    return fig

    

    
