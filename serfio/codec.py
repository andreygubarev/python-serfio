import msgpack


class DecodeError(Exception):
    pass


def encode(seq, command, body=None):
    data = msgpack.packb({"Seq": seq, "Command": command})
    if body:
        data += msgpack.packb(body)
    return data


def decode(buf):
    try:
        data = msgpack.unpackb(buf, raw=False)
        return data, b""
    except msgpack.ExtraData as e:
        return e.unpacked, e.extra
    except msgpack.UnpackValueError:
        raise DecodeError("Failed to decode message")
