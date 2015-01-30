__author__ = 'iravid'

import os
import sys
import logging
import argparse

from src.parser import parser as cpl_parser
from src.codegen import context as codegen_context

def get_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("cpl_file", help="CPL file to compile")

    return arg_parser

def compile_cpl(cpl_filename):
    try:
        cpl_data = open(cpl_filename).readlines()
    except EnvironmentError, e:
        logging.critical("Could not open %s: %s", cpl_filename, str(e))
        return 1

    # Copy CPL data to an .lst file with prepended line numbers
    lst_filename = os.path.basename(cpl_filename).split(".")[0] + ".lst"
    try:
        with open(lst_filename, "w") as lst_file:
            for index, line in enumerate(cpl_data):
                lst_file.write("%d. %s" % (index + 1, line))
    except EnvironmentError, e:
        logging.critical("Could not open %s: %s", lst_filename, str(e))
        return 1

    cpl_parser.parse("\n".join(cpl_data))
    if codegen_context.errors:
        logging.error("Errors during compilation. Exiting.")
        return 1

    # Generate code for the AST
    codegen_context.root.codegen(codegen_context)

    # Write quad code into .qud file
    qud_filename = os.path.basename(cpl_filename).split(".")[0] + ".qud"
    try:
        with open(qud_filename, "w") as qud_file:
            quad_code = codegen_context.get_code()
            qud_file.write(quad_code)
    except EnvironmentError, e:
        logging.critical("Could not open %s: %s", qud_filename, str(e))
        return 1

    return 0


if __name__ == "__main__":
    arg_parser = get_parser()
    args = arg_parser.parse_args()

    ret = compile_cpl(args.cpl_file)
    sys.exit(ret)