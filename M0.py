import asyncio
import aiohttp
import pandas as pd


async def process_code(clients):
    tasks = []
    results = []

    async with aiohttp.ClientSession() as session:
        for id, codes in clients.items():
            tasks.append(
                asyncio.create_task(session.get("http://127.0.0.1:8080/", json={"client": id, "codes": codes})))
        results = await asyncio.gather(*tasks)
        results = [await x.json() for x in results]
    return results


async def main():
    print("Running client script...\n")

    # generate list of client IDs
    list_of_client_ids = list(range(1, 10001))

    # load dataframe
    print("Loading dataframe...\n")
    dataframe = pd.read_json("data/dataset.json", lines=True)
    print("Dataframe loaded.\n")

    # calculate rows per client
    rows_per_client = int(len(dataframe) / len(list_of_client_ids))  # 10

    # create dict for client IDs and their code
    clients = {id: [] for id in list_of_client_ids}
    for id, codes in clients.items():
        from_row = (id - 1) * rows_per_client
        to_row = from_row + rows_per_client
        for index, row in dataframe.iloc[from_row + 1:to_row + 1].iterrows():
            codes.append(row.get("content"))

    results = await process_code(clients)

    # log average number of letters for clients' code
    for result in results:
        print("Average code length for client with ID", result.get("client"), "is", result.get("averageWordcount"))


asyncio.get_event_loop().run_until_complete(main())
