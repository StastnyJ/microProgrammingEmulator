from tabulate import tabulate

class SSCUnit:
    def __init__(self):
        # OVR|C|N|Z
        self._micro_status = 0 
        self._macro_status = 0

    def get_c0(self):
        return (self._micro_status & 0b0100) >> 2

    def run(self, status: int, ce_macro: int, ce_micro: int, instruction: int):
        res = 0
        opcode = instruction & 0b111111
        select = (instruction >> 10) & 0b11

        if select == 0b11:
            raise Exception("SSCUnit: select can not be 0b11")
        
        source = self._micro_status if select == 0b10 else self._macro_status if select == 0b01 else None
        if source is not None:
            C = (source & 0b0100) >> 2
            Z = source & 0b0001
            if opcode == 0b000100:
                res = Z ^ 1
            if opcode == 0b000101:
                res = Z
            if opcode == 0b001010:
                res = C ^ 1
            if opcode == 0b001011:
                res = C
            if opcode == 0b001100:
                res = (C ^ 1) & (Z ^ 1)
            if opcode == 0b001101:
                res = C | Z
        
        if ce_macro == 1:
            self._macro_status = status
        if ce_micro == 1:
            self._micro_status = status

        return res
    
    def __str__(self):
        table = [
            ["","OVR", "C", "N", "Z"],
            ["Micro status register", "{}".format((self._micro_status & 0b1000) >> 3), "{}".format((self._micro_status & 0b0100) >> 2), "{}".format((self._micro_status & 0b0010) >> 1), "{}".format(self._micro_status & 0b0001)],
            ["Macro status register", "{}".format((self._macro_status & 0b1000) >> 3), "{}".format((self._macro_status & 0b0100) >> 2), "{}".format((self._macro_status & 0b0010) >> 1), "{}".format(self._macro_status & 0b0001)],
        ]
        return "------------ Status and Shift Control Unit status ------------\n" + tabulate(table, headers="firstrow", tablefmt="grid") + "\n"
        