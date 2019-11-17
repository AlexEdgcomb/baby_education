from random import shuffle
from math import inf, factorial
from progress.bar import Bar

def edit_distance_runner(str1, str2, m, n):
    if m==0:
        return n
    if n==0:
        return m
    if str1[m-1]==str2[n-1]:
        return edit_distance_runner(str1, str2, m - 1, n - 1)
    return 1 + min(
        edit_distance_runner(str1, str2, m, n - 1),
        edit_distance_runner(str1, str2, m - 1, n),
        edit_distance_runner(str1, str2, m - 1, n - 1)
    )

edit_distance_cache = {}
def edit_distance(str1, str2):
    ordered = sorted([ str1, str2 ])
    key = ''.join(ordered)
    if key not in edit_distance_cache:
        edit_distance_cache[key] = edit_distance_runner(str1, str2, len(str1), len(str2))
    return edit_distance_cache[key]

def find_least_changes(unused, deck=[], deck_cost=0, least_changes=inf, good_enough=None):
    global bar

    if good_enough is None:
        good_enough = len(unused) - 1

    found_good_enough = False

    if len(unused):
        for card in unused:
            tmp_deck_cost = deck_cost
            if len(deck):
                tmp_deck_cost += edit_distance(deck[-1], card)

            if tmp_deck_cost <= least_changes:
                deck.append(card)
                tmp_unused = unused.copy()
                tmp_unused.remove(card)
                (least_changes, found_good_enough) = find_least_changes(tmp_unused, deck, tmp_deck_cost, least_changes, good_enough)
                del deck[-1] # remove last one

                if found_good_enough:

                    # Account for all the skipped sub-trees.
                    indexOfCard = unused.index(card)
                    numCardsSkipped = len(unused) - indexOfCard - 1
                    amountSkipped = numCardsSkipped * factorial(len(unused) - 1)
                    bar.next(amountSkipped)

                    return (least_changes, found_good_enough)
            else:

                # Account for skipped sub-tree.
                amountSkipped = factorial(len(unused) - 1)
                bar.next(amountSkipped)
    else:
        bar.next()
        if deck_cost < least_changes:
            least_changes = deck_cost
            print()
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
                tmp_deck_max_cost -= (max_pair_cost - edit_distance(deck[-1], card))

            if tmp_deck_max_cost >= most_changes:
                deck.append(card)
                tmp_unused = unused.copy()
                tmp_unused.remove(card)
                find_most_changes(tmp_unused, deck, tmp_deck_max_cost, max_pair_cost)
                del deck[-1] # remove last one
    elif deck_max_cost > most_changes:
        most_changes = deck_max_cost
        print('%d: %s' % (deck_max_cost, deck))

cards = [ 'BULB', 'SUB', 'NUN', 'BUN', 'BUS', 'ALBUM', 'ELM', 'RAM', 'MOM', 'MAN', 'FAN', 'FLAN', 'MELON', 'LEMON' ]

bar = Bar('Finding least changes (%d min)' % (len(cards) - 1), max=factorial(len(cards)))
find_least_changes(cards, good_enough=len(cards))
bar.finish()
print()
print('-----------------')
print()
print('Finding most changes')
find_most_changes(cards)