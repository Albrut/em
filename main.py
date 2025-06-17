import asyncio
import json
import websockets

connected = set()

async def handler(ws):
    connected.add(ws)
    try:
        async for message in ws:
            # просто ретранслируем сообщение всем остальным клиентам
            data = json.loads(message)
            for conn in connected:
                if conn != ws:
                    await conn.send(json.dumps(data))
    except websockets.ConnectionClosed:
        pass
    finally:
        connected.remove(ws)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Signaling server started on ws://0.0.0.0:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
