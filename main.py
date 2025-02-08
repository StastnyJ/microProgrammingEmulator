#!/usr/bin/env python3

from sys import argv
from Emulator import Emulator, EmulatorRunModes
from Assembler import Assembler

from MicroProgram import micro_macro_mapping_PROM, micro_program_memory


if __name__ == "__main__":
    mode = EmulatorRunModes.RUN if len(argv) == 1 else EmulatorRunModes[argv[1]]
    file = input("Path to the file to emulate: ") if len(argv) < 3 else argv[2]
    try:
        program, memory = Assembler.assemble(file)
    except Exception as e:
        print("Failed to assemble the program: {}".format(e))
        exit()

    emulator = Emulator(micro_macro_mapping_PROM=micro_macro_mapping_PROM, micro_program_memory=micro_program_memory)
    emulator.init_memory(memory)
    emulator.insert_program(program)
    emulator.run(mode)