import os

bashCommand = "python main.py --graph cube --d 12 --s0 greedy --s1 random --verbose"

for i in range(1,11):
    os.system(bashCommand)

print("Test terminée")
