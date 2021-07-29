import os

if os.name == "nt":
    try:
        import colorama
        colorama.init()
    except:
        G = Y = B = R = W = M = C = reset = Bold = underline = ''

# Colors
G, B, R, W, M, C, reset, Bold, underline = '\033[32m', '\033[94m', '\033[31m', '\x1b[37m', '\x1b[35m', '\x1b[36m', '\033[0m', "\033[1m", "\033[4m"
