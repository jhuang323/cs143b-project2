#the main File

import sys 
import getopt


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

    print(InitFilename)


if __name__ == "__main__":
    main()
        
      