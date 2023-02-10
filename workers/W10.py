import random
import string
import re
import asyncio
from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/")
async def word_count(request):
    try:
        wait_time_for_request = random.uniform(0.1, 0.3)
        await asyncio.sleep(wait_time_for_request)
        request_data = await request.json()
        text = request_data.get("data")
        cleaned_text = re.sub("[" + string.punctuation + "]", "", text)
        word_list = cleaned_text.split()
        result = len(word_list)

        wait_time_for_response = random.uniform(0.1, 0.3)
        await asyncio.sleep(wait_time_for_response)

        return web.json_response({"status": "OK", "number of words": result}, status=200)
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8090)
