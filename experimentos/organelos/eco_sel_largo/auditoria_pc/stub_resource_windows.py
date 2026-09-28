# STUB para Windows (auditoria en el PC): el modulo 'resource' es solo de Unix. Solo informa la memoria pico; no toca ninguna corrida.
import types
RUSAGE_SELF = 0
def getrusage(who):
    try:
        import ctypes, ctypes.wintypes as w
        class PMC(ctypes.Structure):
            _fields_ = [('cb', w.DWORD), ('PageFaultCount', w.DWORD), ('PeakWorkingSetSize', ctypes.c_size_t),
                        ('WorkingSetSize', ctypes.c_size_t), ('QuotaPeakPagedPoolUsage', ctypes.c_size_t),
                        ('QuotaPagedPoolUsage', ctypes.c_size_t), ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t),
                        ('QuotaNonPagedPoolUsage', ctypes.c_size_t), ('PagefileUsage', ctypes.c_size_t), ('PeakPagefileUsage', ctypes.c_size_t)]
        c = PMC(); c.cb = ctypes.sizeof(c)
        k = ctypes.WinDLL('kernel32'); k.GetCurrentProcess.restype = w.HANDLE
        p = ctypes.WinDLL('psapi'); p.GetProcessMemoryInfo.argtypes = [w.HANDLE, ctypes.c_void_p, w.DWORD]
        p.GetProcessMemoryInfo(k.GetCurrentProcess(), ctypes.byref(c), c.cb)
        kb = c.PeakWorkingSetSize / 1024
    except Exception:
        kb = 0
    return types.SimpleNamespace(ru_maxrss=kb)
