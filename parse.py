'''
 @file parse.py
 @brief This is the main file of the project
 @author Jakub Fukala (xfukal01)
'''

import sys
from lark import Lark

def call_help():
    print("Help is here")

def main():
    source_code = sys.stdin.read()
    print(source_code)


if __name__ == "__main__":
    if "--help" in sys.argv:
        call_help()
        sys.exit(0)
    main()

    #Konec souboru parse.py (EOF)
    