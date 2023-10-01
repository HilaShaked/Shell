import argparse
import os
import sys


def hex_dump(dic) -> str:  # s = some string, SIZE  = number of bytes on each line
    """
    print base 16 every byte
    :param s: byte array
    :param SIZE: optional (how many bytes per line)

    :return: Void
    """
    ret = b''
    read_amount = dic.get('n', -1)
    with open(dic['file'], 'rb') as f:
        if read_amount <= -1:
            s = f.read()
        else:
            s = f.read(read_amount)



    size = dic.get('size', 16)

    # print("len=", len(s))  # ** prints the len here **
    # for p in [s[i * SIZE: min((i + 1) * SIZE, len(s))] for i in range(len(s) // SIZE + 1)]:
    #     return (b" ".join(
    #         [b"%02X" % int(p[j])  # (also line below) combine the hex numbers to one byte string (not really a string)
    #          if j < len(p) else b"  " for j in range(SIZE)]).decode() +
    #           "       " + " ".join([chr(p[n])  # printing the chars next to the hex, like in the hex editor
    #                                   if 31 < p[n] < 128 else "." for n in range(len(p))]))


    # print("len=", len(s))  # ** prints the len here **
    for p in [s[i * size: min((i + 1) * size, len(s))] for i in range(len(s) // size + 1)]:
        ret += b"" + b" ".join([b"%02X" % int(p[j]) if j < len(p) else b"  " for j in range(size)]) + \
              b"       |" + b" ".join([chr(p[n]).encode() if 31 < p[n] < 128 else b"." for n in range(len(p))])

        ret += b'|\n'

    return ret.decode()



def run_hex(args):
    when_help = """
    Usage:
    hexdump [options] <file>...
    Display file contents in hexadecimal, decimal, octal, or ascii.
    Options:
    -b, --one-byte-octal      one-byte octal display
    -c, --one-byte-char       one-byte character display
    -C, --canonical           canonical hex+ASCII display
    -d, --two-bytes-decimal   two-byte decimal display
    -o, --two-bytes-octal     two-byte octal display
    -x, --two-bytes-hex       two-byte hexadecimal display
    -n, --length <length>     interpret only length bytes of input
    -s, --skip <offset>       skip offset bytes from the beginning
    -v, --no-squeezing        output identical lines
    -h, --help                display this help
    """
    # ** o is the little indian way it normally presents in, but in octal
    # ** x is exactly the same as the normal way, but with more spaces between he numbers
    # ** v is x but without the tabs between (so it's just normal)
    # should we keep the long stuff?
    # also you can stack the options (-bC, for example, will have one line like -b, and another one like -C)

    dictt = {'file': args[-1]}
    if '-b' in args:
        dictt['b'] = True
    if '-c' in args:
        dictt['c'] = True
    if '-C' in args:
        dictt['C'] = True
    if '-d' in args:
        dictt['d'] = True
    if '-o' in args:
        dictt['o'] = True
    if '-x' in args:
        dictt['x'] = True
    if '-n' in args:
        dictt['n'] = int(args[args.index('-n') + 1])
    if '-s' in args:
        dictt['s'] = int(args[args.index('-s') + 1])
    if '-v' in args:
        dictt['v'] = True
    if '-h' in args or '--help' in args:
        print(when_help)
        return
    print(hex_dump(dictt))



def hexdump():
    parser = argparse.ArgumentParser()
    parser.add_argument("FILE", help="the name of the file that you wish to dump", type=str)
    parser.add_argument("-b", "--one-byte-octal", help="one-byte octal display", action="store_true")
    parser.add_argument("-c", "--one-byte-char", help="one-byte character display", action="store_true")
    parser.add_argument("-C", "--canonical", help="canonical hex+ASCII display", action="store_true")
    parser.add_argument("-d", "--two-bytes-decimal", help="two-byte decimal display", action="store_true")
    parser.add_argument("-o", "--two-bytes-octal", help="two-byte octal display", action="store_true")
    parser.add_argument("-x", "--two-bytes-hex", help="interpret only length bytes of input", action="store_true")
    parser.add_argument("-n, --length", help="canonical hex+ASCII display", type=int, metavar='<length>', dest='length')
    parser.add_argument("-s, --skip", help="skip offset bytes from the beginning", type=int, default=0, dest='skip',
                        metavar='<offset>')
    parser.add_argument("-v", "--no-squeezing", help="output identical lines", action="store_true")
    args = parser.parse_args()

    save_len = args.length

    with open(args.FILE, "rb") as f:
        f.read(args.skip)

        n = 0
        amount_to_read = 16

        no_args = True
        if args.one_byte_octal or args.one_byte_char or args.canonical or args.two_bytes_decimal or \
            args.two_bytes_octal or args.two_bytes_hex:
            no_args = False

        while True:
            if args.length == 0:
                break

            if args.length:
                amount_to_read = min(args.length, amount_to_read)
                args.length -= amount_to_read

            one_data_line = f.read(amount_to_read)

            if not one_data_line:
                break


            if args.one_byte_octal:  # -b
                octal_string = " ".join([f"{i:03o}" for i in one_data_line])
                print(f"{n * 16:08x}  {octal_string}")

            if args.one_byte_char:  # -c
                string = "  ".join([repr(chr(i))[1:-1] for i in one_data_line])
                print(f"{n * 16:08x}  {string}")

            if args.canonical:  # -C
                hex_string = " ".join([f"{i:02x}" for i in one_data_line])
                hex_string = hex_string[:23] + " " + hex_string[23:]
                line_width = 48
                ascii_string = "".join([chr(i) if 32 <= i <= 127 else "." for i in one_data_line])
                print(f"{n * 16:08x}  {hex_string:<{line_width}}  |{ascii_string}|")

            if args.two_bytes_decimal:  # -d
                data = one_data_line
                decimal_string = " ".join([str(int(f"{data[i + 1]:02x}{data[i]:02x}", 16))
                                           for i in range(0, len(data), 2)])
                print(f"{n * 16:08x}  {decimal_string}")

            if args.two_bytes_octal:  # -o
                data = one_data_line
                oct_string = " ".join([f'{int(f"{data[i + 1]:02x}{data[i]:02x}", 16):06o}'
                                           for i in range(0, len(data), 2)])
                print(f"{n * 16:08x}  {oct_string}")

            if args.two_bytes_hex:  # -x
                data = one_data_line
                hex_string = "   ".join([f"{data[i + 1]:02x}{data[i]:02x}" for i in range(0, len(data), 2)])
                print(f"{n * 16:08x}   {hex_string}")

            if args.no_squeezing or no_args:  # -v
                data = one_data_line
                hex_string = " ".join([f"{data[i + 1]:02x}{data[i]:02x}" for i in range(0, len(data), 2)])
                print(f"{n * 16:08x}  {hex_string}")

            n += 1

    file_size = os.path.getsize(args.FILE)
    file_size = file_size - args.skip
    if save_len:
        len_ = min(file_size, save_len)
        print(f"{len_:07x}")
    else:
        print(f"{file_size:07x}")



# print(sys.argv[1])
# run_hex(sys.argv[1:])

hexdump()
