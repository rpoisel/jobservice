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

    def getMin(self):
        return 0

    def getMax(self):
        return len(self.__mRange)**self.__mNumChars - 1


def main():
    lPermutator = Permutator(6, 'abcdefghijklmnopqrstuvwxyz_')
    print("Min: " + str(lPermutator.getMin()))
    print("Max: " + str(lPermutator.getMax()))
    print("Offset Min: " + str(lPermutator.get(lPermutator.getMin())))
    print("Offset Middle: " + str(lPermutator.get(lPermutator.getMax() / 2)))
    print("Offset Max: " + str(lPermutator.get(lPermutator.getMax())))

if __name__ == "__main__":
    main()
