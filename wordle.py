from collections import defaultdict

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def print_dict_with_rank(title, d, top=20):
    print(f"\n-------- {title} --------")
    rank = 1
    for key, value in sorted(d.items(), key=lambda item: item[1], reverse=True)[:top]:
        print(f"{rank:>2} {key}: {value}")
        rank += 1

# --- Calculate letter frequency total and per position
letter_freq = defaultdict(int)
letter_freq_in_position = defaultdict(lambda: defaultdict(int))
with open("five_letter_words.txt") as word_list:
    for word in word_list:
        word = word.rstrip()
        position = 0
        for letter in word:
            letter = letter.upper()
            letter_freq[letter] += 1
            letter_freq_in_position[letter][position] += 1
            position += 1

print("-------- Letters sorted in alphabetical order --------")
for letter, freq in sorted(letter_freq.items()):
    print(f"{letter.upper()}: {freq}")

print_dict_with_rank("Letters sorted by frequency", letter_freq, 26)


# --- Now that we have the letter frequency, calculate the "best words" to use
words_with_freq_weight = {}
words_with_freq_and_position_weight = {}
with open("five_letter_words.txt") as word_list:
    for word in word_list:
        word = word.rstrip()
        freq_weight = 0
        freq_and_position_weight = 0
        letters_in_word = set()
        position = 0
        for letter in word:
            letter = letter.upper()
            freq_weight += letter_freq[letter]
            freq_and_position_weight += letter_freq[letter] * letter_freq_in_position[letter][position]
            letters_in_word.add(letter)
            position += 1
        if len(letters_in_word) == 5:
            words_with_freq_weight[word] = freq_weight
            words_with_freq_and_position_weight[word] = freq_and_position_weight

print_dict_with_rank("Top words with most frequent unrepeated letters", words_with_freq_weight)
print_dict_with_rank("Top words with most frequent unrepeated letters weighted by letter position",
                     words_with_freq_and_position_weight)

# --- Chart letter frequencies by position
freq_in_position_by_letter_with_letter = {}
freq_in_position_by_letter = {}
for letter, total_freq in sorted(letter_freq.items(), key=lambda item: item[1], reverse=True):
    positions = letter_freq_in_position[letter]
    for position in positions:
        freq_in_position_by_letter_with_letter[letter] = [letter.upper(),
                                                          *[positions.get(position, 0) for position in range(5)]]
        freq_in_position_by_letter[letter] = [positions.get(position, 0) for position in range(5)]
df = pd.DataFrame(freq_in_position_by_letter_with_letter)
df = df.transpose().loc[::-1]  # .loc[::-1] will reverse the order

df.set_index(0).plot(kind='barh', stacked=True)
plt.legend(title="Position")
plt.title("Wordle letter frequency: total and broken down by position")
plt.xlabel("Frequency")
plt.ylabel("Letters")
plt.show()

sns.set(style="darkgrid", rc={'axes.labelsize': 20})
fig, axs = plt.subplots(4, 7, figsize=(10, 10), sharex=True, sharey=True)
x_labels = [x + 1 for x in range(5)]
for row in range(4):
    for col in range(7):
        letter = chr(ord('A') + (row * 7) + col)
        if letter <= 'Z':
            sns.barplot(x=x_labels, y=freq_in_position_by_letter[letter], ax=axs[row, col]) \
                .set_xlabel(letter.upper())
plt.suptitle("Wordle comparative letter frequency in position\n(sorted by letter frequency)")
plt.show()
