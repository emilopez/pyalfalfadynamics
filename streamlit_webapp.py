import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

import model


alfalfa_data = pd.read_csv("data/cycles_all.dat", sep=";")
fisher_params = [2.35594909, 0.86735709]
landau_params = [3.05408611, 1.71316648]
gompertz_params = [2.24074685, 3.38374238]

print("\x1b[1;92mStreamlit script running...\x1b[0m")

st.title("Alfalfa dynamics")

st.markdown("""Alfalfa growth modeling using Fisher, Landau and Gompertz models""")


data = pd.DataFrame({
    "x":alfalfa_data.tau,
    "y_mean":alfalfa_data.mean_val,
    "y_fisher": model.fisher(alfalfa_data.tau, *fisher_params),
    "y_landau": model.landau(alfalfa_data.tau, *landau_params),
    "y_gompertz":model.gompertz(alfalfa_data.tau, *gompertz_params),
})

rmse_gompertz = 0.033374733520125356
rmse_landau = 0.019534691782079044
rmse_fisher = 0.018341609219938593

st.subheader("Fitted models")
st.markdown(
"""
The alfalfa growth mean cycle was fitted with the following models:

- Fisher:   $f(x)=\\left [1 + \\beta_0 e^{-\\beta_1x} \\right ]^{-1}$
- Gompertz: $f(x) = e^{-\\beta_0 e^{-\\beta_1 x}}$
- Landau:   $f(x) =[0.5 + 0.5 \cdot \\tanh(\\beta_0 x -  \\beta_1)]^{1/2}$
""")

fig = go.Figure()
fig.add_trace(go.Scatter(x = data.x, y = data.y_mean, mode="markers", name="y_mean"))
fig.add_trace(go.Scatter(x = data.x, y = data.y_fisher, mode="lines", name=f"Fisher         | RMSE = {rmse_fisher:.3f}"))
fig.add_trace(go.Scatter(x = data.x, y = data.y_landau, mode="lines", name=f"Landau      | RMSE = {rmse_landau:.3f}"))
fig.add_trace(go.Scatter(x = data.x, y = data.y_gompertz, mode="lines", name=f"Gompertz | RMSE = {rmse_gompertz:.3f}"))
fig.update_layout(template="ggplot2", legend=dict(x=0.05, y=0.96, orientation='v'))
fig.update_layout(font = dict(size=18, color='black'))
fig.update_traces(line={'width': 3})

st.plotly_chart(fig, use_container_width=True)

st.subheader("Alfalfa normalized data")

st.markdown("""The raw data was smoothed and normalized, then the alfalfa growth cycles were averaged (12 cycles):""")

fig = go.Figure()
fig = go.Figure()
for una_curva in alfalfa_data.columns.values[1:13]:
    fig.add_trace(go.Scatter(x=alfalfa_data.tau, y=alfalfa_data[una_curva], name=una_curva, showlegend=False,
    marker=dict(color='lightgrey', opacity=1, size=10, line=dict(color='MediumPurple', width=1.5))))
fig.add_trace(go.Scatter(x = alfalfa_data.tau, y = alfalfa_data.mean_val, mode="markers+lines", name="y_mean",line=dict(color='red', width=1.5)))
fig.update_layout(template="ggplot2", legend=dict(x=0.05, y=0.96, orientation='v'))
fig.update_layout(font = dict(size=18, color='black'))
fig.update_traces(line={'width': 3})

st.plotly_chart(fig, use_container_width=True)
st.dataframe(alfalfa_data) 

st.subheader("Fisher modelling")
fisher_coef = {"ciclo_a6":[1.575,0.626],
        "ciclo_a7":[1.755,0.722],
        "ciclo_a5":[3.206,1.551],
        "ciclo_a8":[1.849,0.838],
        "ciclo_a2":[2.611,0.840],
        "ciclo_b1":[2.569,0.820],
        "ciclo_b3":[2.648,1.028],
        "ciclo_b4":[3.735,1.549],
        "ciclo_b5":[1.875,0.490],
        "ciclo_b6":[2.616,0.826],
        "ciclo_b7":[2.864,0.834],
        "ciclo_b8":[3.326,1.183]}
opciones = alfalfa_data.columns[1:-2]
# Crear la lista desplegable
cycle_op = st.radio('Growth cycle:', opciones, horizontal=True)

fig = go.Figure()
fig.add_trace(go.Scatter(x = alfalfa_data.tau, y = alfalfa_data[cycle_op], mode="markers", name="y_mean"))
fig.add_trace(go.Scatter(x = alfalfa_data.tau, y = model.fisher(alfalfa_data.tau, *fisher_coef[cycle_op]), mode="lines", name=f"Fisher"))
fig.update_layout(template="ggplot2", legend=dict(x=0.05, y=0.96, orientation='v'))
fig.update_layout(font = dict(size=18, color='black'))
fig.update_traces(line={'width': 3})

st.plotly_chart(fig, use_container_width=True)


st.markdown(
    """
### Useful links:
            
* [Gitlab repository](https://gitlab.com/emilopez/pyalfalfadynamics)
* [Gitlab static app](https://emilopez.gitlab.io/pyalfalfadynamics)
 * Author: [Emiliano López](https://gitlab.com/emilopez/)
"""
)
