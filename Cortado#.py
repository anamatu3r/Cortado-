print('Cortado# --- 1.0 RELEASE')
print('Copyright (c) Eyad Taha')
print('')

# BPOS
enableBPOSLog = False

# Variable Setup
opcode = ''
RAM_ADR_VAL = [0] * 64
RAM_ADR_LBL = [0] * 64
interpreterCache = []
interpreterCache_FORMAT_STRING = ''
stringCache = []
integerCache = []
interpreterCache_DATA_INT_FORMAT_INTEGER = 0
insPro_i = 0
par_i = 0
startFlag = False
dataType = ''
currentLetter = ''
delimiter_i = 0

# Lexer
class lexer:
    # Functions
    def functions():
        global opcode, interpreterCache, interpreterCache_STRING, insPro_i, par_i, startFlag, endFlag, dataType
        if interpreterCache_STRING == 'flash':
            opcode = 'flash'
        elif interpreterCache_STRING == 'placeholder':
            opcode = 'placeholder'
    # Delimters
    def delimiters():
        global opcode, interpreterCache, interpreterCache_STRING, insPro_i, par_i, startFlag, endFlag, dataType, currentLetter, delimiter_i
        global interpreterCache_DATA_INT, interpreterCache_DATA_STR
        
        if currentLetter == '^':
            delimiter_i += 1
            if delimiter_i == 1:
                startFlag = True
                dataType = 'int'
                interpreterCache.remove("^")
            else:
                delimiter_i = 0
                startFlag = False
                interpreterCache.remove("^")
        elif currentLetter == '$':
            delimiter_i += 1
            if delimiter_i == 1:
                startFlag = True
                dataType = 'str'
                interpreterCache.remove('$')
            else:
                delimiter_i = 0
                startFlag = False
                interpreterCache.remove('$')
        
        
# Parser
def parse(instruction):
    global opcode, interpreterCache, interpreterCache_STRING, insPro_i, par_i, startFlag, endFlag, dataType, currentLetter, interpreterCache_DATA_INT, interpreterCache_DATA_STR
    global integerCache, final_INT
    global stringCache, final_STR
    
    interpreterCache = []
    interpreterCache_STRING = ''
    integerCache = []
    stringCache = []
    final_STR = ''
    final_INT = 0
    
    par_i = 0
    while par_i != len(instruction):
        interpreterCache.append(instruction[par_i])
        currentLetter = instruction[par_i]
        interpreterCache_STRING = ''.join(interpreterCache)
        lexer.functions()
        lexer.delimiters()
        if startFlag == True:
            if dataType == 'int':
                integerCache.append(instruction[par_i])
            elif dataType == 'str':
                stringCache.append(instruction[par_i])
        par_i += 1
    
    # Execution Preproccessing
    
    
    # Execution
    if opcode == 'flash':
        if dataType == 'int':
            integerCache.remove('^')
            final_INT = ''.join(integerCache)
            print(final_INT)
        
        elif dataType == 'str':
            stringCache.remove('$')
            final_STR = ''.join(stringCache)
            print(final_STR)


# Program processer
def instructionProcessing(instructions):
    global opcode, interpreterCache, interpreterCache_STRING, insPro_i, par_i, startFlag, endFlag, dataType
    
    print('---EXECUTION---\n')
    while insPro_i != len(instructions):
        interpreterCache = []
        interpreterCache_STRING = ''
        par_i = 0
        startFlag = False
        endFlag = False
        parse(instructions[insPro_i])
        insPro_i += 1
        
def CortadoSHARP(code):
    instructionProcessing(code)
    
code = ''
program = []

while code != '~run':
    code = input('>> ')
    program.append(code)


program.remove('~run')

CortadoSHARP(program)
     
