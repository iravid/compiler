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
    logging.info("Reading %s", cpl_filename)
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

            lst_file.write("Compile log:\n")
    except EnvironmentError, e:
        logging.critical("Could not open %s: %s", lst_filename, str(e))
        return 1

    # Configure the compile logger to append error messages to the .lst file
    compile_logger = logging.getLogger("compile")
    compile_logger.setLevel(logging.INFO)

    stderr_handler = logging.StreamHandler(sys.stderr)
    lst_handler = logging.FileHandler(lst_filename)

    formatter = logging.Formatter("%(levelname)s: %(message)s")
    stderr_handler.setFormatter(formatter)
    lst_handler.setFormatter(formatter)

    compile_logger.addHandler(lst_handler)

    # Start compilation
    compile_logger.info("Compiled by a CPQ compiler written by Itamar Ravid")
    logging.info("Compiling CPL code")
    cpl_parser.parse("".join(cpl_data))
    if codegen_context.errors:
        logging.error("Errors during compilation. Exiting.")
        return 1

    # Generate code for the AST
    codegen_context.root.codegen(codegen_context)

    # Write quad code into .qud file
    qud_filename = os.path.basename(cpl_filename).split(".")[0] + ".qud"
    try:
        with open(qud_filename, "w") as qud_file:
            logging.info("Writing out QUAD instructions to %s", qud_filename)
            quad_code = codegen_context.get_code()
            qud_file.write(quad_code)
            qud_file.write("\n\nCompiled by a CPQ compiler written by Itamar Ravid\n")
    except EnvironmentError, e:
        logging.critical("Could not open %s: %s", qud_filename, str(e))
        return 1

    return 0


if __name__ == "__main__":
    arg_parser = get_parser()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = arg_parser.parse_args()

    logging.info("CPQ Compiler by Itamar Ravid")

    ret = compile_cpl(args.cpl_file)
    sys.exit(ret)