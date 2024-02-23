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

            # print(f"line 0: {TheLines[0]}")
            # print(f"{self._getthrupleList(TheLines[0])}")

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

                else:
                    #allocate PM frame
                    self._appendmemFlistSort(pagetframenum)

            # print(self.nonrespageDict)


            #initialize line 1 page tables


            # print(f"line 1: {TheLines[1]}")
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

    def _findnextFree(self) -> int:
        '''Given a sorted list find the next free frame num'''

        for aindex in range(len(self.MemAllocFrameList)-1):

            ValAtInd = self.MemAllocFrameList[aindex]

            ValAtNextInd = self.MemAllocFrameList[aindex + 1]

            # print(f"ind {aindex} {ValAtInd} {ValAtNextInd}")

            
            
            # print("outer else")
            #case where end of list has not been reached
            if ValAtNextInd - ValAtInd > 1:
                return ValAtInd + 1
            
        #check if last elem + 1 is out of range
        NextIndexAfterLast = self.MemAllocFrameList[len(self.MemAllocFrameList)-1] + 1

        if NextIndexAfterLast > (MAXPMSIZE - 1):
            raise "Error No More Free Frames in PM"
        
        return NextIndexAfterLast
    
    def _copyDisktoPM(self,adiskInd: int, aFreePMInd):
        StartingPMaddr = aFreePMInd * PAGESIZE

        DiskPageBlock = self.Disk[adiskInd]

        for aindex in range(PAGESIZE):
            self.PM[StartingPMaddr + aindex] = DiskPageBlock[aindex]

    
    def VAtoPA(self,aVA: int) -> int:
        TheSPWtup = self._calcSPW(aVA)

        print(f"SPW {TheSPWtup}")

        #Error check if pw >= PM[2s]
        SegSize = self.PM[2*TheSPWtup.s]

        if SegSize is None or TheSPWtup.pw >= SegSize:
            raise "Error VA outside of seg boundary"
        
        #get pt Frame num
        PTFrameNum = self.PM[2*TheSPWtup.s + 1]

        #check for none
        if PTFrameNum is None:
            raise "PTFrameNum Is None DNE"

        #check if PTFnum is negative
        if PTFrameNum < 0:
            print("PT is non resident")

            AfreeFrameNumforPT = self._findnextFree()
            print(f"The freeframe for pt {AfreeFrameNumforPT}")

            self._copyDisktoPM(abs(PTFrameNum),AfreeFrameNumforPT)

            #update list of FF
            self._appendmemFlistSort(AfreeFrameNumforPT)

            #update list of allocated disk blocks
            self.DiskAllocatedList.remove(abs(PTFrameNum))

            #update st entry
            self.PM[2*TheSPWtup.s + 1] = AfreeFrameNumforPT
            PTFrameNum = AfreeFrameNumforPT



        #get Page Frame Num
        PageFrameNum = self.PM[PTFrameNum * PAGESIZE + TheSPWtup.p]

        #check None case
        if PageFrameNum is None:
            raise "ERROR: PageFrameNum is None DNE"

        #check if Page Frame Num is negative

        if PageFrameNum < 0:
            print("Page is not resident")

            AfreeFNumforPage = self._findnextFree()
            print(f"The freeframe for page {AfreeFNumforPage}")

            #update list of FF
            self._appendmemFlistSort(AfreeFNumforPage)

            #update list of allocated disk blocks
            self.DiskAllocatedList.remove(abs(PageFrameNum))

            #update pt entry
            self.PM[PTFrameNum * PAGESIZE + TheSPWtup.p] = AfreeFNumforPage
            PageFrameNum = AfreeFNumforPage




        #get PA address
        PAaddress = PageFrameNum * PAGESIZE + TheSPWtup.w

        return PAaddress








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
            TheretStr += f"Disk[{aindex}]={self.Disk[aindex][0:5]}\n"



        return TheretStr

