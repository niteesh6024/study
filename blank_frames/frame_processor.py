import asyncio
import json
import websockets
from detect_blank import BlankFrameDetector
from detect_frozen import FrozenFrameDetector

WEBSOCKET_URL = "ws://localhost:8765"
FRAME_QUEUE_SIZE = 100

class FrameProcessor:
    def __init__(self):
        self.frame_queue = asyncio.Queue(maxsize=FRAME_QUEUE_SIZE)
        self.frozen_detector = FrozenFrameDetector(buffer_size=60, similarity_threshold=0.99, required_match_count=45)
        self.blank_frame_detector = BlankFrameDetector()
        self.running = False
        self.listener_task = None
        self.processor_task = None

    async def websocket_listener(self):
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            print("Connected to WebSocket... Listening for frames.")
            while self.running:
                try:
                    message = await websocket.recv()
                    frame = json.loads(message)

                    if self.frame_queue.full():
                        await self.frame_queue.get()

                    await self.frame_queue.put(frame)
                except websockets.ConnectionClosed:
                    print("WebSocket Disconnected. Attempting to reconnect...")
                    await asyncio.sleep(2)

    async def frame_processor(self):
        while self.running:
            frame = await self.frame_queue.get()

            frame_id = frame["frame_id"]
            timestamp = frame["timestamp"]
            histogram = frame["histogram"]["gray"]

            is_blank = self.blank_frame_detector.is_blank(histogram)
            is_frozen = self.frozen_detector.is_frozen(histogram,timestamp)

            if is_frozen:
                if is_blank:
                    print(f"Blank/Frozen Frame Detected: {frame_id} at {timestamp}")
                else:
                    print(f"Frozen Frame Detected: {frame_id} at {timestamp}")

            self.frozen_detector.add_frame(histogram)

    async def start(self):
        if self.running:
            print("Already running.")
            return

        self.running = True
        self.listener_task = asyncio.create_task(self.websocket_listener())
        self.processor_task = asyncio.create_task(self.frame_processor())

        await asyncio.gather(self.listener_task, self.processor_task)

    async def stop(self):
        if not self.running:
            print("Already stopped.")
            return

        self.running = False
        await asyncio.sleep(1)

        if self.listener_task:
            self.listener_task.cancel()
        if self.processor_task:
            self.processor_task.cancel()

        print("WebSocket processing stopped.")

ws_processor = FrameProcessor()
asyncio.run(ws_processor.start())

# def open_websocket():
#     asyncio.run(ws_processor.start())

# def close_websocket():
#     asyncio.run(ws_processor.stop())