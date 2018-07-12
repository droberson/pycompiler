#!/usr/bin/env python3

"""
  compile python scripts as ELF.
  based on https://gist.github.com/itdaniher/46fec3dd3b7eb603d7cbb5cd55fa5e1d


  pip3 install Cython

  static linking is possible adding -static flag and -l for each required
  library. modify the globals to do this.

"""

from os import EX_USAGE
from sys import argv
from subprocess import check_call
from tempfile import NamedTemporaryFile
from Cython.Compiler import Main


# You might need to change these.
IFLAGS = "-I/usr/include/python3.5"
LFLAGS = "-L/usr/lib/python3.5"
CFLAGS = "-fPIC"
LIBRARIES = "-lpython3.5m"


def main():
    """
    This will do ugly things to compile a python file.
    """
    try:
        source = open(argv[1]).read()
        outfile = argv[1].replace(".py", ".out")
    except IndexError:
        print("usage: ./compile.py <python file>")
        exit(EX_USAGE)

    temp_py_file = NamedTemporaryFile(suffix=".py", delete=False)
    temp_py_file.write(source.encode())
    temp_py_file.flush()

    Main.Options.embed = "main"
    res = Main.compile_single(temp_py_file.name, Main.CompilationOptions(), "")

    gcc_cmd = "gcc %s %s %s %s %s -o %s" % \
        (CFLAGS, res.c_file, LFLAGS, IFLAGS, LIBRARIES, outfile)

    print(gcc_cmd)
    check_call(gcc_cmd.split(" "))


if __name__ == "__main__":
    main()
