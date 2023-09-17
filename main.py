import traceback

CURR_PATH = 'C:/temp'

# We need add functions to these:
inner_commands = {}  # The keys will be the names of the functions, and values will have the functions themselves
external_commands = []


def main():
    prompt = f'{CURR_PATH} > '
    while True:
        try:
            x = input(prompt)
            x = x.split(' ')
            code = x[0]  # function name
            args = x[1:]  # additional arguments (len == 0 if there aren't any)

            if code in inner_commands:
                inner_commands[code](args)
            elif code in external_commands:
                pass
            else:
                print(f"'{code}' is not recognized as an internal or external command")

        except Exception as e:
            print(e)
            print(traceback.format_exc())  # Debug



if __name__ == '__main__':
    main()
