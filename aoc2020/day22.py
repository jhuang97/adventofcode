file1 = open('day_22_input.txt', 'r')
deckstr = file1.read().split('\n\n')

decks = []
for k in [0, 1]:
    decks.append([int(n) for n in deckstr[k].splitlines()[1:]])

while decks[0] and decks[1]:
    c0 = decks[0].pop(0)
    c1 = decks[1].pop(0)
    winner = 0
    if c1 > c0:
        winner = 1
    decks[winner].append(max(c0, c1))
    decks[winner].append(min(c0, c1))

total = 0
for i, c in enumerate(decks[winner]):
    total += c * (len(decks[winner]) - i)
print(total)


def to_tuple(decks):
    return tuple(decks[0].copy()), tuple(decks[1].copy())


def rec_combat(rec_decks, lvl):
    game_hist = set()
    while rec_decks[0] and rec_decks[1]:
        # print(str(lvl) + ' ' + str(rec_decks))
        if to_tuple(rec_decks) in game_hist:
            print('repeat')
            return 0, rec_decks[0]
        game_hist.add(to_tuple(rec_decks))
        c = [d.pop(0) for d in rec_decks]
        if len(rec_decks[0]) >= c[0] and len(rec_decks[1]) >= c[1]:
            sub_decks = [rec_decks[0][:c[0]].copy(), rec_decks[1][:c[1]].copy()]
            winner, _ = rec_combat(sub_decks, lvl+1)
        else:
            if c[0] > c[1]:
                winner = 0
            else:
                winner = 1
        rec_decks[winner].append(c[winner])
        rec_decks[winner].append(c[1 - winner])
        # print(rec_decks)
    if not rec_decks[0]:
        return 1, rec_decks[1]
    if not rec_decks[1]:
        return 0, rec_decks[0]
    print('oh no')


decks = []
for k in [0, 1]:
    decks.append([int(n) for n in deckstr[k].splitlines()[1:]])
# _, win_deck = rec_combat([[9,2,6,3,1], [5,8,4,7,10]], 0)
_, win_deck = rec_combat(decks, 0)
# _, win_deck = rec_combat([[43, 19], [2, 29, 14]], 0)
print(win_deck)
total = 0
for i, c in enumerate(win_deck):
    total += c * (len(win_deck) - i)
print(total)

# not 33372, 3??68