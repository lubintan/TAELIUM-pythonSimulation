import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import sys

def initialize(dir = None):
    plt.autoscale(enable=True, axis='x', tight=True)

    # dir = '2017_11_10_14_53_17'
    global csvFilePath
    csvFilePath = 'logs//' + dir + '.csv'
    global path_full
    path_full = 'images//' + dir + '//graphs'
    # path_50 = 'images//'+dir+'//last50day_graphs'


    if not os.path.exists(path_full):
        os.makedirs(path_full)

    # if not os.path.exists(path_50):
    #     os.makedirs(path_50)
    #
    #
    #                 dayCounter,
    #                 yesterdayVolume,
    #             dailyVolume,
    #             deltaT,
    #             supplyCurrent,
    #             supplyCap,
    #         supplyCap - supplyCurrent,
    #         g,
    #         rYear,
    #         rDay,
    #     averageRewardPerBlock,
    #     f_deltaT,
    #
    #
    # totalRewardsGivenOut,
    # len(userList),
    # totalTxFees,
    # dailyInterestPaidOut


    global Day
    global YesterdayVolume
    global DailyVolume
    global deltaT
    global SupplyCurrent
    global SupplyCap
    global Spread
    global g
    global rDay
    global rYear
    global averageBlockReward
    global f_deltaT
    global dailyRewardGivenOut
    global noOfUsers

    global totalTxFees
    global dailyInterestPaidOut

    global START_DAY
    global END_DAY

    global header

    Day=[]
    YesterdayVolume=[]
    DailyVolume=[]
    deltaT=[]
    SupplyCurrent=[]
    SupplyCap=[]
    Spread=[]
    g=[]
    rDay=[]
    rYear=[]
    averageBlockReward=[]
    f_deltaT=[]
    dailyRewardGivenOut=[]
    noOfUsers=[]

    totalTxFees=[]
    dailyInterestPaidOut =[]

    START_DAY = 0
    END_DAY = 808

    header = []

def reader(file):
    global Day, YesterdayVolume, DailyVolume, SupplyCurrent, SupplyCap, rDay, rYear, g, deltaT, f_deltaT, dailyInterestPaidOut
    global averageBlockReward, averageActiveUsers, dailyRewardGivenOut, noOfUsers,totalTxFees, header, Spread

    with open(file, 'rb') as f:
        reader = csv.reader(f, delimiter=',')

        counter = 0

        for row in reader:

            # print counter
            counter += 1

            if counter == 1: continue  #Initialization parameters info
            elif counter == 2:
                header = row #headers
                # print header
            else:
                Day.append(row[0])
                YesterdayVolume.append(row[1])
                DailyVolume.append(row[2])
                deltaT.append(row[3])
                SupplyCurrent.append(row[4])
                SupplyCap.append(row[5])
                Spread.append(row[6])
                g.append(row[7])
                rYear.append(row[8])
                rDay.append(row[9])
                averageBlockReward.append(row[10])
                f_deltaT.append(row[11])
                dailyRewardGivenOut.append(row[12])
                noOfUsers.append(row[13])
                totalTxFees.append(row[14])
                dailyInterestPaidOut.append(row[15])
#
#                 dayCounter,
#                 yesterdayVolume,
#             dailyVolume,
#             deltaT,
#             supplyCurrent,
#             supplyCap,
#         supplyCap - supplyCurrent,
#         g,
#         rYear,
#         rDay,
#     averageRewardPerBlock,
#     f_deltaT,
#
#
# totalRewardsGivenOut,
# len(userList),
# totalTxFees,
# dailyInterestPaidOut



def plot4(data1, data1Name, data2, data2Name, data3, data3Name, data4, data4Name, path):
    fig = plt.figure()



    ax1 = fig.add_subplot(221)
    ax1.plot(Day[START_DAY:END_DAY], data1, 'b-')
    ax1.set_xlabel('Day')
    ax1.set_ylabel(data1Name)


    ax2 = fig.add_subplot(222)
    ax2.plot(Day[START_DAY:END_DAY], data2, 'b-')
    ax2.set_xlabel('Day')
    ax2.set_ylabel(data2Name)

    ax3 = fig.add_subplot(223)
    ax3.plot(Day[START_DAY:END_DAY], data3, 'b-')
    ax3.set_xlabel('Day')
    ax3.set_ylabel(data3Name)

    ax4 = fig.add_subplot(224)
    ax4.plot(Day[START_DAY:END_DAY], data4, 'b-')
    ax4.set_xlabel('Day')
    ax4.set_ylabel(data4Name)

    fig.savefig(path + '//' + data1Name.replace('/','').replace('.','').strip() + '_'+ data2Name.replace('/','').replace('.','').strip()
                + '_'+  data3Name.replace('/','').replace('.','').strip()  + '_'+  data4Name.replace('/','').replace('.','').strip()  + '.png')

def plot1(data, dataName, path):
    plt.autoscale(enable=True, axis='x', tight=True)

    fig = plt.figure()

    ax1 = fig.add_subplot(111)
    ax1.grid(True)

    ax1.plot(Day[START_DAY:END_DAY], data)
    ax1.set_xlabel('Day')
    ax1.set_ylabel(dataName)

    fig.savefig(path + '//' + dataName.replace('/','').replace('.','').strip() + '.png',bbox_inches='tight', pad_inches=0)


def runPlotter4(dir):
    global Day, YesterdayVolume, DailyVolume, SupplyCurrent, SupplyCap, rDay, rYear, g, deltaT, f_deltaT, dailyInterestPaidOut
    global averageBlockReward, averageActiveUsers, dailyRewardGivenOut, noOfUsers, totalTxFees, header, Spread

    sys.stdout.write("\rPlotting Data..")


    initialize(dir)
    reader(csvFilePath)

    plot1(YesterdayVolume[START_DAY:END_DAY], header[1], path_full)
    plot1(DailyVolume[START_DAY:END_DAY], header[2], path_full)
    plot1(deltaT[START_DAY:END_DAY], header[3], path_full)
    plot1(SupplyCurrent[START_DAY:END_DAY], header[4], path_full)

    plot1(SupplyCap[START_DAY:END_DAY], header[5], path_full)
    plot1(Spread[START_DAY:END_DAY], header[6], path_full)
    plot1(g[START_DAY:END_DAY], header[7], path_full)

    plot1(rYear[START_DAY:END_DAY], header[8], path_full)
    plot1(rDay[START_DAY:END_DAY], header[9], path_full)
    plot1(averageBlockReward[START_DAY:END_DAY], header[10], path_full)
    plot1(f_deltaT[START_DAY:END_DAY], header[11], path_full)
    plot1(dailyRewardGivenOut[START_DAY:END_DAY], header[12], path_full)
    plot1(noOfUsers[START_DAY:END_DAY], header[13], path_full)
    plot1(totalTxFees[START_DAY:END_DAY], header[14], path_full)
    plot1(dailyInterestPaidOut[START_DAY:END_DAY], header[15], path_full)

    sys.stdout.flush()
    print "Graphs found here:" + path_full


if __name__ == '__main__':


    runPlotter4(raw_input("enter csv file name without extension"))

    #
    #     dayCounter,
    #     yesterdayVolume,
    # dailyVolume,
    # yesterdayVolume - dailyVolume,
    # dailyVolume / yesterdayVolume,
    # supplyCurrent,
    # supplyCap,
    # supplyCap - supplyCurrent,
    # g,
    # rYear,
    # rDay,
    # averageRewardPerBlock,
    # averageActiveUsers,
    # totalRewardsGivenOut,
    # len(userList),
    # totalTxFees