import sys
x = []  # Registers
x.append(0)
for i in range(1, 32):
    x.append(0)
    if (i == 3):
        x[i] = int("0x10000000", 16)  # gp
    elif (i == 2):
        x[i] = int("0x7FFFFFF0", 16)  # sp

memory = {}


def WriteBack(rd, content):
    if rd != 0:
        x[rd] = content
        print("WRITEBACK: write", content, " to x[", rd, "]")
    print("\n")


def printregister():
    for i in range(0, 32):
        print("x[", i, "]=", x[i])


def findnegative(string):  # Pratima_Singh 2018CEB1021 function to get the sign extended value of a negative imm field
    length = len(string)
    neg = -1  # intialize neg with -1
    sum = 0
    i = 0  # counter
    while i <= length - 1:
        if (string[i] == '0'):
            sum += -pow(2, i)
        i = i + 1
    neg = neg + sum
    return neg


def execute(string, rs1, rs2, rd, imm, PC):
    # string is referring to the the operation we are going to do

    if (string == "add" or string == "and" or string == "or" or string == "sll"):

        print("Decode-> operation :", string, ",source register 1:", int(rs1, 2), ",source register 2:", int(rs2, 2),
              ",destination register : ", int(rd, 2), end=" \n", sep=" ")
        executeMuskan(string, rs1, rs2, rd)
    elif (string == "xor" or string == "mul" or string == "div" or string == "rem"):

        print("Decode-> operation:", string, ",source register 1:", int(rs1, 2), ",source register 2:", int(rs2, 2),
              ",destination register : ", int(rd, 2), end=" \n", sep=" ")
        executeManan(string, rs1, rs2, rd)


    elif (string == "slt" or string == "srl" or string == "sub" or string == "sra"):

        print("Decode-> operation :", string, ",source register 1:", int(rs1, 2), ",source register 2:", int(rs2, 2),
              ",destination register : ", int(rd, 2), end=" \n", sep=" ")
        executeRajasekhar(string, rs1, rs2, rd)

    elif (string == "addi" or string == "andi" or string == "ori"):
        temp = imm
        if (temp[0:1] == '1'):
            check = str(temp)
            check = check[::-1]
            temp = findnegative(check)
        else:
            temp = int(temp, 2)
        print("Decode -> operation :", string, ",source register 1:", int(rs1, 2), ",Immediate:", temp,
              ",destination register : ", int(rd, 2), end=" \n", sep=" ")
        executePraveen(string, rd, rs1, imm)


    elif (string == "lui" or string == "auipc"):

        temp = imm
        if (temp[0:1] == '1'):
            check = str(temp)
            check = check[::-1]
            temp = findnegative(check)
        else:
            temp = int(temp, 2)
        print("Decode -> operation :", string, ",Immediate:", temp,
              ",destination register : ", int(rd, 2), end=" \n", sep=" ")
        executePratima(string, rd, imm, PC)

    elif (string == "bge" or string == "blt"):

        temp = imm
        if (temp[0:1] == '1'):
            check = str(temp)
            check = check[::-1]
            temp = findnegative(check)
        else:
            temp = int(temp, 2)
        print("Decode-> operation :", string, ",source register 1:", int(rs1, 2), ",Source register 2:", int(rs2, 2),
              ",Immediate: ", temp, end=" \n", sep=" ")
        PC = executeManan1(string, rs1, rs2, imm, PC)

    elif (string == "beq" or string == "bne"):

        temp = imm
        if (temp[0:1] == '1'):
            check = str(temp)
            check = check[::-1]
            temp = findnegative(check)
        else:
            temp = int(temp, 2)
        print("Decode-> operation :", string, ",source register 1:", int(rs1, 2), ",Source register 2:", int(rs2, 2),
              ",Immediate: ", temp, end=" \n", sep=" ")
        PC = executeRajasekhar1(string, rs1, rs2, imm, PC)


    elif (string == "jal"):

        temp = imm
        if (temp[0:1] == '1'):
            check = str(temp)
            check = check[::-1]
            temp = findnegative(check)
        else:
            temp = int(temp, 2)
        print("Decode:-> operation: ", string, ",destinaton register:", int(rd, 2), ",Immediate: ", temp, end=" \n",
              sep=" ")
        PC = executePraveen1(string, rd, imm, PC)

    elif (string == "jalr"):

        temp = imm
        if (temp[0:1] == '1'):
            check = str(temp)
            check = check[::-1]
            temp = findnegative(check)
        else:
            temp = int(temp, 2)
        print("Decode-> operation: ", string, ",Source register 1:", int(rs1, 2), ",destinaton register:"
              , int(rd, 2), ",Immediate: ", temp, end=" \n", sep=" ")
        PC = executePraveen2(string, rs1, rd, imm, PC)
    elif (string == "sw" or string == "sh" or string == "sb"):

        temp = imm
        if (temp[0:1] == '1'):
            check = str(temp)
            check = check[::-1]
            temp = findnegative(check)
        else:
            temp = int(temp, 2)
        print("Decode-> operation: ", string, ",source register 1:", int(rs1, 2), ",Source register 2:", int(rs2, 2),
              ",Immediate: ", temp, end=" \n", sep=" ")
        executeStore(string, rs1, rs2, imm)
    elif (string == "lw" or string == "lh" or string == "lb"):

        temp = imm
        if (temp[0:1] == '1'):
            check = str(temp)
            check = check[::-1]
            temp = findnegative(check)
        else:
            temp = int(temp, 2)
        print("Decode-> operation: ", string, ",Source register 1:", int(rs1, 2),
              ",destinaton register:", int(rd, 2), ",Immediate: ", temp, end=" \n", sep=" ")
        executeRead(string, rs1, rd, imm)

    return PC


# executing functions
def executeMuskan(string, rs1, rs2, rd):
    if (string == "add"):  # executing add
        rs1 = int(rs1, 2)
        rs2 = int(rs2, 2)
        rd = int(rd, 2)
        s = x[rs1] + x[rs2]
        print("Execute :", string, x[rs1], "and", x[rs2])
        print("MEMORY:No memory  operation")
        if (s >= -(pow(2, 31)) and s <= (pow(2, 31)) - 1):  # checking for underflow or overflow
            WriteBack(rd, s)


    elif (string == "and"):  # executing and
        rs1 = int(rs1, 2)
        rs2 = int(rs2, 2)
        rd = int(rd, 2)
        s = x[rs1] & x[rs2]
        print("Execute :", string, x[rs1], "and", x[rs2])
        print("MEMORY:No memory  operation")
        if (s >= -(pow(2, 31)) and s <= (pow(2, 31)) - 1):  # checking for underflow or overflow
            WriteBack(rd, s)


    elif (string == "or"):  # executing or
        rs1 = int(rs1, 2)
        rs2 = int(rs2, 2)
        rd = int(rd, 2)
        s = x[rs1] | x[rs2]
        print("Execute :", string, x[rs1], "and", x[rs2])
        print("MEMORY:No memory  operation")
        if (s >= -(pow(2, 31)) and s <= (pow(2, 31)) - 1):  # checking for underflow or overflow
            WriteBack(rd, s)


    elif (string == "sll"):  # executing sll
        rs1 = int(rs1, 2)
        rs2 = int(rs2, 2)
        rd = int(rd, 2)
        s = x[rs1] << x[rs2]
        print("Execute :", string, x[rs1], "and", x[rs2])
        print("MEMORY:No memory  operation")
        if (s >= -(pow(2, 31)) and s <= (pow(2, 31)) - 1):  # checking for underflow or overflow
            WriteBack(rd, s)


def executeManan(string, rs1, rs2, rd):
    rd = int(rd, 2)
    rs1 = int(rs1, 2)
    rs2 = int(rs2, 2)
    if string == 'xor':
        output = x[rs1] ^ x[rs2]
        if -(pow(2, 31)) <= output <= (pow(2, 31)) - 1:  # Underflow and overflow
            print("Execute :", string, x[rs1], "and", x[rs2])
            print("MEMORY:No memory  operation")
            WriteBack(rd, output)
    elif string == 'mul':
        output = x[rs1] * x[rs2]
        if -(pow(2, 31)) <= output <= (pow(2, 31)) - 1:  # Underflow and overflow
            print("Execute :", string, x[rs1], "and", x[rs2])
            print("MEMORY:No memory  operation")
            WriteBack(rd, output)
    elif string == "div":
        output = x[rs1] // x[rs2]
        if -(pow(2, 31)) <= output <= (pow(2, 31)) - 1:  # Underflow and overflow
            print("Execute :", string, x[rs1], "and", x[rs2])
            print("MEMORY:No memory  operation")
            WriteBack(rd, output)
    elif string == "rem":
        output = x[rs1] % x[rs2]
        if -(pow(2, 31)) <= output <= (pow(2, 31)) - 1:  # Underflow and overflow
            print("Execute :", string, x[rs1], "and", x[rs2])
            print("MEMORY:No memory  operation")
            WriteBack(rd, output)


def executePratima(string, rd, imm, PC):
    if (imm[0:1] == '1'):
        check = str(imm)
        check = check[::-1]
        imm = findnegative(check)
    else:
        imm = int(imm, 2)
    rd = int(rd, 2)
    
    if string == "lui":  # executing lui
        if (imm <= pow(2, 19) - 1 and imm >= -pow(2, 19)):  # checking range of imm
            temp = 0 | imm
            temp = temp << 12
            if (temp >= -(pow(2, 31)) and temp <= (pow(2, 31)) - 1):  # checking for underflow or overflow
                print("Execute :", string, x[rd], "and", imm)
                print("MEMORY:No memory  operation")
                WriteBack(rd, temp)
    elif string == "auipc":  # executing auipc
        if (imm <= pow(2, 19) - 1 and imm >= -pow(2, 19)):  # checking range of imm
            temp = 0 | imm
            temp = temp << 12
            temp = temp + PC
            if (temp >= -(pow(2, 31)) and temp <= (pow(2, 31)) - 1):  # checking for underflow or overflow
                print("Execute :", string, x[rd], "and", imm)
                print("MEMORY:No memory  operation")
                WriteBack(rd, temp)
    else:
        print("Error")


def executeRajasekhar(string, rs1, rs2, rd):
    # slt,sra,srl,sub
    rd = int(rd, 2)
    rs1 = int(rs1, 2)
    rs2 = int(rs2, 2)

    if (string == "slt"):
        if (x[rs1] < x[rs2]):
            jot = 1
            print("Execute :", string, x[rs1], "and", x[rs2])
            print("MEMORY:No memory  operation")
            WriteBack(rd, jot)
        else:
            jot = 0
            print("Execute :", string, x[rs1], "and", x[rs2])
            print("MEMORY:No memory  operation")
            WriteBack(rd, jot)
    elif (string == "sra"):
        result = x[rs1] >> x[rs2]
        lowerlimit = -1 * (1 << 31)
        upperlimit = (1 << 31) - 1
        if (lowerlimit <= result and result <= upperlimit):  # checking underflow and overflow condition
            print("Execute :", string, x[rs1], "and", x[rs2])
            print("MEMORY:No memory  operation")
            WriteBack(rd, result)
    elif (string == "srl"):
        result = x[rs1] >> x[rs2]
        lowerlimit = -1 * (1 << 31)
        upperlimit = (1 << 31) - 1
        if (lowerlimit <= result and result <= upperlimit):
            print("Execute :", string, x[rs1], "and", x[rs2])
            print("MEMORY:No memory  operation")
            WriteBack(rd, result)
    elif (string == "sub"):
        result = x[rs1] - x[rs2]
        lowerlimit = -1 * (1 << 31)
        upperlimit = (1 << 31) - 1
        if (lowerlimit <= result and result <= upperlimit):
            print("Execute :", string, x[rs1], "and", x[rs2])
            print("MEMORY:No memory  operation")
            WriteBack(rd, result)


def executePraveen(string, rd, rs1, imm):  # PRAVEEN KUMAR 2019CSb1108      #addi,andi,ori
    rs1 = int(rs1, 2)
    rd = int(rd, 2)
    # print(imm)
    if (imm[0:1] == '1'):
        check = str(imm)
        check = check[::-1]
        imm = findnegative(check)
    else:
        imm = int(imm, 2)

    if (string == "addi"):
        if (imm <= pow(2, 11) - 1 and imm >= -pow(2, 11)):  # checking range of imm
            s = x[rs1] + imm
            if (s >= -(pow(2, 31)) and s <= (pow(2, 31)) - 1):  # checking for underflow or overflow
                print("Execute :", string, x[rs1], "and", imm)
                print("MEMORY:No memory  operation")
                WriteBack(rd, s)

    elif (string == "andi"):
        if (imm <= pow(2, 11) - 1 and imm >= -pow(2, 11)):  # checking range of imm
            s = x[rs1] & imm
            if (s >= -(pow(2, 31)) and s <= (pow(2, 31)) - 1):  # checking for underflow or overflow
                print("Execute :", string, x[rs1], "and", imm)
                print("MEMORY:No memory  operation")
                WriteBack(rd, s)

    elif (string == "ori"):
        
        if (imm <= pow(2, 11) - 1 and imm >= -pow(2, 11)):  # checking range of imm
            s = x[rs1] | imm
            if (s >= -(pow(2, 31)) and s <= (pow(2, 31)) - 1):  # checking for underflow or overflow
                print("Execute :", string, x[rs1], "and", imm)
                print("MEMORY:No memory  operation")
                WriteBack(rd, s)


def executeManan1(string, rs1, rs2, imm, pc):
    rs1 = int(rs1, 2)
    rs2 = int(rs2, 2)
    if (imm[0:1] == '1'):
        check = str(imm)
        check = check[::-1]
        imm = findnegative(check)
    else:
        imm = int(imm, 2)
    imm = imm << 1
    if string == "bge":
        if x[rs1] >= x[rs2]:
            print("Execute :", string, x[rs1], "and", x[rs2])
            print("MEMORY:No memory  operation")
            print("WRITEBACK: no writeback \n")
            pc = pc + imm
        else:
            print("Execute :No execute")
            print("MEMORY:No memory  operation")
            print("WRITEBACK: no writeback \n")
            pc = pc + 4
    elif string == 'blt':
        if x[rs1] < x[rs2]:
            print("Execute :", string, x[rs1], "and", x[rs2])
            print("MEMORY:No memory  operation")
            print("WRITEBACK: no writeback \n")
            pc = pc + imm
        else:
            print("Execute :No execute")
            print("MEMORY:No memory  operation")
            print("WRITEBACK: no writeback \n")
            pc = pc + 4

    return pc


def executeRajasekhar1(string, rs1, rs2, imm, pc):
    rs1 = int(rs1, 2)
    rs2 = int(rs2, 2)
    if (imm[0:1] == '1'):
        check = str(imm)
        check = check[::-1]
        imm = findnegative(check)
    else:
        imm = int(imm, 2)
    imm = imm << 1
    if (string == 'beq'):
        if (x[rs1] == x[rs2]):
            print("Execute :", string, x[rs1], "and", x[rs2])
            print("MEMORY:No memory  operation")
            print("WRITEBACK: no writeback \n")
            pc = pc + imm
        else:
            print("Execute :No execute")
            print("MEMORY:No memory  operation")
            print("WRITEBACK: no writeback \n")
            pc = pc + 4
    elif (string == 'bne'):
        if (x[rs1] != x[rs2]):
            print("Execute :", string, x[rs1], "and", x[rs2])
            print("MEMORY:No memory  operation")
            print("WRITEBACK: no writeback \n")
            pc = pc + imm
        else:
            print("Execute :No execute")
            print("MEMORY:No memory  operation")
            print("WRITEBACK: no writeback \n")
            pc = pc + 4

    return pc


def executePraveen1(string, rd, imm, pc):  # Praveen Kumar 2019CSB1108    jal  function
    rd = int(rd, 2)

    if (imm[0:1] == '1'):
        check = str(imm)

        check = check[::-1]
        imm = findnegative(check)

    else:
        imm = int(imm, 2)

    imm = imm << 1

    if (string == 'jal'):
        temp = pc
        pc = pc + imm

        jot = temp + 4
        print("Execute :", string, x[rd], "and", imm)
        print("MEMORY:No memory  operation")
        if rd != 0:
            WriteBack(rd, jot)
        else:
            print("WRITEBACK: no writeback \n")
    return pc


def executePraveen2(string, rs1, rd, imm, pc):  # Praveen Kumar 2019CSB1108    jalr function
    rs1 = int(rs1, 2)
    rd = int(rd, 2)
    if (imm[0:1] == '1'):
        check = str(imm)
        check = check[::-1]
        imm = findnegative(check)
    else:
        imm = int(imm, 2)
    if (string == 'jalr'):
        temp = pc
        pc = x[rs1] + imm
        print("Execute :", string, x[rs1], "and", imm)
        print("MEMORY:No memory  operation")
        if (rd != 0):
            jot = temp + 4
            WriteBack(rd, jot)
        else:
            print("WRITEBACK: no writeback \n")

    return pc


def executeStore(string, rs1, rs2, imm):
    rs1 = int(rs1, 2)
    rs2 = int(rs2, 2)
    if (imm[0:1] == '1'):
        check = str(imm)
        check = check[::-1]
        imm = findnegative(check)
    else:
        imm = int(imm, 2)
    dataa = hex(x[rs2])[2:].zfill(8)
    if (string == "sw"):
        if (x[rs1] + imm >= 268435456):  # data segment starts with address 268435456 or 0x10000000
            address = x[rs1] + imm  # calculating address
            print("Execute : calculating effective address by adding", x[rs1], "and", imm)
            MemoryStore("sw", dataa, address)
    elif (string == "sh"):
        if (x[rs1] + imm >= 268435456):
            address = x[rs1] + imm
            print("Execute : calculating effective address by adding", x[rs1], "and", imm)
            MemoryStore("sh", dataa, address)
    elif (string == "sb"):
        if (x[rs1] + imm >= 268435456):
            address = x[rs1] + imm
            print("Execute : calculating effective address by adding", x[rs1], "and", imm)
            MemoryStore("sb", dataa, address)


def MemoryStore(string, dataa, address):
    print("Memory: accessed memory location at", address)
    if (string == "sw"):
        memory[address] = dataa[6:]
        memory[address + 1] = dataa[4:6]
        memory[address + 2] = dataa[2:4]
        memory[address + 3] = dataa[0:2]
    elif (string == "sh"):
        memory[address] = dataa[6:]
        memory[address + 1] = dataa[4:6]
    elif (string == "sb"):
        memory[address] = dataa[6:]
    print("WRITEBACK: no writeback \n")


def executeRead(string, rs1, rd, imm):
    rs1 = int(rs1, 2)
    rd = int(rd, 2)
    
    check = imm
    if (imm[0:1] == '1'):  # imm is a negative number, since sign bit is 1
        check = str(check)
        check = check[::-1]  # reversing the string
        
        t1 = findnegative(check)
        
        imm = t1
    else:
        imm = int(imm, 2)  # sign bit is 0

    temp1 = x[rs1] + imm  # calculating address
    print("Execute : calculating effective address by adding", x[rs1], "and", imm)
    
    Memoryread(string, temp1, rd, imm)


def Memoryread(string, temp1, rd, imm):  # Pratima Singh 2018CEB1021
    if (imm <= pow(2, 11) - 1 and imm >= -pow(2, 11)):  # checking range of imm
        if (string == "lw"):
            if (temp1 >= 268435456):  # data segment starts with address 268435456 or 0x10000000
                if temp1 in memory:
                    print("Memory: accessed memory location at", temp1)
                    temp2 = memory[temp1 + 3] + memory[temp1 + 2] + memory[temp1 + 1] + memory[temp1]
                    
                    jot = int(temp2, 16)
                    WriteBack(rd, jot)
                else:
                    memory[temp1] = "00"
                    memory[temp1 + 1] = "00"
                    memory[temp1 + 2] = "00"
                    memory[temp1 + 3] = "00"
                    Memoryread(string, temp1, rd, imm)
            else:
                print("\n Invalid offset")
                print(temp1)
        elif string == "lh":
            if temp1 >= 268435456:  # data segment starts with address 268435456 or 0x10000000
                if temp1 in memory:
                    print("Memory: accessed memory location at", temp1)
                    temp2 = memory[temp1 + 3] + memory[temp1 + 2]
                    jot = int(temp2, 16)
                    WriteBack(rd, jot)
                else:
                    memory[temp1] = "00"
                    memory[temp1 + 1] = "00"
                    memory[temp1 + 2] = "00"
                    memory[temp1 + 3] = "00"
                    Memoryread(string, temp1, rd, imm)
            else:
                print("\n Invalid offset")
                print(temp1)
        elif string == "lb":
            if temp1 >= 268435456:  # data segment starts with address 268435456 or 0x10000000
                if temp1 in memory:
                    print("Memory: accessed memory location at", temp1)
                    temp2 = memory[temp1 + 3]
                    jot = int(temp2, 16)
                    WriteBack(rd, jot)
                else:
                    memory[temp1] = "00"
                    memory[temp1 + 1] = "00"
                    memory[temp1 + 2] = "00"
                    memory[temp1 + 3] = "00"
                    Memoryread(string, temp1, rd, imm)
            else:
                print("\n Invalid offset")
                print(temp1)
        else:
            print("\nError")


# decoding functions

def decode(binaryno, PC):
    opcode = binaryno[25:32]

    R_oper = ["0110011"]
    I_oper = ["0010011", "0000011", "1100111"]
    S_oper = ["0100011"]
    SB_oper = ["1100011"]
    U_oper = ["0110111", "0010111"]
    UJ_oper = ["1101111"]

    
   
    if opcode in R_oper:
        # decode

        R_Format(binaryno, PC)
        PC += 4
    elif opcode in I_oper:
        # decode

        PC = I_Format(binaryno, PC)


    elif opcode in S_oper:
        S_Format(binaryno, PC)
        PC += 4

        # decode

    elif opcode in SB_oper:
        # decode

        PC = sb_format(binaryno, PC)

    elif opcode in U_oper:
        # decode

        U_Format(binaryno, PC)
        PC += 4

    elif opcode in UJ_oper:
        # decode

        PC = UJ_Format(binaryno, PC)


    else:
        print("Error")
        PC += 4
    return PC


def R_Format(binaryInstruction, PC):  # MUSKAN GUPTA 2019CSB1100
    # add, and, or, sll, slt, sra, srl, sub, xor, mul, div, rem
    funct7 = binaryInstruction[0:7]
    rs2 = binaryInstruction[7:12]
    rs1 = binaryInstruction[12:17]
    funct3 = binaryInstruction[17:20]
    rd = binaryInstruction[20:25]
    opcode = binaryInstruction[25:32]
    
    if (opcode == "0110011"):
        if (funct7 == "0000000"):
            if (funct3 == "000"):
                # add
                execute("add", rs1, rs2, rd, " ", PC)  # " " is don't care for imm

                
            elif (funct3 == "111"):
                # and
                execute("and", rs1, rs2, rd, " ", PC)
                
            elif (funct3 == "110"):
                # or
                execute("or", rs1, rs2, rd, " ", PC)
                
            elif (funct3 == "001"):
                # sll
                execute("sll", rs1, rs2, rd, " ", PC)

             
            elif (funct3 == "010"):
                # slt
                execute("slt", rs1, rs2, rd, " ", PC)
                
            elif (funct3 == "101"):
                # srl
                execute("srl", rs1, rs2, rd, " ", PC)
                
            elif (funct3 == "100"):
                # xor
                execute("xor", rs1, rs2, rd, " ", PC)
                
            else:
                print("Error")
        elif (funct7 == "0100000"):
            if (funct3 == "000"):
                # sub
                execute("sub", rs1, rs2, rd, " ", PC)
                
            elif (funct3 == "101"):
                # sra
                execute("sra", rs1, rs2, rd, " ", PC)
                
            else:
                print("Error")
        elif (funct7 == "0000001"):
            if (funct3 == "000"):
                # mul
                execute("mul", rs1, rs2, rd, " ", PC)
                
            elif (funct3 == "100"):
                # div
                execute("div", rs1, rs2, rd, " ", PC)
                
            elif (funct3 == "110"):
                # rem
                execute("rem", rs1, rs2, rd, " ", PC)
                
            else:
                print("Error")
        else:
            print("Error")
    else:
        print("Error")
    return


def I_Format(binaryInstruction, PC):  # Pratima_Singh
    # addi, andi, ori, lb, lh, lw, jalr
    imm = binaryInstruction[0:12]
    rs1 = binaryInstruction[12:17]
    funct3 = binaryInstruction[17:20]
    rd = binaryInstruction[20:25]
    opcode = binaryInstruction[25:32]
    # print("opcode: ", opcode, " imm: ", imm, " rs1: ", rs1, " funct3: ", funct3, " rd: ", rd)
    if (opcode == "0000011"):
        if (funct3 == "000"):
            # lb
           
            execute("lb", rs1, " ", rd, imm, PC)
            PC += 4
        elif (funct3 == "001"):
            # lh
            
           
            execute("lh", rs1, " ", rd, imm, PC)
            PC += 4
        elif (funct3 == "010"):
            # lw
            
            execute("lw", rs1, " ", rd, imm, PC)
            PC += 4
        else:
            print("Error")
            PC += 4
    elif (opcode == "0010011"):
        if (funct3 == "000"):
            # addi
            execute("addi", rs1, " ", rd, imm, PC)
            
            PC += 4
        elif (funct3 == "111"):
            # andi
            execute("andi", rs1, " ", rd, imm, PC)
            
            PC += 4
        elif (funct3 == "110"):
            # ori
            execute("ori", rs1, " ", rd, imm, PC)
            
            PC += 4
        else:
            print("Error")
            PC += 4
    elif (opcode == "1100111"):
        if (funct3 == "000"):
            # jalr
            PC = execute("jalr", rs1, " ", rd, imm, PC)
            
        else:
            print("Error")
            PC += 4

    return PC


def sb_format(binary, pc):  # MANAN SINGHAL 2019CSB1099
    sb_opcode = binary[25:32]
    funct3 = binary[17:20]
    rs1 = binary[12:17]
    rs2 = binary[7:12]
    imm = binary[0] + binary[24] + binary[1:7] + binary[20:24]
   
    if funct3 == '000':
        
        pc = execute("beq", rs1, rs2, " ", imm, pc)
    elif funct3 == '001':
        
        pc = execute("bne", rs1, rs2, " ", imm, pc)
    elif funct3 == '101':
       
        pc = execute("bge", rs1, rs2, " ", imm, pc)
    elif funct3 == '100':
        
        pc = execute("blt", rs1, rs2, " ", imm, pc)
    else:
        print("Error")

    return pc


def S_Format(m_c, PC):  # PRAVEEN KUMAR 2019CSB1108

    func3 = m_c[17:20]  # funct3
    rs1 = m_c[12:17]  # source register1
    rs2 = m_c[7:12]  # source register2
    imm = m_c[0:7] + m_c[20:25]  # offset added to base adress
    
    Sr1 = 0  # for decimal value of source register1
    Sr2 = 0  # for decimal value of source register2
    for i in range(0, 5):
        if (rs1[i] == '1'):
            Sr1 = Sr1 + pow(2, 4 - i)
        if (rs2[i] == '1'):
            Sr2 = Sr2 + pow(2, 4 - i)
    
    Offset = 0
    for i in range(0, 12):
        if (imm[i] == '1'):
            Offset = Offset + pow(2, 11 - i)

    

    if (func3 == '000'):

        # Execution of store_byte(sb)
        
        execute("sb", rs1, rs2, " ", imm, PC)

    elif (func3 == '001'):

        # Execution of store_halfword(sh)
      
        execute("sh", rs1, rs2, " ", imm, PC)

    elif (func3 == '010'):
        # Execution of store_word(sw)
        
        execute("sw", rs1, rs2, " ", imm, PC)
    else:
        print("ERROR")


def U_Format(machinecode, PC):  # RAJASEKHAR 2019CSB1105
    # auipc,lui
    imm = machinecode[0:20]
    rd = machinecode[20:25]
    opcode = machinecode[25:32]  # opcode is enough to distinguish u and uj format instructions
    if (opcode == "0010111"):
        # auipc
       
        execute("auipc", " ", " ", rd, imm, PC)

    elif (opcode == "0110111"):
        # lui
       
        execute("lui", " ", " ", rd, imm, PC)
    else:
        print("Error")

    return


def UJ_Format(machinecode, pc):  # RAJASEKHAR 2019CSB1105
    # jal
    opcode = machinecode[25:32]
    imm = machinecode[0] + machinecode[12:20] + machinecode[11] + machinecode[1:11]
    
    rd = machinecode[20:25]
    if (opcode == "1101111"):
        # jal
       
        pc = execute("jal", " ", " ", rd, imm, pc)
       
    else:
        print("Error")

    return pc




def fetch(Instruct):
    # fetching
    file = open(sys.argv[1], 'r')
    PC = 0
    clock = 0

    datasegOrnot = 0
    for line in file:
        if (line == "\n"):
            datasegOrnot = 1
            continue
        if (datasegOrnot == 1):  # fetching memory from data segment
            dataArray = line.split(' ')
            daata = dataArray[1][2:4]
            memory[int(dataArray[0], 16)] = daata
            continue
    file.close()

    last_PC = 0
    file = open(sys.argv[1], 'r')
    for line in file:
        if (line == "\n"):
            break
        inputsArray = line.split(' ')
        tempc = int(inputsArray[0][2:], 16)
        binaryno = bin(int(inputsArray[1][2:], 16))[2:].zfill(32)
        Instruct[tempc] = binaryno
        last_PC = tempc

        
    file.close()
   
    while (PC <= last_PC):
        clock = clock + 1
       
        binaryno = Instruct[PC]
        
        if (binaryno == "11111111111111111111111111111111"):
            
            break
        temp = binaryno
        temp = int(temp, 2)
        print("Fetch instruction : ", hex(temp), "at address :", hex(PC), end=" \n", sep=" ")
        PC = decode(binaryno, PC)
        print("clock =", clock)
        print("\n\n")

    return Instruct


Instruct = {}
Instruct = fetch(Instruct)       #Simulator starting point 

printregister()
print("\n\n")

new_file = open(sys.argv[1], "w")

for line in Instruct:
    new_file.write(str(hex(line)))
    new_file.write(" 0x")
    a = hex(int(Instruct[line], 2))[2:].zfill(8)
    new_file.write(str(a))
    new_file.write("\n")

new_file.write("\n")
for line in memory:
    new_file.write(str(hex(line)))
    new_file.write(" 0x")
    new_file.write(memory[line])
    new_file.write("\n")

new_file.close()

print("MEMORY byte by byte, data is stored in hexa , address in decimal:\n\n",
      memory)  # printing memory key is address and value is data