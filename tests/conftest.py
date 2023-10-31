import os

import pytest
from pytest_docker_tools import build, container

PATH = os.path.dirname(os.path.abspath(__file__))


serf_image = build(path=PATH, tag='serf:latest')
serf_server = container(image='{serf_image.id}', ports={'7373/tcp': None})


@pytest.fixture
@pytest.mark.asyncio
async def serf(serf_server):
    port = serf_server.ports['7373/tcp'][0]

    import serfio
    return await serfio.connect(port=port)
