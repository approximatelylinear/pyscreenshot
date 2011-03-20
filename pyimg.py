import ctypes as ct
from ctypes.util import find_library




lib = find_library("X11")
x11 = ct.cdll.LoadLibrary(lib)
display = x11.XOpenDisplay(None)





# typedef unsigned long VisualID
# typedef char *XPointer
# #define Window  uint32_t
# typedef XID Colormap;
# typedef unsigned long XID
Window = ct.c_ulong
XID = ct.c_ulong
Colormap = XID
XPointer = ct.c_char_p
VisualID = ct.c_ulong

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
    
    
class XExtData(ct.Structure): pass
    
XExtData._fields_ = [
    ("number", ct.c_int),
    ("next", ct.POINTER(XExtData)),
    ("free_private", ct.CFUNCTYPE(ct.c_int, ct.POINTER(XExtData))),
    ("private_data", ct.c_char_p)
]
    
class Visual(ct.Structure):
    _fields_ = [
        ("ext_data", ct.POINTER(XExtData)),
        ("visualid", VisualID),
        ("klass", ct.c_int),
        ("red_mask", ct.c_ulong),
        ("green_mask", ct.c_ulong),
        ("blue_mask", ct.c_ulong),
        ("bits_per_rgb", ct.c_int),
        ("map_entries", ct.c_int),
    ]
    

class _XGC(ct.Structure): pass
class Depth(ct.Structure):
    _fields_ = [
        ("depth", ct.c_int),
        ("nvisuals", ct.c_int),
        ("visuals", ct.POINTER(Visual)),
    ]
    
class _XDisplay(ct.Structure): pass
class Screen(ct.Structure):
    _fields_ = [
        ("ext_data", ct.POINTER(XExtData)),
        ("display", ct.POINTER(_XDisplay)),
        ("root", Window),
        ("width", ct.c_int),
        ("height", ct.c_int),
        ("mwidth", ct.c_int),
        ("mheight", ct.c_int),
        ("ndepths", ct.c_int),
        ("depths", ct.POINTER(Depth)),
        ("root_depth", ct.c_int),
        ("root_visual", ct.POINTER(Visual)),
        ("default_gc", ct.POINTER(_XGC)),
        ("cmap", Colormap),
        ("white_pixel", ct.c_ulong),
        ("black_pixel", ct.c_ulong),
        ("max_maps", ct.c_int),
        ("min_maps", ct.c_int),
        ("backing_store", ct.c_int),
        ("save_unders", ct.c_bool),
        ("root_input_mask", ct.c_long)
    ]
    
# http://tronche.com/gui/x/xlib/window-information/XGetWindowAttributes.html
class XWindowAttributes(ct.Structure):
    _fields_ = [
        ("x", ct.c_int),
        ("y", ct.c_int),
        ("width", ct.c_int),
        ("height", ct.c_int),
        ("border_width", ct.c_int),
        ("depth", ct.c_int),
        ("visual", ct.POINTER(Visual)),
        ("root", Window),
        ("class", ct.c_int),
        ("bit_gravity", ct.c_int),
        ("win_gravity", ct.c_int),
        ("backing_store", ct.c_int),
        ("backing_planes", ct.c_ulong),
        ("backing_pixel", ct.c_ulong),
        ("save_under", ct.c_bool),
        ("colormap", Colormap),
        ("map_installed", ct.c_bool),
        ("map_state", ct.c_int),
        ("all_event_masks", ct.c_long),
        ("your_event_mask", ct.c_long),
        ("do_not_propagate_mask", ct.c_long),
        ("override_redirect", ct.c_bool),
        ("screen", ct.POINTER(Screen)),
    ]
    
    
class Window(object):
    def __init__(self, window):
        self._window = window
        self._attr = XWindowAttributes()
        ret = x11.XGetWindowAttributes(display, self._window, ct.byref(self._attr))
        if ret != 1: raise Exception, "couldn't get window attributes"
        
    def __getattr__(self, name):
        return getattr(self._attr, name)
    
    @classmethod
    def get_root_window(cls):
        return cls(x11.XDefaultRootWindow(display))
    
    def screenshot(self, x, y, w=None, h=None):
        if w is None: w = self.width
        if h is None: h = self.height
        image = x11.XGetImage(display, self._window, x, y, w, h, x11.XAllPlanes(), 1);
        return image




root = Window.get_root_window()
image = root.screenshot(0, 0)
print x11.XGetPixel(image, 30, 30)

# png header
png = "\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"