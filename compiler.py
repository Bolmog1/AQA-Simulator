instructions = ['ADD', 'AND', 'B', 'BEQ', 'BGT', 'BLT', 'BNE', 'CMP', 'EOR', 'HALT', 'INP', 'LDR', 'LSL', 'LSR', 'MOV',
                'MVN', 'ORR', 'OUT', 'STR', 'SUB', 'SYS']
instructions_bits = {'ADD': 0b00000, 'AND': 0b00001, 'B': 0b00010, 'BEQ': 0b00011, 'BGT': 0b00100, 'BLT': 0b00101,
                     'BNE': 0b00110, 'CMP': 0b00111, 'EOR': 0b01000, 'HALT': 0b01001, 'INP': 0b01010, 'LDR': 0b01011,
                     'LSL': 0b01100, 'LSR': 0b01101, 'MOV': 0b01110, 'MVN': 0b01111, 'ORR': 0b10000, 'OUT': 0b10001,
                     'STR': 0b10010, 'SUB': 0b10011, 'SYS': 0b10100}


def isRegister(arg: str):
    if 2 <= len(arg) <= 3:
        valeur = arg[1:]
        return arg.startswith('R') or arg.startswith('r') and valeur.isdigit() and 0 <= int(valeur) <= 12
    return False


def isNumber(arg: str):
    if not arg.startswith("#"):
        return False
    if arg[1:].isdigit():
        return True
    try:
        int(arg[1:], 16)
        return True
    except ValueError:
        return False


def getRegister(arg: str):
    return int(arg[1:])


def getNumber(arg: str):
    arg = arg[1:]
    if arg.isdigit():
        return int(arg)
    try:
        return int(arg, 16)
    except ValueError:
        raise ValueError(f"'{arg}' is not a valid Number")


def get_binary_instruction(instruction: str, arg: list | None, script_label: dict):
    if instruction not in instructions and not instruction.isdigit():
        raise SyntaxError(f"Unknown Instruction: {instruction}")
    if arg:
        for i in range(len(arg)):
            arg[i] = arg[i].strip()
    if instruction in ['B', 'BEQ', 'BGT', 'BLT', 'BNE']:
        arg[0] = '#' + str(script_label[arg[0]])
    if instruction.isdigit():
        return int(instruction)
    binary_instruction: int = instructions_bits[instruction]
    mask: int = 0
    binary_body: int = 0
    match instruction:
        case 'AND' | 'ADD' | 'SUB' | 'ORR' | 'EOR' | 'LSL' | 'LSR' | 'MOV':  # MASK 2 OR 3
            if len(arg) != 3:  # Check number of arguments
                raise SyntaxError(f"Instruction '{instruction}' takes 3 arguments but {len(arg)} were given: {arg}")
            mask = 3 if isRegister(arg[2]) else 2
            if not (isRegister(arg[0]) and isRegister(arg[1]) and isRegister(arg[2]) or isNumber(arg[2])):
                raise SyntaxError(f"Wrong argument(s) for {instruction}: {arg}")
            if mask == 3:
                binary_body = getRegister(arg[0]) << 20 | getRegister(arg[1]) << 16 | getRegister(arg[2]) << 12
            else:
                binary_body = (getRegister(arg[0]) << 20) | (getRegister(arg[1]) << 16) | getNumber(arg[2])
        case 'B' | 'BEQ' | 'BGT' | 'BLT' | 'BNE' | 'HALT' | 'SYS':
            mask = 4
            if arg and len(arg) != 1:  # Check number of arguments
                raise SyntaxError(f"Instruction '{instruction}' takes 1 arguments but {len(arg)} were given: {arg}")
            if arg:
                if not isNumber(arg[0]):
                    raise SyntaxError(f"Wrong argument for {instruction}: {arg[0]}")
                binary_body = getNumber(arg[0])
        case "CMP" | "INP" | "OUT" | "STR" | "LDR" | "MVN":
            if len(arg) != 2:
                raise SyntaxError(f"Instruction '{instruction}' takes 2 arguments but {len(arg)} were given: {arg}")
            if not (isRegister(arg[0]) and isRegister(arg[1]) or isNumber(arg[1])):
                raise SyntaxError(f"Wrong argument(s) for {instruction}: {arg}")
            mask = 2 if isRegister(arg[1]) else 1
            if mask == 2:
                binary_body = getRegister(arg[0]) << 20 | getRegister(arg[1]) << 16
            else:
                binary_body = getRegister(arg[0]) << 20 | getNumber(arg[1])
        case _:
            binary_body = int(instruction)
    binary = binary_instruction << 27 | mask << 24 | binary_body
    return binary


def handle_file(script_line: list[str]):
    override_memory = []
    label = []
    labels = {}
    script_clean = []
    for n, line in enumerate(script_line):
        if line.strip() == "":  # Handling empty line
            continue
        if '/' in line:  # Handling Comment
            line = line.split("/", 1)[0]
        if ":" in line:  # Handling Semi-colon - override memory
            first, second = line.split(":", 1)
            if len(first) == 4 and first[0] == "L" and first[
                                                       1:4].isdigit() and second.strip().isdigit():  # Handling override memory
                override_memory.append([int(first[1:4]), int(second)])
                continue
            else:  # Handling Label
                label.append(first.strip())
                if not second.strip():
                    script_clean.append("§")
                    continue
                else:
                    script_clean.append("§" + second.strip())
                    continue
        script_clean.append(line.strip())
    script_label = []
    for n, line in enumerate(script_clean):
        if "§" == line:
            labels[label.pop(0).upper()] = len(script_label)
            continue
        if line.startswith("§"):
            labels[label.pop(0).upper()] = len(script_label)
            line = line[1:]
        script_label.append(line.upper())
    script = script_label + [0 for _ in range(200 - len(script_label))]
    return script, labels, override_memory


def AQA_Compiler(script: str):
    compiled_bin: list = [0 for _ in range(200)]
    script_line = script.split('\n')
    memory_case: int = 0
    script_line, script_label, override_memory = handle_file(script_line)
    for n, line in enumerate(script_line):
        if line:
            if " " in str(line):
                instruction, argument = line.split(" ", 1)
                argument: list | None = argument.strip().split(",")
            else:
                instruction, argument = line, None
            compiled_bin[memory_case] = get_binary_instruction(str(instruction), argument, script_label)
            memory_case += 1
    for memory in override_memory:
        compiled_bin[memory[0] - 1] = memory[1]

    return compiled_bin


if __name__ == '__main__':
    code = """
main:
    mov r0, r0, #12
    mov R0, R0, #12 / FDP
    mov R0, R12, #12
    mov R9, R6, R3
loop:add R0, R12, #23
    add R5, R12, R9
    sub R0, R0, #23
L200: 45
    halt
    LSR R2, R10, #123
fdp:B main
L100: 92
"""
    print(AQA_Compiler(code))
