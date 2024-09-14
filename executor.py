from random import randint
from GUI import App
from compiler import AQA_Compiler
from time import sleep

NB_REGISTER = 13  # Default 13 (from R0 to R12)

bits_instruction = {0: 'ADD', 1: 'AND', 2: 'B', 3: 'BEQ', 4: 'BGT', 5: 'BLT', 6: 'BNE', 7: 'CMP', 8: 'EOR', 9: 'HALT', 10: 'INP', 11: 'LDR', 12: 'LSL', 13: 'LSR', 14: 'MOV', 15: 'MVN', 16: 'ORR', 17: 'OUT', 18: 'STR', 19: 'SUB', 20: 'SYS'}


def isIdent(line: str) -> bool:
    if len(line) >= 3:
        return line[0:3] == "   "
    return False


def Initialize_Register() -> dict:
    out = {"PC": 0}
    for i in range(NB_REGISTER):
        out[f"R{i}"] = 0
    return out


def Sanitize_line(line: str) -> tuple[str, list]:
    # Remove Label from the line
    if ":" in line:
        line = line.split(":")[1]
    # Remove the indent
    line = line.strip()
    # Separe Instruction form argument
    line = line.split(" ", 1)
    if len(line) == 1:
        return line[0].upper(), []
    else:
        instruction, arguments = line[0], line[1].split(",")
        return instruction.upper(), arguments


def isHex(value: str) -> bool:
    for char in value:
        if char not in "1234567890ABCDEF":
            return False
    return True


"""def Sanitize_Register_Input(arg: str) -> str:
    arg = arg.strip()
    arg = arg.upper()
    if len(arg) >= 2:
        if arg[0] == "R" and arg[1:].isdigit():
            r = int(arg[1:])
            if 0 <= r <= NB_REGISTER:
                return "R" + str(r)
    raise SyntaxError(f"Incorrect Register or Format Register: {arg}")"""


def Sanitize_Register_Input(arg) -> str:
    if arg is str:
        if not arg.isdigit():
            raise SyntaxError(f"Incorrect Register or Format Register: {arg}")
    return 'R' + str(int(arg))

class AqaInterpreter:
    def __init__(self, GUI: App):
        self.GUI = GUI
        self.register: dict = Initialize_Register()
        self.isHALT = False
        self.CMP: list = []
        self.memory: list = [0 for i in range(200)]

    def load(self, file: str):
        self.register: dict = Initialize_Register()
        self.isHALT = False
        self.CMP: list = []
        self.memory: list = AQA_Compiler(file)

    def unload(self):
        self.register: dict = Initialize_Register()
        self.isHALT = False
        self.CMP: list = []
        self.memory: list = [0 for i in range(200)]


    def Dump_Register(self):
        for register in self.register:
            print(f"{register} : {self.register[register]}")

    def Analize_Label(self) -> dict:
        out = {}
        lines = self.file.split("\n")
        for i, line in enumerate(lines):
            if isIdent(line):
                continue
            else:
                label_line = line.split(":", 1)
                if len(label_line) == 2 and label_line[0]:
                    out[label_line[0].upper()] = i
        return out

    def Get_Value(self, arg: str, simple_int: bool = True) -> int:
        arg = str(arg)
        arg = arg.strip()
        arg = arg.upper()
        if simple_int and arg.isdigit():
            return int(arg)
        if len(arg) >= 2:
            if arg[0] == "R" and arg[1:].isdigit() and not simple_int:
                return self.register[arg]
            elif arg[0] == "#" and arg[1:].isdigit():
                return int(arg[1:])
        if len(arg) >= 4:
            if arg[0:3] == "#0X" and isHex(arg[3:]):
                return int(arg[1:], 16)
        raise SyntaxError(f"Incorrect Value Format : {arg}")

    def MOV_inst(self, arg: list) -> None:
        if not len(arg) == 2:
            raise SyntaxError(f"Wrong arguments for MOV instruction : {arg}")
        register_cible = "R" + str(arg[0])
        self.register[register_cible] = arg[1]

    def HALT_inst(self) -> None:
        self.isHALT = True

    def ADD_inst(self, arg: list) -> None:
        if len(arg) == 3:
            register_to = Sanitize_Register_Input(arg[0])
            register_from = Sanitize_Register_Input(arg[1])
            value = self.Get_Value(arg[2])
            self.register[register_to] = value + self.register[register_from]
        else:
            raise SyntaxError(f"Wrong arguments for ADD instruction : {arg}")

    def SUB_inst(self, arg: list) -> None:
        if len(arg) == 3:
            register_to = Sanitize_Register_Input(arg[0])
            register_from = Sanitize_Register_Input(arg[1])
            value = self.Get_Value(arg[2])
            self.register[register_to] = self.register[register_from] - value
        else:
            raise SyntaxError(f"Wrong arguments for SUB instruction : {arg}")

    def B_inst(self, arg: list) -> None:
        self.register['PC'] = arg[0] - 1

    def BXX_inst(self, instruction: str, arg: list) -> None:
        if not self.CMP:
            raise SyntaxError("No previous comparator (CMP) used for B** instruction")
        if not len(arg) == 1:
            raise SyntaxError(f"Wrong arguments for B** instruction : {arg}")
        first, second, register = self.CMP
        first = self.register[first]
        if register:
            second = self.register["R" + str(second)]
        destination = arg[0]
        match instruction:
            case "BEQ":
                if first == second:
                    self.B_inst([destination])
                return
            case "BNE":
                if first != second:
                    self.B_inst([destination])
                return
            case "BGT":
                if first > second:
                    self.B_inst([destination])
                return
            case "BLT":
                if first < second:
                    self.B_inst([destination])
                return

    def CMP_inst(self, arg: list, register: bool) -> None:
        if len(arg) == 2:
            first = Sanitize_Register_Input(arg[0])
            second = self.Get_Value(arg[1]) if not register else Sanitize_Register_Input(arg[1])
            self.CMP = [first, second, register]
        else:
            raise SyntaxError(f"Wrong arguments for CMP instruction : {arg}")

    def INP_inst(self, arg: list) -> None:
        if len(arg) > 2:
            raise SyntaxError(f"Wrong arguments for INP instruction : {arg}")
        type = arg[1]
        destination = Sanitize_Register_Input(arg[0])
        value: int = 0
        if len(arg) == 2:
            match type:
                case 8:
                    self.register[destination] = randint(0, 2**31)
                    return
                case 4:
                    c = self.GUI.get_last_key_press()
                    if c:
                        self.register[destination] = ord(c)
                        print(c)
                    return
                case 5:
                    self.GUI.reset_last_key_press()
                    return
                case 2:
                    self.GUI.WaitForEntry()
                    self.GUI.print_debug("Waiting for Entry")
                    while not self.GUI.entry:
                        sleep(0.1)
                    self.register[destination] = self.Get_Value(self.GUI.entry, True)
                    self.GUI.entry = None
                    return
            pass  # TODO : Enhanced input

    def OUT_inst(self, arg: list) -> None:
        if len(arg) > 2:
            raise SyntaxError(f"Wrong arguments for OUT instruction : {arg}")
        destination = Sanitize_Register_Input(arg[0])
        if len(arg) == 2:
            match int(arg[1]):
                case 4 | 5:
                    self.GUI.output(self.register[destination])
                case 6:
                    self.GUI.output(hex(self.register[destination]))
                case 7:
                    self.GUI.output(chr(self.register[destination]))
                case 8:
                    self.GUI.output("\n")
        else:
            self.GUI.output(self.register[destination])
            pass  # TODO : Enhanced Output

    def BIN_inst(self, instruction: str, arg: list) -> None:
        if len(arg) != 3:
            raise SyntaxError(f"Wrong arguments for Binary (AND, ORR, EOR, LSL, LSR) instructions : {arg}")
        destination = Sanitize_Register_Input(arg[0])
        first = Sanitize_Register_Input(arg[1])
        second = self.Get_Value(arg[2])
        match instruction:
            case "AND":
                self.register[destination] = self.register[first] & second
                return
            case "ORR":
                self.register[destination] = self.register[first] | second
                return
            case "EOR":
                self.register[destination] = self.register[first] ^ second
                return
            case "LSL":
                self.register[destination] = self.register[first] << second
                return
            case "LSR":
                self.register[destination] = self.register[first] >> second
                return

    def MVN_inst(self, arg: list) -> None:
        if len(arg) != 2:
            raise SyntaxError(f"Wrong arguments for MVN instruction : {arg}")
        destination = Sanitize_Register_Input(arg[0])
        value = self.Get_Value(arg[1])
        self.register[destination] = ~value

    def Handle_Line(self) -> None:
        #line = self.lines[self.register["PC"]]  # Get the line executed
        #instruction, arguments = Sanitize_line(line)  # Get the instruction + args

        binary = self.memory[self.register["PC"]]
        instruction = bits_instruction[(binary >> 27) & 0b11111]
        mask = (binary >> 24) & 0b111
        arguments = []
        match mask:
            case 1:
                arguments.append((binary >> 20) & 0b1111)
                arguments.append(binary & 0b11111111_11111111_1111)
            case 2:
                arguments.append((binary >> 20) & 0b1111)
                arguments.append((binary >> 16) & 0b1111)
                arguments.append(binary & 0b11111111_11111111)
                if not arguments[2]:
                    arguments.pop(2)
            case 3:
                arguments.append((binary >> 20) & 0b1111)
                arguments.append((binary >> 16) & 0b1111)
                arguments.append((binary >> 12) & 0b1111)
            case 4:
                arguments.append(binary & 0b11111111_11111111_11111111)
        #print(instruction, mask,arguments)

        match instruction:
            case "ADD":
                self.ADD_inst(arguments)
                return
            case "B":
                self.B_inst(arguments)
                return
            case "BEQ" | "BNE" | "BGT" | "BLT":
                self.BXX_inst(instruction, arguments)
                return
            case "AND" | "ORR" | "EOR" | "LSL" | "LSR":
                self.BIN_inst(instruction, arguments)
                return
            case "CMP":
                self.CMP_inst(arguments, mask == 2)
                return
            case "HALT":
                self.HALT_inst()
                self.GUI.print_debug("script halted")
                return
            case "INP":
                self.INP_inst(arguments)
                return
            case "MOV":
                self.MOV_inst(arguments)
                return
            case "MVN":
                self.MVN_inst(arguments)
                return
            case "OUT":
                self.OUT_inst(arguments)
                return
            case "SUB":
                self.SUB_inst(arguments)
                return
            case _:
                self.GUI.print_debug(f"Unknown Instruction: {instruction}")
                self.GUI.Running(False)
                return

    def Step(self):
        if not self.isHALT and self.GUI.isRunning:
            self.Handle_Line()
            self.register["PC"] += 1
            self.GUI.refresh_register()
            self.GUI.refresh_memory()

    def Run(self):
        sleep_time = self.GUI.get_sleep_time() * 0.1
        self.GUI.Running(True)
        self.GUI.checkThreadAlive()
        while not self.isHALT and self.GUI.isRunning:
            self.Handle_Line()
            self.register["PC"] += 1
            self.GUI.refresh_register()
            self.GUI.refresh_memory()
            sleep(sleep_time)
        self.GUI.Running(False)
