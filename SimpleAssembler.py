import sys

##################################### FILE HANDLING ####################################
def decimal_binary(n):                            
    n=float(n)

    if n==int(n):
        n=int(n)
        ans=[]
        while n!=0:
            rem=n%2    
            ans.append(rem)
            n=int(n/2)
            n=int(n)
        ans.reverse()
        string=""
        for i in ans:
            string +=i
        
        return string[:7]
    else:
        x=int(n)
        y=n-x
        ans=[]
        while x!=0:
            rem=x%2
            ans.append(str(rem))
            x=int(x/2)
        ans.reverse()
        
        ans2=[]
        
        while y!=0:
            y=y*2
            ans2.append(str(int(y)))
            y=y-int(y)
        
        sample=ans.copy()
        sample.append(".")
        sample.extend(ans2)
        string=""
        for fun in sample:
            string+=fun
    
            
        return string[:7]
        # return string



f=open("assembler_testcase.txt")
lines = f.readlines()
instructions = []
for x in lines:
    instructions.append(x.split())
#instructions = []
# for line in sys.stdin:
#    instructions.append(list(map(str,line.split())))
# count = 0

#removing blank lines
while [] in instructions:
    instructions.remove([])
n=0
total=len(instructions)
for i in range(len(instructions)):
    n = n + 1
#given instructions converted into list.
def getlist(dict):
    list = []
    for key in dict.keys():
        list.append(key)
    return list


ISA = {'add':'10000',
        'sub':'10001',
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
        'hlt':'01010',
        'addf':'00000',
        'subf':'00001',
        'movf':'00010'}
ISA_List = getlist(ISA)
Reg_opcode={
        'R0':'000',
        'R1':'001',
        'R2':'010',
        'R3':'011',
        'R4':'100',
        'R5':'101',
        'R6':'110',
        'FLAGS':'111'}
Reg_List = getlist(Reg_opcode)
        
#counting variables and storing them and their address in binary
var_List = []
var_count = 0
for i in range(len(instructions)):
    if instructions[i][0] == "var":
        var_List.append(instructions[i][1])
        var_count +=1
    else:
        break

#counting labels and storing them and their address in binary
label_list =[]
label_dict = dict()
for i in range(len(instructions)):
    if instructions[i][0][-1] == ":":
        label_list.append(instructions[i][0][:-1])
        
        label_address = str(bin(i - var_count ))
        
        addr=label_address[2:]
        
        
        while len(addr)!=8:
            addr='0'+addr
            
        
        label_dict[instructions[i][0][:-1]] = addr
        

var_dict =dict()
for i in range(len(instructions)):
    if instructions[i][0] == "var":
        variable_address = bin(len(instructions) - var_count + i).replace('0b','')
        addr = variable_address[::-1]
        while len(addr) != 8:
            addr += '0'
        variable_address = addr[::-1]
        var_dict[instructions[i][1]] = variable_address
    else:
        break
for i in range(len(instructions)):
   if(instructions[i][0][-1]==':'):
       instructions[i].remove(instructions[i][0])
##################################### ERROR HANDLING BEGINS #####################################
flag = 0
Error_list=[]
#General Syntax Error Handling
for i in range(len(instructions)):
    if(instructions[i][0]=='add' or instructions[i][0]=='sub' or instructions[i][0]=='mul' or instructions[i][0]=='xor' or instructions[i][0]=='or' or instructions[i][0]=='and' or instructions[i][0]=='addf' or instructions[i][0]=='subf'):
        if(len(instructions[i])!=4):
           Error_list.append(f"General Syntax Error in Line {i+1}")
           flag = 1
           break
    if(instructions[i][0]=='mov' or instructions[i][0]=='movf' or instructions[i][0]=='ld' or instructions[i][0]=='st' or instructions[i][0]=='div' or instructions[i][0]=='rs' or instructions[i][0]=='ls' or instructions[i][0]=='not' or instructions[i][0]=='cmp'):
        if(len(instructions[i])!=3):
               Error_list.append(f"General Syntax Error in Line {i+1}")
               flag = 1
               break
    if(instructions[i][0]=='jmp' or instructions[i][0]=='jlt' or instructions[i][0]=='jgt' or instructions[i][0]=='je'):
        if(len(instructions[i])!=2):
               Error_list.append(f"General Syntax Error in Line {i+1}")
               flag = 1
               break
    if(instructions[i][0]=='hlt'):
        if(len(instructions[i])!=1):
               Error_list.append(f"General Syntax Error in Line {i+1}")
               flag = 1
               break
    if(instructions[i][0]=='hlt'):
        if(i!=total-1):
                Error_list.append(f"General Syntax Error in Line {i+1}")
                flag = 1
                break

#B and C and F part Error Handling
if(flag==0):
 for i in range(len(instructions)):
    if(instructions[i][0]=='st' or instructions[i][0]=='ld'):
        if(instructions[i][2] not in var_List):
            Error_list.append(f"Undefinded Variable in Line {i+1}")
            flag = 1
            break
    elif(instructions[i][0]=='je' or instructions[i][0]=='jgt' or instructions[i][0]=='jlt' or instructions[i][0]=='jmp'):
        if(instructions[i][1] not in label_dict):
            Error_list.append(f"Undefinded label in Line {i+1}")
            flag = 1
            break

#A & D part Error Handling
     #Instruction Handling
if(flag==0):
 for i in range(len(instructions)):
    if(instructions[i][0] not in ISA_List and instructions[i][0] != 'var' and instructions[i][0] != 'mov' and instructions[i][0][-1] != ':'):
         Error_list.append(f"Undefined Instruction in Line {i+1}")
         flag = 1
         break

      #Register Name Handling
if(flag==0):
 for i in range(len(instructions)):
    if(instructions[i][0]=='add' or instructions[i][0]=='sub' or instructions[i][0]=='mul' or instructions[i][0]=='xor' or instructions[i][0]=='and' or instructions[i][0]=='or' or instructions[i][0]=='addf' or instructions[i][0]=='subf'):
        if(instructions[i][1] not in Reg_List or instructions[i][2] not in Reg_List or instructions[i][3] not in Reg_List):
            Error_list.append(f"Undefined Register name in Line {i+1}")
            flag = 1
            break
        if(instructions[i][1]=='FLAGS' or instructions[i][2]=='FLAGS' or instructions[i][3]=='FLAGS' ):
            Error_list.append(f"Misuse of FLAGS in Line {i+1}")
            flag = 1
            break
    if(instructions[i][0]=='div' or instructions[i][0]=='not' or instructions[i][0]=='cmp'):
        if(instructions[i][1] not in Reg_List or instructions[i][2] not in Reg_List):
            Error_list.append(f"Undefined Register name in Line {i+1}")
            flag = 1
            break
        if(instructions[i][1]=='FLAGS' or instructions[i][2]=='FLAGS'):
            Error_list.append(f"Misuse of FLAGS in Line {i+1}")
            flag = 1
            break
    if(instructions[i][0]=='rs' or instructions[i][0]=='ls'):
        if(instructions[i][1] not in Reg_List):
            Error_list.append(f"Undefined Register name in Line {i+1}")
            flag = 1
            break
        if(instructions[i][1]=='FLAGS'):
            Error_list.append(f"Misuse of FLAGS in Line {i+1}")
            flag = 1
            break
    if((instructions[i][0]=='mov' and instructions[i][2][0]=='$') or (instructions[i][0]=='movf' and instructions[i][2][0]=='$')):                                     #INCOMPLETE MOV
        if(instructions[i][1] not in Reg_List):
            Error_list.append(f"Undefined Register name in Line {i+1}")
            flag = 1
            break
        if(instructions[i][1]=='FLAGS'):
            Error_list.append(f"Misuse of FLAGS in Line {i+1}")
            flag = 1
            break
    if(instructions[i][0]=='mov' and instructions[i][2][0]!='$'):                                     
        if(instructions[i][1] not in Reg_List or instructions[i][2] not in Reg_List):
            Error_list.append(f"Undefined Register name in Line {i+1}")   
            flag = 1
            break         
        if(instructions[i][1]=='FLAGS' or instructions[i][2]=='FLAGS'):
            Error_list.append(f"Misuse of FLAGS in Line {i+1}")
            flag = 1
            break
if(flag == 0):
 for i in range(len(instructions)):
    if(instructions[i][0]=='add' or instructions[i][0]=='sub' or instructions[i][0]=='mul' or instructions[i][0]=='xor' or instructions[i][0]=='and' or instructions[i][0]=='or' or instructions[i][0]=='addf' or instructions[i][0]=='subf'):
        if(instructions[i][1] =='FLAGS' or instructions[i][2]=='FLAGS' or instructions[i][3]=='FLAGS'):
            Error_list.append(f"Illegal use of flags {i+1}")
            flag = 1
            break
    elif(instructions[i][0]=='div' or instructions[i][0]=='not' or instructions[i][0]=='cmp'):
        if(instructions[i][1]=='FLAGS' or instructions[i][2]=='FLAGS'):
            Error_list.append(f"Illegal use of flags {i+1}")
            flag = 1
            break
    elif(instructions[i][0]=='rs' or instructions[i][0]=='ls'):
        if(instructions[i][1]=='FLAGS'):
            Error_list.append(f"Illegal use of flags {i+1}")
            flag = 1
            break
    elif(instructions[i][0]=='mov'):                                    
        if(instructions[i][2]=='FLAGS'):
            Error_list.append(f"Illegal use of flags {i+1}")
            flag = 1
            break
      
# Type E error handling
for i in range(len(instructions)):
    if(len(instructions[i])==3):
     if(instructions[i][2][0]=="$"):
        temp = instructions[i][2][1:]
        # try:
        #     temp = int(temp)
        # except:
        #     Error_list.append(f"Misuse of Immediate value in Line {i+1}")
        #     flag = 1
        #     break
        temp=float(temp)
        if(temp<0.0 or temp>256.0):
            Error_list.append(f"Misuse of Immediate value in Line {i+1}")
            flag = 1
            break
        

#Part G
if(flag==0):
 for i in range(len(instructions)):
    if (instructions[i][0] == "var" and i > var_count):
        Error_list.append(f"Variable not declared at the begining {i+1}")
        flag = 1
        break
    


#H part Error Handling
flag1 = 0
if(flag==0):
    
 for i in range(len(instructions)):
    if('hlt' not in instructions[i]):
       flag1 = flag1 + 1    
 if(flag1==n and flag==0):
    Error_list.append("Missing hlt instructions")
    flag = 1
    
#I Part Error Handling
if(instructions[n-1][0]!='hlt' and flag==0):
    Error_list.append("hlt is not used as a last instruction")
    flag = 1


##################################### ERROR HANDLING ENDS #####################################


##################################### MAIN PROGRAM BEGINS#####################################
if(flag==0):  
#type A : 3 register type
 for i in instructions:
    #printing opcode bits
    if (i[0] == "add" or i[0] == "sub" or i[0] == "mul" or i[0] == "xor" or i[0] == "and" or i[0] == "or" or i[0] == "addf" or i[0] == "subf"):
        for j in ISA:
            if (i[0] == j):
                print(ISA[j],end = "")
                break
    
    #print Unused bits
        print("00",end="")

    #printing register bits    
        for registerBits in Reg_opcode:
            if i[1] == registerBits:
                print(Reg_opcode[registerBits], end="") 
                break

        for registerBits in Reg_opcode:
            if i[2] == registerBits:
                print(Reg_opcode[registerBits], end="") 
                break
        for registerBits in Reg_opcode:
            if i[3] == registerBits:
                print(Reg_opcode[registerBits]) 
                break

#type B : register and immediate 
    elif ((i[0] == "mov" and i[2][0] == "$") or (i[0] == "movf" and i[2][0] == "$") or (i[0] == "ls" or i[0] == "rs")):
    
    #ISA bits
        if i[0] == "mov":
            print("10010",end="")
        else:
            print(ISA[i[0]],end="")

    #register bits
        for registerBits in Reg_opcode:
            if i[1] == registerBits:
                print(Reg_opcode[registerBits], end="")
                break
    #immediate value bits
        if(i[0]=="movf"):
            imm_value = i[2][1:]
            addr = decimal_binary(imm_value)
            for m in range(len(addr)):
             if(addr[m]=="."):
                 break
            m-=1
            
         
            m = str(bin(int(m)))[2:]
            while len(m)!=3:
             m  = "0"+m
            #print(m,end="")
            mantissa = ""
            for d in range(2,len(addr)):
             if(addr[d]!="."):
              mantissa += str(addr[d])   
            while len(mantissa)!=5:
             mantissa = mantissa + "0"
            #print(mantissa)
            imm_value = m + mantissa
            print(imm_value)
        else:
            imm_value = i[2][1:]
            imm_value = str(bin(int(imm_value)))
            addr = imm_value[2:]
            while len(addr)!=8:
                addr = "0"+addr
            imm_value = addr
            print(imm_value)
        
            
#type C : 2 register type
    elif (i[0] == "mov" or i[0] == "div" or i[0] == "not" or i[0] == "cmp"):
        #ISA bits
        if(i[0] == "mov"):
            print("10011",end="")
        else:
            for j in ISA:
                if (i[0] == j):
                    print(ISA[j],end = "")
                    break
        
        #Unused bits
        print("00000", end ="")

        #register bits
        for registerBits in Reg_opcode:
            if i[1] == registerBits:
                print(Reg_opcode[registerBits], end="")
                break

        for registerBits in Reg_opcode:
            if i[2] == registerBits:
                print(Reg_opcode[registerBits])
                break

#type D : register and memory type
    elif (i[0] == "ld" or i[0] == "st"):

        #ISA bits
        for j in ISA:
            if (i[0] == j):
                print(ISA[j],end = "")
                break
        
        #register bits
        
        if i[1] in Reg_opcode:
            print(Reg_opcode[i[1]],end="")
            
        
        #memory address bits
        
        # for check in instructions:
        #     #variable ki bits
        #     if(check[1] == i[2]):
        #         print(j[2])
        #         break
     
        if i[2] in var_dict:
           
            print(var_dict[i[2]])
        
#Type E: memory address type
    elif(i[0] == "jmp" or i[0] == "jlt" or i[0] == "jgt" or i[0] == "je"):
        #ISA bits
        for j in ISA:
            if(i[0] == j):
                print(ISA[j],end="")
        #unused bits
        print("000",end="")

        #memory address bits
        # for check in instructions:
        #     if j[0]
        if i[1] in label_dict:
            print(label_dict[i[1]])

#type F: halt

    elif (i[0] == "hlt"):
        #ISA bits
        for j in ISA:
            if i[0] == j:
                print(ISA[j],end="")
                break
        #unused bits
        print("00000000000")
    
else:
    print(Error_list[0])
      ##################################### MAIN PROGRAM ENDS#####################################  
