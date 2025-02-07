from typing import Dict


micro_macro_mapping_PROM: Dict[int, int] = {
    0x01: 0x0, # TODO - Insert starting address of the instruction: MOV <r_a> <r_b>
    0x02: 0x0, # TODO - Insert starting address of the instruction: MOV const <r_b>
    0x03: 0x0, # TODO - Insert starting address of the instruction: MOV [<r_a>] <r_b>
    0x04: 0x0, # TODO - Insert starting address of the instruction: MOV <r_a> [<r_b>]
    0x05: 0x0, # TODO - Insert starting address of the instruction: ADD <r_a> <r_b>
    0x06: 0x0, # TODO - Insert starting address of the instruction: SUB <r_a> <r_b>
    0x07: 0x0, # TODO - Insert starting address of the instruction: CMP <r_a> <r_b>
    0x08: 0x0, # TODO - Insert starting address of the instruction: XOR <r_a> <r_b>
    0x09: 0x0, # TODO - Insert starting address of the instruction: TEST <r_a> <r_b>
    0x0A: 0x0, # TODO - Insert starting address of the instruction: JMP <r_b>
    0x0B: 0x0, # TODO - Insert starting address of the instruction: JMP const
    0x0C: 0x0, # TODO - Insert starting address of the instruction: JZ <r_b>
    0x0D: 0x0, # TODO - Insert starting address of the instruction: JZ const
    0x0E: 0x0, # TODO - Insert starting address of the instruction: JL <r_b>
    0x0F: 0x0, # TODO - Insert starting address of the instruction: JL const
    0x10: 0x0, # TODO - Insert starting address of the instruction: JLE <r_b>
    0x11: 0x0, # TODO - Insert starting address of the instruction: JLE const
    0x12: 0x0, # TODO - Insert starting address of the instruction: WTF
    0x13: 0x0, # TODO - Insert starting address of the instruction: UPP <r_a> <r_b>
    0xff: 0b1111_1111_1111 # DO NOT REMOVE, IMPORTANT FOR EMULATOR TO STOP
} 

micro_program_memory: Dict[int, int] = {
    # IFETCH
    0: 0b00000_0000000000_0000000000_0000000000_0000000000_0000000011_1000000000_0000000100,
    1: 0b00000_0000000000_0000000000_0000000000_0000000000_0000000011_1000000000_0000001010,
    2: 0b00000_0000000000_0000000000_0000000000_0000000000_0000000000_1000000000_0000000000,
    
    # TODO: PLACE YOUR INSTRUCTIONS HERE

    0b1111_1111_1111: 0b11111_1111111111_1111111111_1111111111_1111111111_1111111111_1111111111_1111111111 # DO NOT REMOVE, IMPORTANT FOR EMULATOR TO STOP
}