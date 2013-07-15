from permutator import Permutator


def main():
    #lPermutator = Permutator(5, 'abcdefghijklmnopqrstuvwxyz_')
    lPermutator = Permutator(3, 'abcdefghij')
    for lCombination in lPermutator.getIter(0, 52):
        print(lCombination)
    for lCombination in lPermutator.getIter(12, 52):
        print(lCombination)

if __name__ == "__main__":
    main()
