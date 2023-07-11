import numpy as np
import pandas as pd
import plotly.express as px
from rdkit.Chem import PandasTools
from dash import dcc, html, Input, Output, no_update, Dash, callback
from rdkit.Chem import MolFromSmiles, Draw
import os

app = Dash(__name__)
server = app.server

# for reverse proxy, add prefix to dash app settings
if (os.environ.get('PROXY_PREFIX', '') != ''):
    app.config.update({
        'routes_pathname_prefix': os.environ['PROXY_PREFIX'],
        'requests_pathname_prefix': os.environ['PROXY_PREFIX']
    })

umap_df = pd.read_csv('umap_df.csv')
    # df = umap_df.loc[umap_df.set.isin(filter_sets)]
graph = dcc.Graph(id='umap-plot', clear_on_unhover=True, config=dict(scrollZoom=True))
dropdown = dcc.Dropdown(umap_df.set.unique().tolist(), 'Tox21', id='set-select', clearable=False)
tooltip = dcc.Tooltip(id='graph-tooltip')

app.layout = html.Div([dropdown, graph, tooltip], style=dict(width='200px'))


@app.callback(Output(graph, 'figure'), Input(dropdown, 'value'))
def update_figure(dataset):
    fig = px.scatter(umap_df.loc[umap_df.set.isin(['biomolecules', dataset])],
                     x='umap1', y='umap2', color='set',
                     custom_data=['smiles'],
                     template='simple_white',
                     color_discrete_map={'biomolecules': '#aaaaaa'} |
                     {s: '#fc054b' for s in umap_df.set.unique().tolist() if s != 'biomolecules'})
    fig.update_traces(hoverinfo='none', hovertemplate=None)
    fig.update_traces(marker={'size': 2})
    fig.update_layout(
        dragmode='pan',
        width=800, height=700,
    )
    return fig


@app.callback(
    Output('graph-tooltip', 'show'),
    Output('graph-tooltip', 'bbox'),
    Output('graph-tooltip', 'children'),
    Output('umap-plot', 'extendData'),
    Input('umap-plot', 'hoverData'),
)
def display_hover(hoverData):
    if hoverData is None:
        return False, no_update, no_update, no_update
    pt = hoverData['points'][0]
    if ('customdata' not in pt): # hovering over highlight
        return False, no_update, no_update, no_update
    bbox = pt['bbox']
    smiles, = pt['customdata']
    ext_data = no_update
    data = Draw._moltoimg(MolFromSmiles(smiles), (200, 200), [], '', returnPNG=True)
    children = [
        html.Div([
            html.Img(src=f'data:image/png;base64,{PandasTools._get_image(data)}',
                     alt='SMILES: ' + smiles,
                     style=dict(float='left', margin='0px 15px 15px 0px', height=120, width=120, border=2)),
            # html.P(f'SMILES: {smiles}', style={'font-size': '6px'}),
        ], style={'width': '120px', 'white-space': 'normal'})
    ]
    return True, bbox, children, ext_data

if __name__ == '__main__':
    app.run()
