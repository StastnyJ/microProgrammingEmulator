from tabulate import tabulate

class MicroInstruction:
    def __init__(self, instruction:int):
        if instruction < 0 or instruction >= (1 << 75):
            raise Exception("MIInstruction: instruction out of range")
        self._raw_instruction = instruction

    @property
    def mwe(self):
        return self._raw_instruction & 0b1
    @property
    def ir(self):
        return (self._raw_instruction >> 1) & 0b1
    @property
    def ic(self):
        return (self._raw_instruction >> 2) & 0b1111
    @property
    def bar(self):
        return (self._raw_instruction >> 6) & 0b1111_1111_1111
    @property
    def controller_instruction(self):
        return (self._raw_instruction >> 18) & 0b1111
    @property
    def ccen(self):
        return (self._raw_instruction >> 22) & 0b1
    @property
    def srM(self):
        return (self._raw_instruction >> 23) & 0b1
    @property
    def srm(self):
        return (self._raw_instruction >> 24) & 0b1
    @property
    def sscu_instruction(self):
        return (self._raw_instruction >> 25) & 0b1111_1111_1111
    @property
    def y_mux(self):
        return (self._raw_instruction >> 37) & 0b11
    @property
    def b_mux(self):
        return (self._raw_instruction >> 39) & 0b1
    @property
    def rb_addr(self):
        return (self._raw_instruction >> 40) & 0b1111
    @property
    def a_mux(self):
        return (self._raw_instruction >> 44) & 0b1
    @property
    def ra_addr(self):
        return (self._raw_instruction >> 45) & 0b1111
    @property
    def alu_instruction(self):
        return (self._raw_instruction >> 49) & 0b111_111_111
    @property
    def constant(self):
        return (self._raw_instruction >> 58) & 0b1111_1111_1111_1111
    @property
    def k_mux(self):
        return (self._raw_instruction >> 74) & 0b1
    
    def __str__(self):
        table = [
            ["MWE", "IR", "IC", "BAR", "Controller", "CCEN", "SRM", "SRM", "SSCU", "Y_MUX", "B_MUX", "RB_ADDR", "A_MUX", "RA_ADDR", "ALU", "CONSTANT", "K_MUX"],
            [format(self.mwe, "01b"), format(self.ir, "01b"), format(self.ic, "04b"), format(self.bar, "12b"), format(self.controller_instruction, "04b"), format(self.ccen, "01b"), format(self.srM, "01b"), format(self.srm, "01b"), format(self.sscu_instruction, "12b"), format(self.y_mux, "02b"), format(self.b_mux, "01b"), format(self.rb_addr, "04b"), format(self.a_mux, "01b"), format(self.ra_addr, "04b"), format(self.alu_instruction, "12b"), format(self.constant, "16b"), format(self.k_mux, "01b")]
        ]
        return tabulate(table, headers="firstrow", tablefmt="grid")