#the main File

import sys 
import getopt

import VMManager


def main():
    # print("IN Main")

    InitFilename = None

    argv = sys.argv[1:]

    try: 
        opts, args = getopt.getopt(argv, "i:") 
      
    except getopt.GetoptError as err: 
        print(err)
        print("Usage: test.py -i init-dp.txt < inpt.txt > out.txt")
        sys.exit(2) 
  
    try:
        for opt, arg in opts: 
            if opt in ['-i']: 
                InitFilename = arg
            else:
                print("Usage: test.py -i init-dp.txt < inpt.txt > out.txt")
                sys.exit()

    except UnboundLocalError:
        print("Usage: test.py -i init-dp.txt < inpt.txt > out.txt")

    TheVMmanagerobj = VMManager.VMManager()

    TheVMmanagerobj.initialize(InitFilename)

    #debug print vmmanger obj
    # print(TheVMmanagerobj)

    
    while(True):
        try:

            userinpt = input()
            userinpt = userinpt.strip()

            VAList = list()

            FinalPAList = list()

            for aintstr in userinpt.split():

                #error checking
                try:
                    VAList.append(int(aintstr))
                except ValueError:
                    VAList.append(-1)

            

            #translate
                
            for aVMaddr in VAList:
                try:
                    FinalPAList.append(TheVMmanagerobj.VAtoPA(aVMaddr))
                except Exception as e:
                    FinalPAList.append(-1)

            # print(FinalPAList)

            FinalStr = ""

            for acnt,aPMaddr in enumerate(FinalPAList):
                if acnt == len(FinalPAList)-1:
                    FinalStr += str(aPMaddr)
                else:
                    FinalStr += f"{aPMaddr} "

            #debug print vmmanger obj
            # print(TheVMmanagerobj)

            print(FinalStr)

            



        except KeyboardInterrupt:
            exit()
        except EOFError:
            exit()
    

    


if __name__ == "__main__":
    main()
        
      