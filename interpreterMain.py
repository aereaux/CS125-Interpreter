import os
import sys

def setcodes(num, registers):
    registers["n"] = False
    registers["z"] = False
    registers["p"] = False
    if num < 0: registers["n"] = True
    if num == 0: registers["z"] = True
    if num > 0: registers["p"] = True

def execute(lines):
    registers = {"r0":0, "r1":0, "r2":0, "r3":0, "r4":0, "r4":0, "r5":0, "r6":0, "r7":0, "pc":0, "n":0, "z":0, "p":0}
    memory = [int(x) for x in lines.pop(0).split(',')]
    registers["pc"] = 0
    while registers["pc"] < len(lines):
        line = lines[registers["pc"]]
        words = line.split(" ")
        if words[0] == "zero_reg":
            registers[words[1]] = 0
            setcodes(0, registers)
        elif words[0] == "add":
            try:
                num = int(words[3])
            except ValueError:
                num = registers[words[3]]
            registers[words[5]] = registers[words[1]] + num
            setcodes(registers[words[5]], registers)
        elif words[0] == "sub":
            try:
                num = int(words[3])
            except ValueError:
                num = registers[words[3]]
            registers[words[5]] = registers[words[1]] - num
            setcodes(registers[words[5]], registers)
        elif words[0] == "load":
            registers[words[1]] = memory[registers[words[3][1:3]] + int(words[3][3:].strip("]"))]
            setcodes(registers[words[1]], registers)
        elif words[0] == "store":
            memory[registers[words[3][1:3]] + int(words[3][4:].strip("]"))] = registers[words[1]]
            setcodes(memory[registers[words[3][1:3]] + int(words[3][4:].strip("]"))], registers)
        elif words[0][:2] == "br":
            for letter in words[0][3:]:
                if registers[letter]: registers["pc"] = registers["pc"] + int(words[1])
        registers["pc"] += 1
    print(memory)

def run(fp):
    program_contents = []
    while True:
        read = os.read(fp, 4096).split("\n")
        if len(read) == 1:
            break
        program_contents += read
    execute(program_contents)
    os.close(fp)

def entry_point(argv):
    try:
        filename = argv[1]
    except IndexError:
        print("You must supply a filename")
        return 1

    run(os.open(filename, os.O_RDONLY, 0o0777))
    return 0

def target(*args):
    return entry_point, None

if __name__ == "__main__":
    entry_point(sys.argv)
