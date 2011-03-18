import ctypes as ct


class XImage(ct.Structure):
    _fields_ = [
        ("width", ct.c_int),
        ("height", ct.c_int),
        ("xoffset", ct.c_int),
        ("format", ct.c_int),
        ("data", ct.c_char_p),
        ("byte_order", ct.c_int),
        ("bitmap_unit", ct.c_int),
        ("bitmap_bit_order", ct.c_int),
        ("bitmap_pad", ct.c_int),
        ("depth", ct.c_int),
        ("bytes_per_line", ct.c_int),
        ("bits_per_pixel", ct.c_int),
        ("red_mask", ct.c_ulong),
        ("green_mask", ct.c_ulong),
        ("blue_mask", ct.c_ulong),
    ]

x11 = ct.cdll.LoadLibrary("libX11.so")
display = x11.XOpenDisplay(None)
window = x11.XDefaultRootWindow(display)
image = x11.XGetImage(display, window, 0, 0, 100, 100, x11.XAllPlanes(), 1);

#image_p = ct.cast(image, ct.POINTER(XImage))
print x11.XGetPixel(image, 30, 30)
