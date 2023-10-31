async def test_stats(serf):
    async with serf:
        header, body = await serf.stats()
        assert not header['Error']
        assert 'serf' in body
