import sys
#f = open("simulator.txt")

reg={"000":0,"001":0,"010":0,"011":0,"100":0,"101":0,"110":0,"111":"0000000000000000"}

ISA = {'add':'10000',
        'sub':'10001',
        'movimm':'10010',
        'movreg':'10011',
        'ld':'10100',
        'st':'10101',
        'mul':'10110',
        'div':'10111',
        'rs':'11000',
        'ls':'11001',
        'xor':'11010',
        'or':'11011',
        'and':'11100',
        'not':'11101',
        'cmp':'11110',
        'jmp':'11111',
        'jlt':'01100',
        'jgt':'01101',
        'je':'01111',
        'hlt':'01010'}

def integer_to_binary(num):          #converts binary values in integer
    converted = bin(int(num))[2:]
    return converted

def complete_bits(str,l):            #to complete the remaining bits by adding zeros in the front
    final = "0"*(l - len(str))+str
    return final

def reset_Flag():                    #Used to reset old flags values
    return "0000000000000000"
def set_flag_overflow():             #set flag high in cases of overflow and underflow
    return "0000000000001000"
def set_flag_lessthan():             #set flag high in cases when value1 is less than value2
    return "0000000000000100"
def set_flag_greaterthan():          #set flag high in cases when value1 is greater than value2
    return "0000000000000010"       
def set_flag_equal():                #set flag high in cases when value1 is equal to value2
    return "0000000000000001"

def simulator(i,pc):

# for type A : 3 register type
   
    if i[:5] == ISA["add"]:      #add
        a = i[7:10]
        b = i[10:13]
        c = i[13:16]

        reg[c] = reg[a] + reg[b]

        if reg[c] > ((2**16)-1):
            reg["111"] = set_flag_overflow()
        else:
            reg["111"] = reset_Flag()
        pc+=1
       

    if i[:5] == ISA["sub"]:      #sub
        a = i[7:10]
        b = i[10:13]
        c = i[13:16]

        reg[c] = reg[a] - reg[b]
       
        if reg[c] < 0:
            reg["111"] = set_flag_overflow()
        else:
            reg["111"] = reset_Flag()
       
        pc+=1
    if i[:5] == ISA["mul"]:      #mul
        a = i[7:10]
        b = i[10:13]
        c = i[13:16]

        reg[c] = reg[a] * reg[b]
        pc+=1
       
        if reg[c] > ((2**16)-1):
            reg["111"] = set_flag_overflow()
        else:
            reg["111"] = reset_Flag()
       
       
   
    if i[:5] == ISA["or"]:      #exclusive OR
        a = i[7:10]
        b = i[10:13]
        c = i[13:16]

        reg[c] = reg[a]|reg[b]
        pc+=1
        reg["111"] = reset_Flag()

    if i[:5] == ISA["and"]:      #exclusive and
        a = i[7:10]
        b = i[10:13]
        c = i[13:16]

        reg[c] = reg[a]&reg[b]
        pc+=1
        reg["111"] = reset_Flag()

    # type B : register and immediate

    if i[:5] == ISA["movimm"]:
        a = i[5:8]                #moves numerical value in register
        num = int(i[8:16],2)
        reg[a] = num
        
        pc+=1
        reg["111"] = reset_Flag()

    if i[:5] == ISA["ls"]:        #performs left shift 
        a = i[5:8]
        num = int(i[8:16],2)
        reg[a] = reg[a] << num
        
        pc+=1
        reg["111"] =reset_Flag()

    if i[:5] == ISA["rs"]:         #performs right shift
        a = i[5:8]
        num = num = int(i[8:16],2)
        reg[a] = reg[a]>>num
        # print(reg[a])
        pc+=1
        reg["111"] = reset_Flag()

#for type C: 2 register type

    if i[:5] == ISA["movreg"]:        #moves register value in another value
        a = i[10:13]
        b = i[13:16]
        reg[b] = reg[a]

        pc+=1
        reg["111"] = reset_Flag()

    if i[:5] == ISA["div"]:           #performs division between two register values
        a = i[10:13]
        b = i[13:16]

        reg["000"] = reg[a]/reg[b]          #stores quotient value in r0 
        reg["001"] = reg[a]%reg[b]          #stores remainder value in r1

        pc+=1
        reg["111"] = reset_Flag()
   
    if i[:5] == ISA["not"]:                 #inverts register2 value in register1
        a = i[10:13]
        b = i[13:16]

        reg[a] = ~reg[b]
   
        pc+=1
        reg["111"] = reset_Flag()
   
    if i[:5] == ISA["cmp"]:                #compares values of two register
        a=i[10:13]
        b=i[13:16]

        if(reg[a]==reg[b]):
            reg['111']=set_flag_equal()
        if(reg[a]>reg[b]):
            reg['111']=set_flag_greaterthan()
        if(reg[a]<reg[b]):
            reg['111']=set_flag_lessthan()
        pc+=1

#type D: register and memory address
    if i[:5] == ISA["ld"]:                   #load value stored at memory address in register
        a = i[5:8]

        reg[a]=int(bitcodes[int(i[8:16],2)],2)
        pc+=1
        reg['111']= reset_Flag()

    if i[:5] == ISA["st"]:                   #stores value of register in memory
       
        a=i[5:8]
       
        b=int(i[8:16],2)      #memory address
        bitcodes[b] = complete_bits(integer_to_binary(reg[a]),16)
         
        pc+=1
        reg['111']=reset_Flag()

#type E: Memory address type

    if i[:5] == ISA["jmp"]:                  #unconditional jump
        pc =int(i[8:16],2)
        reg["111"] = reset_Flag()
   
    if i[:5] == ISA["jlt"]:                  #jump to memory address if value is less than when compared

        if (reg["111"][13]=="1"):
            pc = (int(i[8:16],2))
        else:
            pc +=1
        reg["111"] = reset_Flag()
    if i[:5] == ISA["jgt"]:                  #jump to memory address if value is greater than when compared

        if (reg["111"][14] == "1"):
            pc = int(i[8:16],2)
        else:
            pc +=1  
        reg["111"] = reset_Flag() 
    if i[:5] == ISA["je"]:                    #jump to memory address if value is equal to when compared

        if(reg["111"][15] == "1"):
            pc = int(i[8:16],2)
        else:
            pc +=1  
        reg["111"] = reset_Flag()  

    if i[:5] == ISA["hlt"]:                   

        pc+=1
        reg["111"] = reset_Flag()
        halt = True
        return True,pc
    else:
        return False,pc


##MAIN##
bitcodes = []
#for instructions in f.readlines():
for instructions in sys.stdin:
    #if("\n" in instructions):
     #   instructions = instructions[:-1]
    bitcodes.append(instructions)

lines = 256-len(bitcodes)
while (lines !=0):
    bitcodes.append("0000000000000000")
    lines -=1

pc = 0
halt = False

while(not halt):
    final_pc = complete_bits(integer_to_binary(pc),8)
    print(final_pc,end = " ")
    instruction = bitcodes[pc]
    halt,pc = simulator(instruction, pc)
    for i in reg:
        if (i == "111"):
            print(reg[i],end=" ")
        else:
            print(complete_bits(integer_to_binary(reg[i]),16),end= " ")
    print()
   
for i in range(256):
    print(bitcodes[i])
