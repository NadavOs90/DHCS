import nltk
import re
import sys
import random
import inflect
'''Only for the first time you run'''
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        command = ''
    regex_in = r'((?:Yes, and how|Yes, how|How) many) ([a-z]+) (must|will|can) ([\'a-z\s]+) ([a-z]+)(\n)(.*)(\?)'
    regex_out = r'\4 \3 \5 {} \2\n\7.'.format(inflect.engine().number_to_words(random.randint(0, 100000)))
    regex_in_tagged = r'(.*) ([a-z]+/NNS) ([a-z]+/MD) ([a-z]+/(CD|DT|PRP))( take/VB)? ((cannon/NN |white/JJ )?[a-z]+/(NNS|NN)) (.*) ([A-Z].*)(\?/\.)'
    regex_out_tagged = r'\4 \7 \3 \10 {} \2\n\11.'.format(inflect.engine().number_to_words(random.randint(0, 100000)))
    pos = True if command == 'pos' else False
    regexp = True if command == 'regexp' else False
    song = '''How many roads must a man walk down
            Before you can call him a man?
            How many seas must a white dove sail
            Before she sleeps in the sand?
            Yes, how many times must the cannon balls fly
            Before they're forever banned?
            The answer my friend is blowin' in the wind
            The answer is blowin' in the wind.

            Yes, how many years can a mountain exist
            Before it's washed to the sea?
            Yes, how many years can some people exist
            Before they're allowed to be free?
            Yes, how many times can a man turn his head
            Pretending he just doesn't see?
            The answer my friend is blowin' in the wind
            The answer is blowin' in the wind.

            Yes, how many times must a man look up
            Before he can really see the sky?
            Yes, how many ears must one man have
            Before he can hear people cry?
            Yes, how many deaths will it take till he knows
            That too many people have died?
            The answer my friend is blowin' in the wind
            The answer is blowin' in the wind.'''

    if pos:
        tokenized_lyrics = nltk.word_tokenize(song)
        tagged_lyrics = nltk.pos_tag(tokenized_lyrics)
        tags = list(set(['/'+pos[1] for pos in tagged_lyrics]))
        tags.sort(reverse=True)
        pos_lyrics = [pos[0] + "/" + pos[1] for pos in tagged_lyrics]
        song = " ".join(pos_lyrics).replace('/. ', '/.\n')
        solution = re.sub(regex_in_tagged, regex_out_tagged, song).replace('/. ', '/.\n')
        for tag in tags:
            solution = solution.replace(tag, '')
    elif regexp:
        solution = re.sub(regex_in, regex_out, song).replace('            ', '')
    else:
        solution = ''
    print solution
