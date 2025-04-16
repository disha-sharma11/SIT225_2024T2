import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time

# Load latest CSV file dynamically
def load_latest_data():
    files = sorted([f for f in os.listdir() if f.startswith("gyroscope_data") and f.endswith(".csv")])
    if files:
        return pd.read_csv(files[-1])  # Load the most recent file
    return None

df = load_latest_data()
if df is None:
    st.error("No data file found.")
    st.stop()

# Sidebar controls
st.sidebar.header("Controls")
graph_type = st.sidebar.selectbox("Choose a graph type", ['scatter', 'line', 'bar', 'histogram', 'box', 'violin'])
columns = st.sidebar.multiselect("Choose columns", df.columns[1:], default=['x'])

# Sample size selection with manual input
sample_size = st.sidebar.text_input("Number of samples", "100")
try:
    sample_size = int(sample_size)
    if sample_size <= 0:
        raise ValueError
except ValueError:
    st.warning("Please enter a valid positive number.")
    sample_size = 100

# Pagination controls
if "start_idx" not in st.session_state:
    st.session_state.start_idx = 0

max_idx = max(0, len(df) - sample_size)
prev_button = st.sidebar.button("Previous")
next_button = st.sidebar.button("Next")

if prev_button:
    st.session_state.start_idx = max(0, st.session_state.start_idx - sample_size)
if next_button:
    st.session_state.start_idx = min(max_idx, st.session_state.start_idx + sample_size)

df_subset = df.iloc[st.session_state.start_idx:st.session_state.start_idx + sample_size]

# Create graph
fig = None
if graph_type == "scatter":
    fig = px.scatter(df_subset, x=df_subset.index, y=columns, title="Scatter Plot")
elif graph_type == "line":
    fig = px.line(df_subset, x=df_subset.index, y=columns, title="Line Chart")
elif graph_type == "bar":
    fig = px.bar(df_subset, x=df_subset.index, y=columns, title="Bar Chart")
elif graph_type == "histogram":
    fig = px.histogram(df_subset, x=columns, title="Histogram")
elif graph_type == "box":
    fig = px.box(df_subset, y=columns, title="Box Plot")
elif graph_type == "violin":
    fig = px.violin(df_subset, y=columns, title="Violin Plot")

if fig:
    st.plotly_chart(fig)

# Statistics Table
st.subheader("Statistical Summary")
st.write(df_subset[columns].describe())

# Auto-refresh data every 10 seconds
time.sleep(10)
st.rerun()
