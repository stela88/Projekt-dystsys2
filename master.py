import aiohttp
from aiohttp import web
import asyncio
import json
import logging
import random

logging.basicConfig(level=logging.INFO)

CHUNK_SIZE = 1000
MAX_REQUESTS = 10_000
received_requests = 0
received_responses = 0
sent_tasks = 0
received_tasks = 0

num_workers = random.randint(5, 10)

workers = {"worker_id_" + str(id): [] for id in range(0, num_workers)}

routes = web.RouteTableDef()

@routes.get("/")
async def master_handler(request):
    try:
        global received_responses
        global sent_tasks
        logging.info(f"Current requests status: {int(received_requests / MAX_REQUESTS)}")

        client_data = await request.json()

        combined_code = "\n".join(client_data.get("code"))
        code_split_newline = combined_code.split("\n")
        client_data["code"] = [
            "\n".join(code_split_newline[i : i + CHUNK_SIZE])
            for i in range(0, len(code_split_newline), CHUNK_SIZE)
        ]

        tasks = []
        results = []
        async with aiohttp.ClientSession() as session:
            active_worker = 1
            for i in range(len(client_data.get("code"))):
                task = asyncio.create_task(
                    session.get(
                        f"http://localhost:{8080 + active_worker}/worker_{active_worker}",
                        json={"id": client_data.get("id"), "code": client_data.get("code")[i]},
                    )
                )
                sent_tasks += 1
                tasks.append(task)
                workers["worker_id_" + str(active_worker)].append(tasks)

                if active_worker != num_workers:
                    active_worker += 1

            results = await asyncio.gather(*tasks)
            results = [await data.json() for data in results]

            avg_word_counter = [result.get("number_of_words") for result in results]
            avg_word_counter = int(sum(avg_word_counter) / len(client_data.get("code")))

            received_responses += 1

        return web.json_response(
            {"status": "ok", "average words": avg_word_counter}, status=200
        )

    except Exception as e:
        return web.json_response({"port": 8080, "error": str(e)}, status=500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=8080)
