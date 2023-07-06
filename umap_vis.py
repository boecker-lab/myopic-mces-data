import numpy as np
import pandas as pd
import plotly.express as px
from rdkit.Chem import PandasTools
from dash import dcc, html, Input, Output, no_update
from jupyter_dash import JupyterDash
from rdkit.Chem import MolFromSmiles, Draw

app = JupyterDash(__name__)

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
    data = Draw._moltoimg(MolFromSmiles(smiles), (200, 200), [], '', returnPNG=True, kekulize=True)
    children = [
        html.Div([
            html.Img(src=f'data:image/png;base64,{PandasTools._get_image(data)}'),
            html.P(f'SMILES: {smiles}'),
        ], style={'width': '200px', 'white-space': 'normal'})
    ]
    return True, bbox, children, ext_data


def get_dash_app(filter_sets=None):
    umap_df = pd.read_csv('umap_df.csv')
    if filter_sets is not None:
        df = umap_df.loc[umap_df.set.isin(filter_sets)]
    else:
        df = umap_df

    fig = px.scatter(df, x='umap1', y='umap2', color='set',
                     custom_data=['smiles'])
    fig.update_traces(hoverinfo='none', hovertemplate=None)
    fig.update_layout(width=800, height=700)
    fig.update_layout(clickmode='event+select')
    app.layout = html.Div([html.Div(dcc.Graph(id='umap-plot', figure=fig, clear_on_unhover=True),
                                    style={'display': 'inline-block'}),
                           dcc.Tooltip(id='graph-tooltip')],
                          style={'display': 'inline-block'})
    return app

if __name__ == '__main__':
    app = get_dash_app()
    app.run()
