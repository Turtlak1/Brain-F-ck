import getopt, sys, keyboard, time

def log(type, message, error):
    log = ''
    if error != 0:
        log = f'[!] {message} Error code: {str(error)}'
        log = log + f'\n[.] Exiting... Program ended in {(time.time() - start_time)}s'
        print(log)
        exit()
    else :
        log = f'[{type}] {message}'
    
    print(log)

# Code 2 FILE NOT FOUND
# Code 3 KEYBOARD INTERRUP CTRL-C
# Code 4 FILE PATH WAS NOT ADDED
# Code 5 FILE WAS NOT OPEN
# Code 6 ARRAY IS TOO SMALL
# Code 7 ENTERED SIZE IS NOT NUMBER
# Code 8 CODEC "CHARMAP" CAN NOT DECODE BYTE AT POSITION {POSITION OF THE BYTE}

def program():
    global start_time
    start_time = time.time()
    debug = 0
    argumentList = sys.argv[1:]
    # Options
    options = "hf:gds:"

    # Long options
    long_options = ["help", "file=", "gui", "debug", 'size']
    size = 256

    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        
        # checking each argument
        for currentArgument, currentValue in arguments:

            if currentArgument in ("-h", "--help"):
                pr_help()     
            elif currentArgument in ("-f", "--file"):
                try :
                    file = open(currentValue, 'r')
                    log('.', f'Opening file {currentValue}', 0)
                except FileNotFoundError:
                    log('!', f'Error file {currentValue} not found', 2)
                
            elif currentArgument in ("-g", "--gui"):
                print('nothing to see')
            elif currentArgument in ("-d", "--debug"):
                log('.', 'Running in debug mode', 0)
                debug = 1
            elif currentArgument in ("-s", "--size"):
                log('.', f'Array size was set to {currentValue}', 0)
                try:
                    size = int(currentValue)
                except :
                    log('!', 'Entered size is not number', 7)
                
    except getopt.GetoptError:
        # output error, and return with an error code
        log('!', 'Error file path was not added', 4)

    array = []
    for i in range(0, size):
        array.append(0)

    try:
        file_content = list(file.read())
    except NameError as err:
        print(err)
        log('!', 'Error file was not opened', 5)
    except UnicodeDecodeError as err:
        log('!', f'Error {err}', 8)
    index = 0
    loops = 0
    index_loops = [0, 0, 0, 0, 0, 0, 0, 0]
    program_index = 0
    command = ''
    start_time = time.time()
    i = 0

    try : 
        while program_index != len(file_content):
            command = file_content[program_index]
            if debug == 1:
                print(array)
            try :
                if command == "+":
                    array[index]=array[index]+1
                elif command == "-":
                    array[index]=array[index]-1
                elif command == ">":
                    index += 1
                elif command == "<":
                    index -= 1
            except TypeError :
                pass
            if command == ",":
                i = 0
                while i == 0:
                    try:
                        array[index]=ord(keyboard.read_key())
                        i = 1
                    except KeyboardInterrupt:
                        log('!', 'Keyboard Interrupt Ctrl-C', 3)
                    except TypeError:
                        pass
            elif command == ".":
                try :
                    print(chr(array[index]), end='')
                except TypeError:
                    print(str(array[index]), end='')
            elif command == "[":
                index_loops[loops]=program_index
                loops += 1
            elif command == "]":
                if array[index] != 0:
                    program_index = index_loops[loops-1]
                else :
                    loops -= 1
            
            for i in range(0, size):
                try :
                    if array[i] < 0:
                        array[i]= 255
                    if array[i] > 255:
                        array[i]= 0
                except TypeError:
                    pass
            if index == size:
                index = 0
            
            program_index = program_index + 1
        else :
            print()
    except KeyboardInterrupt:
        log('!', 'Keyboard Interrupt Ctrl-C', 3)
        print()
    except IndexError:
        log('!', 'Array size is too small', 6)
        print()
    log('.', 'Done!', 0)
    log('.', f'Exiting... Program ended in {(time.time() - start_time)}s', 0)



def pr_help():
    print( 
    '''Brain Fuck interpreter
Version 1.0

Commands :
    -h --help   Display help/this
    -f --file   Path to your .bf program
    -g --gui    Run your program with GUI resolution is 16x16
    -d --debug  Run your program in debug mode
    -s --size   Set size of array(default=256)
            
    ''')


try:
    if sys.argv[1] == '':
        pass
    program()
except :
    pr_help()

