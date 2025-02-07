from tabulate import tabulate

class ALU:
    def __init__(self):
        self._q_reg = 0
        self._registers = [0] * 16

    def run(self, instruction: int, a: int, b: int, d: int, c_n: int):
        data_select = instruction & 0b111
        opcode = (instruction >> 3) & 0b111
        result_select = instruction >> 6
        if result_select > 0b011:
            raise Exception("ALU: unsupported result select")

        R = self._registers[a] if data_select <= 0b001 else 0 if data_select <= 0b100 else d
        S = self._q_reg if data_select in [0b000, 0b010, 0b110] else self._registers[b] if data_select in [0b001, 0b011] else self._registers[a] if data_select in [0b100, 0b101] else 0

        res = 0
        if opcode == 0b000: # ADD
            res = R + S + c_n
        if opcode == 0b001: # SUBR
            res = S - R - c_n
        if opcode == 0b010: # SUBS
            res = R - S - c_n
        if opcode == 0b011: # OR
            res = R | S
        if opcode == 0b100: # AND
            res = R & S
        if opcode == 0b101: # NOTRS
            res = (R ^ 0xFFFF) & S
        if opcode == 0b110: # EXOR
            res = R ^ S
        if opcode == 0b111: # EXNOR
            res = (R ^ S) ^ 0xFFFF

        overflow = res > 0xFFFF or res < 0
        negative = res < 0
        res = res & 0xFFFF
        output = self._registers[a] if result_select == 0b010 else res

        if result_select == 0b001:
            self._q_reg = res
        if result_select == 0b010 or result_select == 0b011:
            self._registers[b] = res

        status = 0
        if overflow:
            status += 0b1100
        if negative:
            status += 0b0010
        if res == 0:
            status += 0b0001

        return output, status 

    def __str__(self):
        table = [
            ["r00", "r01", "r02", "r03", "r04", "r05", "r06", "r07", "r08", "r09", "r10", "r11", "r12", "r13", "r14", "r15"],
            ["0" if r == 0 else "{}\n0x{:04X}".format(r, r) for r in  self._registers]
        ]
        return "------------ ALU status ------------\nRegisters\n" + tabulate(table, headers="firstrow", tablefmt="grid") + "\nQ register: {:04X} ({})\n".format(self._q_reg, self._q_reg)