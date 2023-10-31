import asyncio
import resource


class Transport:
    BUFFER_SIZE = resource.getpagesize()

    CONNECTION_TIMEOUT = 10

    def __init__(self, reader, writer):
        self.reader = reader
        self._rlock = asyncio.Lock()
        self.writer = writer
        self._wlock = asyncio.Lock()

    @classmethod
    async def connect(cls, host, port):
        async with asyncio.timeout(cls.CONNECTION_TIMEOUT):
            reader, writer = await asyncio.open_connection(host, port)
            return cls(reader, writer)

    async def read(self):
        if self.reader.at_eof():
            raise ConnectionError("Connection closed")

        async with self._rlock:
            return await self.reader.read(self.BUFFER_SIZE)

    async def write(self, data):
        async with self._wlock:
            self.writer.write(data)
            await self.writer.drain()
