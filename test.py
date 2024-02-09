#For testing purposes

import sys 
import getopt

import VMManager

def findnextFree(alist):
    '''Given a sorted list find the next free frame num'''

    for aindex in range(len(alist)-1):

        ValAtInd = alist[aindex]

        ValAtNextInd = alist[aindex + 1]

        print(f"ind {aindex} {ValAtInd} {ValAtNextInd}")

        
        
        print("outer else")
        #case where end of list has not been reached
        if ValAtNextInd - ValAtInd > 1:
            return ValAtInd + 1
        
    #check if last elem + 1 is out of range
    return alist[len(alist)-1] + 1
            

        

        
    return None


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

    TheVMmanagerobj.initialize("init-dp-justtest.txt")

    print(TheVMmanagerobj)

    # testVA = 2359818

    # CompS = testVA >> 18

    # CompP = (testVA >> 9) & 0b111111111

    # CompW = testVA & 0b111111111

    # CompPW = testVA & 0b111111111111111111

    # print(f"s {CompS} p {CompP} w {CompW} pw {CompPW}")


    print(f"PA {TheVMmanagerobj.VAtoPA(2097162)}")

    print(f"PA {TheVMmanagerobj.VAtoPA(2097162)}")
    print(f"PA {TheVMmanagerobj.VAtoPA(2097674)}")
    print(f"PA {TheVMmanagerobj.VAtoPA(2359306)}")

    print(TheVMmanagerobj)

    

    # print(f"PA {TheVMmanagerobj.VAtoPA(2359818)}")

    # print(TheVMmanagerobj)

    # TestList = [1,2,3,4,5,6,7,111]

    # print(findnextFree(TestList))




if __name__ == "__main__":

    main()
        
      