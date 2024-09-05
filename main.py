from random import randint

NB_REGISTER = 13  # Default 13 (from R0 to R12)

code = """
main:
    mov r0, #0x56
"""


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


def Sanitize_Register_Input(arg: str) -> str:
    arg = arg.strip()
    arg = arg.upper()
    if len(arg) >= 2:
        if arg[0] == "R" and arg[1:].isdigit():
            r = int(arg[1:])
            if 0 <= r <= NB_REGISTER:
                return "R" + str(r)
    raise SyntaxError(f"Incorrect Register or Format Register: {arg}")


class AqaInterpreter:
    def __init__(self, file: str):
        self.file = file
        self.lines: list = self.Create_Lines()
        self.labels: dict = self.Analize_Label()
        self.register: dict = Initialize_Register()
        self.nb_line = self.file.count("\n")
        self.isHALT = False
        self.CMP: list = []

    def Create_Lines(self) -> list:
        lines = self.file.split("\n")
        for l in range(len(lines)):
            line = lines[l].split("/", 1)
            lines[l] = line[0]
        return lines

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

    def Get_Value(self, arg: str, simple_int:bool = False) -> int:
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
        register_cible = Sanitize_Register_Input(arg[0])
        valeur = self.Get_Value(arg[1])
        self.register[register_cible] = valeur

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
        if len(arg) == 1:
            if arg[0].upper() in self.labels.keys():
                self.register["PC"] = self.labels[arg[0].upper()]
            else:
                raise SyntaxError(f"No label : {arg}")
        else:
            raise SyntaxError(f"Wrong arguments for B instruction : {arg}")

    def BXX_inst(self, instruction: str, arg: list) -> None:
        if not self.CMP:
            raise SyntaxError("No previous comparator (CMP) used for B** instruction")
        if not len(arg) == 1:
            raise SyntaxError(f"Wrong arguments for B** instruction : {arg}")
        if not arg[0].upper() in self.labels.keys():
            raise SyntaxError(f"No label : {arg}")
        first, second = self.CMP
        first = self.register[first]
        destination = arg[0].upper()
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

    def CMP_inst(self, arg: list) -> None:
        if len(arg) == 2:
            first = Sanitize_Register_Input(arg[0])
            second = self.Get_Value(arg[1])
            self.CMP = [first, second]

    def INP_inst(self, arg: list) -> None:
        type = arg[1].strip()
        if len(arg) > 2 or not type.isdigit():
            raise SyntaxError(f"Wrong arguments for INP instruction : {arg}")
        type = int(type)
        destination = Sanitize_Register_Input(arg[0])
        value: int = 0
        if len(arg) == 2:
            match type:
                case 8:
                    self.register[destination] = randint(0, 2**31)
                    return
                case 2 | _:
                    self.register[destination] = self.Get_Value(input("INPUT > "), True)
                    return
            pass  # TODO : Enhanced input

    def OUT_inst(self, arg: list) -> None:
        if len(arg) > 2:
            raise SyntaxError(f"Wrong arguments for OUT instruction : {arg}")
        destination = Sanitize_Register_Input(arg[0])
        if len(arg) == 2:
            match int(arg[1]):
                case 4 | 5:
                    print(self.register[destination])
                case 6:
                    print(hex(self.register[destination]))
                case 7:
                    print(chr(self.register[destination]), end='')
                case 8:
                    print("\0")
        else:
            print(self.register[destination])
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
        line = self.lines[self.register["PC"]]  # Get the line executed
        instruction, arguments = Sanitize_line(line)  # Get the instruction + args
        if not instruction: return
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
                self.CMP_inst(arguments)
                return
            case "HALT":
                self.HALT_inst()
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
                print("Unknown Instruction: ", instruction)
                return

    def Run(self):
        while self.register["PC"] <= self.nb_line and not self.isHALT:
            self.Handle_Line()
            self.register["PC"] += 1
        print("Done!")


o = AqaInterpreter(code)
print(o.labels)
o.Run()
print(o.register)
