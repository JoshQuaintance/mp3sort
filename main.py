import os
import glob
from tkinter import Tk, filedialog

def filter(dir: list) -> list:
    # First filter if folder starts with '.'
    pass


def main():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    open_file = filedialog.askdirectory()

    # TODO: Make a function to get all the ignored directories
    ignore_list = ['node_modules']

    files = glob.glob(open_file + "/**/*.svelte", recursive=True )
    



if __name__ == "__main__":
    main()