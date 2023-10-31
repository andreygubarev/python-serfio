# Serfio: Python asyncio client for Serf

![License](https://img.shields.io/badge/license-MIT-blue.svg)

`serfio` is a Python `asyncio` client for [Serf](https://www.serf.io/). The goal was to create client with zero or minimal dependencies. It allows to use it with Debian 12 (Bookworm) without installing any additional packages, besides `python3` and `python3-msgpack`. As far as I know, this eliminates licensing and security concerns, relieving my headaches.

`serfio` implements all Serf RPC commands. It includes `streams` implemented as async iterators (everything is implemented as an async iterator 🧐). That was another goal: to make easy to use interface. At this stage of development is very straightforward and simple, and might not change in future.

`serfio` is *under development*, it is not yet tested in production. It was tested with Serf 0.8.2. For more mature client see [alternatives](#alternatives).

## Installation

PyPi: https://pypi.org/project/serfio/

```bash
pip install serfio
```

## Usage

```python
import asyncio
import serfio

async def main():
    async with serfio.Serf() as serf:
        response = await serf.members()
    print(response)
```

## Development

```bash
direnv allow .
pipenv install --dev
make lint
make test
```

Prerequisites:
-  direnv: https://direnv.net/
-  pipenv: https://pipenv.pypa.io/en/latest/
-  pytest: https://docs.pytest.org/en/latest/
-  docker: https://www.docker.com/

## Reference

Serf:
-  Serf: https://www.serf.io/
-  Serf RPC: https://www.serf.io/docs/agent/rpc.html

### Alternatives

-  aioserf: https://pypi.org/project/aioserf/
-  asyncserf: https://pypi.org/project/asyncserf/
