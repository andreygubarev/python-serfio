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
        header = await serf.event("test", "test")
        assert not header["Error"]


async def test_stream(serf):
    async with serf:

        async def serf_event():
            await asyncio.sleep(0.1)
            header = await serf.event("test", "test")
            assert not header["Error"]

        serf_event = asyncio.create_task(serf_event())

        async for event in serf.stream():
            header, body = event
            assert not header["Error"]
            assert body["Event"] == "user"
            assert body["Name"] == "test"
            assert body["Payload"] == b"test"
            break

        await asyncio.gather(serf_event)


async def test_monitor(serf):
    async with serf:
        async for event in serf.monitor():
            header, body = event
            assert not header["Error"]
            assert "Serf agent starting" in body["Log"]
            break


async def test_tags(serf):
    async with serf:
        header = await serf.tags(tags={"test": "test", "test2": "test2"})
        assert not header["Error"]

        with pytest.raises(TypeError):
            await serf.tags(tags=["test"])

        header = await serf.tags(delete_tags=["test2"])
        assert not header["Error"]

        with pytest.raises(TypeError):
            await serf.tags(delete_tags={"test2": "test2"})

        members = await serf.members_filtered(tags={"test": "test"})
        assert len(members) == 1


async def test_query(serf):
    async with serf:
        async for event in serf.query("test", "test"):
            header, body = event
            assert not header["Error"]
            assert "Type" in body
            assert body["Type"] == "ack"
            break


async def test_respond(serf):
    async with serf:

        async def query():
            await asyncio.sleep(0.1)
            async for event in serf.query("test", "test"):
                header, body = event
                assert not header["Error"]
                if body["Type"] == "ack":
                    continue
                if body["Type"] == "response":
                    assert body["Payload"] == b"response:test:test"

        async def respond():
            async for event in serf.stream("query"):
                header, body = event
                assert not header["Error"]
                query_id = body["ID"]
                query_name = body["Name"]
                query_payload = body["Payload"].decode()
                query_response = f"response:{query_name}:{query_payload}"
                await serf.respond(query_id, query_response)
                break

        query = asyncio.create_task(query())
        respond = asyncio.create_task(respond())
        await asyncio.gather(query, respond)
