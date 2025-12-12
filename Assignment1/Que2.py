Data = input("enter the number:")

number = []
num = " "

for ch in Data:
    if ch !=",":
        num += ch
    else:
        number.append(int(num))
        num = ""

number.append(int(num))


even = 0
odd = 0

for n in number:
    if n%2 == 0:
        even +=1
    else:
        odd +=1

print("even numbers", even)
print("odd numbers", odd)