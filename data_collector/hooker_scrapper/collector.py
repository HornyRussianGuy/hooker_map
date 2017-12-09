#!/usr/bin/env python
import asyncio
import json
import os
from sys import stdin

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = int(os.getenv('MONGO_PORT'))
MONGO_NAME = os.getenv('MONGO_NAME')


async def upsert_document(collection: AsyncIOMotorCollection, document: dict):
    await collection.update_one({
        '_id': document['_id']
    }, {
        '$set': document
    }, upsert=True)


async def stdin_reader(loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader(loop=loop)
    reader_protocol = asyncio.StreamReaderProtocol(reader, loop=loop)
    await loop.connect_read_pipe(lambda: reader_protocol, stdin)
    return reader


async def main(collection: AsyncIOMotorCollection, loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()
    reader = await stdin_reader(loop=loop)
    tasks = []
    while True:
        line = await reader.readline()
        if not line:
            break
        document = json.loads(line.decode('utf-8'))
        tasks.append(asyncio.ensure_future(upsert_document(collection, document), loop=loop))
    for task in tasks:
        await task


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = AsyncIOMotorClient(MONGO_HOST, MONGO_PORT)
    collection = client[MONGO_NAME]['hookers']
    loop.run_until_complete(main(collection, loop=loop))
