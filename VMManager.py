import bisect
from collections import namedtuple

MAXPMSIZE = 524288
PAGESIZE = 512
DISKBLOCKNUM = 1024

class VMManager:
    def __init__(self) -> None:
        #initialize PM
        self.PM = [None] * MAXPMSIZE
        #init allocated frame List
        self.MemAllocFrameList = list()

        self.nonrespageDict = dict()

        self.DiskAllocatedList = list()

        self.Disk = [ [None]*PAGESIZE for i in range(DISKBLOCKNUM) ]


    def _appendmemFlistSort(self,aval: int):
        bisect.insort(self.MemAllocFrameList,aval)
        


    def _getthrupleList(self,aline: str) -> [(int,int,int)]:

        TheRetthrupleList = list()

        CleanLine = aline.strip()

        CleanLineList = CleanLine.split(" ")

        # CLiter = iter(CleanLineList)

        # return [*zip(CLiter,CLiter,CLiter)]

        counter = 0

        templist = list()

        for anumstr in CleanLineList:

            tempnum = int(anumstr)

            templist.append(tempnum)
            counter += 1

            if counter == 3:
                TheRetthrupleList.append(tuple(templist))
                templist = list()
                counter = 0

        return TheRetthrupleList


    def initialize(self,afilename: str):

        #read the init file line by line
        with open(afilename) as fp:
            TheLines = fp.readlines()

            print(f"line 0: {TheLines[0]}")
            print(f"{self._getthrupleList(TheLines[0])}")

            Line0ThrupList = self._getthrupleList(TheLines[0])

            for aln0Thrup in Line0ThrupList:
                (segnum,segsize,pagetframenum) = aln0Thrup

                Thesegindex = 2*segnum

                #initialize seg size
                self.PM[Thesegindex] = segsize

                #initialize pt fram num
                self.PM[Thesegindex + 1] = pagetframenum


                #check if pt frame is nonres

                if pagetframenum < 0:
                    self.nonrespageDict[segnum] = pagetframenum
                    #allocate disk
                    disknum = abs(pagetframenum)

                    self.DiskAllocatedList.append(disknum)

            print(self.nonrespageDict)


            #initialize line 1 page tables


            print(f"line 1: {TheLines[1]}")
            Line1ThrupList = self._getthrupleList(TheLines[1])

            for a1Thrup in Line1ThrupList:
                (segnum,ptoffset,pageframenum) = a1Thrup



                #check if pt is non resident
                if segnum in self.nonrespageDict:
                    #append to disk
                    Thediskindex = abs(self.nonrespageDict[segnum])
                    self.Disk[Thediskindex][ptoffset] = pageframenum

                else:
                    #resident page
                    #calc pt address
                    Thesegindex = 2*segnum
                    ThePtnum = self.PM[Thesegindex + 1]
                    ThePTAddress = ThePtnum * PAGESIZE

                    #set the pt in mem
                    self.PM[ThePTAddress + ptoffset] = pageframenum




                #allocate page frame num
                if pageframenum < 0:
                    #allocate disk
                    self.DiskAllocatedList.append(abs(pageframenum))
                else:
                    #alloc pm
                    self._appendmemFlistSort(pageframenum)


            #remove from mem frame 0,1 for segments
            self._appendmemFlistSort(0)
            self._appendmemFlistSort(1)

            

    def _calcSPW(self,aVAint:int):
        SPW = namedtuple("SPW","s p w pw")
        CompS = aVAint >> 18

        CompP = (aVAint >> 9) & 0b111111111

        CompW = aVAint & 0b111111111

        CompPW = aVAint & 0b111111111111111111

        return SPW(CompS,CompP,CompW,CompPW)
    
    def VAtoPA(self,aVA: int) -> int:
        TheSPWtup = self._calcSPW(aVA)

        print(f"SPW {TheSPWtup}")

        #Error check if pw > 








    def __repr__(self) -> str:
        TheretStr = "VMManger:\n"

        TheretStr += "Physical mem:\n" 

        for aindex in range(len(self.PM)):

            if self.PM[aindex] is not None:
                TheretStr += f"PM[{aindex}]={self.PM[aindex]}\n"

        TheretStr += "\nMem Alloc List:\n"

        for afframenum in self.MemAllocFrameList:
            
            
            TheretStr += f"Alloc Mem Page Frame Num: {afframenum}\n"

        TheretStr += "\nDisk: \n"

        for aindex in self.DiskAllocatedList:
            TheretStr += f"Disk[{aindex}]={self.Disk[aindex][0:5]}"



        return TheretStr

