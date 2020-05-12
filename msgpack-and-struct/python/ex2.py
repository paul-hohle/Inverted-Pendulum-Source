

from io import BytesIO
import msgpack


def ex2():

    import datetime

    useful = {
        "id": 1,
        "created": datetime.datetime.now(),
    }

    def decode_datetime(obj):
        if b'__datetime__' in obj:
            obj = datetime.datetime.strptime(obj["as_str"], "%Y%m%dT%H:%M:%S.%f")
        return obj

    def encode_datetime(obj):
        if isinstance(obj, datetime.datetime):
            return {'__datetime__': True, 'as_str': obj.strftime("%Y%m%dT%H:%M:%S.%f")}
        return obj


    packed   = msgpack.packb(useful, default=encode_datetime, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, object_hook=decode_datetime, raw=False)

    print ("Packed message   : ",packed)
    print ("Unpacked message : ", unpacked)

ex2()
