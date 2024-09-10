import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# 1. Charger les données depuis l'URL
url = 'https://raw.githubusercontent.com/chriszapp/datasets/main/books.csv'
data = pd.read_csv(url, on_bad_lines='skip')  # Ignorer les lignes problématiques

# Nettoyage des données
data = data.dropna(subset=['  num_pages'])  # Supprimer les lignes où 'num_pages' est manquant
data['  num_pages'] = data['  num_pages'].astype(int)  # S'assurer que 'num_pages' est un entier

# 2. Initialiser l'application Dash
app = dash.Dash(__name__)

# 3. Construire le layout de l'application
app.layout = html.Div(children=[
    # Titre principal
    html.H1(children='Bibliothèque de Livres'),

    # Sélection d'un auteur
    html.Label('Sélectionnez un auteur:'),
    dcc.Dropdown(
        id='dropdown-authors',
        options=[{'label': auteur, 'value': auteur} for auteur in data['authors'].unique()],
        value=data['authors'].unique()[0]
    ),

    # Saisie d'un nombre maximal de pages
    html.Label('Nombre maximal de pages:'),
    dcc.Input(
        id='input-pages-max',
        type='number',
        value=500
    ),

    # Graphique en barres créé avec Plotly Express
    dcc.Graph(
        id='graphique-pages-par-livre'
    )
])

# 4. Callback pour mettre à jour le graphique en fonction de l'auteur sélectionné et du nombre de pages
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
        fig.update_layout(
          width=1500,
          height=1000 )
    else:
        # Trier les livres par nombre de pages et sélectionner les 10 premiers
        top_books = filtered_data.nlargest(10, '  num_pages')

        # Créer le graphique en barres
        fig = px.bar(top_books, x='title', y='  num_pages', title=f'Livres de {selected_author} avec moins de {max_pages} pages')
        fig.update_layout(
          width=1500,
          height=1000 )

    return fig

# 5. Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)
