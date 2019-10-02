from random import shuffle
from math import inf

def two_card_difference(card1, card2):
    differences = set()
    for index, character1 in enumerate(card1):
        character2 = card2[index]
        if character1 != character2:
            differences.add(character1 + character2)
    return len(differences)

def find_least_changes(unused, deck=[], deck_cost=0, least_changes=inf, good_enough=None):
    if good_enough is None:
        good_enough = len(unused) - 1

    found_good_enough = False

    if len(unused):
        for card in unused:
            tmp_deck_cost = deck_cost
            if len(deck):
                tmp_deck_cost += two_card_difference(deck[-1], card)

            if tmp_deck_cost <= least_changes:
                deck.append(card)
                tmp_unused = unused.copy()
                tmp_unused.remove(card)
                (least_changes, found_good_enough) = find_least_changes(tmp_unused, deck, tmp_deck_cost, least_changes, good_enough)
                del deck[-1] # remove last one

                if found_good_enough:
                    return (least_changes, found_good_enough)
    elif deck_cost < least_changes:
        least_changes = deck_cost
        print('%d: %s' % (least_changes, deck))
        if least_changes <= good_enough:
            found_good_enough = True
    return (least_changes, found_good_enough)

most_changes = 0
def find_most_changes(unused, deck=[], deck_max_cost=inf, max_pair_cost=inf):
    global most_changes

    if max_pair_cost == inf:
        max_pair_cost = len(unused[0])

    if deck_max_cost == inf:
        deck_max_cost = (len(unused) - 1) * max_pair_cost

    if len(unused):
        for card in unused:
            tmp_deck_max_cost = deck_max_cost
            if len(deck):
                tmp_deck_max_cost -= (max_pair_cost - two_card_difference(deck[-1], card))

            if tmp_deck_max_cost >= most_changes:
                deck.append(card)
                tmp_unused = unused.copy()
                tmp_unused.remove(card)
                find_most_changes(tmp_unused, deck, tmp_deck_max_cost, max_pair_cost)
                del deck[-1] # remove last one
    elif deck_max_cost > most_changes:
        most_changes = deck_max_cost
        print('%d: %s' % (deck_max_cost, deck))

cards = [ 'MOM', 'NON', 'NUN', 'SUN', 'RUN', 'RUS', 'RON', 'RAN', 'MAN', 'RAM', 'RUM', 'SUM', 'SAM', 'SAL' ]

print('Finding least changes (%d min)' % (len(cards) - 1))
find_least_changes(cards, good_enough=len(cards))
print()
print('-----------------')
print()
print('Finding most changes')
find_most_changes(cards)