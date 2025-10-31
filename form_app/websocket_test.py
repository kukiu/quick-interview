import asyncio
import websockets

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws/submissions/"
    try:
        async with websockets.connect(uri) as websocket:
            print("WebSocket connection established")
            while True:
                message = input("Enter message to send (or 'quit' to exit): ")
                if message.lower() == 'quit':
                    break
                await websocket.send(message)
                response = await websocket.recv()
                print(f"Received: {response}")
    except Exception as e:
        print(f"Error: {e}")

asyncio.get_event_loop().run_until_complete(test_websocket())
