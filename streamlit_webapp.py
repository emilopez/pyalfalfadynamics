import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

import model


alfalfa_data = pd.read_csv("data/cycles_all.dat", sep=";")
fisher_params = [2.35594909, 0.86735709]
landau_params = [3.05408611, 1.71316648]
gompertz_params = [2.2560388524572836, 3.5285080544747816]

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

rrmse_gompertz = 0.04887656494425247
rrmse_landau = 0.026585082154547086
rrmse_fisher = 0.02496139654509409

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
fig.add_trace(go.Scatter(x = data.x, y = data.y_fisher, mode="lines", name=f"Fisher         |% RMSE = {rrmse_fisher:.3f}"))
fig.add_trace(go.Scatter(x = data.x, y = data.y_landau, mode="lines", name=f"Landau      |% RMSE = {rrmse_landau:.3f}"))
fig.add_trace(go.Scatter(x = data.x, y = data.y_gompertz, mode="lines", name=f"Gompertz |% RMSE = {rrmse_gompertz:.3f}"))
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

st.markdown("""Each alfalfa growth cycle was fitted using Fisher model:""")

# Crear la lista desplegable
cycle_op = st.radio('Growth cycle:', opciones, horizontal=True)

fig = go.Figure()
fig.add_trace(go.Scatter(x = alfalfa_data.tau, y = alfalfa_data[cycle_op], mode="markers", name="y_mean"))
fig.add_trace(go.Scatter(x = alfalfa_data.tau, y = model.fisher(alfalfa_data.tau, *fisher_coef[cycle_op]), mode="lines", name=f"Fisher"))
fig.update_layout(template="ggplot2", legend=dict(x=0.05, y=0.96, orientation='v'))
fig.update_layout(font = dict(size=18, color='black'))
fig.update_traces(line={'width': 3})

st.plotly_chart(fig, use_container_width=True)

st.subheader("Alfalfa yield")

st.markdown("""

Alfalfa DMY (Dry Matter Yield) was computed using multiple linear regression as:

$DMY= a_1\\;\\varphi_1(t) + a_2\\;\\varphi_2(t) + a_3\\;\\varphi_3(t)$

Where

- $DMY$ is Dry Matter Yield in Tn/Ha
- $\\varphi_1(t)$ is cumulative rainfall in mm
- $\\varphi_2(t)$ is final plant height in cm
- $\\varphi_3(t)$ is cumulative $GDD$ in $^{\circ}$C-day""")

alfa_yield = pd.read_csv("data/yield.csv", sep=",", comment="#")

scatters = go.Scatter3d(
    x = alfa_yield.GDD,
    y = alfa_yield.Rainfall,
    z = alfa_yield.Ha,
    mode='markers',
    showlegend=False,
    marker=dict(
        size = alfa_yield.DMY*10.5,
        line = dict(color = "black"),
        color=alfa_yield.DMY,                # set color to an array/list of desired values
        colorscale='Blugrn',              # choose a colorscale
        opacity=0.95, 
        colorbar=dict(title='DMY [Tn/Ha]', len = 0.5),
    )
)

fig = go.Figure(data = [scatters])

fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), template="ggplot2", width=700, height=600)

fig.update_layout(
    scene=dict(
        xaxis_title='GDD [ºC * day]',
        yaxis_title='Rainfall [mm]',
        zaxis_title='Height [cm]'
    )
)

# Rango de ejes
fig.update_layout(
    scene=dict(
        xaxis=dict(range=[100, 700]), # rango eje X = GDD
        yaxis=dict(range=[-5, 300]),   # rango eje Y = Rainfall
        zaxis=dict(range=[5, 70]),    # rango eje Z = height
        aspectratio=dict(x=1.1, y=0.7, z=1)
    )
)

fig.update_layout(
    scene=dict(
        xaxis=dict(title=dict(font=dict(size=20))),
        yaxis=dict(title=dict(font=dict(size=20))),
        zaxis=dict(title=dict(font=dict(size=20))),
    )
)

st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
* [Gitlab repository](https://gitlab.com/emilopez/pyalfalfadynamics)
* [PyCafe webapp](https://py.cafe/app/emilopez/pyalfalfadynamics)
* [Streamlit webapp](https://pyalfalfadynamics.streamlit.app/)
* [Gitlab static app](https://emilopez.gitlab.io/pyalfalfadynamics)
 * Author: [Emiliano López](https://gitlab.com/emilopez/)
"""
)
