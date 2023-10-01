import argparse
import os


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
                hex_string = " ".join([f"{data[i + 1]:02x}{data[i]:02x}" if i + 1 < len(data) else f"00{data[i]:02x}"
                                       for i in range(0, len(data), 2)])
                print(f"{n * 16:08x}  {hex_string}")

            n += 1

    file_size = os.path.getsize(args.FILE)
    file_size = file_size - args.skip
    if save_len:
        len_ = min(file_size, save_len)
        print(f"{len_:07x}")
    else:
        print(f"{file_size:07x}")


if __name__ == '__main__':
    hexdump()
