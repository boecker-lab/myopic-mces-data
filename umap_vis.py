import numpy as np
import pandas as pd
import plotly.express as px
from rdkit.Chem import PandasTools
from dash import dcc, html, Input, Output, no_update, Dash, callback
from rdkit.Chem import MolFromSmiles, Draw
import os

dash_settings = {}
# for reverse proxy, add prefix to dash app settings
try:
    dash_settings.update({
        'requests_pathname_prefix': os.environ['PROXY_PREFIX_REQUESTS'],
        'routes_pathname_prefix': os.environ['PROXY_PREFIX_ROUTES']
    })
    dash_settings.update({
                'url_base_pathname': os.environ['PROXY_PREFIX_URL'],
    })
except:
    pass

app = Dash(__name__, **dash_settings)
server = app.server


umap_df = pd.read_csv('umap_df.csv')
graph = dcc.Graph(id='umap-plot', clear_on_unhover=True, config=dict(scrollZoom=True))
dropdown = dcc.Dropdown(umap_df.set.unique().tolist(), 'Tox21', id='set-select', clearable=False)
tooltip = dcc.Tooltip(id='graph-tooltip')

app.layout = html.Div([dropdown, graph, tooltip], style=dict(width='200px'))


@app.callback(Output(graph, 'figure'), Input(dropdown, 'value'))
def update_figure(dataset):
    fig = px.scatter(umap_df.loc[umap_df.set.isin(['biomolecules', dataset])],
                     x='umap1', y='umap2', color='set',
                     custom_data=['smiles', 'name', 'classyfire_labels'],
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
    smiles, name, classes = pt['customdata']
    ext_data = no_update
    data = Draw._moltoimg(MolFromSmiles(smiles), (200, 200), [], '', returnPNG=True)
    children = [
        html.Div([
            #html.H4(name),
            html.Img(src=f'data:image/png;base64,{PandasTools._get_image(data)}',
                     alt='SMILES: ' + smiles,
                     style=dict(float='left', margin='0px 15px 15px 0px', height=200, width=200, border=2)),
            html.Div([
                html.P('ClassyFire classes'),
                html.Ul([html.Li(c, style={'font-size': '10pt'}) for c in classes.split('; ')])
            ] if classes is not None else [])
            # html.P(f'SMILES: {smiles}', style={'font-size': '6px'}),
        ], style={'width': '200px', 'white-space': 'normal'})
    ]
    return True, bbox, children, ext_data

if __name__ == '__main__':
    app.run()
