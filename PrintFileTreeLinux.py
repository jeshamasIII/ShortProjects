import colorama
from colorama import Fore, Style
import argparse
import os

colorama.init()

# provides a description and defines path, hidden and maxLevel command line
# arguments
parser = argparse.ArgumentParser(
    description='python script to print file directory'
)
parser.add_argument('-p', '--path', default=os.getcwd(), type=str,
                    metavar='P', help='path to root of file directory')
parser.add_argument('-s', '--show_hidden', action='store_true',
                    default=False, help='show hidden folders and files',)
parser.add_argument('-d', '--max_depth', default=3, type=int,
                    metavar='D', help='Maximum File tree traversal depth')

args = parser.parse_args()

# if path ends with a slash, remove it.
if args.path[-1] == os.sep:
    args.path = args.path[:-1]

# Process output of os.walk by removing hidden files and directories, and
# directories, subdirectories, and files whose depth exceed maximum traversal
# depth.
last_subdirectory = {}
file_tree = []
for current_path, subdirectories, files in os.walk(args.path):

    if (not args.show_hidden
            and any(s.startswith('.') for s in current_path.split(os.sep))):
        continue

    current_path_depth = current_path.count(os.sep) - args.path.count(os.sep)

    if current_path_depth > args.max_depth:
        continue

    if current_path_depth == args.max_depth:
        files = []
        subdirectories = []

    if not args.show_hidden:
        subdirectories = [directory for directory in subdirectories
                          if not directory.startswith('.')]

        files = [file for file in files if not file.startswith('.')]

    if len(subdirectories) > 0:
        last_subdirectory[current_path] = subdirectories[-1]

    file_tree.append((current_path, current_path_depth, subdirectories, files))

# represent file tree as list of strings
# for each directory, print it's name, then first print it's files,
output = []
for current_path, current_path_depth, subdirectories, files in file_tree:

    # split current_path at it's last slash
    current_path_head, current_path_tail = os.path.split(current_path)

    # print name of current directory
    if current_path_depth == 0:
        output.append(Fore.BLUE + current_path_tail + Style.RESET_ALL)

    elif current_path_depth > 0:
        if current_path_tail != last_subdirectory[current_path_head]:
            connector = '├─ '
        else:
            connector = '└─ '

        output.append(
            list(' ' * (3 * (current_path_depth - 1))
                 + connector
                 + Fore.BLUE
                 + current_path_tail
                 + Style.RESET_ALL
                 )
        )

    # connect current directory to it's parent in output
    if len(output) > 1:
        row_number = -2
        while output[row_number][3 * (current_path_depth - 1)] == ' ':
            output[row_number][3 * (current_path_depth - 1)] = '│'
            row_number -= 1

    # append current path's files to output
    for file_index, file in enumerate(files):
        if (file_index < len(files) - 1 or
                file_index == len(files) - 1 and len(subdirectories) > 0):
            output.append(list(' ' * (3 * current_path_depth) + '├─ ' + file))

        elif file_index == len(files) - 1 and len(subdirectories) == 0:
            output.append(list(' ' * (3 * current_path_depth) + '└─ ' + file))

# print output
for line in output:
    print(''.join(line))
