from matplotlib import pyplot
import matplotlib.pyplot as plt

import os
import sys

LINE_CHART_COLOR_LIST = [
    'red',
    'green',
    'brown',
    'blue',
    'teal',
    'gray',
    'orange',
]


class QuickViewLineChart:
    def __init__(self, logFilePath, keywordList):

        self.logFilePath = logFilePath
        self.keywordList = keywordList
        '''
            {
                "STATE::" : [5905.602:'<== EX == CLEANING', 5905.603: '== EN ==> DOCKING', ...],
                "VmRSS:"  : [7474.221:392068, 7684.341:425940, ...],
                ...
            }
        '''
        self.keywordCoordinateDict = {}
        for keyword in self.keywordList:
            self.keywordCoordinateDict[keyword] = {}

    '''
    @func:      通过关键词列表解析log文件
    @param:     无
    @return:    无
    '''

    def parseLogByKeywordList(self):

        f = open(self.logFilePath, "r", encoding="utf-8")
        for line in f.readlines():
            for keyword in self.keywordList:
                try:
                    if keyword in line:
                        line = line.strip('\n')
                        lineList = line.split()
                        if "STATE::" == keyword:
                            self.keywordCoordinateDict[keyword][lineList[
                                5]] = lineList[10] + ' ' + lineList[12]
                        elif ("VmRSS:" == keyword) or ("memfree:" == keyword):
                            for data in lineList:
                                if keyword in data:
                                    self.keywordCoordinateDict[keyword][
                                        lineList[5]] = float(
                                            data[len(keyword):]) / 1024
                        elif "nLMs:" == keyword:
                            self.keywordCoordinateDict[keyword][lineList[
                                5]] = lineList[lineList.index(keyword) + 1]
                    else:
                        pass
                except:
                    pass
            else:
                pass
        else:
            pass

        for keyword in self.keywordList:
            for item in self.keywordCoordinateDict[keyword].items():
                print(item)

    '''
    @func:      根据keywordCoordinateDict进行绘图
    @param:     无
    @return:    无
    '''

    def drawLineChart(self):

        for index in range(len(self.keywordList)):
            keyList = list(
                self.keywordCoordinateDict[self.keywordList[index]].keys())
            valueList = list(
                self.keywordCoordinateDict[self.keywordList[index]].values())

            plt.plot(
                keyList,
                valueList,
                marker='o',
                mec=LINE_CHART_COLOR_LIST[index],
                mfc='w',
                label=self.keywordList[index])

            plt.text(
                -4, 3,
                r'$This\ is\ the\ some\ text.\ \mu_j\ \sigma_i\ \alpha_t$')

        plt.legend()  # 让图例生效

        plt.margins(0)
        plt.subplots_adjust(bottom=0.10)
        plt.xlabel('run time: s')
        plt.ylabel("mem: MB")
        plt.title("Memory trend")
        plt.show()
        plt.savefig('D:\\f1.jpg', dpi=900)


t1 = QuickViewLineChart("log.log", ["VmRSS:", "memfree:"])
# t1 = QuickViewLineChart("log.log", ["memfree:"])
t1.parseLogByKeywordList()
t1.drawLineChart()
