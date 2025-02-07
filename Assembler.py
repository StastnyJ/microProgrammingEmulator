import re
from typing import List, Tuple, Dict

'''
Supported instructions:

MOV <r_a> <r_b>     Opcode 0x01
MOV const <r_b>     Opcode 0x02
MOV [<r_a>] <r_b>   Opcode 0x03
MOV <r_a> [<r_b>]   Opcode 0x04
ADD <r_a> <r_b>     Opcode 0x05
SUB <r_a> <r_b>     Opcode 0x06
CMP <r_a> <r_b>     Opcode 0x07
XOR <r_a> <r_b>     Opcode 0x08
TEST <r_a> <r_b>    Opcode 0x09
JMP <r_b>           Opcode 0x0A
JMP const           Opcode 0x0B
JZ <r_b>            Opcode 0x0C
JZ const            Opcode 0x0D
JL <r_b>            Opcode 0x0E
JL const            Opcode 0x0F
JLE <r_b>           Opcode 0x10
JLE const           Opcode 0x11
WTF                 Opcode 0x12
UPP <r_a> <r_b>     Opcode 0x13
'''

def is_register(s: str) -> bool:
    return s[0] == "r" and s[1:].isnumeric() and int(s[1:]) <= 15 and int(s[1:]) >= 0

def is_memory_request(s: str) -> bool:
    return s[0] == "[" and s[-1] == "]" and is_register(s[1:-1])

def is_constant(s: str) -> bool:
    if s.isnumeric():
        return int(s) < 2**16
    if s.startswith("0x"):
        return int(s[2:], 16) < 2**16
    if s.startswith("0b") and s[2:].isnumeric():
        return int(s[2:], 2) < 2**16
    return False

class Assembler:
    @staticmethod
    def assemble_string(program: str) -> Tuple[List[int], Dict[int, int]]:
        instructions = []
        memory = {}
        loadingMemory = False
        for l in program.split("\n"):
            line = re.sub(r'[ ]+', " ", re.sub(r'\s', ' ', l)).strip().lower()
            if line == "":
                continue
            if line == "memory:":
                loadingMemory = True
                continue
            if loadingMemory:
                data = line.split(":")
                assert len(data) == 2 and is_constant(data[0]) and is_constant(data[1]), "Invalid memory request: {}".format(line)
                memory[Assembler._parse_constant(data[0])] = Assembler._parse_constant(data[1])
            else:
                instructions += Assembler._parse_instruction(line)
        instructions += [Assembler._build_instruction(0b11111111, 0, 0)]
        return instructions, memory

    @staticmethod
    def _parse_instruction(line: str) -> List[int]:
        operands = line.split(" ")
        if operands[0] == "mov":
            assert len(operands) == 3 and ((is_register(operands[1]) and is_register(operands[2])) or (is_constant(operands[1]) and is_register(operands[2])) or (is_memory_request(operands[1]) and is_register(operands[2])) or (is_register(operands[1]) and is_memory_request(operands[2]))), "Invalid instruction: {}".format(line)
            if is_register(operands[1]) and is_register(operands[2]):
                return [Assembler._build_instruction(1, int(operands[1][1:]), int(operands[2][1:]))]
            elif is_constant(operands[1]) and is_register(operands[2]):
                return [Assembler._build_instruction(2, 0, int(operands[2][1:])), Assembler._parse_constant(operands[1])]
            elif is_memory_request(operands[1]) and is_register(operands[2]):
                return [Assembler._build_instruction(3, int(operands[1][2:-1]), int(operands[2][1:]))]
            elif is_register(operands[1]) and is_memory_request(operands[2]):
                return [Assembler._build_instruction(4, int(operands[1][1:]), int(operands[2][2:-1]))]
        if operands[0] == "add":
            assert len(operands) == 3 and is_register(operands[1]) and is_register(operands[2]), "Invalid instruction: {}".format(line)
            return [Assembler._build_instruction(5, int(operands[1][1:]), int(operands[2][1:]))]
        if operands[0] == "sub":
            assert len(operands) == 3 and is_register(operands[1]) and is_register(operands[2]), "Invalid instruction: {}".format(line)
            return [Assembler._build_instruction(6, int(operands[1][1:]), int(operands[2][1:]))]
        if operands[0] == "cmp":
            assert len(operands) == 3 and is_register(operands[1]) and is_register(operands[2]), "Invalid instruction: {}".format(line)
            return [Assembler._build_instruction(7, int(operands[1][1:]), int(operands[2][1:]))]
        if operands[0] == "xor":
            assert len(operands) == 3 and is_register(operands[1]) and is_register(operands[2]), "Invalid instruction: {}".format(line)
            return [Assembler._build_instruction(8, int(operands[1][1:]), int(operands[2][1:]))]
        if operands[0] == "test":
            assert len(operands) == 3 and is_register(operands[1]) and is_register(operands[2]), "Invalid instruction: {}".format(line)
            return [Assembler._build_instruction(9, int(operands[1][1:]), int(operands[2][1:]))]
        if operands[0] == "jmp":
            assert len(operands) == 2 and is_register(operands[1]) or is_constant(operands[1]), "Invalid instruction: {}".format(line)
            if is_register(operands[1]):
                return [Assembler._build_instruction(10, 0, int(operands[1][1:]))]
            else:
                return [Assembler._build_instruction(11, 0, 0), Assembler._parse_constant(operands[1])]
        if operands[0] == "jz":
            assert len(operands) == 2 and is_register(operands[1]) or is_constant(operands[1]), "Invalid instruction: {}".format(line)
            if is_register(operands[1]):
                return [Assembler._build_instruction(12, 0, int(operands[1][1:]))]
            else:
                return [Assembler._build_instruction(13, 0, 0), Assembler._parse_constant(operands[1])]
        if operands[0] == "jl":
            assert len(operands) == 2 and is_register(operands[1]) or is_constant(operands[1]), "Invalid instruction: {}".format(line)
            if is_register(operands[1]):
                return [Assembler._build_instruction(14, 0, int(operands[1][1:]))]
            else:
                return [Assembler._build_instruction(15, 0, 0), Assembler._parse_constant(operands[1])]
        if operands[0] == "jle":
            assert len(operands) == 2 and is_register(operands[1]) or is_constant(operands[1]), "Invalid instruction: {}".format(line)
            if is_register(operands[1]):
                return [Assembler._build_instruction(16, 0, int(operands[1][1:]))]
            else:
                return [Assembler._build_instruction(17, 0, 0), Assembler._parse_constant(operands[1])]
        if operands[0] == "wtf":
            assert len(operands) == 1, "Invalid instruction: {}".format(line)
            return [Assembler._build_instruction(18, 0, 0)]
        if operands[0] == "upp":
            assert len(operands) == 3 and is_register(operands[1]) and is_register(operands[2]), "Invalid instruction: {}".format(line)
            return [Assembler._build_instruction(19, int(operands[1][1:]), int(operands[2][1:]))]

    @staticmethod
    def _build_instruction(opcode: int, reg_a: int, reg_b: int) -> int:
        return opcode << 8 | reg_a << 4 | reg_b
    
    @staticmethod
    def _parse_constant(s: str) -> int:
        if s.isnumeric():
            return int(s)
        if s.startswith("0x"):
            return int(s[2:], 16)
        if s.startswith("0b") and s[2:].isnumeric():
            return int(s[2:], 2)
        return 0

    
    @staticmethod
    def assemble(file: str) -> Tuple[List[int], Dict[int, int]]:
        with open(file, "r") as f:
            return Assembler.assemble_string(f.read())
