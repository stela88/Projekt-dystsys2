from aiohttp import web
import random
import asyncio
import aiohttp
import logging

# setup port and logging settings
PORT = 8080
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# variables for storing data
SAMPLE_SIZE = 1000
MAX_NUM_REQUESTS = 10000
num_received_requests = 0
num_returned_responses = 0
num_sent_tasks = 0
num_completed_tasks = 0

# calculate number of workers (random 5 - 10)
num_workers = random.randint(5, 10)
print("Number of workers:", num_workers)

# assign IDs to workers and store in a dictionary
workers = {"worker_{}".format(id): [] for id in range(1, num_workers + 1)}
print("Workers:", workers)