#the main File

import sys 
import getopt

import VMManager


def main():
    print("IN Main")

    InitFilename = None

    argv = sys.argv[1:]

    try: 
        opts, args = getopt.getopt(argv, "i:") 
      
    except: 
        print("Error") 
  
    try:
        for opt, arg in opts: 
            if opt in ['-i']: 
                InitFilename = arg
    except UnboundLocalError:
        print("Usage: test.py -i InitialFileName.txt")

    TheVMmanagerobj = VMManager.VMManager()

    TheVMmanagerobj.initialize(InitFilename)

    
    while(True):
        try:
            userinpt = input()
            userinpt = userinpt.strip()

            VAList = list()

            FinalPAList = list()

            for aintstr in userinpt.split():
                VAList.append(int(aintstr))

            #translate
                
            for aVMaddr in VAList:
                FinalPAList.append(TheVMmanagerobj.VAtoPA(aVMaddr))

            print(FinalPAList)

            FinalStr = ""

            for acnt,aPMaddr in enumerate(FinalPAList):
                if acnt == len(FinalPAList)-1:
                    FinalStr += str(aPMaddr)
                else:
                    FinalStr += f"{aPMaddr} "

            print(FinalStr)



        except KeyboardInterrupt:
            exit()
        except EOFError:
            exit()
    

    print(InitFilename)


if __name__ == "__main__":
    main()
        
      