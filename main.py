from shlex import shlex  # splits like in shell
import traceback
import sys
import os


# curr_path = 'C:/Shell'
SAVE_DIR = os.getcwd()

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
curr_path = FILE_PATH
os.chdir(curr_path)


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

    # return prompt.maketrans(to_replace)  # doesn't work with more than 1 char as the key


def clear_screen(_):
    os.system('cls')


# def change_directory(directory: str):
#     global curr_path
#     if isinstance(directory, list):
#         directory = directory[0]
#
#     directory = directory.replace('/', '\\')
#     new_dir = curr_path + directory
#
#     if directory[1] == ':':
#         new_dir = directory
#     elif './' in directory:
#
#         temp = curr_path.count('..\\')
#         new_dir = curr_path + directory
#
#     if os.path.isdir(new_dir):
#         curr_path = new_dir
#         print(f'Debug: curr_path = {curr_path}')
#
#     print('after check')

def change_directory(new_path: str):
    global curr_path

    if isinstance(new_path, list):
        new_path = new_path[0]

    try:
        os.chdir(new_path)
        curr_path = os.getcwd()
    except WindowsError as e:
        raise e

    # print(f'Debug: curr_path = {curr_path}')


# We need add functions to these:
inner_commands = {'cls': clear_screen, 'cd': change_directory}  # The keys will be the names of the functions, and values will have the functions themselves
external_commands = []


def output(output_method, to_output):  # very temp function. need to change
    if to_output is None:
        print()

    if output_method is None:
        print(to_output)
        return

    print('error', f'\nto_output = {to_output}')



def get_output_location(args: list):  # also temp
    if (not '>' in args) and '>>' not in args:
        return None, None

    to_find, output_mode = '>', 'w'
    if '>>' in args:
        to_find, output_mode = '>>', 'a'

    try:
        return args[args.index(to_find) + 1], output_mode
    except IndexError:
        return None, 'Incorrect syntax of >'


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
            x = input(get_prompt(prompt)).strip()

            # print(f'Debug: x = {x}')
            if x == '':
                continue  # goes back to the beginning of the loop

            x = my_split(x)
            code = x[0].lower()  # function name
            args = x[1:]  # additional arguments (len == 0 if there aren't any)
            print(f'Debug: code = {code}, args = {args}')

            if code == 'exit':
                sys.exit()
                # break


            output_location, err = get_output_location(args)
            if err is not None:
                output(None, err)

            elif code in inner_commands:
                output(output_location, inner_commands[code](args))


            elif code in external_commands:
                pass

            else:
                print(f"'{code}' is not recognized as an internal or external command")

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

    # print(my_split('dir>p.txt <"a file name".txt'))
    # print(my_split('dir>>p.txt <"a file name, wow".txt'))
    # print(get_prompt('$$U$U: $P $G$_$L$L$$ $'))
    # change_directory(input('mashehu > cd '))
