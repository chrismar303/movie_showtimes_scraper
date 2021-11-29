def get_zip_code(args):
    validate_input(args)
    return args[1]


def validate_input(args):
    if len(args) <= 1 or not args[1].isdigit():
        print('please enter a valid zipcode')
        sys.exit(-1)
