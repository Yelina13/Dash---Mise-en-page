from dash import Dash, html, dcc

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Titre Principal"),
    html.P("Ceci est un paragraphe décrivant le contenu de la page."),
    html.A("Lien vers la Wild Code School", href="https://www.wildcodeschool.com/"),

    html.Ul([
        html.Li("Premier élément"),
        html.Li("Deuxième élément"),
        html.Li("Troisième élément")
    ]),
    html.Img(src="https://www.wildcodeschool.com/hs-fs/hubfs/booster-carriere.png?width=575&height=620&name=booster-carriere.png"),

    dcc.Dropdown(
        id='dropdown-exemple',
        options=[{'label': i, 'value': i} for i in ['Option 1', 'Option 2']],
        value='Option 1'
    ),
    dcc.Graph(id='graph-exemple'),

    dcc.Input(id='input-exemple', type='text', value='Texte initial'),
    dcc.Slider(min=0, max=10, step=0.5, value=5),
    dcc.RadioItems(
        id='radioitems-exemple',
        options=[{'label': i, 'value': i} for i in ['Option A', 'Option B']],
        value='Option A'
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
