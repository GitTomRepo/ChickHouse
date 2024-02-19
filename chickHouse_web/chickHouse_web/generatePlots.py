import plotly as px
import plotly.graph_objects as go
import pandas as pd
from .doorCTRL import doorCTRL

def doorEvents_bar (door:doorCTRL) :
    nb_opening = door.df_events[door.df_events['TypeEvent'] == True].groupby([door.df_events['DateTimeEvent'].dt.date]).apply(len).reset_index()
    nb_closing = door.df_events[door.df_events['TypeEvent'] == False].groupby([door.df_events['DateTimeEvent'].dt.date]).apply(len).reset_index()
    
    nb_opening.columns = ['DateTimeEvent', 'LEN']
    nb_closing.columns = ['DateTimeEvent', 'LEN']

    nb_opening['DateTimeEvent'] = nb_opening['DateTimeEvent'].astype(str)
    nb_closing['DateTimeEvent'] = nb_closing['DateTimeEvent'].astype(str)

    fig = go.Figure()
    fig.add_bar(y=nb_opening['DateTimeEvent'], x=nb_opening['LEN'], name="Ouverture", orientation='h')
    fig.add_bar(y=nb_closing['DateTimeEvent'], x=nb_closing['LEN'], name="Fermeture", orientation='h')


    fig.update_layout(
        yaxis=dict(tickformat="%d/%m/%Y", tickangle=90, fixedrange=True),
        xaxis=dict(fixedrange=True),
        title = "Ouverture/Fermeture de la porte",
        margin=dict(l=5, r=5, t=50, b=5)
    )
    fig['layout']['xaxis'].update(autorange = True)
    config = {'scrollZoom': False}

    return fig.to_html(full_html=False, config=config)