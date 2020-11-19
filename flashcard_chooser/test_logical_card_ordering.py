from math import inf
from progress.bar import Bar

cards = [ 'NUN', 'BUN', 'BUS', 'BULB', 'SUB', 'BIB', 'BIN', 'BED', 'ROD', 'RAM', 'MOM', 'ELM', 'ALBUM', 'SLED', 'LID', 'LAD', 'DAD', 'SAD', 'MAD', 'MAT', 'BAT', 'MAN', 'FAN', 'FLAN' ]
size_of_deck = len(cards)

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


def edit_distance(str1, str2):
    return edit_distance_runner(str1, str2, len(str1), len(str2))


class Pair:
    def __init__(self, first, second, cost):
        self.first = first
        self.second = second
        self.cost = cost

    def __str__(self):
        return '%s, %s, %d' % (self.first, self.second, self.cost)

pairs = []
for index, first in enumerate(cards):
    other_cards = cards[index + 1:]
    for second in other_cards:
        cost = edit_distance(first, second)
        pairs.append(Pair(first, second, cost))
        pairs.append(Pair(second, first, cost))

class Combo:
    def __init__(self, initial=None):
        if isinstance(initial, Combo):
            self.pairs = initial.pairs[:]
            self.cost = initial.cost
            self.cards = set()
            for pair in self.pairs:
                self.cards.update([ pair.first, pair.second ])
        elif isinstance(initial, Pair):
            self.pairs = [ initial ]
            self.cost = initial.cost
            self.cards = set([ initial.first, initial.second ])
        else:
            self.pairs = []
            self.cost = 0
            self.cards = set()

    def add_pair(self, pair):
        self.pairs.append(pair)
        self.cost += pair.cost
        self.cards.update([ pair.first, pair.second ])

    def add_combo_to_right(self, combo):
        for pair in combo.pairs:
            self.add_pair(pair)

    def can_connect_combo_to_right(self, new_combo):

        # Last of self's pairs must match first of new_combo's pairs.
        return (not bool(self.pairs)) or (not bool(new_combo.pairs)) or (self.pairs[-1].second == new_combo.pairs[0].first)

    def can_use_combo(self, new_combo):
        return self.can_use_combo_to_right(new_combo) or new_combo.can_use_combo_to_right(self)

    def can_use_combo_to_right(self, new_combo):

        # Cards from self's first to second-to-last card aren't in any of new_combo.
        if self.pairs:
            all_but_last_self = self.cards.copy()
            all_but_last_self.remove(self.pairs[-1].second)
            if all_but_last_self & new_combo.cards:
                return False

        # Cards from new_combo's second to last card aren't in any of self.
        if new_combo.pairs:
            all_but_first_new_combo = new_combo.cards.copy()
            all_but_first_new_combo.remove(new_combo.pairs[0].first)
            if all_but_first_new_combo & self.cards:
                return False

        return True

    def __str__(self):
        combo_str = '<empty>'
        if self.pairs:
            first_cards = [ self.pairs[0].first, self.pairs[0].second ]
            remaining_cards = [ pair.second for pair in self.pairs[1:] ]
            combo_str = '%d: %s' % (self.cost, ', '.join(first_cards + remaining_cards))
        return combo_str

    def avg_cost(self):
        return self.cost / len(self.pairs)

    def __lt__(self, other):
        if self.avg_cost() == other.avg_cost():
            return len(self.pairs) > len(other.pairs)
        else:
            return self.avg_cost() < other.avg_cost()

    def __eq__(self, other):
        return (self.cards == other.cards) and (self.pairs[0].first == other.pairs[0].first) and (self.pairs[-1].second == other.pairs[-1].second)


def make_all_combos(combos, remaining_pairs, curr):
    usable_pairs = [ pair for pair in remaining_pairs if curr.can_use_combo_to_right(Combo(pair)) ]
    connectable_pairs = [ pair for pair in usable_pairs if curr.can_connect_combo_to_right(Combo(pair)) ]
    for pair in connectable_pairs:
        tmp_curr = Combo(curr)
        tmp_curr.add_pair(pair)
        combos.append(tmp_curr)
        make_all_combos(combos, usable_pairs, tmp_curr)

# Make all combos of cost 1s. Include each cost 2+ pair as a combo. Don't make combos of cost 2+ since we won't use those.
not_lowest_cost_pairs = [ pair for pair in pairs if pair.cost > 1 ]
combos = [ Combo(pair) for pair in not_lowest_cost_pairs ]
lowest_cost_pairs = [ pair for pair in pairs if pair.cost == 1 ]
make_all_combos(combos, lowest_cost_pairs, Combo())
combos.sort()

# Keep combos that have a unique set of cards AND unique first and last cards.
unique_combos = []
for combo in combos:
    if combo not in unique_combos:
        unique_combos.append(combo)

def find_best_deck(unused, curr, lowest_cost_deck=inf, first_call=True):

    # Keep only usable combos.
    usable_combos = [ combo for combo in unused if curr.can_use_combo(combo) ]

    # Check if no way to beat best given usable_combos and curr.
    lowest_cost_unused = usable_combos[0].avg_cost() if usable_combos else inf
    num_cards_remaining = size_of_deck - len(curr.pairs)
    lowest_cost_for_deck = lowest_cost_unused * num_cards_remaining
    if (curr.cost + lowest_cost_for_deck) > lowest_cost_deck:
        return lowest_cost_deck

    # Check if no way to fill deck given usable_combos and curr.
    deck = curr.cards.copy()
    for combo in usable_combos:
        deck.update(combo.cards)
    if len(deck) < size_of_deck:
        return lowest_cost_deck

    usable_combos_to_right = [ combo for combo in usable_combos if curr.can_use_combo_to_right(combo) ]
    usable_combos_to_left = [ combo for combo in usable_combos if combo.can_use_combo_to_right(curr) ]
    connectable_combos_to_right = [ combo for combo in usable_combos_to_right if curr.can_connect_combo_to_right(combo) ]
    connectable_combos_to_left = [ combo for combo in usable_combos_to_left if combo.can_connect_combo_to_right(curr) ]

    # Start progress tracker.
    if first_call:
        bar = Bar('Finding lowest cost', max=len(connectable_combos_to_right) + len(connectable_combos_to_left))

    if connectable_combos_to_left:
        for combo in connectable_combos_to_left:

            # Update progress tracker.
            if first_call:
                bar.next()

            tmp_combo = Combo(combo)
            tmp_combo.add_combo_to_right(curr)
            lowest_cost_deck = find_best_deck(usable_combos_to_left, tmp_combo, lowest_cost_deck, False)

    elif connectable_combos_to_right:
        for combo in connectable_combos_to_right:

            # Update progress tracker.
            if first_call:
                bar.next()

            tmp_curr = Combo(curr)
            tmp_curr.add_combo_to_right(combo)
            lowest_cost_deck = find_best_deck(usable_combos_to_right, tmp_curr, lowest_cost_deck, False)

    elif not usable_combos_to_right and (curr.cost < lowest_cost_deck):
        lowest_cost_deck = curr.cost
        print()
        print(curr)

    # End progress tracker.
    if first_call:
        bar.finish()

    return lowest_cost_deck

find_best_deck(unique_combos, Combo())
print()
