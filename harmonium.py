import asyncio
import websockets
import json
import random
import time

try:
    from pybooklid import LidSensor
except ImportError:
    class LidSensor:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def monitor(self, interval=0.05):
            angle, direction = 120.0, -1
            while True:
                angle += direction * 0.5
                if angle < 80: direction = 1
                if angle > 120: direction = -1
                yield angle
                time.sleep(interval)

async def handler(websocket):
    print("\nWeb App connected!")
    try:
        with LidSensor() as sensor:
            for angle in sensor.monitor(interval=0.05):
                await websocket.send(json.dumps({"angle": angle}))
                await asyncio.sleep(0.01) # Small sleep to yield
    except websockets.ConnectionClosed:
        print("\nWeb App disconnected.")
    except Exception as e:
        print(f"Error in handler: {e}")

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Bridge active! Waiting for your web app on port 8765...")
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping Bridge...")