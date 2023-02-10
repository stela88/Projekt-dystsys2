from aiohttp import web
import random
import asyncio
import aiohttp
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

num_workers = random.randint(5, 10)
print("Number of workers:", num_workers)

workers = {"worker_{}".format(id): [] for id in range(1, num_workers + 1)}
print("Workers:", workers)

SAMPLE_SIZE = 1000
MAX_NUM_REQUESTS = 10000
num_received_requests = 0
num_returned_responses = 0
num_sent_tasks = 0
num_completed_tasks = 0

routes = web.RouteTableDef()


@routes.get("/")
async def main_function(request):
    global num_workers, chunk_size, max_num_req_res
    global num_received_reqs, num_returned_resps
    global num_sent_tasks, num_completed_tasks

    num_received_reqs += 1
    logging.info(f"New request received. Current received requests status: {num_received_reqs} / {max_num_req_res}")
    data = await request.json()
    codes_length = len(data.get("codes"))

    all_codes = '\n'.join(data.get("codes"))
    codes = all_codes.split("\n")
    data["codes"] = ["\n".join(codes[i:i + chunk_size]) for i in range(0, len(codes), chunk_size)]

    tasks = []
    results = []
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:

        current_worker = 1
        for i in range(len(data.get("codes"))):
            task = asyncio.create_task(
                session.get(f"http://127.0.0.1:{8080 + current_worker}/",
                            json={"id": data.get("client"), "data": data.get("codes")[i]})
            )
            num_sent_tasks += 1
            logging.info(f"New task sent to worker {current_worker}. Current sent tasks status: {num_sent_tasks}")
            tasks.append(task)
            workers["workerWithId{}".format(current_worker)].append(task)
            if current_worker == num_workers:
                current_worker = 1
            else:
                current_worker += 1

        results = await asyncio.gather(*tasks)
        num_completed_tasks += len(results)
        logging.info(
            f"Another {len(results)} more tasks completed. Current completed tasks status: {num_completed_tasks}")
        results = [await result.json() for result in results]
        results = [result.get("numberOfWords") for result in results]

    num_returned_resps += 1
    logging.info(f"New response sent. Current sent responses status: {num_returned_resps} / {max_num_req_res}")

    return web.json_response({"status": "OK", "client": data.get("client"),
                              "averageWordcount": round(sum(results) / codes_length, 2)}, status=200)


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8080, access_log=None)
