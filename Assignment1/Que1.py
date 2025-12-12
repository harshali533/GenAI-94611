sentence = input("enter the sentence:")


char_count = 0
for ch in sentence:
    char_count += 1


words = sentence.split()
word_count = 0
for w in words:
    word_count += 1


vowels = "aeiouAEIOU"
vowel_count = 0
for ch in sentence:
    if ch in vowels:
        vowel_count += 1

print("Characters:", char_count)
print("Words:", word_count)
print("Vowels:", vowel_count)
