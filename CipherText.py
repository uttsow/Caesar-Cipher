

"""
Uttsow Rahman

Output to file:
writeToFile()
Creates a new text document with the encrypted or decrypted text

Input from keyboard:
The name of the file you are modifiying or encrypting/decrypting

Tasks allocated to functions:
makeName(fileName, operation, rotationKey)
Creates the name of the written file

fileNameValidated(name)
Validates the file name, by ensuring that the file is reachable

validateOperation(opStr):
Validates the opearton from the user.
  
validateRotationKey(rotationKeyStr):
Validates that the rotation key is an integer

convertRotationKey(op, rotationKeyStr):
Converts rotation key to negaitive if decrypt or leaves it as
it is if encrypt

keepInBound(ordinal)
keeps the rotation in bound between 32 and 128
    
processMessage(message, rotationKey,opStr):
creates the encrypted/decrypted message
"""    



import os.path

#Define global constants

# Mapping of valid operations to rotationKey factor
OPERATIONS = {'e':[1,"Encrypted"], 'd':[-1, "Decrypted"]}

ENCRYPT = 1
DECRYPT = -1

# Required file extension
FILE_EXT = ".txt"

# File processing modes
READ_MODE = 'r'
WRITE_MODE = 'w'

# Min and limit ordinals of printable ASCII
ASCII_MIN = 32
ASCII_LIMIT = 127
FIXED_SPACE = 32

KEY_PREFIX = "-"

#All functions defined 

def writeToFile(aFile, rotationKey, opStr):
  try:
    inFile = open(aFile, READ_MODE)
    
    try:
      outFile = open(makeName(aFile, opStr, rotationKey), WRITE_MODE)
      

      try:      
        aLine = inFile.readline()
        try:
          while aLine:
            strList = aLine.split()
            aLine = " ".join(strList)
            dataLine = processMessage(aLine, rotationKey, opStr)
            outFile.write(dataLine + '\n')
            aLine = inFile.readline()
     

        except IOError as err: # inner exception handler for outfile processing
          print("\nProblem writing data: \n" + str(err))
        except ValueError as err:  # inner exception handler for outfile processing
          print("\nProblem writing data, wrong format or corrupted?  \n" + str(err) + '\n')
        except Exception as err: # inner exception handler for outfile processing
          print("\nData cannot be written to file: \n" + str(err) + '\n')
        finally:# will close file whether or not exception has been raised
          outFile.close()
          
      except IOError as err: # "outer" exception handler for outfile open
        print("\nExecption raised during open of output file, no write performed: \n" + str(err) + '\n')
      except Exception as err: # outer exception handler for outfile processing
        print("\nData cannot be read:  \n" + str(err) + '\n')
        
    except IOError as err: # inner exception handler for infile processing
      print("\nProblem reading data: \n" + str(err))
    except ValueError as err: # inner exception handler for infile processing
      print("\nProblem processing data, wrong format or corrupted? \n" + str(err) + '\n')
    except Exception as err: # inner exception handler for infile processing
      print("\nData cannot be read:  \n" + str(err) + '\n')        
    finally:# will close file whether or not exception has been raised
      inFile.close()
      
  except FileNotFoundError as err:  # outer exception handler for infile open
    print("\nFile not found:  deleted or in wrong folder?  \n" + str(err) + '\n')
  except IOError as err: # outer exception handler for infile open
    print("\nException raised during open of input file, try a different file: \n" + str(err) + '\n')
  except Exception as err: # outer exception handler for infile open
    print("\nData cannot be read:  \n" + str(err) + '\n')
            


# Generates output file name from input file name, 
#   operation requested and rotation key
# param fileName (str) - input file name
# param operation (str)
# param rotationKey (int) - converted key
# invoke str.split(), str.replace() and str.join()
# return output file name (str)
def makeName(fileName, operation, rotationKey):
  nameList = fileName.split(".")
  nameList[0] = nameList[0].replace(OPERATIONS['e'][1], "")
  nameList[0] = nameList[0].replace(OPERATIONS['d'][1], "")
  nameList[0] += (OPERATIONS[operation][1] + str(rotationKey))
  return ".".join(nameList)

# Checks that file exists and that extension is .txt
# param name (str) - file name
# invoke isFile() from module os.path and endswith()
# return True when valid, False otherwise (bool)
def fileNameValidated(name):
  return os.path.isfile(name) and name.endswith(FILE_EXT)

#Validates operation based on user input
def validateOperation(opStr):
  return len(opStr) == 1 and opStr.lower() in OPERATIONS

#Validates that the rotation key is an integer
def validateRotationKey(rotationKeyStr):
  return (rotationKeyStr[0] == KEY_PREFIX and rotationKeyStr[1:].isdigit()) \
         or rotationKeyStr.isdigit() 


#Converts key 
def convertRotationKey(op, rotationKeyStr):
  return (int(rotationKeyStr)) * OPERATIONS[op][0]

#keeps the key inbound based on ASCII limits 
def keepInBound(ordinal):
  asciiDiff = ASCII_LIMIT - ASCII_MIN
  while ordinal > ASCII_LIMIT or ordinal < ASCII_MIN or ordinal == ASCII_LIMIT: 
    if ordinal > ASCII_LIMIT:
      ordinal -= asciiDiff
    elif ordinal < ASCII_MIN:
      ordinal += asciiDiff
    elif ordinal == ASCII_LIMIT:
      ordinal = FIXED_SPACE
  return ordinal


#Creates the message from the file
def processMessage(message, rotationKey,opStr):
  cryption = ''


  for char in message:
    if opStr in "eE":
      cryption += chr(keepInBound(ord(char) + rotationKey))
    else:
      cryption += chr(keepInBound(ord(char) - (DECRYPT*rotationKey)))
  return cryption

# MAIN BODY

def main():

  print("This program encrypts or decrypts a file " + \
        "using a Caesar cipher. Enter a message or press <ENTER> to quit.")
  
  #Start of the program (Priming Reed)
  aFile = input("What is the name of the file?: ")
 
  while aFile:            #Continutation loop
    while not fileNameValidated(aFile):
      aFile = input("Invalid file name, try again!: ")
      
    cryption = input("Do you want to encrypt (E or e) or decrypt (D or d)?: ")      #OPERATION

    while not validateOperation(cryption):                                        #VALIDATE OPERATION
      print("Invalid input, please try again")
      cryption = input("Do you want to encrypt (E or e) or decrypt (D or d)?: ")

    #cryptionCheck = validateOperation(cryption) 
    #print(cryptionCheck)


    rotation = input("What is the rotation key?: ")                     #ROTATION KEY

    while not validateRotationKey(rotation):                            #VALIDATE KEY
      print("Invalid rotation key, please try again: ")
      rotation = input("What is the rotation key?: ")

    #rotation1 = validateRotationKey(rotation)
    #print(rotation1)
    
    conversion = convertRotationKey(cryption,rotation)

    #print("your key is: ", conversion, "for this cryption: ", cryption)

                    

    #Performs writing to file
    writeToFile(aFile, conversion, cryption)

    
    aFile = input("What is the name of the file?: ")

main()

