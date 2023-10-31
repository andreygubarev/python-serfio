import os

import pytest
from pytest_docker_tools import build, container

PATH = os.path.dirname(os.path.abspath(__file__))

image = build(path=PATH, tag='serf:latest')
server = container(image='{image.id}', ports={'7373/tcp': None})


@pytest.fixture
def serf(server):
    import serfio
    port = server.ports['7373/tcp'][0]
    return serfio.Serf(port=port)
