import pandas as pd
import time
import random

while True:
    new_data = pd.DataFrame({
        'index': range(1, 101),
        'x': [random.uniform(-10, 10) for _ in range(100)],  
        'y': [random.uniform(-10, 10) for _ in range(100)],
        'z': [random.uniform(-10, 10) for _ in range(100)]
    })
    filename = f"gyroscope_data_{int(time.time())}.csv"  # Unique timestamped file
    new_data.to_csv(filename, index=False)
    print(f"Created new file: {filename}")
    time.sleep(10)  # Create a new file every 10 seconds
