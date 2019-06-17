import csv

letter_to_sound = {
    'A': [ 'AE' ],
    'E': [ 'EH1' ],
    'F': [ 'F' ],
    'I': [ 'IH' ],
    'L': [ 'L' ],
    'M': [ 'M' ],
    'N': [ 'N' ],
    'O': [ 'AO', 'AA' ],
    'R': [ 'R' ],
    'S': [ 'S' ],
    'U': [ 'AH' ],
    'V': [ 'V' ],
    'W': [ 'W' ],
    'Z': [ 'Z' ],

    # Non-continuant letters.
    #'B': [ 'B' ],
    #'D': [ 'D' ],
    #'G': [ 'G' ],
    #'H': [ 'HH' ],
    #'J': [ 'JH' ],
    #'K': [ 'K' ],
    #'P': [ 'P' ],
    #'T': [ 'T' ],
}

words_found = {}

with open('dataset.csv', encoding = "ISO-8859-1") as in_file:
    with open('out.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        for sounds in csv.reader(in_file):
            word = sounds.pop(0)

            try:
                index = word.index('(')
                word = word[:index]
            except:
                pass

            # Each letter has a sound.
            if len(word) == len(sounds):

                # Each |letter| of |word| must be in |letter_to_sound| AND
                # each |letter|'s sound must be in the list of sounds in |letter_to_sound|.
                # Note: Some sounds have variants. Ex: Letter 'A' has variant's AE0, AE1, and AE2. However, we treat those variants as the same sound.
                if all([
                    (letter in letter_to_sound) and any([
                        sounds[index].startswith(letter_sound) for letter_sound in letter_to_sound[letter]
                    ])
                    for index, letter in enumerate(word)
                ]):
                    if word not in words_found:
                        words_found[word] = True
                        writer.writerow([ word, len(word) ])


