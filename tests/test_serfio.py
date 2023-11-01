import asyncio


async def test_stats(serf):
    async with serf:
        header, body = await serf.stats()
        assert not header['Error']
        assert 'serf' in body


async def test_members(serf):
    async with serf:
        header, body = await serf.members()
        assert not header['Error']
        assert 'Members' in body


async def test_event(serf):
    async with serf:
        header = await serf.event('test', 'test')
        assert not header['Error']


async def test_stream(serf):
    async with serf:
        async def serf_event():
            await asyncio.sleep(0.1)
            header = await serf.event('test', 'test')
            assert not header['Error']
        serf_event = asyncio.create_task(serf_event())

        async for event in serf.stream():
            header, body = event
            assert not header['Error']
            assert body['Event'] == 'user'
            assert body['Name'] == 'test'
            assert body['Payload'] == b'test'
            break

        await asyncio.gather(serf_event)


async def test_monitor(serf):
    async with serf:
        async for event in serf.monitor():
            header, body = event
            assert not header['Error']
            assert "Serf agent starting" in body['Log']
            break


async def test_members(serf):
    async with serf:
        header, body = await serf.members()
        assert not header['Error']
        assert 'Members' in body


async def test_members_filtered(serf):
    async with serf:
        header, body = await serf.members_filtered(tags={'test': 'test'})
        assert not header['Error']
        assert 'Members' in body
        assert len(body['Members']) == 0
