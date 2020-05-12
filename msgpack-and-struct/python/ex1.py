
from io import BytesIO
import msgpack

#***************************************************************************************************************

def ex1():

    buf = BytesIO()
    header = 0x2000
    for i in range(100):
       buf.write(msgpack.packb(header,i, use_bin_type=True))

    buf.seek(0)

    unpacker = msgpack.Unpacker(buf, raw=False)
    for unpacked in unpacker:
        print(unpacked)


#***************************************************************************************************************

ex1()
