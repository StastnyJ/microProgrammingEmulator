import os
from enum import Enum
from tabulate import tabulate
from typing import Dict, List
from ControlUnit import ControlUnit
from ALU import ALU
from SSCUnit import SSCUnit
from MIInstruction import MicroInstruction

class EmulatorRunModes(Enum):
    RUN = 0
    DEBUG = 1
    FULL_DEBUG = 2

class Emulator:
    def __init__(self, micro_macro_mapping_PROM: Dict[int, int], micro_program_memory: Dict[int, int]):
        self._data_BUS: int = 0
        self._address_BUS: int = 0
        self._memory: Dict[int, int] = {}
        self._micro_macro_mapping_PROM: Dict[int, int] = micro_macro_mapping_PROM
        self._micro_program_memory: Dict[int, int] = micro_program_memory
        self._instruction_register: int = 0
        self._mi_register: int = 0
        self._instruction_counter: int = 0
        self._control_unit = ControlUnit()
        self._alu = ALU()
        self._ssc_unit = SSCUnit()
        self._run_mode = EmulatorRunModes.RUN

        self._last_instruction_address = 0

    def clear_memory(self):
        self._memory = {}

    def set_memory_value(self, address: int, value: int):
        self._memory[address] = value

    def init_memory(self, memory: Dict[int, int]):
        self._memory = memory

    def insert_program(self, program: List[int]):
        for i in range(len(program)):
            self._memory[i] = program[i]

        self._last_instruction_address = len(program) - 1

    def init_registers(self, registers: List[int]):
        self._alu._registers = registers

    def init_status_register(self, status_register: int):
        self._ssc_unit._macro_status = status_register

    def get_status(self):
        return {
            "memory": self._memory,
            "instruction_counter": self._instruction_counter,
            "instruction_register": self._instruction_register,
            "data_bus": self._data_BUS,
            "address_bus": self._address_BUS,
            "cu_stack": self._control_unit._stack,
            "micro_status_register": self._ssc_unit._micro_status,
            "macro_status_register": self._ssc_unit._macro_status,
            "q_register": self._alu._q_reg,
            "registers": self._alu._registers
        }
    
    def run(self, mode: EmulatorRunModes = EmulatorRunModes.RUN):
        self._run_mode = mode
        for _ in range(1000000):
            current_mic = self._control_unit.get_mic()
            mi_instruction = MicroInstruction(self._micro_program_memory[current_mic])

            if mi_instruction._raw_instruction == (1 << 75) - 1:
                print("----------------------------- PROGRAM FINISHED -----------------------------")
                print("Final state of the system\n")
                print(self)
                return self.get_status()
            
            if mode == EmulatorRunModes.FULL_DEBUG or (mode == EmulatorRunModes.DEBUG and current_mic > 2):
                print("Evaluating microinstruction on address: " + str(current_mic))
                print(str(mi_instruction))
                print()
            
            # IC
            if (mi_instruction.ic & 0b0001) + ((mi_instruction.ic & 0b0010) >> 1) + ((mi_instruction.ic & 0b0100) >> 2) + ((mi_instruction.ic & 0b1000)  >> 3) > 1:
                raise Exception("More than 1 instruction counter control bits were set to 1")
            if mi_instruction.ic == 0b0001:
                self._address_BUS = self._instruction_counter
            if mi_instruction.ic == 0b0010:
                self._instruction_counter += 1
            if mi_instruction.ic == 0b0100:
                self._data_BUS = self._instruction_counter

            # ALU
            alu_y_output, alu_status = self._alu.run(
                instruction=mi_instruction.alu_instruction,
                a=mi_instruction.ra_addr if mi_instruction.a_mux else (self._instruction_register >> 4) & 0b1111,
                b=mi_instruction.rb_addr if mi_instruction.b_mux else self._instruction_register & 0b1111,
                c_n=self._ssc_unit.get_c0(),
                d=mi_instruction.constant if mi_instruction.k_mux else self._data_BUS
            )
            if mi_instruction.y_mux & 0b01:
                self._address_BUS = alu_y_output
            if mi_instruction.y_mux & 0b10:
                self._data_BUS = alu_y_output

            if mi_instruction.ic == 0b1000:
                self._instruction_counter = self._data_BUS
            # IR
            if mi_instruction.ir:
                self._instruction_register = self._data_BUS
            # SSCU
            status_test = self._ssc_unit.run(
                status=alu_status,
                ce_macro=mi_instruction.srM,
                ce_micro=mi_instruction.srm,
                instruction=mi_instruction.sscu_instruction
            )
            # Controller
            opcode = (self._instruction_register >> 8) & 0b11111111
            if opcode not in self._micro_macro_mapping_PROM and opcode != 0:
                raise Exception(f"Opcode {opcode} is not present in PROM")
            self._control_unit.run(
                bar=mi_instruction.bar,
                ccen=mi_instruction.ccen,
                cc=status_test,
                d=self._micro_macro_mapping_PROM[opcode] if opcode != 0 else 0,
                instruction=mi_instruction.controller_instruction
            )

            # Memory
            if mi_instruction.mwe:
                self._memory[self._address_BUS] = self._data_BUS
            else:
                self._data_BUS = self._memory[self._address_BUS] if self._address_BUS in self._memory else 0
            
            if mode == EmulatorRunModes.FULL_DEBUG or (mode == EmulatorRunModes.DEBUG and current_mic > 2):
                print("State of the system after the instruction\n")
                print(self)
                print("Press ENTER to continue...")
                input()
                os.system('cls' if os.name == 'nt' else 'clear')
            
                
        print("Emulator terminated after 1000000 instructions")
        return None


    def __str__(self):
        memory_table = [["Address", "Data"]]
        for i in sorted(self._memory.keys()):
            if (self._run_mode == EmulatorRunModes.FULL_DEBUG or i > self._last_instruction_address) and self._memory[i] != 0:
                memory_table.append(["0x{:04X} ({})".format(i,i), "0x{:04X} ({})".format(self._memory[i], self._memory[i])])
        return "" + str(self._alu) + "\n" + str(self._ssc_unit) + "\n" + str(self._control_unit) + \
            "\nInstruction counter: " + str(self._instruction_counter) + "\nInstruction register: 0x{:04X} ({})".format(self._instruction_register, self._instruction_register) + \
            "\nAddress bus: 0x{:04X} ({})".format(self._address_BUS, self._address_BUS) + "\nData bus: 0x{:04X} ({})".format(self._data_BUS, self._data_BUS) +\
            "\n\n------------ Memory ------------\n" + tabulate(memory_table, headers="firstrow", tablefmt="grid") + "\n"
