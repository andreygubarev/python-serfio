import pytest

import serfio

async def test_stat(port):
    serf = await serfio.connect(port=port)
    header, body = await serf.stats()
    assert not header['Error']
    assert 'serf' in body
    await serf.close()
