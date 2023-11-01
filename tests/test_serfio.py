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
