import aiohttp
from aiohttp import web
import asyncio
from blocking_parse import parse_page_html
import sys

async def handle(request):
    url = request.rel_url.query.get("url")
    if not url:
        return web.json_response({"error": "no url"}, status=400)

    try:
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as r:
                if r.status != 200:
                    return web.json_response({"error": f"HTTP {r.status}"}, status=400)
                html = await r.text()
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

    loop = asyncio.get_event_loop()
    item_names, total = await loop.run_in_executor(None, parse_page_html, html)

    if item_names:
        with open("async_results.txt", "a", encoding="utf-8") as f:
            for item_name in item_names:
                f.write(item_name + "\n")

    return web.json_response({
        "items": len(item_names),
        "total_price": total
    })

app = web.Application()
app.add_routes([web.get("/parse", handle)])

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    web.run_app(app, host="0.0.0.0", port=8002)