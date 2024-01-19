#For testing purposes

import sys 
import getopt

import VMManager

def main():
    print("IN Test")

    # InitFilename = None

    # argv = sys.argv[1:]

    # try: 
    #     opts, args = getopt.getopt(argv, "i:") 
      
    # except: 
    #     print("Error") 
  
    # try:
    #     for opt, arg in opts: 
    #         if opt in ['-i']: 
    #             InitFilename = arg 
    # except UnboundLocalError:
    #     print("Usage: test.py -i InitialFileName.txt")

    # print(InitFilename)

    TheVMmanagerobj = VMManager.VMManager()

    TheVMmanagerobj.initialize("init-dp.txt")

    print(TheVMmanagerobj)

    # testVA = 789002

    # CompS = testVA >> 18

    # CompP = (testVA >> 9) & 0b111111111

    # CompW = testVA & 0b111111111

    # CompPW = testVA & 0b111111111111111111

    # print(f"s {CompS} p {CompP} w {CompW} pw {CompPW}")




if __name__ == "__main__":

    main()
        
      