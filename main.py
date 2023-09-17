import traceback
import os


CURR_PATH = 'C:/temp'


def clear_screen(_):
    os.system('cls')


def change_directory(args):
    # check if there is a c:/ or d:/ etc. (always one letter) and if there is, change the entire 'CURR_PATH'
    # if not, add the directory to the end of 'CURR_PATH'
    # also need to check if these directories actually exists
    pass


# We need add functions to these:
inner_commands = {'cls': clear_screen, 'cd': change_directory}  # The keys will be the names of the functions, and values will have the functions themselves
external_commands = []


def main():
    clear_screen(0)
    prompt = f'{CURR_PATH} > '
    while True:
        try:
            x = input(prompt).strip()
            if x == '':
                continue  # goes back to the beginning of the loop

            x = x.split(' ')
            code = x[0].lower()  # function name
            args = x[1:]  # additional arguments (len == 0 if there aren't any)

            if code == 'exit':
                # sys.exit()
                return  # exit loop (could have used break as well)

            if code in inner_commands:
                inner_commands[code](args)

            elif code in external_commands:
                pass

            else:
                print(f"'{code}' is not recognized as an internal or external command")
            print()  # to make an empty line space down a line

        except Exception as e:
            print(e)
            print(traceback.format_exc())  # Debug



if __name__ == '__main__':
    main()
