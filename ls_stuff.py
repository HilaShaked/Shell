import datetime
import os


def ls_long(dir_data, dir_path):
    lines = []  # a list of lists
    for i in dir_data:
        stat = os.stat(f'{dir_path}/{i}')
        curr = [get_mode(stat.st_mode), f'{stat.st_size}', get_time_from_seconds(stat.st_mtime),
                get_time_from_seconds(stat.st_ctime, True), i]
        lines += [curr]

    return format_ls_long(lines)


def get_mode(st_mode):
    modes = ['r', 'w', 'x']
    st_mode = bin(st_mode)[-9:]
    ret = ''
    for i, val in enumerate(st_mode):
        if val == '0':
            ret += '-'
            continue
        ret += modes[i % 3]
    return ret


def get_time_from_seconds(seconds, c=False):
    curr_time = datetime.datetime.fromtimestamp(seconds)
    if c:
        return curr_time.strftime('%d-%m-%y %H:%M')
    return curr_time.strftime('%a %d-%m-%y %H:%M')


def format_ls_long(lines):
    col_widths = get_col_widths(lines)
    titles = ['mode', 'size', 'last modified', 'date created', 'name']
    space_amount = 4

    ret = format_titles(titles, col_widths, space_amount)

    for line in lines:
        temp = (' '*space_amount).join([val.rjust(col_widths[i]) for i, val in enumerate(line[:-1])] + [line[-1]])
        ret += [temp]

    return ret


def format_titles(titles: list, col_widths: list, spaces: int):
    diffs = [col_widths[i] - len(titles[i]) for i in range(len(titles) - 1)]

    first_title = f"{titles[0]}{' ' * diffs[0]}"
    sec_title = f"{' ' * diffs[1]}{titles[1]}"
    mid_titles = []

    for i, val in enumerate(titles[2:-1]):
        temp = diffs[i + 2]//2
        mid_titles += [f"{temp * ' '}{val}" + f"{(temp + diffs[i] % 2) * ' '}"]

    # last_title = f"{titles[-1]}"

    ret = (' ' * spaces).join([first_title, sec_title] + mid_titles + [titles[-1]])
    return [ret]


def get_col_widths(lines):
    max_field_widths = []
    for i in range(0, len(lines[0])):
        col = [line[i] for line in lines]  # line[i] is current field (col is a list of field #i in each line
        max_field_widths += [len(max(col, key=len))]  # the length of the string with the biggest length
    return max_field_widths
