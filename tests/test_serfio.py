import serfio

async def test_stats(port):
    async with await serfio.connect(port=port) as serf:
        header, body = await serf.stats()
        assert not header['Error']
        assert 'serf' in body
