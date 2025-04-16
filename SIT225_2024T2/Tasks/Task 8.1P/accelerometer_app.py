# accelerometer_app.py

# import logging
# logging.basicConfig(level=logging.DEBUG)

import sys
import traceback
import time
from arduino_iot_cloud import ArduinoCloudClient
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Output, Input
import plotly.graph_objs as go

# --- 1. Your device credentials (replace with yours) ---
DEVICE_ID  = "8804f551-ab6a-4878-9b3d-9beae644d0e7"
SECRET_KEY = "nl49dbaA4#Y#hQe8N9JArkMyx"
USERNAME   = DEVICE_ID

# --- 2. Sampling parameters ---
N = 1000      # block size for saving CSV/PNG
window = N  # number of samples to show in the live plot

# --- 3. Buffers for incoming data ---
sensor_buffer = { 'x': [], 'y': [], 'z': [] }
last_fig = go.Figure()  # initial empty figure for Dash

def log_block():
    """Save a block of N samples to CSV + PNG, return the figure."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    # build DataFrame
    df = pd.DataFrame({
        'AccelerometerX': sensor_buffer['x'][:N],
        'AccelerometerY': sensor_buffer['y'][:N],
        'AccelerometerZ': sensor_buffer['z'][:N]
    })
    # drop those N samples from buffer
    for axis in ('x','y','z'):
        sensor_buffer[axis] = sensor_buffer[axis][N:]
    # save CSV
    csv_file = f"/Users/dishasharma/Documents/Coding/SIT225/Task 8.1P/accelerometer_data_{timestamp}.csv"
    df.to_csv(csv_file, index=False)
    # save PNG
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df['AccelerometerX'], name='X'))
    fig.add_trace(go.Scatter(y=df['AccelerometerY'], name='Y'))
    fig.add_trace(go.Scatter(y=df['AccelerometerZ'], name='Z'))
    img_file = f"/Users/dishasharma/Documents/Coding/SIT225/Task 8.1P/accelerometer_graph_{timestamp}.png"
    fig.write_image(img_file)
    print(f"Saved {csv_file} and {img_file}")
    return fig

def check_and_buffer():
    """If we have ≥N samples on each axis, save that block."""
    if all(len(sensor_buffer[a]) >= N for a in ('x','y','z')):
        print(f"[DEBUG] Collected {N} samples per axis → saving block")
        global last_fig
        last_fig = log_block()

# --- 4. Callbacks: print & buffer each new reading ---
def on_accelerometer_x_changed(client, value):
    ts = time.strftime("%H:%M:%S.%f")[:-3]
    print(f"[{ts}] X → {value}", flush=True)
    sensor_buffer['x'].append(value)
    check_and_buffer()

def on_accelerometer_y_changed(client, value):
    ts = time.strftime("%H:%M:%S.%f")[:-3]
    print(f"[{ts}] Y → {value}", flush=True)
    sensor_buffer['y'].append(value)
    check_and_buffer()

def on_accelerometer_z_changed(client, value):
    ts = time.strftime("%H:%M:%S.%f")[:-3]
    print(f"[{ts}] Z → {value}", flush=True)
    sensor_buffer['z'].append(value)
    check_and_buffer()

# --- 5. Dash app for live plotting ---
app = Dash(__name__)
app.layout = html.Div([
    html.H2("Live Accelerometer Data"),
    dcc.Graph(id='live-graph'),
    dcc.Interval(id='interval', interval=1000, n_intervals=0)  # 0.5s
])

@app.callback(
    Output('live-graph','figure'),
    Input('interval','n_intervals')
)
def update_graph(n):
    # take the last `window` samples
    xs = sensor_buffer['x'][-window:]
    ys = sensor_buffer['y'][-window:]
    zs = sensor_buffer['z'][-window:]
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=xs, name='X'))
    fig.add_trace(go.Scatter(y=ys, name='Y'))
    fig.add_trace(go.Scatter(y=zs, name='Z'))
    fig.update_layout(
        xaxis_title='Sample Index (latest → right)',
        yaxis_title='Acceleration'
    )
    return fig

# --- 6. Main: connect to Cloud & start Dash ---
def main():
    print("Initializing Arduino Cloud client for accelerometer data...")
    client = ArduinoCloudClient(
        device_id=DEVICE_ID,
        username=USERNAME,
        password=SECRET_KEY
    )
    # register your Python‑Thing properties
    client.register("py_x", value=None, on_write=on_accelerometer_x_changed)
    client.register("py_y", value=None, on_write=on_accelerometer_y_changed)
    client.register("py_z", value=None, on_write=on_accelerometer_z_changed)
    client.start()
    app.run_server(debug=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error occurred:", e)
        traceback.print_exc()
