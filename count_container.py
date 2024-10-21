#!/usr/bin/env python3
import os
import re
import socket
from collections import Counter

# Rip apart and tokenize contractions, keeps everything together. Used this trick more than a few times in document creation. update contraction base as we go.
def de_contract(text):
    contractions_database = {
        "I'm": "I am",
        "I'll": "I will",
        "it's": "it is",
        "don't": "do not",
        "can't": "cannot",
        "won't": "will not",
        "you're": "you are",
        "he's": "he is",
        "she's": "she is",
        "they're": "they are",
        "that's": "that is",
        "what's": "what is",
        "who's": "who is",
        "let's": "let us",
        "I've": "I have",
        "you've": "you have",
        "you're": "you are",
        "you'll": "you will",
        "we've": "we have",
        "they've": "they have",
        "hadn't": "had not",
        "hasn't": "has not",
        "won't": "will not",
        "wouldn't": "would not",
        "shouldn't": "should not",
        "couldn't": "could not",
        "mightn't": "might not",
    }
    
    for contraction, expanded in contractions_database.items():
        text = re.sub(r'\b' + re.escape(contraction) + r'\b', expanded, text)

    return text

def count_words(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read()
        # Handle contractions using our nifty database
        words = de_contract(text)
        words = re.findall(r'\b\w+\b', words.lower())
        word_count = len(words)
        word_frequency = Counter(words)
    return word_count, word_frequency

def get_container_ip():
    return socket.gethostbyname('host.docker.internal')

def main():
    directory = '/home/data'
    # Counting the files...
    total_word_count = 0
    total_word_frequencies = Counter()
    file_word_counts = {}
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            word_count, word_frequencies = count_words(filepath)
            file_word_counts[filename] = word_count
            total_word_count += word_count
            if (filepath == '/home/data/AlwaysRememberUsThisWay.txt'):
                total_word_frequencies.update(word_frequencies)
    ip_addr = get_container_ip()
    # Printing Output...
    f = open('results.txt', 'w')
    f.write("Word Count Per File: \n")
    for filename, word_count in file_word_counts.items():
        f.write(f"{filename} contained {word_count} words\n")
    f.write(f"Total Word Count: {total_word_count} words across all files\n")
    top_words = total_word_frequencies.most_common(3)
    for word, count in top_words:
        f.write(f"{word} appeared {count} times\n")
    f.write(f"Ip address of the container is: {ip_addr}\n")
    f.close()
    f = open('results.txt', 'r')
    file_contents = f.read()
    print(file_contents)

if __name__ == "__main__":
    main()


