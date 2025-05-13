# Напишите программу, которая выводит n первых элементов
# последовательности 122333444455555… (число повторяется столько раз, чему оно равно).
from random import randint

num = randint(1, 10)

sequence = ''

i = 1
while i < num+1:
    repeat = 0
    while repeat != i:
        sequence += str(i)
        repeat += 1
    i += 1

print(sequence)
