import csv
import sys


def main(argv):
    #Check for command-line usage
    if len(argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        return
    #open up the files and set them both to read mode
    databaseFile = open(argv[1],'r')
    sequenceFile = open(argv[2],'r')
    #read the database file as a dictionary
    database = csv.DictReader(databaseFile)
    #get the field names from the dictionary to use as keys
    keys = database.fieldnames
    #read the sequnce stored in the DNA sequence file
    sequence = csv.reader(sequenceFile)
    for i in sequence:
        dnaSequence = i
    #create a dictionary to store how many times each sequence was fonud
    matches = {}
    #check all of the dna seqs to see the greatest amonut of times that they appear in the sequence inputted
    for cseq in keys[1:len(keys)]:
        value = longest_match(dnaSequence[0],cseq)
        matches[cseq] = value

    counter = 0
    #iterate through the entire database searching for a match
    for person in database:
        #check to see of the person matches the matches
        for seq in keys[1:len(keys)]:
            #if seq amount matches then check the next seq to see if it mactches
            if int(person[seq]) == matches[seq]:
                counter += 1
            #if there is a seq amount that is different then check the next person
            else:
                break
        #if all the seqs are eqaul to each other then print their name
        if counter == len(matches):
            print(person["name"])
            return
        else:
            counter = 0
    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main(sys.argv)
