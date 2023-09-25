from shlex import shlex  # splits like in shell
import subprocess
import traceback
import datetime
import sys
import os


SAVE_DIR = os.getcwd()

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
curr_path = FILE_PATH
os.chdir(curr_path)

output_location = sys.stdout
input_location = sys.stdin
output_mode = 'w'


PATH = [r'C:\Shell\externals']


def get_prompt(prompt):
    """
    replaces all the $ stuff with their values specified in the 'to_replace' dictionary
    """
    to_replace = {'$P': curr_path, '$U': os.getenv("USERNAME"), '$_': '\n', '$G': '>', '$L': '<', '$B': '\\', '$F': '/'}
    to_replace_order = ['$$'] + list(to_replace.keys()) + ['%temp%']  # so that $$ gets replaced first, and %temp% last
    to_replace['$$'] = '%temp%'
    to_replace['%temp%'] = '$'

    for i in to_replace_order:
        prompt = prompt.replace(i, to_replace[i])

    return prompt


def clear_screen(_):
    os.system('cls')


def change_directory(new_path: str):
    global curr_path

    if len(new_path) == 0:
        return curr_path

    if isinstance(new_path, list):
        new_path = new_path[0]

    try:
        os.chdir(new_path)
        curr_path = os.getcwd()
    except WindowsError as e:
        raise e


def ls(args):
    """
    -l	known as a long format that displays detailed information about files and directories.          √
    -a	Represent all files Include hidden files and directories in the listing.                        √
    -m	Displaying the files and directories by the most recently modified ones first.                  √
    -c	Displaying the files and directories by the most recently created ones first.                   √
    -r	known as reverse order which is used to reverse the default order of listing.                   √
    -s	Sort files and directories by their sizes, listing the largest ones first.                      √
    -d	List only directories                                                                           √
    ** size will always take priority when sorting with both size and mod date
    """
    if len(args) == 0 or args[0][0] == '-':
        dir_path = curr_path
    else:
        dir_path = args[0]
        del args[0]


    dir_cont = os.listdir(dir_path)

    ret = [x for x in dir_cont if x[0] != '.']
    if len(args) != 0 and '-' in args[0]:
        if 'a' in args[0]:
            ret = dir_cont
        elif 'd' in args[0]:
            ret = [x for x in dir_cont if '.' not in x]

        if 'm' in args[0]:
            ret.sort(key=lambda x: os.stat(f'{dir_path}/{x}').st_mtime, reverse=True)

        if 'c' in args[0]:
            ret.sort(key=lambda x: os.stat(f'{dir_path}/{x}').st_ctime, reverse=True)

        if 's' in args[0]:
            ret.sort(key=lambda x: os.stat(f'{dir_path}/{x}').st_size, reverse=True)

        if 'l' in args[0]:
            ret = ls_long(ret, dir_path)

        if 'r' in args[0]:
            ret.reverse()

    return '\n'.join(ret)


def ls_long(dir_data, dir_path):
    ret = ['\nmode\t  size  \tlast modified\t\tdate created  \t\tname\n']
    for i in dir_data:
        stat = os.stat(f'{dir_path}/{i}')
        # print(f"Debug: os.stat(f'{dir_path}/{i}') = {stat}")
        curr = [get_mode(stat.st_mode), stat.st_size, get_time(stat.st_mtime), get_time(stat.st_ctime, True)]
        ret += [f'{curr[0]} {str(curr[1]).zfill(8)}\t{curr[2]}\t{curr[3]}\t\t{i}']

    return ret


def get_mode(st_mode):
    modes = ['r', 'w', 'x']
    st_mode = bin(st_mode)[-9:]
    ret = ''
    for i, val in enumerate(st_mode):
        if val == '0':
            ret += '-'
            continue
        ret += modes[i%3]
    return ret


def get_time(seconds, c=False):
    time = datetime.datetime.fromtimestamp(seconds)
    if c:
        return time.strftime('%d-%m-%y %H:%M')
    return time.strftime('%b %d-%m-%y %H:%M')


def title(args):
    return args[0].title()


# We need add functions to these:
inner_commands = {'cls': clear_screen, 'cd': change_directory, 'ls': ls, 'title': title}
external_commands = []


def get_func(func_name):
    if func_name in inner_commands:
        return inner_commands[func_name]

    return None


def output(to_output):  # very temp function. need to change
    if to_output is None:
        print()
        return

    # print(f'Debug: output_location = {output_location}, output_mode = {output_mode}')
    if output_location == sys.stdout:
        print(to_output)
        return

    with open(output_location, output_mode) as f:
        print(to_output, file=f)

    # print('error', f'\nto_output = {to_output}')


def get_output_location(args: list):  # also temp
    global output_location, output_mode

    if (not '>' in args) and '>>' not in args:
        output_location, output_mode = sys.stdout, 'w'
        return

    to_find, output_mode = '>', 'w'
    if '>>' in args:
        to_find, output_mode = '>>', 'a'

    try:
        index = args.index(to_find)
        output_location, output_mode = args[index + 1], output_mode
        del args[index]
        del args[index]
        return
    except IndexError:
        raise 'Incorrect syntax of >'


def my_split(s: str, comments=False, posix=True):
    """
    the shlex.split() calls shlex with 'punctuation_chars=False'
    so stuff like < don't get split
    this function just does what shlex.split() does but with 'punctuation_chars=True'
    """
    s = s.replace('\\', '/')  # cuz the shlex makes '\' disappear, and there shouldn't be a difference between them
    if s is None:
        import warnings
        warnings.warn("Passing None for 's' to shlex.split() is deprecated.",
                      DeprecationWarning, stacklevel=2)
    lex = shlex(s, posix=posix, punctuation_chars=True)
    lex.whitespace_split = True
    if not comments:
        lex.commenters = ''
    return list(lex)


def main():
    clear_screen(0)
    prompt = f'$P-@-$U > '
    print()
    while True:
        try:
            comm = input(get_prompt(prompt)).strip()

            if comm == '':
                continue  # goes back to the beginning of the loop

            x = my_split(comm)
            code = x[0].lower()  # function Name
            args = x[1:]  # additional arguments (len == 0 if there aren't any)
            print(f'Debug: code = {code}, args = {args}')

            if code == 'exit':
                sys.exit()

            func = get_func(code)

            if func is None:
                subprocess.run(comm, shell=True, encoding='utf-8')  # it's fine as long as you don't call to external commands when a shell command is first
                continue

            do_pipes = False
            if not do_pipes:
                get_output_location(args)
                output(func(args))

            # elif code in inner_commands:
            #     output(output_location, inner_commands[code](args))
            #
            #
            # elif code in external_commands:
            #     pass
            #
            # else:
            #     print(f"'{code}' is not recognized as an internal or external command")

            print()  # to make an empty line space down a line


        except KeyboardInterrupt:
            print()
        except Exception as e:
            print(e)
            print(traceback.format_exc())  # Debug

    os.chdir(SAVE_DIR)



if __name__ == '__main__':
    main()
    # os.chdir(SAVE_DIR)

    # print(my_split('dir>p.txt <"a file Name".txt'))
    # print(my_split('dir>>p.txt <"a file Name, wow".txt'))
    # print(get_prompt('$$U$U: $P $G$_$L$L$$ $'))
    # change_directory(input('mashehu > cd '))
