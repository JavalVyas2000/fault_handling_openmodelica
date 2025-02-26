import pandas as pd
import plotly.express as px
def plot_fig(df):
    # plotting some dfs in plotly
    fig = px.scatter(df, title="reconf benchmark datasets")
    fig.show()
    return

df1 = pd.read_csv("C:/Users/jv624/Desktop/fault_handling_openmodelica/data/ds2/ds2_hybrid_s.csv")

df_list = [df1]

for df in df_list:
    plot_fig(df)