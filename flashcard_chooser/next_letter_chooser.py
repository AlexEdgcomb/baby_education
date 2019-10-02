already_letters = [
    'A',
    'M',
    'N',
    'O',
    'R',
    'S',
    'U',
    'L',
]
letters = [
    'A',
    'B',
    'C',
    'D',
    'E',
    'F',
    'G',
    'H',
    'I',
    'J',
    'K',
    'L',
    'M',
    'N',
    'O',
    'P',
    'Q',
    'R',
    'S',
    'T',
    'U',
    'V',
    'W',
    'X',
    'Y',
    'Z',
]
words = [
    'AL',
    'AM',
    'AN',
    'IF',
    'IN',
    'ON',
    'US',
    'ALF',
    'ELF',
    'ELM',
    'FAN',
    'FEZ',
    'FIN',
    'FUN',
    'LIN',
    'LIZ',
    'MAN',
    'MEN',
    'MOM',
    'NON',
    'NUN',
    'RAM',
    'RAN',
    'REV',
    'RIM',
    'RON',
    'RUM',
    'RUN',
    'RUS',
    'SAL',
    'SAM',
    'SIN',
    'SUM',
    'SUN',
    'VAL',
    'VAN',
    'WIN',
    'WON',
    'ZEN',
    'FILM',
    'FLAN',
    'FLIM',
    'FRAN',
    'FROM',
    'SELF',
    'SLAM',
    'SLIM',
    'SLUM',
    'SWAM',
    'SWIM',
    'SWUM',
    'ALVIN',
    'ELSON',
    'ELVIS',
    'FRANZ',
    'LEMON',
    'MELON',
    'SELFS',
    'VENOM',
    'ELISON',
    'NELSON',
    'RANSOM',
    'SINFUL',
    'WILSON',
    'SOLOMON',
    'FLIMFLAM',
]

not_yet_letters = [ letter for letter in letters if letter not in already_letters ]
not_yet_words = [ word for word in words if any([ letter for letter in not_yet_letters if letter in word ]) ]

for new_letter in not_yet_letters:
    maybe_letters = already_letters.copy() + [ new_letter ]

    maybe_words = [ word for word in not_yet_words if all([ letter in maybe_letters for letter in word ]) ]
    count = len(maybe_words)
    if count > 0:
        print('%s had %d matches: %s' % (new_letter, count, ', '.join(maybe_words)))
