import asyncio
import aiofiles
import json
import pandas as pd
from aiohttp import web


routes = web.RouteTableDef()


@routes.get("/JsonData")
async def json_data(request):
    async with aiofiles.open('file-000000000040.json', mode='r') as file_data:
        read_data = {await file_data.readline() for _ in range(10)}
        whole_data = [json.loads(line) for line in read_data]
        client_ids = [f"client{i}" for i in range(10)]
        database = {}
        for i, item in enumerate(whole_data):
            db_item = {"python_code": item["content"]}
            database[client_ids[i]] = db_item
        print(database)
        return web.json_response(database, status=200)


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8081)
