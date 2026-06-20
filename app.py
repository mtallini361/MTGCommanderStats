# Import packages
from dash import Dash, html
import dash_ag_grid as dag
import pandas as pd

# Incorporate data
df = pd.read_csv('/home/mtall/MTGCommanderStats/game_records.csv')

# Initialize the app
app = Dash()

# App layout
app.layout = [
    html.Div(children='My First App with Data'),
    dag.AgGrid(
        rowData=df.to_dict('records'),
        columnDefs=[{"field": i} for i in df.columns]
    )
]

# Run the app
if __name__ == '__main__':
    app.run(debug=True)