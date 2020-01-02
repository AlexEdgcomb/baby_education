from math import inf
from progress.bar import Bar

cards = [ 'MAN', 'BUS', 'DAD', 'BULB', 'BUN', 'MOM', 'BAT', 'SAD', 'MAD', 'SLED', 'SUB', 'BED', 'MAT', 'LAD', 'ROD', 'RAM', 'FLAN', 'ELM', 'LID', 'ALBUM', 'NUN', 'BIN', 'FAN', 'BIB' ]

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

    def add_combo(self, combo):
        for pair in combo.pairs:
            self.add_pair(pair)

    def can_end_with_pair(self, new_pair):

        # The new pair cannot end share any cards with the existing pairs.
        for pair in self.pairs[:-1]:
            if set([ pair.first, pair.second ]) & set([ new_pair.first, new_pair.second ]):
                return False

        if self.pairs:

            # The last pair's second card must match the new pair's first card.
            if self.pairs[-1].second != new_pair.first:
                return False

            # The last pair's first card cannot be the same as the new pair's second card.
            if self.pairs[-1].first == new_pair.second:
                return False

        return True

    def can_connect(self, new_combo):
        # Last of self's pairs must match first of new_combo's pairs.
        return (not bool(self.pairs)) or (self.pairs[-1].second == new_combo.pairs[0].first)

    def can_use_combo(self, new_combo):

        # Cards from self's first to second-to-last card aren't in any of new_combo.
        if self.pairs:
            all_but_last_self = self.cards.copy()
            all_but_last_self.remove(self.pairs[-1].second)
            if all_but_last_self & new_combo.cards:
                return False

        # Cards from new_combo's second to last card aren't in any of self.
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


def make_all_combos(combos, remaining_pairs, curr):
    remaining_pairs = [ pair for pair in remaining_pairs if curr.can_end_with_pair(pair) ]
    for pair in remaining_pairs:
        tmp_curr = Combo(curr)
        tmp_curr.add_pair(pair)
        combos.append(tmp_curr)
        make_all_combos(combos, remaining_pairs, tmp_curr)

# Make all combos of cost 1s. Include each cost 2+ pair as a combo. Don't make combos of cost 2+ since we won't use those.
max_cost = max([ pair.cost for pair in pairs ])
not_lowest_cost_pairs = [ pair for pair in pairs if pair.cost > 1 ]
combos = [ Combo(pair) for pair in not_lowest_cost_pairs ]
lowest_cost_pairs = [ pair for pair in pairs if pair.cost == 1 ]
make_all_combos(combos, lowest_cost_pairs, Combo())
combos.sort()

def find_best_deck(unused, curr, lowest_cost_deck=inf, first_call=True):

    # Check if no way to beat best given unused and curr.
    lowest_cost_unused = unused[0].avg_cost() if unused else 0
    num_cards_remaining = len(cards) - len(curr.pairs)
    lowest_cost_for_deck = lowest_cost_unused * num_cards_remaining
    if (curr.cost + lowest_cost_for_deck) > lowest_cost_deck:
        return lowest_cost_deck

    usable_combos = [ combo for combo in unused if curr.can_use_combo(combo) ]
    connectable_combos = [ combo for combo in usable_combos if curr.can_connect(combo) ]

    # Start progress tracker.
    if first_call:
        bar = Bar('Finding lowest cost', max=len(usable_combos))

    if connectable_combos:
        for combo in connectable_combos:

            # Update progress tracker.
            if first_call:
                bar.next()

            tmp_curr = Combo(curr)
            tmp_curr.add_combo(combo)
            lowest_cost_deck = find_best_deck(usable_combos, tmp_curr, lowest_cost_deck, False)
    elif curr.cost < lowest_cost_deck:
        lowest_cost_deck = curr.cost
        print()
        print(curr)

    # End progress tracker.
    if first_call:
        bar.finish()

    return lowest_cost_deck

find_best_deck(combos, Combo())
print()
