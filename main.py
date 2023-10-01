from ls_stuff import *
from shlex import shlex  # splits like in shell
import subprocess
import traceback
import datetime
import time
import sys
import os


SAVE_DIR = os.getcwd()

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
curr_path = FILE_PATH
# os.chdir(curr_path)

output_location = sys.stdout
input_location = sys.stdin
output_mode = 'w'


PATH = [r'C:\Shell\externals', curr_path + r'\externals']  # Would erase the first one, but then it looks too short

prompt = f'$P-@-$U > '


self_enviro = ['PATH', 'PROMPT', 'PYTHONPATH']
enviro_vars = {}



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

    if len(args) != 0 and '-' in args[0] and '?' in args[0]:
        return """"""


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

#
# def ls_long(dir_data, dir_path):
#     ret = ['\nmode\t  size  \tlast modified\t\tdate created  \t\tname\n']
#     for i in dir_data:
#         stat = os.stat(f'{dir_path}/{i}')
#         # print(f"Debug: os.stat(f'{dir_path}/{i}') = {stat}")
#         curr = [get_mode(stat.st_mode), stat.st_size, get_time_from_seconds(stat.st_mtime),
#                 get_time_from_seconds(stat.st_ctime, True)]
#         ret += [f'{curr[0]} {str(curr[1]).zfill(8)}\t{curr[2]}\t{curr[3]}\t\t{i}']  # doesn't look well in files cus
#         # tabs are different
#
#     return ret
#
#
# def get_mode(st_mode):
#     modes = ['r', 'w', 'x']
#     st_mode = bin(st_mode)[-9:]
#     ret = ''
#     for i, val in enumerate(st_mode):
#         if val == '0':
#             ret += '-'
#             continue
#         ret += modes[i % 3]
#     return ret
#
#
# def get_time_from_seconds(seconds, c=False):
#     curr_time = datetime.datetime.fromtimestamp(seconds)
#     if c:
#         return curr_time.strftime('%d-%m-%y %H:%M')
#     return curr_time.strftime('%b %d-%m-%y %H:%M')
#

def title(args):
    return args[0].title()


def cool(_):
    import time
    for x in range(0, 4):
        b = "Loading" + "." * x
        print(b, end="\r")
        time.sleep(1)


def copy(args):  # initial copy
    src_dst = [x for x in args if x[0] != '/']
    src = src_dst[0]
    dst = src_dst[1]

    with open(src, 'r') as f:
        data = f.read()

    with open(dst, 'w') as f:
        f.write(data)


def my_set(args):  # initial set
    def format_enviro():
        enviro_sorted = sorted(enviro_vars)
        return '\r\n'.join(f'{x}={enviro_vars[x]}' for x in enviro_sorted)

    if len(args) == 0:
        return format_enviro()



inner_commands = {'cls': clear_screen, 'cd': change_directory, 'ls': ls, 'title': title, 'cool': cool}
external_commands = {'print': 'print.py'}



def get_prompt():
    """ replaces all the $ stuff with their values specified in the 'to_replace' dictionary """
    global prompt

    to_replace = {'$P': curr_path, '$U': os.getenv("USERNAME"), '$_': '\n', '$G': '>', '$L': '<', '$b': '\\', '$f': '/',
                  '$T': datetime.datetime.now().strftime("%H:%M"), '$d': datetime.datetime.now().strftime('%d-%m-%y'),
                  '$D': datetime.datetime.now().strftime('%a %d-%m-%y'), '$A': '&', '$B': '|', '$C': '(', '$F': ')',
                  '$H': '\b', '$N': enviro_vars['SystemDrive'], '$Q': '=', '$S': ' '}
    to_replace_order = ['$$'] + list(to_replace.keys()) + ['%temp%']  # so that $$ gets replaced first, and %temp% last
    to_replace['$$'] = '%temp%'
    to_replace['%temp%'] = '$'

    for i in to_replace_order:
        prompt = prompt.replace(i, to_replace[i])

    return prompt


def run_func(func: str, args: list):
    if func in inner_commands:
        return inner_commands[func](args)
    # if func in external_commands:
    #     temp = subprocess.run(['python', external_commands[func]] + args)
    #     return temp.stdout
    ret = run_external(func, args)
    if ret is None:
        ret = run_external(func, args, add_python=True)
    return ret


def run_external(func: str, args: list, add_python=False):
    before = []
    if add_python:
        before = ['python']
        func += '.py'

    if func in os.listdir(curr_path):
        temp = subprocess.run(before + [func] + args)
        return temp.stdout
    else:
        for i in PATH:
            try:
                dir_cont = os.listdir(i)
                if func in dir_cont:
                    temp = subprocess.run(before + [i + f'/{func}'] + args)
                    return temp.stdout
            except FileNotFoundError:
                pass


def does_external_exist(func_name: str):
    # if func_name in external_commands:
    #     return True

    for i in PATH + [curr_path]:
        try:
            dir_cont = os.listdir(i)
            if func_name in dir_cont or func_name + '.py' in dir_cont:
                return True
        except FileNotFoundError:
            pass

    return False


def is_shell_command(func_name: str):
    return not (func_name in inner_commands or does_external_exist(func_name) or func_name in self_enviro)


def output(to_output):  # very temp function. need to change
    if to_output is None:
        print()
        return

    # print(f'Debug: output_location = {output_location}, output_mode = {output_mode}')
    if output_location == sys.stdout or not isinstance(output_location, str):
        print(to_output)
        sys.stdout.flush()
        return

    with open(output_location, output_mode) as f:
        print(to_output, file=f)
        sys.stdout.flush()

    # print('error', f'\nto_output = {to_output}')


def get_output_location(args: list):  # also temp
    global output_location, output_mode

    if '>' not in args and '>>' not in args:
        output_location, output_mode = sys.stdout, 'w'
        return

    to_find, output_mode = '>', 'w'
    if '>>' in args:
        to_find, output_mode = '>>', 'a'

    # try:
    #     # > is always at the end
    #     # index = args.index(to_find)
    #     # output_location, output_mode = args[index + 1], output_mode
    #     # del args[index]
    #     # del args[index]
    # except IndexError:
    #     raise 'Incorrect syntax of >'
    if args[-2] != to_find:
        raise SyntaxError('Incorrect syntax of >')

    output_location = args.pop(-1)
    del args[-1]



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


def handle_pipes(commands: str):
    # print('Debug: In "handle_pipes"')

    commands = commands.split('|')
    if len(commands) > 2:
        raise SyntaxError('This program does not support more than 1 pipe')
    if len(commands) < 2:
        raise SyntaxError('Bad | synthax or somrthing')

    comm1 = my_split(commands[0])
    comm2 = my_split(commands[1])
    # print(f'Debug: comm1 = {comm1}, comm2 = {comm2}')

    def get_pre(comm: str):
        # if comm in inner_commands or comm in external_commands:
        if comm in inner_commands:
            return ['python', "main.py"], False

        return [], True

    pre_for_1, shell1 = get_pre(comm1[0].lower())
    pre_for_2, shell2 = get_pre(comm2[0].lower())
    # print(f'Debug: pre_for_1 = {pre_for_1}, pre_for_2 = {pre_for_2}')

    args1 = pre_for_1 + comm1
    args2 = pre_for_2 + comm2
    # print(f'Debug: args1 = {args1}, args2 = {args2}')

    p1 = subprocess.Popen(args1, stdout=subprocess.PIPE, shell=shell1)
    p2 = subprocess.Popen(args2, stdin=p1.stdout, shell=shell2)
    p1.stdout.close()

    # print()
    # print()
    # print()

    outs, errs = p2.communicate()

    # print('Debug: Back in "handle_pipes"')

    if outs:
        output(outs)
    elif errs:
        output(errs)


def add_cmd_path_to_path():
    global enviro_vars

    out = subprocess.run(['path'], shell=True, capture_output=True).stdout.decode().strip().split('=')
    out = out[-1].split(';')
    enviro_vars['PATH'] += out  # our path with the cmd path


def add_to_env_the_cmd_env():
    global enviro_vars

    out = subprocess.run('set', shell=True, capture_output=True).stdout.strip().split(b'\r\n')

    for i in out:
        curr = i.split(b'=')
        key = curr[0].decode()
        if key not in enviro_vars:
            enviro_vars[key] = curr[1].decode()


def reset_enviro_vars():
    global enviro_vars

    enviro_vars = {'PATH': PATH, 'PROMPT': prompt, 'PYTHONPATH': curr_path}

    add_to_env_the_cmd_env()
    add_cmd_path_to_path()
    ';'.join(enviro_vars['PATH'])


def main():
    # clear_screen(0)
    while True:
        print()  # to make an empty line space down a line
        try:
            reset_enviro_vars()
            time.sleep(0.05)
            comm = input(get_prompt()).strip()

            if comm == '':
                continue  # goes back to the beginning of the loop

            x = my_split(comm)

            if '|' in x:
                handle_pipes(comm)
                continue

            code = x[0].lower()  # function Name
            args = x[1:]  # additional arguments (len == 0 if there aren't any)
            # print(f'Debug: code = {code}, args = {args}')

            if code == 'exit':
                sys.exit()

            is_shell = is_shell_command(code)

            if is_shell:
                subprocess.run(comm, shell=True)  # works fine unless the script is running in pycharm and trying to
                # call an external command with pipe (works fine in cmd though)
                continue


            get_output_location(args)
            output(run_func(code, args))


        except KeyboardInterrupt:
            pass  # moved the  print to the beginning of the function
        except Exception as e:
            print(e)
            print(f'Debug:')
            print(traceback.format_exc())  # Debug

    os.chdir(SAVE_DIR)


def do_one_main():
    # print('Debug: in "do_one_main"')

    x = sys.argv[1:]

    code = x[0].lower()
    args = x[1:]
    # print(f'Debug: code = {code}, args = {args}')

    if code == 'exit':
        sys.exit()

    is_shell = is_shell_command(code)
    # print(f'Debug: is_shell = {is_shell}')


    if is_shell:
        subprocess.run(x, shell=True)
        return

    # print(f'Debug:\n{ls([])}')
    # temp = func([])
    # output(f'Debug: temp = \n{temp}')
    get_output_location(args)
    output(run_func(code, args))


if __name__ == '__main__':
    reset_enviro_vars()
    if len(sys.argv) > 1:
        do_one_main()
    else:
        main()
    # os.chdir(SAVE_DIR)

    # print(my_split('dir>p.txt <"a file Name".txt'))
    # print(my_split('dir>>p.txt <"a file Name, wow".txt'))
    # print(get_prompt('$$U$U: $P $G$_$L$L$$ $'))
    # change_directory(input('mashehu > cd '))

    # print(datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))
