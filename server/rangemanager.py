import time


class RangeManager(object):

    def __init__(self, pNumRanges=100, pTimeout=100, pListeners=[]):
        super(RangeManager, self).__init__()
        self.__mTimeout = pTimeout
        self.__mNumRanges = pNumRanges
        self.__mRanges = []
        self.__mMessage = ''
        self.__mSuccess = False
        self.__mListeners = pListeners
        for lCnt in range(pNumRanges):
            self.__mRanges.append(
                {
                    'completed': False,
                    'startTime': 0,
                    'job': '',
                    'numRanges': self.__mNumRanges,
                    'rangeId': lCnt
                }
            )

    def getRange(self):
        lCnt = 0
        if self.hasSucceeded():
            return {}

        for lRange in self.__mRanges:
            if lRange['completed'] is False and \
                    time.time() - lRange['startTime'] > self.__mTimeout:
                self.__assignRange(lRange, lCnt)
                return lRange
            lCnt += 1

        return {}

    def __assignRange(self, pRange, pRangeId):
        pRange['startTime'] = time.time()
        pRange['rangeId'] = pRangeId
        pRange['job'] = self.defineJob(
            self.__mNumRanges,
            pRangeId
        )

    def report(self, pSuccess, pRangeId, pMessage):
        if pRangeId >= len(self.__mRanges):
            return
        self.__mRanges[pRangeId]['completed'] = True
        if pSuccess:
            self.__mMessage = pMessage
            self.__mSuccess = True
        for lListener in self.__mListeners:
            lListener.updateProgress()

    def getSuccessMessage(self):
        return self.__mMessage

    def getProgress(self):
        lProgress = 0
        if self.__mSuccess:
            lProgress = 100
        else:
            for lRange in self.__mRanges:
                if lRange['completed'] is True:
                    lProgress += 1
        return {
            'value': 100 * lProgress / self.__mNumRanges,
            'success': self.__mSuccess,
            'message': self.__mMessage
        }

    def hasSucceeded(self):
        return self.__mSuccess

    def reset(self):
        self.__init__(self.__mNumRanges, self.__mTimeout, self.__mListeners)
        for lListener in self.__mListeners:
            lListener.reset()

    def addListener(self, pListener):
        self.__mListeners.append(pListener)

    def removeListener(self, pListener):
        self.__mListeners.remove(pListener)

    def defineJob(self, pNumRanges, pRangeId):
        return [pRangeId, pNumRanges]
