import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# 1. Charger les données depuis l'URL
url = 'https://raw.githubusercontent.com/chriszapp/datasets/main/books.csv'
data = pd.read_csv(url, on_bad_lines='skip')  # Ignorer les lignes problématiques

# Nettoyage des données
data = data.dropna(subset=['  num_pages'])  # Supprimer les lignes où 'num_pages' est manquant
data['  num_pages'] = data['  num_pages'].astype(int)  # S'assurer que 'num_pages' est un entier

# 2. Créer une palette de couleurs pour les auteurs
unique_authors = data['authors'].unique()
color_palette = px.colors.qualitative.Plotly  # Palette de couleurs prédéfinie
author_color_map = {author: color_palette[i % len(color_palette)] for i, author in enumerate(unique_authors)}

# 3. Initialiser l'application Dash avec le thème Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 4. Construire le layout de l'application avec DBC
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Bibliothèque de Livres'), className='mb-4')
    ]),

    dbc.Row([
        dbc.Col([
            html.Label('Sélectionnez un auteur:'),
            dcc.Dropdown(
                id='dropdown-authors',
                options=[{'label': auteur, 'value': auteur} for auteur in unique_authors],
                value=unique_authors[0],
                style={'width': '100%'}
            )
        ], width=6),

        dbc.Col([
            html.Label('Nombre maximal de pages:'),
            dcc.Input(
                id='input-pages-max',
                type='number',
                value=500,
                style={'width': '100%'}
            )
        ], width=6)
    ], className='mb-4'),

    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='graphique-pages-par-livre',
                style={'height': '80vh', 'width': '100%'}  # Ajuster la taille du graphique
            )
        )
    ])
], fluid=True)

# 5. Callback pour mettre à jour le graphique en fonction de l'auteur sélectionné et du nombre de pages
@app.callback(
    Output('graphique-pages-par-livre', 'figure'),
    Input('dropdown-authors', 'value'),
    Input('input-pages-max', 'value')
)
def update_graph(selected_author, max_pages):
    if max_pages is None or max_pages <= 0:
        max_pages = 500  # Valeur par défaut si l'utilisateur n'a rien saisi ou a saisi une valeur invalide

    # Filtrer les données en fonction de l'auteur sélectionné et du nombre maximal de pages
    filtered_data = data[(data['authors'] == selected_author) & (data['  num_pages'] <= max_pages)]

    if filtered_data.empty:
        # Gérer le cas où aucun livre ne correspond aux critères de filtrage
        fig = px.bar(title=f'Aucun livre de {selected_author} avec moins de {max_pages} pages')
    else:
        # Trier les livres par nombre de pages et sélectionner les 10 premiers
        top_books = filtered_data.nlargest(10, '  num_pages')

        # Créer le graphique en barres avec des couleurs spécifiques pour les auteurs
        fig = px.bar(
            top_books,
            x='title',
            y='  num_pages',
            color='authors',
            color_discrete_map=author_color_map,
            title=f'Livres de {selected_author} avec moins de {max_pages} pages'
        )

    return fig

# 6. Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)
