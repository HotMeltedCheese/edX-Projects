from cs50 import get_string


def main():
    #ask the user for the text they want to rate
    text = get_string("Text: ")
    letters = letter_count(text)
    words = word_count(text)
    sentences = sentence_count(text)
    index = (int)((0.0588 * (letters/words * 100) - 0.296 * (sentences/words * 100) - 15.8) + 0.5)
    if index < 1:
        print("Before Grade 1")
    elif index > 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


def letter_count(text):
    strlen = len(text)
    letter_counter = 0
    for i in range(strlen):
        if(text[i:i+1].isalpha()):
            letter_counter += 1
    return(letter_counter)


def word_count(text):
    strlen = len(text)
    word_counter = 0
    for i in range(strlen):
        if(text[i:i+1] == ' '):
            word_counter += 1
    word_counter += 1
    return word_counter


def sentence_count(text):
    strlen = len(text)
    sentence_counter = 0
    for i in range(strlen):
        if text[i:i+1] in [".", "?", "!"]:
            sentence_counter += 1
    return(sentence_counter)


main()