from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, MultiSelect, Select, CheckboxButtonGroup, TextInput, Button, DataTable, TableColumn
from bokeh.layouts import column, row
from bokeh.io import curdoc
import pandas as pd
import os
import glob

# Load latest CSV file dynamically
def load_latest_data():
    files = sorted(glob.glob("gyroscope_data*.csv"), key=os.path.getctime)
    if files:
        return pd.read_csv(files[-1])  # Load the most recent file
    return None

df = load_latest_data()
if df is None or df.empty:
    raise ValueError("No valid data file found.")

# Default parameters
sample_size = 100
start_idx = 0

df_subset = df.iloc[start_idx:start_idx + sample_size]
source = ColumnDataSource(data={'index': df_subset.index, 'x': df_subset['x'], 'y': df_subset['y'], 'z': df_subset['z']})

def create_figure(graph_type, selected_columns):
    p = figure(title="Gyroscope Data", x_axis_label="Index", y_axis_label="Value")
    colors = {"x": "blue", "y": "green", "z": "red"}
    
    for col in selected_columns:
        if graph_type == "scatter":
            p.scatter('index', col, source=source, legend_label=col, color=colors[col])
        elif graph_type == "line":
            p.line('index', col, source=source, legend_label=col, color=colors[col])
        elif graph_type == "bar":
            p.vbar(x='index', top=col, source=source, legend_label=col, color=colors[col], width=0.5)
        elif graph_type == "histogram":
            p.quad(top=col, bottom=0, left='index', right='index', source=source, legend_label=col, color=colors[col])
    
    return p

column_select = MultiSelect(title="Select Columns", value=["x"], options=list(df.columns[1:]))
select_all_checkbox = CheckboxButtonGroup(labels=["Select All"], active=[])
graph_type_select = Select(title="Graph Type", value="line", options=["scatter", "line", "bar", "histogram"])

sample_input = TextInput(value=str(sample_size), title="Number of Samples")
prev_button = Button(label="Previous", button_type="primary")
next_button = Button(label="Next", button_type="primary")

table_source = ColumnDataSource(data={"Metric": [], "X": [], "Y": [], "Z": []})

def update_table(df_subset):
    selected_columns = column_select.value
    metrics = ["Mean", "Min", "Max", "Std Dev"]
    
    summary_data = {"Metric": metrics}

    for col in df.columns[1:]:
        if col in selected_columns:
            summary_data[col.upper()] = [
                round(df_subset[col].mean(), 2),
                round(df_subset[col].min(), 2),
                round(df_subset[col].max(), 2),
                round(df_subset[col].std(), 2)
            ]
        else:
            summary_data[col.upper()] = ["N/A"] * 4  

    table_source.data = {col: summary_data[col] for col in summary_data}

def update():
    global start_idx, sample_size, p, df

    df = load_latest_data()  # Reload latest CSV file

    if df is None or df.empty:
        return

    try:
        sample_size = max(10, min(int(sample_input.value), len(df)))
    except ValueError:
        return
    
    df_subset = df.iloc[start_idx:start_idx + sample_size]
    
    new_data = {'index': df_subset.index}
    for col in df.columns[1:]:
        new_data[col] = df_subset[col] if col in column_select.value else [None] * len(df_subset)

    source.data = new_data
    update_table(df_subset)

    layout.children[-2] = create_figure(graph_type_select.value, column_select.value)

def prev_data():
    global start_idx
    start_idx = max(0, start_idx - sample_size)
    update()

def next_data():
    global start_idx
    start_idx = min(len(df) - sample_size, start_idx + sample_size)
    update()

def toggle_select_all(attr, old, new):
    if 0 in new:
        column_select.value = list(df.columns[1:])
    else:
        column_select.value = []

column_select.on_change("value", lambda attr, old, new: update())
graph_type_select.on_change("value", lambda attr, old, new: update())
sample_input.on_change("value", lambda attr, old, new: update())
select_all_checkbox.on_change("active", toggle_select_all)
prev_button.on_click(prev_data)
next_button.on_click(next_data)

columns = [TableColumn(field="Metric", title="Metric")] + [TableColumn(field=col.upper(), title=col.upper()) for col in df.columns[1:]]
data_table = DataTable(source=table_source, columns=columns, width=400, height=200)

p = create_figure(graph_type_select.value, column_select.value)
layout = column(row(column_select, select_all_checkbox, graph_type_select), row(sample_input, prev_button, next_button), p, data_table)

curdoc().add_root(layout)
curdoc().title = "Gyroscope Dashboard"

# Auto-update every 5 seconds**
curdoc().add_periodic_callback(update, 5000)
