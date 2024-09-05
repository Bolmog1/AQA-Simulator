from math import log2

value = [3785359360, 3925868544, 167772160, 436207616, 3388997632, 3120562176, 3785359392, 3785359360, 4009754624,
         4009820160, 4009885696, 3785359360, 3789553664, 3780116480, 3843031040, 3841982464, 3766484992, 3762290688,
         3758096384, 3783262208, 3759144960, 201326592, 0]
instr = ["MOV", "B", "BEQ", "BNE", "BLT", "BGT", "LSR", "LSL", "HALT", "INP", "OUT", "MOV", "MVN", "CMP", "LDR", "STR",
         "ADD", "SUB", "AND", "ORR", "EOR", "MOV", "ILLEGAL"]

dic = "{"
for i in range(len(value)):
    ins = instr[i]
    val = str(value[i])
    #print(i, ins, val)
    dic += f"'{ins}' : {val}, "
#print(dic + "}")

def int_to_8bit_binary(value):
    """
    Convertit un entier en une chaîne binaire de 8 bits.

    Parameters:
    value (int): L'entier à convertir (doit être compris entre 0 et 255).

    Returns:
    str: La représentation binaire sur 8 bits sous forme de chaîne.
    """
    if not (0 <= value <= 255):
        raise ValueError("La valeur doit être comprise entre 0 et 255.")

    # Format binaire sur 8 bits avec remplissage de zéros si nécessaire
    return f"{value:08b}"

def generate_mov(register: int, register2: int | None = None, value: int | None = None):
    return 3785359360 + (register * 4096) + (register2 if register2 else 0) + (value + 33554432 if value else 0)

def generate_b(ligne: int):
    ffw = 0
    if ligne > 0:
        ffw = ligne - 1
    else:
        ffw = 16777216 - (ligne * -1) - 2
        #print(ffw)
    return 3925868544 + ffw

def generate_add(dest:str, source:str, add:str):
    instr = '11100010' if add[0] != "R" else '11100000'
    add = int(add) if add[0] != "R" else int(add[1:])

    V1 = int_to_8bit_binary(int(source) + 128)
    V2 = int_to_8bit_binary(int(dest) * 16)
    V3 = int_to_8bit_binary(add)

    return instr + V1 + V2 + V3

def generate_sub(dest:str, source:str, add:str):
    instr = '11100010' if add[0] != "R" else '11100000'
    add = int(add) if add[0] != "R" else int(add[1:])

    V1 = int_to_8bit_binary(int(source) + 64)
    V2 = int_to_8bit_binary(int(dest) * 16)
    V3 = int_to_8bit_binary(add)

    return instr + V1 + V2 + V3

print(generate_add("12", "12", "145"))
print(int("11100010100011001100000010010001", 2))

print(generate_sub("12", "0", "2"))
print(int("11100010010000001100000000000010", 2))

#print(generate_mov(2, value=32))
print(generate_b(1))
#print(generate_mov(12, value=64))

def hack_mov(inst: int):
    argument = inst - 3785359360
    if argument >= 33554432:
        argument -= 33554432
    print(argument % 4096)
    print(argument // 4096)

hack_mov(generate_mov(12, 12))
hack_mov(generate_mov(2, value=32))


#exit(0)
official = {'MOV': 3785359360, 'B': 3925868544, 'BEQ': 167772160, 'BNE': 436207616, 'BLT': 3388997632,
            'BGT': 3120562176, 'LSR': 3785359392, 'LSL': 3785359360, 'HALT': 4009754624, 'INP': 4009820160,
            'OUT': 4009885696, 'MOV': 3785359360, 'MVN': 3789553664, 'CMP': 3780116480, 'LDR': 3843031040,
            'STR': 3841982464, 'ADD': 3766484992, 'SUB': 3762290688, 'AND': 3758096384, 'ORR': 3783262208,
            'EOR': 3759144960, 'MOV': 201326592, 'ILLEGAL': 0}

all_value = list(official.values())

all_value = sorted(all_value)

final = {}

last_one = 0
for i in all_value:
    inst = ""
    for j in official.keys():
        if official[j] == i:
            inst = j
            break
    if i:
        final[i] = inst
        #print(inst, i, i - last_one, log2(i - last_one))
    last_one = i


#print(final)
sort = sorted(official.values())
#print(sort)

def isMOV(i: int) -> bool:
    return 3925868544 <= i < 4009754624
