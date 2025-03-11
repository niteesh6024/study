import asyncio
import json
import websockets
import uuid
import random
import time

# WebSocket Server Configuration
WEBSOCKET_HOST = "localhost"
WEBSOCKET_PORT = 8765
FRAMES_PER_SECOND = 10  # Number of frames per second

async def generate_frame():
    """Generates a dummy frame JSON with a grayscale histogram."""
    return {
        "frame_id": str(uuid.uuid4()),  # Random frame ID
        "histogram": {
            # "gray": [random.randint(0, 5) for _ in range(256)] 
            # "gray": [2001,2002,2003,1223,121,123,12,12,1,12] + [0]*256 # blank and frozen
              "gray": [0]*256 +[2001,2002,2003,1223,121,123,12,12,1,12]  # white and frozen
        },
        "timestamp": int(time.time() * 1000),  # Current time in milliseconds
        "timestamp_raw": time.time()  # Floating-point timestamp
    }

async def websocket_handler(websocket):
    """Handles WebSocket connections and streams dummy frames."""
    print("Client connected... Sending frames.")
    try:
        while True:
            frame = await generate_frame()
            await websocket.send(json.dumps(frame))
            await asyncio.sleep(1 / FRAMES_PER_SECOND)  # Control frame rate
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected.")

async def main():
    """Starts the WebSocket server."""
    server = await websockets.serve(websocket_handler, WEBSOCKET_HOST, WEBSOCKET_PORT)
    print(f"WebSocket Server running on ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
    await server.wait_closed()

# Run the WebSocket server
asyncio.run(main())


# import random

# def genearte_blank_frame():
#     frames = []
#     f=True
#     for _ in range(30):
#         size = 256
#         max_sum = 2073600
#         frame = []
#         for _ in range(size):
#             random_int = random.randint(0, max_sum)
#             frame.append(random_int)
#             max_sum=max_sum-random_int
#         frames.append({
#             "frame_id": random.randint(0, 1000),
#             "timestamp":random.randint(0, 100000),
#             "histogram":{"gray":frame[::-1]}
#             })
#     return frames

