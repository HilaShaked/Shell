import sys



def hex_dump(**kwargs):  # s = some string, SIZE  = number of bytes on each line
    """
    print base 16 every byte
    :param s: byte array
    :param SIZE: optional (how many bytes per line)

    :return: Void
    """
    s = kwargs['file']
    SIZE = kwargs.get('size',8)
    #print("len=", len(s))  # ** prints the len here **
    for p in [s[i * SIZE: min((i + 1) * SIZE, len(s))] for i in range(len(s) // SIZE + 1)]:
        return (b" ".join(
            [b"%02X" % int(p[j])  # (also line below) combine the hex numbers to one byte string (not really a string)
             if j < len(p) else b"  " for j in range(SIZE)]).decode() + \
              "       " + " ".join([chr(p[n])  # printing the chars next to the hex, like in the hex editor
                                      if 31 < p[n] < 128 else "." for n in range(len(p))]))


def run_hex(args: str):
    if '-' not in args:
        print(hex_dump(file=args[0]))
        return
    dictt = {}
    args = args.split()
    if '-b' in args:
        dictt['b'] = True
    if '-C' in args:
        dictt['C'] = True
    if '-c' in args:
        dictt['c'] = True
    if '-n' in args:
        dictt['n'] = args[args.index('-n')+1]
    if '-s' in args:
        dictt['s'] = args[args.index('-s')+1]
    if '-h' in args:
        dictt['h'] = True
    if '-o' in args:
        dictt['o'] = True
    if '-x' in args:
        dictt['x'] = True
    if '-d' in args:
        dictt['d'] = True
    if '-v' in args:
        dictt['v'] = True
    dictt['file'] = args[-1]
    print(hex_dump(dictt))

