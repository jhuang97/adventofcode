import numpy as np

file1 = open('day_4_input.txt', 'r')
parts = file1.read().split('\n\n')
seq = [int(m) for m in parts[0].split(',')]
boards = np.zeros((len(parts)-1, 5, 5))

for k in range(len(parts)-1):
    row_list = parts[k+1].strip().split('\n')
    for r in range(5):
        row = row_list[r].strip().split()
        for c in range(5):
            boards[k, r, c] = int(row[c])

board_match = np.zeros((len(parts)-1, 5, 5))
board_win_order = []
for num in seq:
    board_match += boards == num
    xmatch = np.sum(board_match, axis=1)
    ymatch = np.sum(board_match, axis=2)
    xwhere = np.argwhere(xmatch == 5)
    ywhere = np.argwhere(ymatch == 5)
    if len(board_win_order) == 0:
        found = -1
        if len(xwhere) > 0:
            found = xwhere[0][0]
        if len(ywhere) > 0:
            found = ywhere[0][0]
        if found > -1:
            print(num*np.sum(np.multiply(boards[found], 1-board_match[found])))
            board_win_order.append(found)
    else:
        if len(xwhere) > 0:
            for arr in xwhere:
                if arr[0] not in board_win_order:
                    board_win_order.append(arr[0])
        if len(ywhere) > 0:
            for arr in ywhere:
                if arr[0] not in board_win_order:
                    board_win_order.append(arr[0])
last_board_id = board_win_order[-1]

board_match = np.zeros((len(parts)-1, 5, 5))
for num in seq:
    board_match += boards == num
    xmatch = np.sum(board_match, axis=1)
    ymatch = np.sum(board_match, axis=2)
    xwhere = np.argwhere(xmatch[last_board_id] == 5)
    ywhere = np.argwhere(ymatch[last_board_id] == 5)
    if len(xwhere) > 0 or len(ywhere) > 0:
        print(num*np.sum(np.multiply(boards[last_board_id], 1-board_match[last_board_id])))
        break
