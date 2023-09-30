import sys


def hex_dump(s, SIZE=8):  # s = some string, SIZE  = number of bytes on each line
    """
    print base 16 every byte
    :param s: byte array
    :param SIZE: optional (how many bytes per line)

    :return: Void
    """
    print("len=", len(s))  # ** prints the len here **
    for p in [s[i * SIZE: min((i + 1) * SIZE, len(s))] for i in range(len(s) // SIZE + 1)]:
        return (b" ".join(
            [b"%02X" % int(p[j])  # (also line below) combine the hex numbers to one byte string (not really a string)
             if j < len(p) else b"  " for j in range(SIZE)]).decode() + \
              "       " + " ".join([chr(p[n])  # printing the chars next to the hex, like in the hex editor
                                      if 31 < p[n] < 128 else "." for n in range(len(p))]))




