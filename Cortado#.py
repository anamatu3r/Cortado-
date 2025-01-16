from time import sleep

print('Cortado# --- BETA 1.0 RELEASE')
print('Copyright (c) Eyad Taha')
print('')

# BPOS
enableBPOSLog = False

# Variable Setup
opcode = ''
RAM_ADR_VAL = ['null'] * 64
RAM_ADR_LBL = [0] * 64
parserCache = []
parserCache_STRING = 0
stringCache = []
integerCache = []
stringCache_DCS = []
integerCache_DCS = []
rmlCache = []
rmlCache_DCS = []
dataTypeList = []
instructionProcessing_i = 0
parser_i = 0
startFlag = False
dataType = ''
currentLetter = ''
delimiter_i = 0
rml_i = 0
int_i = 0
str_i = 0

# Lexer
class lexer:
    # Functions
    @staticmethod
    def functions(self):
        global opcode, parserCache, parserCache_STRING, instructionProcessing_i, parser_i, startFlag, endFlag, dataType
        if parserCache_STRING == 'flash':
            opcode = 'flash'
        elif parserCache_STRING == '.RAM':
            opcode = 'ram'
        elif parserCache_STRING == 'delay':
            opcode = 'delay'
        elif parserCache_STRING == 'branch':
            opcode = 'branch'
        elif parserCache_STRING == 'request':
            opcode = 'request'

        elif parserCache_STRING == '.ALU.add':
            opcode = 'add'
            
    # Delimiters
    @staticmethod
    def delimiters(self):
        global opcode, parserCache, parserCache_STRING, instructionProcessing_i, parser_i, startFlag, endFlag, dataType, currentLetter, delimiter_i
        global integerCache, integerCache_DCS
        global stringCache, stringCache_DCS
        global rmlCache, rmlCache_DCS
        global dataTypeList

        if currentLetter == '^':

            delimiter_i += 1
            
            if delimiter_i == 1:
                dataTypeList.append('int')
                startFlag = True
                dataType = 'int'
                parserCache.remove("^")
            else:
                delimiter_i = 0
                startFlag = False
                parserCache.remove("^")
                
        elif currentLetter == '$':
            delimiter_i += 1
            
            if delimiter_i == 1:
                dataTypeList.append('str')
                startFlag = True
                dataType = 'str'
                parserCache.remove('$')
            else:
                delimiter_i = 0
                startFlag = False
                parserCache.remove('$')

        elif currentLetter == '|':
            delimiter_i += 1
            parserCache.remove('|')
            
            if delimiter_i == 1:
                dataTypeList.append('rml')
                startFlag = True
                dataType = 'rml'
                
            else:
                delimiter_i = 0
                startFlag = False



def executer():
    if opcode == 'flash':
        if dataType == 'int':
            integerCache.remove('^')
            try:
                final_INT = ''.join(integerCache)
            except ValueError:
                print('CORTADO#--- Exception Occurred --- String entered at an integer datatype.')
                print('The following output is converted to a string: \n')
            print(final_INT)

        elif dataType == 'str':
            stringCache.remove('$')
            final_STR = ''.join(stringCache)
            print(final_STR)

        elif dataType == 'rml':
            rmlCache.remove('|')
            final_RML = int(''.join(rmlCache))
            print(RAM_ADR_VAL[final_RML])

    elif opcode == 'ram':
        rmlCache.remove('|')
        final_RML = int(''.join(rmlCache))

        if dataType == 'str':
            stringCache.remove('$')
            final_STR = ''.join(stringCache)
            RAM_ADR_VAL[final_RML] = final_STR
            
        elif dataType == 'int':
            integerCache.remove('^')
            final_INT = int(''.join(integerCache))
            RAM_ADR_VAL[final_RML] = final_INT
            
        elif dataTypeList.count('rml') == 2:
            rmlCache_DCS.remove('|')
            final_RML_DCS = int(''.join(rmlCache_DCS))
            RAM_ADR_VAL[final_RML] = RAM_ADR_VAL[final_RML_DCS]

    elif opcode == 'delay':
        if dataType == 'int':
            integerCache.remove('^')
            final_INT = int(''.join(integerCache))
            sleep(final_INT)
        elif dataType == 'rml':
            rmlCache.remove('|')
            final_RML = int(''.join(rmlCache))

    elif opcode == 'branch':
        integerCache.remove('^')
        final_INT = int(''.join(integerCache))
        instructionProcessing_i = final_INT

    elif opcode == 'request':
        if dataType == 'str':

            rmlCache.remove('|')
            final_RML = int(''.join(rmlCache))

            stringCache.remove('$')
            final_STR = ''.join(stringCache)

            RAM_ADR_VAL[final_RML] = input(final_STR)
        


                

# Parser
def parse(instruction):
    global opcode, parserCache, parserCache_STRING, instructionProcessing_i, parser_i, startFlag, endFlag, dataType, currentLetter, parserCache_DATA_INT, parserCache_DATA_STR
    global integerCache, integerCache_DCS
    global stringCache, stringCache_DCS
    global rmlCache, rmlCache_DCS
    global final_STR_DCS, final_INT_DCS, final_RML_DCS
    global dataTypeList
    
    parserCache = []
    parserCache_STRING = ''
    integerCache = []
    stringCache = []
    rmlCache = []
    final_STR = ''
    final_INT = 0
    final_RML = 0
    dataTypeList = []

    parser_i = 0
    while parser_i != len(instruction):
        parserCache.append(instruction[parser_i])
        currentLetter = instruction[parser_i]
        parserCache_STRING = ''.join(parserCache)
        lexer.functions(self='')
        lexer.delimiters(self='')
        if startFlag == True:
            if dataType == 'int':
                if dataTypeList.count('int') == 1:
                    integerCache.append(instruction[parser_i])
                elif dataTypeList.count('int') == 2:
                    integerCache_DCS.append(instruction[parser_i])
                    
            elif dataType == 'str':
                stringCache.append(instruction[parser_i])
                
            elif dataType == 'rml':
                if dataTypeList.count('rml') == 1:
                    rmlCache.append(instruction[parser_i])
                elif dataTypeList.count('rml') == 2:
                    rmlCache_DCS.append(instruction[parser_i])
        parser_i += 1
    executer()



# Program processer
def instructionProcessing(instructions):
    global opcode, parserCache, parserCache_STRING, instructionProcessing_i, parser_i, startFlag, endFlag, dataType

    print('---EXECUTION---\n')
    while instructionProcessing_i != len(instructions):
        parserCache = []
        parserCache_STRING = ''
        parser_i = 0
        startFlag = False
        endFlag = False
        parse(instructions[instructionProcessing_i])
        instructionProcessing_i += 1

def CortadoSHARP(code):
    instructionProcessing(code)

code = ''
program = []

while code != '~run':
    code = input('>> ')
    program.append(code)

program.remove('~run')

CortadoSHARP(program)

# Note for future self: Add the branch function. (branch^5^) and also the if statement. put it in lexer.delimiters().
