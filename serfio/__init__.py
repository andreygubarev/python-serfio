from .serf import Serf


async def connect(host='localhost', port=7373, auth_key=None):
    return await Serf(host, port, auth_key).connect()
