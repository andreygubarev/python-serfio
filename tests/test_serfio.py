import asyncio

import pytest


async def test_stats(serf):
    async with serf:
        stats = await serf.stats()
        assert "serf" in stats


async def test_members(serf):
    async with serf:
        members = await serf.members()
        assert len(members) == 1


async def test_members_filtered(serf):
    async with serf:
        members = await serf.members_filtered(tags={"test": "test"})
        assert len(members) == 0


async def test_event(serf):
    async with serf:
        resp = await serf.event("test", "test")
        assert resp is None


async def test_stream(serf):
    async with serf:

        async def serf_event():
            await asyncio.sleep(0.1)
            resp = await serf.event("test", "test")
            assert resp is None

        serf_event = asyncio.create_task(serf_event())

        async for event in serf.stream():
            assert event["Event"] == "user"
            assert event["Name"] == "test"
            assert event["Payload"] == b"test"
            break

        await asyncio.gather(serf_event)


async def test_monitor(serf):
    async with serf:
        async for event in serf.monitor():
            assert "Serf agent starting" in event["Log"]
            break


async def test_tags(serf):
    async with serf:
        resp = await serf.tags(tags={"test": "test", "test2": "test2"})
        assert resp is None

        with pytest.raises(TypeError):
            await serf.tags(tags=["test"])

        resp = await serf.tags(delete_tags=["test2"])
        assert resp is None

        with pytest.raises(TypeError):
            await serf.tags(delete_tags={"test2": "test2"})

        members = await serf.members_filtered(tags={"test": "test"})
        assert len(members) == 1


async def test_respond(serf):
    async with serf:

        async def query():
            await asyncio.sleep(0.1)
            async for event in serf.query("test", "test"):
                assert event["Type"] == "response"
                assert event["Payload"] == b"response:test:test"

        async def respond():
            async for event in serf.stream("query"):
                query_id = event["ID"]
                query_name = event["Name"]
                query_payload = event["Payload"].decode()
                query_response = f"response:{query_name}:{query_payload}"
                await serf.respond(query_id, query_response)
                break

        query = asyncio.create_task(query())
        respond = asyncio.create_task(respond())
        await asyncio.gather(query, respond)


async def test_respond_one(serf):
    async with serf:

        async def query():
            await asyncio.sleep(0.1)
            event = await serf.query_one("test", "test")
            assert event["Type"] == "response"
            assert event["Payload"] == b"response:test:test"

        async def respond():
            async for event in serf.stream("query"):
                query_id = event["ID"]
                query_name = event["Name"]
                query_payload = event["Payload"].decode()
                query_response = f"response:{query_name}:{query_payload}"
                await serf.respond(query_id, query_response)
                break

        query = asyncio.create_task(query())
        respond = asyncio.create_task(respond())
        await asyncio.gather(query, respond)
