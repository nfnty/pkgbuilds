#!/usr/bin/python3
''' Convert '''

import os
import sys

PATH = os.path.realpath(sys.argv[1])


def main():
    ''' Main '''
    for filename in os.listdir(PATH):
        path = os.path.join(PATH, filename)
        newfile = ''
        with open(path) as filedesc:
            for line in filedesc.readlines():
                split = line.split()
                if split[0] == '24':
                    size0 = str(round(int(split[0]) / 2))
                    size1 = str(round(int(split[1]) / 2))
                    size2 = str(round(int(split[2]) / 2))
                elif split[0] == '48':
                    size0 = str(round(int(split[0]) / 3))
                    size1 = str(round(int(split[1]) / 3))
                    size2 = str(round(int(split[2]) / 3))
                else:
                    raise RuntimeError('size0 is unknown')

                newfile += '{0:s} {1:s} {2:s} {3:s}\n'.format(
                    size0, size1, size2, ' '.join(split[3:]))

        with open(path, 'w') as filedesc:
            filedesc.write(newfile)

if __name__ == '__main__':
    main()
