import numpy as np
import pandas as pd
import plotly.express as px
from rdkit.Chem import PandasTools
from dash import dcc, html, Input, Output, no_update, Dash, callback
from rdkit.Chem import MolFromSmiles, Draw
import os

COLOR_MAPPING = {'Amino acids, peptides, and analogues': '#fe9929',
                 'Peptides': '#cc4c02',
                 'Fatty Acyls': '#fc9272',
                 'Glycerolipids': '#ef3b2c',
                 'Glycerophospholipids': '#99000d',
                 'Cholines': '#67000d',
                 'Amines': '#fff7bc',
                 'Trialkylamines': '#fee391',
                 'Sphingolipids': '#df65b0',
                 'Organoheterocyclic compounds': '#dadaeb',
                 'Benzenoids': '#6a51a3',
                 'Diazines': '#3300cc',
                 'Azoles': '#3f007d',
                 'Steroids and steroid derivatives': '#c7e9c0',
                 'Prenol lipids': '#41ab5d',
                 'Triterpenoids': '#00441b',
                 'Bile acids, alcohols and derivatives': '#02818a',
                 'Phenylpropanoids and polyketides': '#a6cee3',
                 'Carbohydrates and carbohydrate conjugates': '#fccde5',
                 'Organosulfur compounds': '#ffea19',
                 'Other': '#b6b6b6'}

# for reverse proxy, add prefix to dash app settings
dash_settings = {}
try:
    for env in ['PROXY_PREFIX_ROUTES', 'PROXY_PREFIX_REQUESTS', 'PROXY_PREFIX_URL']:
        if (os.environ.get(env, '') != ''):
            dash_settings.update({
                {'PROXY_PREFIX_ROUTES': 'routes_pathname_prefix',
                 'PROXY_PREFIX_REQUESTS': 'requests_pathname_prefix',
                 'PROXY_PREFIX_URL': 'url_base_pathname'}[env]: os.environ[env]
            })
except Exception as e:
    print('failed setting proxy setting in Dash', e)

app = Dash(__name__, title='UMAP-MCES Visualization',
           **dash_settings)
server = app.server

umap_df = pd.read_csv('umap_df.csv')
graph = dcc.Graph(id='umap-plot', clear_on_unhover=True, config=dict(scrollZoom=True))
dropdown = dcc.Dropdown(umap_df.set.unique().tolist(), 'Tox21', id='set-select', clearable=False)
tooltip = dcc.Tooltip(id='graph-tooltip')

app.layout = html.Div([dropdown, graph, tooltip], style=dict(width='200px'))


@app.callback(Output(graph, 'figure'), Input(dropdown, 'value'))
def update_figure(dataset):
    if (dataset == 'biomolecules'):
        # special plot with ClassyFire classes colored
        fig = px.scatter(umap_df.loc[umap_df.set == 'biomolecules'],
                     x='umap1', y='umap2', color='classyfire_label',
                     custom_data=['smiles', 'name', 'classyfire_labels'],
                     template='simple_white',
                     color_discrete_map=COLOR_MAPPING)
    else:
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
        width=970 if dataset == 'biomolecules' else 800, height=700,
        legend={'itemsizing': 'constant'},
        legend_title_text=None
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
            html.H5(name),
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
