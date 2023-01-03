
# The edit distance between talk and also is 2.
# The edit distance between Score and scores is also 2.
# We'll use common subsequences between normalized strings as a criterion for similarity.

# Then we'll randomly replace parts of the string with 'aaa's, and compare the histograms with
# cosine similarity or something

# Suppose common(s1, s2) = c
# - distance from s1 to c, and distance from s2 to c


# Replacing with 'a's increases the length of the common subsequence
# Leaves it the same (if the strings are equal)
# reduces it 

# replacing with 'a's and 'b's

# set of common substrings (bounded by n**2)
# Distance between two sparse arrays

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
