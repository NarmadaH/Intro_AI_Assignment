
from optparse import OptionParser
import sys
import copy
import random

class chessBoard:
  
    def __init__(self):

        # print ("=======Start ChessBoard=======")

        self.chessBoard = [[0 for i in range(0,8)] for j in range(0,8)]

        for i in range(0,8):
            while True:
                rowRandom = random.randint(0,7)
                colRandom = random.randint(0,7)

                if self.chessBoard[rowRandom][colRandom] == 0:
                    self.chessBoard[rowRandom][colRandom] = "1"
                    break

                
    def __repr__(self):
        mstr = ""
        for i in range(0,8):
            for j in range(0,8):
                mstr = mstr + str(self.chessBoard[i][j]) + " "
            mstr = mstr + "\n"
        return (mstr)


class queen:
    def __init__(self, runCount, printing, move):
        self.totRuns = runCount
        self.totSuccusful = 0
        self.totSteps = 0
        self.totStepsSuccusful = 0
        self.totStepsFail = 0
        self.printing = printing
        self.isSucsses = False
        self.move = move

        # print ("=======Start Queen=======")

        for i in range(0, self.totRuns):

            # print ("=======Start Runs=======")
            if self.printing == True: 
                print ("====================")
                print ("BOARD",i)
                print ("====================")

            self.isSucsses = False
            self.hostBoard = chessBoard()
            self.cost = self.calHeuristicVal(self.hostBoard)
            climbStepCount = self.hillClimbingSearch(move)

            if self.isSucsses == True:
                self.totStepsSuccusful +=climbStepCount
            else:
                self.totStepsFail +=climbStepCount



    def calHeuristicVal(self, myBoard):

        # print ("=======Start calHeuristicVal=======")
        # print(myBoard)
    
        totRowColCost = 0
        totDiagCost = 0
        totBoardCost = 0

        for i in range(0,8):
            for j in range(0,8):
                
                if myBoard.chessBoard[i][j] == "1":

                    totRowColCost -= 2

                    #Row violations
                    for n in range(0,8):
                        if myBoard.chessBoard[i][n] == "1":
                            totRowColCost += 1

                    #Coloum violations
                    for n in range(0,8):
                        if myBoard.chessBoard[n][j] == "1":
                            totRowColCost += 1


                    #Diagonal Violations
                    n, m = i+1, j+1
                    while n < 8 and m < 8:
                        if myBoard.chessBoard[n][m] == "1":
                            totDiagCost += 1
                        n +=1
                        m +=1

                    n, m = i-1, j-1
                    while n >= 0 and m >= 0:
                        if myBoard.chessBoard[n][m] == "1":
                            totDiagCost += 1
                        n -=1
                        m -=1

                    n, m = i+1, j-1
                    while n < 8 and m >= 0:
                        if myBoard.chessBoard[n][m] == "1":
                            totDiagCost += 1
                        n +=1
                        m -=1

                    n, m = i-1, j+1
                    while n >= 0 and m < 8:
                        if myBoard.chessBoard[n][m] == "1":
                            totDiagCost += 1
                        n -=1
                        m +=1


        totBoardCost = (totRowColCost + totDiagCost)/2
        # print ("Board Tot Cost", totBoardCost)
        return totBoardCost


    # Generate Board when dioganal moves are allowed
    def generateBestBoardWithDioganal(self):

        # print ("=======Start generateBestBoardWithDioganal=======")
        # print ("Self chess", self.hostBoard.chessBoard)

        childBoard = self.hostBoard  
        childBoard = [[0 for i in range(0,8)] for j in range(0,8)]    
        currentLow = self.calHeuristicVal(self.hostBoard)

        # print ("Self current low", currentLow)
        sameCostChildren = []

        for row in range(0,8):
            for col in range(0,8):
                if self.hostBoard.chessBoard[row][col] == "1":
                    # print ("Self chess", self.hostBoard.chessBoard)
                    
                    for tem_row in range(0,8):
                        for tem_col in range(0,8):
                            if self.hostBoard.chessBoard[tem_row][tem_col] != "1":
                                tempChessBoard = copy.deepcopy(self.hostBoard)
                                tempChessBoard.chessBoard[row][col] = 0
                                tempChessBoard.chessBoard[tem_row][tem_col] = "1"

                                # print ("Temp chess", tempChessBoard.chessBoard)

                                tempLow = self.calHeuristicVal(tempChessBoard)

                                # print ("Temp chess", tempChessBoard.chessBoard)

                                if (tempChessBoard != self.hostBoard):
                                    if (tempLow < currentLow):
                                        childBoard = copy.deepcopy(tempChessBoard)
                                        currentLow = tempLow
                                    
                                    elif (tempLow == currentLow):
                                        sameCostChildren.append(tempChessBoard)
                                        x = random.randint(0, len(sameCostChildren) - 1)
                                        childBoard = sameCostChildren[x]

                                        # print ("sameCostChildren", sameCostChildren)
                                        # print ("Temp childBoard", childBoard)
                               
                        
        self.hostBoard = childBoard
        self.cost = currentLow        



    # Generate Board when dioganal moves are not allowed
    def generateBestBoardWithoutDioganal(self):

        tempLow = self.calHeuristicVal(self.hostBoard)
        lowestCostBoard = self.hostBoard        

        for row in range(0,8):
            for col in range(0,8):
                if self.hostBoard.chessBoard[row][col] == "1":
                    
                    for tem_row in range(0,8):
                        for tem_col in range(0,8):
                            if self.hostBoard.chessBoard[tem_row][tem_col] != "1":
                               
                                temChessBoard = copy.deepcopy(self.hostBoard)
                                temChessBoard.chessBoard[row][col] = 0
                                temChessBoard.chessBoard[tem_row][tem_col] = "1"

                                temBoardCost = self.calHeuristicVal(temChessBoard)

                                if temBoardCost < tempLow:
                                    tempLow = temBoardCost
                                    lowestCostBoard = temChessBoard
                        
        self.hostBoard = lowestCostBoard
        self.cost = tempLow  


    def hillClimbingSearch(self, move):

        # print ("=======Start hillClimbingSearch=======")
        climbStepCount = 0

        while 1:
            boardVioalation = self.cost

            if (move == 1):
                self.generateBestBoardWithoutDioganal()
            elif (move == 2):   
                self.generateBestBoardWithDioganal()
            
            if boardVioalation == self.cost:
                break
            self.totSteps += 1
            climbStepCount += 1

            if self.printing == True:
                print ("Board Violations", self.calHeuristicVal(self.hostBoard))
                print (self.hostBoard)
            
            if self.cost != 0:
                if self.printing == True:
                    print ("No Solution found")
            else:
                if self.printing == True:
                    print ("Solution found")
                self.totSuccusful += 1
                self.isSucsses = True
                
        
        return climbStepCount
    
    def printstatistics(self):
        print ("Total Runs: ", self.totRuns)
        print ("Total Success: ", self.totSuccusful)
        print ("Total Fail: ", (self.totRuns - self.totSuccusful))
        print ("Success Percentage: ", float(self.totSuccusful)/float(self.totRuns)*100)
        print ("Average number of steps: ", float(self.totSteps)/float(self.totRuns))

        if self.totSuccusful != 0:
            print("Average steps when success: ", float(self.totStepsSuccusful)/float(self.totSuccusful))
        if (self.totRuns - self.totSuccusful) != 0:    
            print("Average steps when failure: ", float(self.totStepsFail)/float(self.totRuns - self.totSuccusful))             


if __name__ == "__main__":
 
    mboard = queen(1000, False, 1)

    print ("8 Queens Problem - Hill Climbing")
    mboard.printstatistics()