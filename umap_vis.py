import numpy as np
import pandas as pd
import plotly.express as px
from rdkit.Chem import PandasTools
from dash import dcc, html, Input, Output, no_update, Dash, callback
from rdkit.Chem import MolFromSmiles, Draw

app = Dash(__name__)
server = app.server

umap_df = pd.read_csv('umap_df.csv')
    # df = umap_df.loc[umap_df.set.isin(filter_sets)]
graph = dcc.Graph(id='umap-plot', clear_on_unhover=True, config=dict(scrollZoom=True))
dropdown = dcc.Dropdown(umap_df.set.unique().tolist(), 'Tox21', id='set-select', clearable=False)
tooltip = dcc.Tooltip(id='graph-tooltip')

app.layout = html.Div([dropdown, graph, tooltip])


@app.callback(Output(graph, 'figure'), Input(dropdown, 'value'))
def update_figure(dataset):
    fig = px.scatter(umap_df.loc[umap_df.set.isin(['biomolecules', dataset])],
                     x='umap1', y='umap2', color='set',
                     custom_data=['smiles'])
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
            html.Img(src=f'data:image/png;base64,{PandasTools._get_image(data)}'),
            # html.P(f'SMILES: {smiles}', style={'font-size': '6px'}),
        ], style={'width': '200px', 'white-space': 'normal'})
    ]
    return True, bbox, children, ext_data

if __name__ == '__main__':
    app.run()
