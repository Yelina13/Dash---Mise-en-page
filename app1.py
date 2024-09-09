import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# 1. Charger les données depuis l'URL
url = 'https://raw.githubusercontent.com/chriszapp/datasets/main/books.csv'
data = pd.read_csv(url, on_bad_lines='skip')  # Ignorer les lignes problématiques

# 2. Créer un graphique en barres avec Plotly Express
# Trier les livres par nombre de pages et sélectionner les 10 premiers
top_books = data.nlargest(10, '  num_pages')

# Créer le graphique en barres
fig = px.bar(top_books, x='title', y='  num_pages', title='Top 10 des livres par nombre de pages')

# 3. Initialiser l'application Dash
app = dash.Dash(__name__)

# 4. Construire le layout de l'application
app.layout = html.Div(children=[
    # Titre principal
    html.H1(children='Bibliothèque de Livres'),

    # Graphique en barres créé avec Plotly Express
    dcc.Graph(
        id='graphique-pages-par-livre',
        figure=fig
    ),

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
    )
])

# 5. Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)
