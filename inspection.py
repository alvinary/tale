# The edit distance between talk and also is 2.
# The edit distance between Score and scores is also 2.
# We'll use common subsequences between normalized strings as a criterion for similarity.

# Then we'll randomly replace parts of the string with 'aaa's, and compare the histograms with
# cosine similarity or something

# Suppose common(s1, s2) = c
# - distance from s1 to c, and distance from s2 to c

# Replacing random characters with 'a's (or deleting characters)
# in both strings may increase the length and number of common
# substrings and the size/shape of the longest common subsequence.
# Replacements and deletiions don't change anything only if edits
# are coindexed.
# If both strings are equal, the number of common substrings increases
# and the size of the longest common subsequence drops.
# Seems fun but pointless.

# Maybe just using the set of common substrings (which is bounded
# by n**2, since any common substring is a substring of both
# strings, and there are as many indices as string index pairs i, j,
# with i < j and j < len(s), and can be computed in at least O(n**3) -
# just pick the shortest string, and for each substring do linear search
# in the ooother string, to see if you find it. A cheap trick like
# 'only look for indices starting with the same character' maybe can
# improve practical performance but is not necessary for comparing tokens.

# And then you just use ''some'' distance between two sets of strings

# This also seems pointless, but less ill-defined


def commonSubsequence(first, second):

    if not first or not second:

        return ''

    if first[0] == second[0]:

        char = first[0]
        first = first[1:]
        second = second[1:]

        return char + commonSubsequence(first, second)

    else:

        poppedFirst = first[1:]
        poppedSecond = second[1:]

        popFirst = commonSubsequence(poppedFirst, second)
        popSecond = commonSubsequence(first, poppedSecond)

        if len(popFirst) < len(popSecond):
            return popSecond
        else:
            return popFirst


def testCommon():
    print(commonSubsequence('AGGTAB', 'GXTXAYB'))
    print(commonSubsequence('AGXGTAB', 'GXTXAYB'))
    print(commonSubsequence('AGXGTABY', 'GXTXAYB'))
    print(commonSubsequence('AGXGTAYB', 'GXTXAYB'))
    print(commonSubsequence('Score'.lower(), 'scores'.lower()))
    print(commonSubsequence('talk'.lower(), 'also'.lower()))
    print(commonSubsequence('talk'.lower(), 'also'.lower()))
