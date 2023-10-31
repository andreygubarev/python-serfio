# Serfio: Python asyncio client for Serf
PyPi: https://pypi.org/project/serfio/
Serf: https://www.serf.io/
Serf RPC: https://www.serf.io/docs/agent/rpc.html

## Usage

```python
import asyncio
import serfio

async def main():
    async with serfio.Serf() as serf:
        response = await serf.members()
    print(response)
```

## Installation

```bash
pip install serfio
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

Alternatives:

-  aioserf: https://pypi.org/project/aioserf/
-  asyncserf: https://pypi.org/project/asyncserf/
