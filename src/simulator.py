import numpy as np
import streamlit as st

st.title("Bacillus cartridge release-rate simulator")
st.caption("Screening tool. Inputs are assumptions, not measured values.")

# --- inputs ---
loss = st.slider("Loss rate (log10 per week)", 0.0, 1.5, 0.1, 0.01)
c_target = st.number_input("Target concentration (CFU/mL)", value=22000)  #22,000 = the Oliveira peak, 22.1 x 10^3 CFU/ml
v_res_l = st.number_input("Reservoir volume (L)", value=100.0)

# --- calculation ---
k_net = loss * np.log(10)                  # per week (np.log is ln)
v_ml = v_res_l * 1000
R = k_net * c_target * v_ml                # CFU per week

# --- output ---
st.metric("Release rate needed", f"{R:.2e} CFU/week")
weeks = np.arange(0, 9)
no_cart = c_target * np.exp(-k_net * weeks)    # one dose, no cartridge
st.line_chart({"One dose": no_cart, "With cartridge": [c_target] * len(weeks)})
