import asyncio
import aiohttp
import pandas as pd

client_ids = list(range(1, 10001))
df = pd.read_json("file-000000000040.json", lines=True)

rows_per_client = int(len(df) / len(client_ids))
clients = {id: [] for id in client_ids}
for client_id, codes in clients.items():
    from_row = (client_id - 1) * rows_per_client
    to_row = from_row + rows_per_client
    for _, row in df.iloc[from_row + 1:to_row + 1].iterrows():
        codes.append(row.get("content"))

tasks = []
results = []


async def process_code():
    async with aiohttp.ClientSession() as session:
        for client_id, codes in clients.items():
            tasks.append(asyncio.create_task(
                session.get("http://127.0.0.1:8080/", json={"client": client_id, "codes": codes})
            ))
        results = await asyncio.gather(*tasks)
        results = [await result.json() for result in results]

    for result in results:
        print("Average code length for client with ID", result.get("client"), "is", result.get("averageWordcount"))


asyncio.get_event_loop().run_until_complete(process_code())
