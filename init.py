from src.util import *


def modules():
    return "Battle"


def h():
    print("Control Functions:\n\
    modules()\tprint a list of loaded modules\n\
    [module_name]()\topen an interactive session for the given module\n\
    [module_name](\"function_name\", [args])\tcall [function] on the given module with arguments [args]")


def main():
    print("To load an interactive session, run \"python -i init.py\"")
    print("Welcome to the DM assistant!  Type 'h()' for a list of commands")


if __name__ == "__main__":
    main()
