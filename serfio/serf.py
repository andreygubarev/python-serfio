import asyncio

from .protocol import Protocol


class Serf:
    PROTOCOL = Protocol
    TIMEOUT = 10

    def __init__(self, protocol):
        self.protocol = protocol
        self.streams = {}

    @classmethod
    async def connect(cls, host='localhost', port=7373, auth_key=None):
        protocol = await cls.PROTOCOL.connect(host, port, auth_key)
        return cls(protocol)

    async def event(self, name, payload=None, coalesce=False):
        req = await self.protocol.send({
            "command": "event",
            "body": {
                "Name": name,
                "Payload": payload,
                "Coalesce": coalesce,
            },
        })

        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                return await anext(stream)

    async def force_leave(self, node):
        req = await self.protocol.send({
            "command": "force-leave",
            "body": {
                "Node": node,
            },
        })

        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                return await anext(stream)

    async def join(self, addresses, replay=False):
        req = await self.protocol.send({
            "command": "join",
            "body": {
                "Existing": addresses,
                "Replay": replay,
            },
        })

        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                return await anext(stream)

    async def members(self):
        req = await self.protocol.send({
            "command": "members",
        })

        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                return await anext(stream)

    async def members_filtered(self, name=None, status=None, tags=None):
        msg = {
            "command": "members-filtered",
            "body": {},
        }

        if name:
            msg["body"]["Name"] = name

        if status:
            msg["body"]["Status"] = status

        if tags:
            msg["body"]["Tags"] = tags

        req = await self.protocol.send(msg)
        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                return await anext(stream)

    async def tags(self, tags=None, delete_tags=None):
        msg = {
            "command": "tags",
            "body": {},
        }

        if tags:
            msg["body"]["Tags"] = tags

        if delete_tags:
            msg["body"]["DeleteTags"] = tags

        req = await self.protocol.send(msg)
        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                return await anext(stream)

    async def stream(self, event_type="*"):
        req = await self.protocol.send({
            "command": "stream",
            "body": {
                "Type": event_type,
            },
        })

        async with self.protocol.recv(req) as stream:
            async for event in stream:
                yield event

    async def monitor(self, log_level):
        req = await self.protocol.send({
            "command": "monitor",
            "body": {
                "LogLevel": log_level,
            },
        })

        async with self.protocol.recv(req) as stream:
            async for event in stream:
                yield event

    async def stop(self, seq):
        req = await self.protocol.send({
            "command": "stop",
            "body": {
                "Seq": seq,
            },
        })

        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                return await anext(stream)

    async def leave(self):
        req = await self.protocol.send({
            "command": "leave",
        })

        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                return await anext(stream)

    async def query(
        self,
        filter_nodes=None,
        filter_tags=None,
        request_ack=True,
        timeout=0,
        name=None,
        payload=None,
    ):
        msg = {
            "command": "query",
            "body": {
                "RequestAck": request_ack,
                "Timeout": timeout,
            },
        }

        if filter_nodes:
            msg["body"]["FilterNodes"] = filter_nodes

        if filter_tags:
            msg["body"]["FilterTags"] = filter_tags

        if name:
            msg["body"]["Name"] = name

        if payload:
            msg["body"]["Payload"] = payload

        req = await self.protocol.send(msg)
        async with self.protocol.recv(req) as stream:
            async for event in stream:
                yield event

    async def respond(self, id_, payload=None):
        msg = {
            "command": "respond",
            "body": {
                "ID": id_,
                "Payload": payload,
            },
        }

        req = await self.protocol.send(msg)
        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                return await anext(stream)

    async def install_key(self, key):
        req = await self.protocol.send({
            "command": "install-key",
            "body": {
                "Key": key,
            },
        })

        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                return await anext(stream)

    async def use_key(self, key):
        req = await self.protocol.send({
            "command": "use-key",
            "body": {
                "Key": key,
            },
        })

        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                return await anext(stream)

    async def remove_key(self, key):
        req = await self.protocol.send({
            "command": "remove-key",
            "body": {
                "Key": key,
            },
        })

        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                return await anext(stream)

    async def list_keys(self):
        req = await self.protocol.send({
            "command": "list-keys",
        })

        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                return await anext(stream)

    async def stats(self):
        req = await self.protocol.send({
            "command": "stats",
        })

        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                return await anext(stream)

    async def get_coordinate(self, node):
        req = await self.protocol.send({
            "command": "get-coordinate",
            "body": {
                "Node": node,
            },
        })

        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                return await anext(stream)
