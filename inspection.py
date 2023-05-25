# The Hamming distance between two strings is not an adequate
# measure of "typo distance"
# For instance, Score and scores are potentially mutual typos,
# but talk and also are very unlikely to be mistyped as each other.
# However, the edit distance between talk and also is 2, and
# the edit distance between Score and scores is also 2.
# So in order to report very similar names as warnings, some
# other criterion is needed.

# A token is likely to be a mispelled version of some other if
# it has a low frequency, and shares a large common subsequence
# with a frequent token

# Since reliable cutoffs are hard to obtain, we'll just report
# any pair of tokens whose length is greater than 4 and whose
# lowercase versions share a very large common subsequence,
# but do not differ much in length (say, 3 characters)

# This is overly conservative (e.g. prefetch and fetch, or locate and
# location), but additional constraints are not likely to be exhaustive
# or helpful

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
