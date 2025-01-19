from time import sleep

print('Cortado# --- 1.1 RELEASE')
print('Copyright (c) 2024-2025 Eyad Taha')
print('')

# BPOS
enableBPOSLog = False

# Variable Setup
opcode = ''
RAM_ADR_VAL = ['null'] * 67
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
        elif parserCache_STRING == '.RML':
            opcode = 'ram'
        elif parserCache_STRING == 'delay':
            opcode = 'delay'
        elif parserCache_STRING == 'branch':
            opcode = 'branch'
        elif parserCache_STRING == 'request':
            opcode = 'request'

        elif parserCache_STRING == '.ALU.add':
            opcode = 'add'
        elif parserCache_STRING == '.ALU.sub':
            opcode = 'sub'

        elif parserCache_STRING == '.ALU.mul':
            opcode = 'mul'
        elif parserCache_STRING == '.ALU.div':
            opcode = 'div'

        elif parserCache_STRING == 'branch.if_ac.ZERO':
            opcode = 'bIZ'

        elif parserCache_STRING == 'branch.if_ac':
            opcode = 'bI'

        elif parserCache_STRING == 'branch.eq.if':
            opcode = 'branchIF'

        elif parserCache_STRING == 'newline':
            opcode = 'nl'

        elif parserCache_STRING == 'convert.Int':
            opcode = 'convertInt'



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
    global instructionProcessing_i
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
        instructionProcessing_i = final_INT - 1

    elif opcode == 'request':
        if dataType == 'str':

            rmlCache.remove('|')
            final_RML = int(''.join(rmlCache))

            stringCache.remove('$')
            final_STR = ''.join(stringCache)

            RAM_ADR_VAL[final_RML] = input(final_STR)

    elif opcode == 'add':
        rmlCache.remove('|')
        final_RML = int(''.join(rmlCache))

        if dataType == 'int':
            integerCache.remove('^')
            final_INT = int(''.join(integerCache))
            RAM_ADR_VAL[65] = RAM_ADR_VAL[final_RML] + final_INT

        elif dataTypeList.count('rml') == 2:
            rmlCache_DCS.remove('|')
            final_RML_DCS = int(''.join(rmlCache_DCS))
            RAM_ADR_VAL[65] = RAM_ADR_VAL[final_RML] + RAM_ADR_VAL[final_RML_DCS]

    elif opcode == 'sub':
        rmlCache.remove('|')
        final_RML = int(''.join(rmlCache))

        if dataType == 'int':
            integerCache.remove('^')
            final_INT = int(''.join(integerCache))
            RAM_ADR_VAL[65] = RAM_ADR_VAL[final_RML] - final_INT


        elif dataTypeList.count('rml') == 2:
            rmlCache_DCS.remove('|')
            final_RML_DCS = int(''.join(rmlCache_DCS))
            RAM_ADR_VAL[65] = RAM_ADR_VAL[final_RML] - RAM_ADR_VAL[final_RML_DCS]


    elif opcode == 'mul':
        rmlCache.remove('|')
        final_RML = int(''.join(rmlCache))

        if dataType == 'int':
            integerCache.remove('^')
            final_INT = int(''.join(integerCache))
            RAM_ADR_VAL[65] = RAM_ADR_VAL[final_RML] * final_INT

        elif dataTypeList.count('rml') == 2:
            rmlCache_DCS.remove('|')
            final_RML_DCS = int(''.join(rmlCache_DCS))
            RAM_ADR_VAL[65] = RAM_ADR_VAL[final_RML] + RAM_ADR_VAL[final_RML_DCS]

    elif opcode == 'div':
        rmlCache.remove('|')
        final_RML = int(''.join(rmlCache))

        if dataType == 'int':
            integerCache.remove('^')
            final_INT = int(''.join(integerCache))
            RAM_ADR_VAL[65] = RAM_ADR_VAL[final_RML] / final_INT


        elif dataTypeList.count('rml') == 2:
            rmlCache_DCS.remove('|')
            final_RML_DCS = int(''.join(rmlCache_DCS))
            RAM_ADR_VAL[65] = RAM_ADR_VAL[final_RML] - RAM_ADR_VAL[final_RML_DCS]

    elif opcode == 'bIZ':
        if RAM_ADR_VAL[65] == 0:
            integerCache.remove('^')
            final_INT = int(''.join(integerCache))
            instructionProcessing_i = final_INT - 1

    elif opcode == 'bI':

        integerCache_DCS.remove('^')
        final_INT_DCS = int(''.join(integerCache_DCS))

        if dataType == 'int':
            integerCache.remove('^')
            final_INT = int(''.join(integerCache))

            if RAM_ADR_VAL[65] == final_INT:
                instructionProcessing_i = final_INT_DCS - 1

        elif dataType == 'rml':
            rmlCache.remove('|')
            final_RML = int(''.join(rmlCache))

            if RAM_ADR_VAL[65] == final_RML:
                instructionProcessing_i = final_INT_DCS - 1

        elif dataType == 'str':
            stringCache.remove('|')
            final_STR = int(''.join(stringCache))

            if RAM_ADR_VAL[65] == final_STR:
                instructionProcessing_i = final_INT_DCS - 1

    elif opcode == 'nl':
        print('')


    elif opcode == 'convertInt':
        rmlCache.remove('|')
        final_RML = int(''.join(rmlCache))
        RAM_ADR_VAL[final_RML] = int(RAM_ADR_VAL[final_RML])

    elif opcode == 'branchIF':
        rmlCache.remove('|')
        final_RML = int(''.join(rmlCache))

        integerCache_DCS.remove('^')
        final_INT_DCS = int(''.join(integerCache_DCS))

        if dataType == 'int':
            integerCache.remove('^')
        final_INT = int(''.join(integerCache))
        if RAM_ADR_VAL[final_RML] == final_INT:
            instructionProcessing_i = final_INT_DCS - 1

        elif dataType == 'str':
            stringCache.remove('$')
        final_STR = ''.join(stringCache)
        if RAM_ADR_VAL[final_RML] == final_STR:
            instructionProcessing_i = final_INT_DCS - 1

        elif dataTypeList.count('rml') == 2:
            rmlCache_DCS.remove('|')
        final_RML_DCS = ''.join(rmlCache_DCS)
        if RAM_ADR_VAL[final_RML] == final_RML_DCS:
            instructionProcessing_i = final_INT_DCS - 1

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

    integerCache_DCS = []
    stringCache_DCS = []
    rmlCache_DCS = []

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
    print('')
    print('---Code Execution Successful---')
    sleep(1)
    input('To run more code, restart the app. Enter any key to allow this: ')

def CortadoSHARP(code):
    instructionProcessing(code)

code = ''
program = []

while code != '~run':
    code = input('>> ')
    program.append(code)

program.remove('~run')
CortadoSHARP(program)
