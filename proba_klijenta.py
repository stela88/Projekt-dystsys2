import asyncio
import aiofiles
import json
import aiohttp
from aiohttp import web

routes = web.RouteTableDef()


async def process_data(client, code):
    avg_letters = sum(len(word) for word in code.split()) / len(code.split())
    print(f"For {client}, average number of letters is: {avg_letters}")


@routes.get("/JsonData")
async def json_data(request):
    async with aiohttp.ClientSession() as session:
        async with aiofiles.open('file-000000000040.json', mode='r') as file_data:
            read_data = [await file_data.readline() for _ in range(10)]
            whole_data = [json.loads(line) for line in read_data]
            client_ids = [f"client{i}" for i in range(10)]
            tasks = []
            database = []
            for i, item in enumerate(whole_data):
                db_item = {"client_id": client_ids[i], "python_code": item["content"]}
                database.append(db_item)
                baza = database
                tasks.append(
                    asyncio.create_task(session.post("http://1.0.0.127:8082/JsonData", json=database)))
                final_results = await asyncio.gather(*baza)
                final_results = [await x.json() for x in final_results]

            return web.json_response(final_results, status=200)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8080)
