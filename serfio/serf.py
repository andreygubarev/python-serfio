import asyncio
import logging

from .errors import SerfError
from .protocol import Protocol

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Serf:
    PROTOCOL = Protocol
    TIMEOUT = 10

    def __init__(self, host="localhost", port=7373, auth_key=None):
        self.host = host
        self.port = port
        self.auth_key = auth_key

        self.protocol = None

    async def connect(self):
        self.protocol = await self.PROTOCOL.connect(self.host, self.port, self.auth_key)
        return self

    async def close(self):
        await self.protocol.close()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def event(self, name, payload=None, coalesce=False):
        req = await self.protocol.send(
            {
                "command": "event",
                "body": {
                    "Name": name,
                    "Payload": payload,
                    "Coalesce": coalesce,
                },
            }
        )

        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                header = (await anext(stream))[0]
                if header["Error"]:
                    raise SerfError(header["Error"])

    # async def force_leave(self, node):
    #     req = await self.protocol.send(
    #         {
    #             "command": "force-leave",
    #             "body": {
    #                 "Node": node,
    #             },
    #         }
    #     )

    #     async with self.protocol.recv(req) as stream:
    #         async with asyncio.timeout(self.TIMEOUT):
    #             return await anext(stream)

    # async def join(self, addresses, replay=False):
    #     req = await self.protocol.send(
    #         {
    #             "command": "join",
    #             "body": {
    #                 "Existing": addresses,
    #                 "Replay": replay,
    #             },
    #         }
    #     )

    #     async with self.protocol.recv(req) as stream:
    #         async with asyncio.timeout(self.TIMEOUT):
    #             return await anext(stream)

    async def members(self):
        req = await self.protocol.send(
            {
                "command": "members",
            }
        )

        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                header, body = await anext(stream)
                if header["Error"]:
                    raise SerfError(header["Error"])
                return body["Members"]

    async def members_filtered(self, name=None, status=None, tags=None):
        msg = {
            "command": "members-filtered",
            "body": {},
        }

        if name:
            if not isinstance(name, str):
                raise TypeError("name must be a str")
            msg["body"]["Name"] = name

        if status:
            if not isinstance(status, str):
                raise TypeError("status must be a str")
            msg["body"]["Status"] = status

        if tags:
            if not isinstance(tags, dict):
                raise TypeError("tags must be a dict")
            msg["body"]["Tags"] = tags

        req = await self.protocol.send(msg)
        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                header, body = await anext(stream)
                if header["Error"]:
                    raise SerfError(header["Error"])
                return body["Members"]

    async def tags(self, tags=None, delete_tags=None):
        msg = {
            "command": "tags",
            "body": {},
        }

        if tags:
            if not isinstance(tags, dict):
                raise TypeError("tags must be a dict")
            msg["body"]["Tags"] = tags

        if delete_tags:
            if not isinstance(delete_tags, list):
                raise TypeError("delete_tags must be a list")
            msg["body"]["DeleteTags"] = tags

        req = await self.protocol.send(msg)
        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                header = (await anext(stream))[0]
                if header["Error"]:
                    raise SerfError(header["Error"])

    async def stream(self, event_type="*"):
        req = await self.protocol.send(
            {
                "command": "stream",
                "body": {
                    "Type": event_type,
                },
            }
        )

        async with self.protocol.recv(req) as stream:
            await anext(stream)  # skip header
            async for header, body in stream:
                logger.debug("serf.stream: %s %s", header, body)
                if header["Error"]:
                    raise SerfError(header["Error"])
                yield body

    async def monitor(self, log_level="DEBUG"):
        req = await self.protocol.send(
            {
                "command": "monitor",
                "body": {
                    "LogLevel": log_level,
                },
            }
        )

        async with self.protocol.recv(req) as stream:
            await anext(stream)  # skip header
            async for header, body in stream:
                if header["Error"]:
                    raise SerfError(header["Error"])

                logger.debug("serf.monitor: %s", body)
                yield body

    # async def stop(self, seq):
    #     req = await self.protocol.send(
    #         {
    #             "command": "stop",
    #             "body": {
    #                 "Seq": seq,
    #             },
    #         }
    #     )

    #     async with self.protocol.recv(req) as stream:
    #         async with asyncio.timeout(self.TIMEOUT):
    #             return await anext(stream)

    # async def leave(self):
    #     req = await self.protocol.send(
    #         {
    #             "command": "leave",
    #         }
    #     )

    #     async with self.protocol.recv(req) as stream:
    #         async with asyncio.timeout(self.TIMEOUT):
    #             return await anext(stream)

    async def query(
        self,
        name,
        payload=None,
        filter_nodes=None,
        filter_tags=None,
        timeout=0,
        request_ack=True,
    ):
        payload = payload or b""
        msg = {
            "command": "query",
            "body": {
                "Name": name,
                "Payload": payload,
                "RequestAck": request_ack,
                "Timeout": timeout,
            },
        }

        if filter_nodes:
            if not isinstance(filter_nodes, list):
                raise TypeError("filter_nodes must be a list")
            msg["body"]["FilterNodes"] = filter_nodes

        if filter_tags:
            if not isinstance(filter_tags, dict):
                raise TypeError("filter_tags must be a dict")
            msg["body"]["FilterTags"] = filter_tags

        req = await self.protocol.send(msg)
        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                await anext(stream)  # skip header
                acks = 0
                async for header, body in stream:
                    if header["Error"]:
                        raise SerfError(header["Error"])

                    if body["Type"] == "ack":
                        acks += 1
                        continue

                    if body["Type"] == "done":
                        break

                    yield body

    async def query_one(
        self,
        name,
        payload=None,
        filter_nodes=None,
        filter_tags=None,
        timeout=0,
        request_ack=True,
    ):
        async for event in self.query(
            name,
            payload,
            filter_nodes=filter_nodes,
            filter_tags=filter_tags,
            timeout=timeout,
            request_ack=request_ack,
        ):
            return event

    async def respond(self, event_id, payload):
        if isinstance(payload, str):
            payload = payload.encode()

        if not isinstance(payload, bytes):
            raise TypeError("payload must be bytes")

        msg = {
            "command": "respond",
            "body": {
                "ID": event_id,
                "Payload": payload,
            },
        }

        req = await self.protocol.send(msg)
        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                return await anext(stream)

    # async def install_key(self, key):
    #     req = await self.protocol.send(
    #         {
    #             "command": "install-key",
    #             "body": {
    #                 "Key": key,
    #             },
    #         }
    #     )

    #     async with self.protocol.recv(req) as stream:
    #         async with asyncio.timeout(self.TIMEOUT):
    #             return await anext(stream)

    # async def use_key(self, key):
    #     req = await self.protocol.send(
    #         {
    #             "command": "use-key",
    #             "body": {
    #                 "Key": key,
    #             },
    #         }
    #     )

    #     async with self.protocol.recv(req) as stream:
    #         async with asyncio.timeout(self.TIMEOUT):
    #             return await anext(stream)

    # async def remove_key(self, key):
    #     req = await self.protocol.send(
    #         {
    #             "command": "remove-key",
    #             "body": {
    #                 "Key": key,
    #             },
    #         }
    #     )

    #     async with self.protocol.recv(req) as stream:
    #         async with asyncio.timeout(self.TIMEOUT):
    #             return await anext(stream)

    # async def list_keys(self):
    #     req = await self.protocol.send(
    #         {
    #             "command": "list-keys",
    #         }
    #     )

    #     async with self.protocol.recv(req) as stream:
    #         async with asyncio.timeout(self.TIMEOUT):
    #             return await anext(stream)

    async def stats(self):
        req = await self.protocol.send(
            {
                "command": "stats",
            }
        )

        async with self.protocol.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                header, body = await anext(stream)
                if header["Error"]:
                    raise SerfError(body["Error"])
                return body

    # async def get_coordinate(self, node):
    #     req = await self.protocol.send(
    #         {
    #             "command": "get-coordinate",
    #             "body": {
    #                 "Node": node,
    #             },
    #         }
    #     )

    #     async with self.protocol.recv(req) as stream:
    #         async with asyncio.timeout(self.TIMEOUT):
    #             return await anext(stream)
