
# from hashlib import sha256
# import threading
import sys
import time
# import numpy as np
import csv
# import matplotlib
import math
import datetime
# import gc
import random
import plotter4

now = datetime.datetime.now()
# GLOBALS and Initialization

# random.seed = 51243


# CONSTANTS

NAME = "newR%d_%d_%d_%d_%d_%d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)

FILENAME = "logs//" + NAME + ".csv"
# FILENAME =  NAME + ".csv"

print 'Log File Name:', FILENAME,

DAYS = 150 #number of days to run simulation for
# USER_GROWTH_LIMIT = 3 #per block
USER_LIMIT = 1e9
MAX_DEC_PLACES = 3
NUM_OF_DAILY_BLOCKS = 1440 #1440
TX_LIMIT = 1e3 # Max amount sent per transaction. What would humans do?
TX_FEE = 0.001


STARTING_SUPPLY_CAP = float(25e6)
STARTING_CURRENT_SUPPLY = float(21e6)
STARTING_INTEREST_RATE = 0.05
BUFFER_BETWEEN_SUPCAP_AND_SUPCUR = 0
STARTING_NUM_USERS = 20
WINDOW = 10
R_MAX = 0.2
R_MIN = -0.1

#for reward equation

PI = 3.1415926536
K = (0.5/NUM_OF_DAILY_BLOCKS) * (2.0/PI) #0.1 * (1.0/NUM_OF_DAILY_BLOCKS) * (2.0/math.pi)
H = float(1e6)


#Debug usage.
VERBOSE = False
SHOW_TRANSACTIONS = VERBOSE #whether to print transactions to the screen
SHOW_BALANCE = False
TIMING_DEBUG = False
USER_INPUT = False
transactionsTotalTime = 0
blockTotalTime = 0

#Initialize variables.
dailyMinusYestVolList = []
dayCounter = 0
userList = []
supplyCap = STARTING_SUPPLY_CAP
supplyCurrent = STARTING_CURRENT_SUPPLY
yesterdayVolume = 0
writer = None
rYearYest = STARTING_INTEREST_RATE


print "###########\t\tINITIALIZE\t\t###########"
print "Supply Cap:", supplyCap, 'Current Supply:', supplyCurrent

# def calculateMA(list, windowLength, newElement = None):
#     if (len(list) >= windowLength) and (newElement!=None):
#         list.pop(0)
#
#     if newElement!=None: list.append(newElement)
#
#     return (sum(list))/(float(len(list)))

def randomlyDetermineWinner(reward, txFees):
    global userList, supplyCap,supplyCurrent

    if len(userList) != 0 :
        luckyWinner = random.randint(0, len(userList)-1)
        userList[luckyWinner] += (reward + txFees)
        supplyCap -= reward
        supplyCurrent += reward
        if VERBOSE: print "\nLUCKY WINNER:", luckyWinner, 'won', reward, '.' '\n'



def transact(senderIndex, receiverIndex, amountToSend):

    if userList[senderIndex] >= amountToSend:
        userList[senderIndex] -= (amountToSend + TX_FEE)
        userList[receiverIndex] += amountToSend

def transactions(senderIndex, userList):

    receiverIndex = random.randint(0, len(userList)-1)

    #make sure not sending to own self

    while (senderIndex == receiverIndex): receiverIndex = random.randint(0, len(userList)-1)

    # if senderIndex != receiverIndex:

    if userList[senderIndex] < TX_LIMIT:
        amountToSend = round(random.random() * (userList[senderIndex]-TX_FEE), MAX_DEC_PLACES)
    else:
        amountToSend = random.randint(1, int(TX_LIMIT)-math.ceil(TX_FEE))

    transact(senderIndex,receiverIndex,amountToSend)
    # volume += amountToSend
    if SHOW_TRANSACTIONS: print '{', amountToSend, '}', senderIndex, '====>', receiverIndex, '\t sender balance:', userList[senderIndex]

    return amountToSend





def main():

    start = time.time()

    global supplyCurrent, userList, dayCounter, writer, transactionsTotalTime, blockTotalTime



    #Initialize logger

#     dayCounter,
#     yesterdayVolume,
# dailyVolume,
# deltaT,
# supplyCurrent,
# supplyCap,
# supplyCap - supplyCurrent,
# g,
# rYear,
# rDay,
# averageRewardPerBlock,
# f_deltaT,
# totalRewardsGivenOut,
# len(userList),
# totalTxFees,
# dailyInterestPaidOut
    with open(FILENAME, 'w') as f:
        fieldnames = ['Day', 'Yesterday Tx Value', 'Today Tx Value', 'deltaT',
                      'Supply Current', 'Supply Cap','Spread','g', 'r (yearly)',
                      'r(daily)', 'average reward per block', 'f_deltaT', 'rewards given out per day', 'no. of users',
                      'tx fees paid per day','Total Daily Interest Paid Out']
        # writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer = csv.writer(f)

        initialValueString = 'INITIAL VALUES', 'No. of Blocks Per Day:', NUM_OF_DAILY_BLOCKS, 'User Limit:', USER_LIMIT, "Starting # of users::", STARTING_NUM_USERS\
            # , "Additional Users Per block Capped At:", USER_GROWTH_LIMIT

        initialValues = [initialValueString]

        writer.writerow(initialValues)

        writer.writerow(fieldnames)

    #Initialize userList
    for i in range(STARTING_NUM_USERS):
        if (i>=0) and (i<=3):
            userList.append(supplyCurrent * 0.1) #10% to NXT, 10% each to us.
        else:
            userList.append((supplyCurrent*0.6) / (STARTING_NUM_USERS-4))

    # for each in userList:
        # print each

    if SHOW_BALANCE:
        for i in range(len(userList)):
            # print i, "-- Balance:", round(userList[i], MAX_DEC_PLACES)
            print i, "-- Balance:", userList[i]






    while dayCounter < DAYS:
        if USER_INPUT: raw_input()

        # if TIMING_DEBUG: start = time.time()

        dailyOperations()

        # if TIMING_DEBUG:
        #     dayTotalTime = time.time() - start
        #     print "Time Day", dayCounter," took:", dayTotalTime, 's'
        #     print "Day Operations minus BlockTotalTime:", dayTotalTime - blockTotalTime, 's'


        sys.stdout.write("\rCalculating... %.2f %% complete. Currently on day %i. No. of Users: %i" % (float(dayCounter)*100.0/(DAYS-1), dayCounter, len(userList)))
        sys.stdout.flush()

        dayCounter += 1






    end = time.time()

    print 'Time taken:', end-start, 's'



def dailyOperations():
    global dayCounter, blockTotalTime,transactionsTotalTime, yesterdayVolume, rYearYest
    global userList, supplyCurrent, supplyCap, dailyMinusYestVolList, writer

    supplyTotal = supplyCurrent + supplyCap

    # print '\n\nSum User Balances:', sum(userList), 'S Curr:', supplyCurrent, 'S Cap:', supplyCap

    if VERBOSE:
        print '@@@@@@@@@@@@@@@@@@@@ START DAY #', dayCounter , '@@@@@@@@@@@@@@@@@@@@'
        print 'running at', NUM_OF_DAILY_BLOCKS, 'blocks per day'
        print '***** (Press Enter to continue) *****'


    # if TIMING_DEBUG: blockTotalTime = 0

    ###########         run blocks      ########################
    # totalActiveUsers = 0
    totalRewardsGivenOut = 0
    totalTxFees = 0
    dailyVolume = 0 ######### DOES REWARD NEED TO BE ADDED TO DAILY VOLUME? ###########
    for i in range (NUM_OF_DAILY_BLOCKS):

        # print 'block:', i

        # if TIMING_DEBUG: start = time.time()

        blockVolume, reward, txFees = blockOperations(userList) #supplyCurrent updated in this function

        # if TIMING_DEBUG:
        #     thisBlockTime = time.time() - start
        #     blockTotalTime += thisBlockTime
        #     print "Time Block", i, "took:", thisBlockTime, 's'
        #     print "Block Operations minus TxTotalTime:", thisBlockTime - transactionsTotalTime, 's'
        dailyVolume += blockVolume
        totalRewardsGivenOut += reward
        # totalActiveUsers += activeUsers
        totalTxFees += txFees

    ###########         end daily blocks      ########################

    # print '########\t\trun blocks\t\t########'
    # print 'Sum User Balances:', sum(userList), 'S Curr:', supplyCurrent, 'S Cap:', supplyCap
    # print 'rewards:', totalRewardsGivenOut, 'tx fees:', totalTxFees
    # print 'current circulation + rewards + Scap == Total?', (supplyTotal == (supplyCurrent + supplyCap))
    # print (supplyCurrent + supplyCap)
    # print supplyTotal


    if TIMING_DEBUG: print "Total block time:", blockTotalTime, 's'
    if SHOW_TRANSACTIONS: print "Daily Volume:", dailyVolume


    # calculate rYear and rDay
    # y = (0.15)(2/pi)arctan(x/(.5e7))+.05
    # x = change in transaction value (total amount transacted today - total amount transacted yesterday)
    # Take PI = 3.1415926536 (10 dec places)
#######################################################################################################
#######################   R EQUATION!!!!##############################################################
    deltaT = dailyVolume - yesterdayVolume

    f_deltaT = 0.15 * (2.0/PI) * math.atan(deltaT/(5e8))

    rYear = rYearYest - f_deltaT

    if rYear >= R_MAX: rYear = R_MAX
    elif rYear <= R_MIN: rYear = R_MIN

    rDay = rYear / 365.0
############################################################################################
############################################################################################

    # get MA of today tx value - yesterday tx value.
    if len(dailyMinusYestVolList) >= WINDOW:
        dailyMinusYestVolList.pop(0)
    dailyMinusYestVolList.append(dailyVolume - yesterdayVolume)

    maDailyMinusYestVol = sum(dailyMinusYestVolList) / len(dailyMinusYestVolList)


    # calculate g.


    # g = (rDay*supplyCurrent) + maDailyMinusYestVol

    g = (rDay*supplyCurrent) + deltaT


    ## Calculate new Supply Cap.
    supplyCap = supplyCap + g
    if supplyCap <= (supplyCurrent + BUFFER_BETWEEN_SUPCAP_AND_SUPCUR):
        supplyCap = supplyCurrent + BUFFER_BETWEEN_SUPCAP_AND_SUPCUR


    ## Pay the people interest.

    dailyInterestPaidOut = 0

    if (supplyCurrent * rDay) < (supplyCap - (supplyCurrent + BUFFER_BETWEEN_SUPCAP_AND_SUPCUR) ):

        if VERBOSE:
            print 'total interest paid out:',(supplyCurrent * rDay)
            print 'Scap - Scurr:',(supplyCap - (supplyCurrent + BUFFER_BETWEEN_SUPCAP_AND_SUPCUR) )


        # overallInterest = 0
        # print 'supply curr:', supplyCurrent
        for i in range(len(userList)):
            if userList[i] != 0:
                interest = round(rDay * userList[i], MAX_DEC_PLACES)
                userList[i] += interest
                supplyCap -= interest
                supplyCurrent += interest
                # overallInterest+=interest

                dailyInterestPaidOut += interest

        # if overallInterest<0: print 'interest is negative:', overallInterest, 'supply curr:', supplyCurrent

    averageRewardPerBlock = totalRewardsGivenOut / NUM_OF_DAILY_BLOCKS  # average reward
    # averageActiveUsers = totalActiveUsers / NUM_OF_DAILY_BLOCKS #average active users




    # print supplyTotal, (supplyCurrent + supplyCap - g)



    if VERBOSE:
        print "g:", g, "Supply Cap:", supplyCap

        print "r per Year:", rYear, '\tCurrent Supply:', supplyCurrent, "\tvolume:", dailyVolume
        print 'average reward per block:', averageRewardPerBlock, '\ttotal reward per day:', totalRewardsGivenOut, '\tno. of users:', len(userList)


    #log data

    # dataToWrite = {'Day':dayCounter + 1,
    #                'Price':prices[dayCounter],
    #                'Daily Volume':dailyVolume,
    #                'Supply Current': supplyCurrent,
    #                'Supply Cap':supplyCap,
    #                'MA-Volume': maV,
    #                'interest rate (per day)':rDay,
    #               'vwap1': vwap1,
    #                 'vwap2':vwap2,
    #                 'MA-vwap1/vwap2':maVwap1OverVwap2,
    #                 'average reward':averageRewardPerBlock,
    #                 'total reward given in past day':totalRewardsGivenOut,
    #                     'no. of users':len(userList)}
    dataToWrite = [
                    dayCounter,
                    yesterdayVolume,
                   dailyVolume,
        deltaT,
                   supplyCurrent,
                   supplyCap,
        supplyCap - supplyCurrent,
                   g,
                   rYear,
                    rDay,
                   averageRewardPerBlock,
                    f_deltaT,
                   totalRewardsGivenOut,
                   len(userList),
                    totalTxFees,
                    dailyInterestPaidOut

                    ]

    with open(FILENAME, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(dataToWrite)

    ###Perform calculations for next day's use###
    yesterdayVolume = dailyVolume
    rYearYest = rYear


def blockOperations(userList):
    global supplyCurrent, supplyCap, transactionsTotalTime



    if VERBOSE:
       print '********** Start Block **********'
       print '***** (Press Enter to continue) *****'
    if USER_INPUT: raw_input()


    # Add new users
    # numOfNewUsers = random.randint(0, USER_GROWTH_LIMIT)

    # userGrowthPerBlock = 1e-4

    userGrowthPerBlock = 3
    numOfNewUsers = random.randint(0, math.ceil(userGrowthPerBlock))

    if len(userList) <= USER_LIMIT:
       for each in range(0, numOfNewUsers):
           # newUser = user()
           userList.append(0)



    #run transactions
    blockVolume = 0


    #Make no. of txs proportional to users. Otherwise daily volume will keep going down if number of txs remain constant while
    # money is spread amongst more and more people.

    maxNoOfTxs = int(len(userList)**.5)

    # if maxNoOfTxs > TRANS_LIMIT: maxNoOfTxs = TRANS_LIMIT
    # print 'maxNoOfTxs:' , maxNoOfTxs

    numberOfTransactionsThisBlock = random.randint(0,maxNoOfTxs+1)
    txFees = 0

    # print numberOfTransactionsThisBlock

    transactingUsers = []

    # print numberOfTransactionsThisBlock

    # if TIMING_DEBUG: transactionsTotalTime = 0

    for each in range(0, numberOfTransactionsThisBlock):

       txSenderIndex = random.randint(0, len(userList) - 1)

       # make sure sender has balance more than TX_FEE
       while (userList[txSenderIndex] <= TX_FEE):
           txSenderIndex = random.randint(0, len(userList)-1)

       # if TIMING_DEBUG: start = time.time()

       amountTransactedByThisSender = transactions(txSenderIndex,userList)
       blockVolume += amountTransactedByThisSender
       txFees += TX_FEE

       if not (txSenderIndex in transactingUsers):
           transactingUsers.append(txSenderIndex)

       # if TIMING_DEBUG: transactionsTotalTime += time.time() - start


       # raw_input()
       # print 'amount:', amountTransactedByThisSender, 'blockVolume:', blockVolume

    # if TIMING_DEBUG:print "Transactions took:", transactionsTotalTime, 's'

    if SHOW_TRANSACTIONS:
       print "no.of tx:", numberOfTransactionsThisBlock
       print "block tx volume:", blockVolume



    #winner
    # print 'K * cap - current:', K*(supplyCap-supplyCurrent), '\tactive users:' ,activeUsers, "K:", K

    #active users = people ONLINE in last block
    #use a random number here between transacting users and total users

    # activeUsers = random.randint(len(transactingUsers),len(userList))

    reward = K*math.atan(yesterdayVolume/H)

    randomlyDetermineWinner(reward, txFees)



    if SHOW_BALANCE: print "___Current Balances____"
    if SHOW_BALANCE:
       for i in range(len(userList)):
           # print i, "-- Balance:", round(userList[i], MAX_DEC_PLACES)
           print i, "-- Balance:", userList[i]


    if VERBOSE:
        # print "Current Supply:", currentSupply
       print '********** End Block **********'
       print



    return blockVolume, reward, txFees











if __name__ == '__main__':






    main()

    plotter4.runPlotter4(NAME)





