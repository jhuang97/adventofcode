'''
Created on Dec 1, 2019

@author: Jeffrey
'''

def try_run(noun, verb):
    codes = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,6,19,1,19,5,23,2,13,23,27,1,10,27,31,2,6,31,35,1,9,35,39,2,10,39,43,1,43,9,47,1,47,9,51,2,10,51,55,1,55,9,59,1,59,5,63,1,63,6,67,2,6,67,71,2,10,71,75,1,75,5,79,1,9,79,83,2,83,10,87,1,87,6,91,1,13,91,95,2,10,95,99,1,99,6,103,2,13,103,107,1,107,2,111,1,111,9,0,99,2,14,0,0]
    codes[1] = noun
    codes[2] = verb
    
#     codes = [2, 3, 0, 3, 99]
    
    idx = 0
    while True:
        if codes[idx] == 1:
            codes[codes[idx+3]] = codes[codes[idx+1]] + codes[codes[idx+2]]
            idx = idx + 4
        elif codes[idx] == 2:
            codes[codes[idx+3]] = codes[codes[idx+1]] * codes[codes[idx+2]]
            idx = idx + 4
        elif codes[idx] == 99:
            break
    
    return codes[0]

if __name__ == '__main__':
#     codes = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,6,19,1,19,5,23,2,13,23,27,1,10,27,31,2,6,31,35,1,9,35,39,2,10,39,43,1,43,9,47,1,47,9,51,2,10,51,55,1,55,9,59,1,59,5,63,1,63,6,67,2,6,67,71,2,10,71,75,1,75,5,79,1,9,79,83,2,83,10,87,1,87,6,91,1,13,91,95,2,10,95,99,1,99,6,103,2,13,103,107,1,107,2,111,1,111,9,0,99,2,14,0,0]
#     codes[1] = 12
#     codes[2] = 2
#     
# #     codes = [2, 3, 0, 3, 99]
#     
#     idx = 0
#     while True:
#         if codes[idx] == 1:
#             codes[codes[idx+3]] = codes[codes[idx+1]] + codes[codes[idx+2]]
#             idx = idx + 4
#         elif codes[idx] == 2:
#             codes[codes[idx+3]] = codes[codes[idx+1]] * codes[codes[idx+2]]
#             idx = idx + 4
#         elif codes[idx] == 99:
#             break
#     
#     print(codes[0])
    for n in range(0, 100):
        for v in range(0, 100):
            if try_run(n, v) == 19690720:
                print(100*n + v)