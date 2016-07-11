#!/usr/bin/python

import re
import operator
import sys

LIST_SIZE = 100
BORING_WORDS = 'data/omit_lists/combined_omit.txt'
UPLOAD_PATH = 'uploads/'
OUTPUT_PATH = 'output/'
MESSAGE_FILE = sys.argv[1]
TIMELINE_FILE = sys.argv[2]

# retrieves list of words to omit
def get_omitted_words(words):
    boring_file = open(words)
    boring_words = boring_file.read()
    omit_words = boring_words.split()
    return omit_words


# Filter out all timeline comment aside from user's timeline posts
def get_comments(filepath):
    # read contents of timeline file into a variable
    timeline_file = open(filepath)
    timeline_content = timeline_file.read()
    timeline_file.close()

    # isolate actual comments from the rest of timeline content
    comment_list = re.findall('<div class="comment">.*?</div>', timeline_content)
    comments = ''

    # concatenate comment strings
    for comment in comment_list:
        comments += comment + ' '
    return comments


# Retrieve private message text
def get_messages(filepath):
    # read contents of messages file into a variable
    messages_file = open(filepath)
    messages_content = messages_file.read()
    messages_file.close()
    return messages_content


# Filter out unwanted characters via regular expressions
def filter_by_regex(corpus):
    # strip timestamps (from messages.htm)
    corpus = re.sub('<span class="meta">.*?</span>', '', corpus)
    # strip html tags
    corpus = re.sub('<.*?>', ' ', corpus)
    # html decoding for apostrophes
    corpus = re.sub('&#039;', '\'', corpus)
    # decode heart symbol
    corpus = re.sub('&lt;3', '<3', corpus)
    # filter out parentheses that aren't part of an emoji
    corpus = re.sub('[^:][(|)]', '', corpus)
    # strip punctuation
    corpus = re.sub('\.|,|!|-', '', corpus)
    # set all chars to uppercase
    corpus.upper()
    return corpus


# Tally occurrences of all words in corpus
def count_words(corpus):
    # count words
    words = corpus.split()
    word_counts = {}

    # count instances of words
    for word in words:
        word = word.strip(" ")
        if word in word_counts:
            count = word_counts[word]
            word_counts[word] = count + 1
        else:
            word_counts[word] = 1
    return word_counts


# Filter out "boring" words
def filter_and_sort_words(word_counts, omitted_words):
    # remove boring words from dictionary
    for omit in omitted_words:
        word_counts.pop(omit, None)

    # return tuples in descending order by count
    ranked_words = sorted(word_counts.items(), key=operator.itemgetter(1), reverse=True)
    return ranked_words


# Make sure total number of words is greater than specified list size
def get_max_words(ranked_words):
    total_words = len(ranked_words)

    if total_words > LIST_SIZE:
        total_words = LIST_SIZE

    return total_words


# Prints words and occurrence counts in console
def print_ranked_words(ranked_words):
    if len(ranked_words) > 0:
        total_words = get_max_words(ranked_words)
        diff = ranked_words[total_words - 1][1]
        i = 0

        while i < total_words:
            print str(i + 1) + ": " + ranked_words[i][0] + " (" + str(ranked_words[i][1]) + "/" + str(diff) \
                  + " = " + str(ranked_words[i][1] / diff) + ")"
            i += 1
    return


# Outputs top n highest occurring words to a .txt file
def output_ranked_words(ranked_words, filepath):
    if len(ranked_words) > 0:
        total_words = get_max_words(ranked_words)
        diff = ranked_words[total_words - 1][1]
        output_str = ''

        # Dividing all ranked word counts by lowest ranked word in the set
        # This makes the word cloud easier to read, overall
        for i in range(total_words):
            count = ranked_words[i][1] / diff

            for j in range(count):
                output_str += ranked_words[i][0] + ' '

        # output stripped text file
        output_file = open(filepath, 'w')
        output_file.write(output_str)
        output_file.close()
    return


# Generates an output filename based on the uploaded file's partially pseudorandom username
def get_output_filename(filename):
    split_name = filename.split('.')
    output_file = split_name[0] + '.txt'
    path = OUTPUT_PATH + output_file
    return path


# Process timeline data
comments = get_comments(UPLOAD_PATH + TIMELINE_FILE)
comments = filter_by_regex(comments)
comments = comments.upper()
comment_dict = count_words(comments)
comment_dict = filter_and_sort_words(comment_dict, get_omitted_words(BORING_WORDS))
output_ranked_words(comment_dict, get_output_filename(TIMELINE_FILE))

# Process private message data
messages = get_messages(UPLOAD_PATH + MESSAGE_FILE)
messages = filter_by_regex(messages)
messages = messages.upper()
message_dict = count_words(messages)
message_dict = filter_and_sort_words(message_dict, get_omitted_words(BORING_WORDS))
output_ranked_words(message_dict, get_output_filename(MESSAGE_FILE))

# Print results to console
print '\nComments:'
print_ranked_words(comment_dict)

print '\nMessages:'
print_ranked_words(message_dict)
