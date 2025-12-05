import asyncio
import os

def count_lines(path):
    total = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            try:
                with open(os.path.join(root, f), "r", errors="ignore") as fh:
                    total += sum(1 for _ in fh)
            except:
                pass
    return total

async def handle(reader, writer):
    data = await reader.read(1024)
    path = data.decode().strip()
    
    loop = asyncio.get_event_loop()
    total = await loop.run_in_executor(None, count_lines, path)
    
    writer.write(str(total).encode())
    await writer.drain()
    writer.close()

async def main():
    server = await asyncio.start_server(handle, "0.0.0.0", 9002)
    print("Async socket server on 9002")
    async with server:
        await server.serve_forever()

asyncio.run(main())