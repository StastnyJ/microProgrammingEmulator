STACK_SIZE = 5


class ControlUnit:
    def __init__(self):
        self._stack = []
        self._mic = 0

    def get_mic(self):
        return self._mic

    def run(self, instruction: int, bar: int, ccen: int, cc: int, d: int):
        res = -1
        cond = ccen == 1 and cc == 0
        if instruction == 0b0000: # JZ
            self._stack = []
            res = 0
        if instruction == 0b0001: # CJS
            if cond:
                res = self._mic + 1
            else:
                if len(self._stack) == STACK_SIZE:
                    raise Exception("ControlUnit: stack overflow")
                self._stack.append(self._mic + 1)
                res = bar
        if instruction == 0b0010: # JMAP
            res = d
        if instruction == 0b0011: # CJP
            if cond:
                res = self._mic + 1
            else:
                res = bar
        if instruction == 0b0100: # PUSH
            if len(self._stack) == STACK_SIZE:
                raise Exception("ControlUnit: stack overflow")
            self._stack.append(bar)
            res = self._mic + 1
        if instruction == 0b1010: # CRTN
            if cond:
                res = self._mic + 1
            else:
                if len(self._stack) == 0:
                    raise Exception("ControlUnit: stack underflow")
                res = self._stack.pop()
        if instruction == 0b1011: # CJPP
            if cond:
                res = self._mic + 1
            else:
                if len(self._stack) == 0:
                    raise Exception("ControlUnit: stack underflow")
                self._stack.pop()
                res = bar
        if instruction == 0b1110: # CONT
            res = self._mic + 1

        if res < 0:
            raise Exception("ControlUnit: invalid instruction 0b" + format(instruction, "04b"))
        
        self._mic = res
        return res
    
    def __str__(self):
        return "------------ Control unit status ------------\nStack: " + str(self._stack) + "\n"