
"""
def to8bit(value):
    if not (0 <= value <= 255):
        raise ValueError("La valeur doit être comprise entre 0 et 255.")

    # Format binaire sur 8 bits avec remplissage de zéros si nécessaire
    return f"{value:08b}"


def generate_mov(register: int, register2: int | None = None, value: int | None = None):
    return 3785359360 + (register * 4096) + (register2 if register2 else 0) + (value + 33554432 if value else 0)


def generate_b(ligne: int):
    if ligne > 0:
        ffw = ligne - 1
    else:
        ffw = 16777216 - (ligne * -1) - 2
    return 3925868544 + ffw


def generate_add(dest: str, source: str, add: str):
    instr = '11100010' if add[0] != "R" else '11100000'
    add = int(add) if add[0] != "R" else int(add[1:])

    V1 = to8bit(int(source) + 128)
    V2 = to8bit(int(dest) * 16)
    V3 = to8bit(add)

    return instr + V1 + V2 + V3


def generate_sub(dest:str, source:str, add:str):
    instr = '11100010' if add[0] != "R" else '11100000'
    add = int(add) if add[0] != "R" else int(add[1:])

    V1 = to8bit(int(source) + 64)
    V2 = to8bit(int(dest) * 16)
    V3 = to8bit(add)

    return instr + V1 + V2 + V3"""


def generate_binary(instruction, arguments):
    # Vérifier que l'instruction existe
    if instruction not in INmame:
        raise ValueError("Instruction non reconnue.")

    # Trouver l'index de l'instruction
    index = INmame.index(instruction)

    # Récupérer le masque et la valeur pour l'instruction
    mask = IMask[index]
    value = IValue[index]
    decode_type = IDecode[index]

    # Appliquer les arguments selon le type de décodage
    binary_instruction = apply_decoding(value, mask, decode_type, arguments)

    return binary_instruction


def apply_decoding(value, mask, decode_type, arguments):
    # Appliquer les masques et les valeurs aux arguments en fonction du type de décodage
    if decode_type == 0:  # Aucun argument
        return value
    elif decode_type == 1:  # Un registre
        reg = arguments[0] << 12
        return (value & mask) | reg
    elif decode_type == 2:  # Deux registres
        reg1 = arguments[0] << 16
        reg2 = arguments[1] << 12
        return (value & mask) | reg1 | reg2
    elif decode_type == 3:  # Un registre et une valeur immédiate
        reg = arguments[0] << 12
        imm = arguments[1] & 0xFFF
        return (value & mask) | reg | imm
    elif decode_type == 4:  # Comparaison entre deux registres
        reg1 = arguments[0] << 16
        reg2 = arguments[1] << 12
        return (value & mask) | reg1 | reg2
    elif decode_type == 5:  # Un registre et un shift
        reg = arguments[0] << 12
        shift = arguments[1] & 0xFF
        return (value & mask) | reg | shift
    elif decode_type == 6:  # Une adresse de branchement
        addr = arguments[0] & 0xFFFFFF
        return (value & mask) | addr
    elif decode_type == 7:  # Opérations logiques avec deux registres
        reg1 = arguments[0] << 16
        reg2 = arguments[1] << 12
        return (value & mask) | reg1 | reg2
    elif decode_type == 8:  # Instruction "MOV" avec registre et valeur immédiate
        reg = arguments[0] << 12
        imm = arguments[1] & 0xFFF
        return (value & mask) | reg | imm
    else:
        raise ValueError("Type de décodage non supporté.")


# Exemple d'utilisation
IMask = [4294905840, 4278190080, 4278190080, 4278190080, 4278190080, 4278190080, 4294901856, 4294901856, 4294967295,
         4294905840, 4294905840, 4261347328, 4261347328, 4260425728, 4285530112, 4285530112, 4260364288, 4260364288,
         4260364288, 4260364288, 4260364288, 201326592, 0]
IValue = [3785359360, 3925868544, 167772160, 436207616, 3388997632, 3120562176, 3785359392, 3785359360, 4009754624,
          4009820160, 4009885696, 3785359360, 3789553664, 3780116480, 3843031040, 3841982464, 3766484992, 3762290688,
          3758096384, 3783262208, 3759144960, 201326592, 0]
INmame = ["MOV", "B", "BEQ", "BNE", "BLT", "BGT", "LSR", "LSL", "HALT", "INP", "OUT", "MOV", "MVN", "CMP", "LDR", "STR",
          "ADD", "SUB", "AND", "ORR", "EOR", "MOV", "ILLEGAL"]
IDecode = [3, 6, 6, 6, 6, 6, 5, 5, 0, 1, 1, 3, 3, 4, 2, 2, 7, 7, 7, 7, 7, 8, 0]

# Exemples de compilation
print(generate_binary("ADD", [0, 1, 25433]))  # Exemple pour MOV avec registre 1 et valeur immédiate 5
print((generate_binary("B", [123456])))  # Exemple pour branchement à l'adresse 123456
