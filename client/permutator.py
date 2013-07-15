class PermutatorIterator:

    def __init__(self, pPermutator, pOffsetStart, pOffsetEnd):
        self.__mPermutator = pPermutator
        self.__mOffsetCur = pOffsetStart
        self.__mOffsetEnd = pOffsetEnd

    def __iter__(self):
        return self

    def next(self):
        if self.__mOffsetCur == self.__mOffsetEnd:
            raise StopIteration
        else:
            lCurrent = self.__mPermutator.get(self.__mOffsetCur)
            self.__mOffsetCur += 1
            return lCurrent


class Permutator:

    def __init__(self, pNumChars, pRange):
        self.__mNumChars = pNumChars
        self.__mRange = pRange

    def get(self, pOffset):
        lPass = ''
        lOffset = pOffset
        lCnt = self.__mNumChars - 1
        while lCnt >= 0:
            lPass += self.__mRange[lOffset / len(self.__mRange)**lCnt]
            lOffset %= len(self.__mRange)**lCnt
            lCnt -= 1

        return lPass

    def getNumPerms(self):
        return len(self.__mRange)**self.__mNumChars

    def getIter(self, pRangeId, pNumRanges):
        if pRangeId + 1 > pNumRanges:
            raise ValueError
        else:
            lNumExtendedRanges = self.getNumPerms() % pNumRanges
            lNumPermsPerRange = self.getNumPerms() // pNumRanges
            lOffsetStart = (lNumPermsPerRange + 1) * \
                (
                    pRangeId
                    if pRangeId < lNumExtendedRanges
                    else lNumExtendedRanges
                ) + \
                lNumPermsPerRange * \
                (
                    pRangeId - lNumExtendedRanges
                    if pRangeId > lNumExtendedRanges
                    else 0
                )
            lOffsetEnd = lOffsetStart + \
                (
                    lNumPermsPerRange + 1
                    if pRangeId < lNumExtendedRanges
                    else lNumPermsPerRange
                )
            return PermutatorIterator(
                self,
                lOffsetStart,
                lOffsetEnd
            )
