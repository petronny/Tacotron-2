#!/bin/python3
import os
import re
#import jieba
import random
import logging
import thulac
from pypinyin import pinyin, Style
from .split_pinyin_sp import split_pinyin
logger = logging.getLogger(__name__)



def g2p(text):
    thu1 = thulac.thulac(seg_only=True)

    fullstops = ['，', '。', '？', '！']

    #i[1] = i[1].replace('：', ' ')
    #i[1] = i[1].replace(':', ' ')
    text = text.replace('\u3000', '')
    text = text.replace('.', '。')
    text = text.replace('!', '！')
    text = re.sub(r'[“”]', ' ', text)
    text = re.sub(r'[:、：,\-]', '，', text)
    text = re.sub(r'([a-zA-Z“”])', r' \1 ', text)
    words = thu1.cut(text, text=True).split(' ')
    #print(words)
    char_pinyin = [i[0] for i in pinyin(text, style=Style.TONE3)]
    char_pinyin = re.sub(r' +', ' ', ' '.join(char_pinyin)).split(' ')
    char_pinyin = [i for i in char_pinyin if i != '']
    char_pinyin = [re.sub(r'^([a-z]*$)', '\g<1>5', i) for i in char_pinyin]
    #char_pinyin = [re.sub(r'^ ', '','%s %s%s' % split_pinyin(i)[:3]) for i in char_pinyin]
    logger.debug(char_pinyin)
    logger.debug(words)
    word_pinyin = []
    for j in range(len(words)):
        l = len(''.join(words[0:j]))
        r = len(''.join(words[0:j + 1]))
        word_pinyin.append(' '.join(char_pinyin[l:r]))
        logger.debug((l, r, words[j], word_pinyin[-1]))
    for j in range(len(words)):
        if words[j] == '。':
            word_pinyin[j] = '.'
        elif words[j] == '？':
            word_pinyin[j] = '?'
        elif words[j] == '！':
            word_pinyin[j] = '!'
        elif words[j] == '，':
            word_pinyin[j] = '，'
        elif j < len(words) - 1 and words[j + 1] in fullstops:
            pass
        elif j == len(words) - 1 and not words[j] in fullstops:
            word_pinyin.append('.')
        else:
            word_pinyin[j] += ' |'
    if r != len(char_pinyin):
        logger.error('文本拼音分词对齐错误')
        return None
    if ',' in text or '.' in text or '!' in text:
        logger.error('半角标点')
        return None
    if not text[-1] in fullstops:
        logger.warning('末尾缺少标点')
    return ' '.join(word_pinyin)

def split_keys(keys, valid=0.1, test=0.01, seed=1234):
    random.seed(seed)
    keys = list(keys)
    random.shuffle(keys)
    train = keys[:int(len(keys) * (1 - valid - test))]
    valid = keys[int(len(keys) * (1 - valid - test)):int(len(keys) * (1 - test))]
    test = keys[int(len(keys) * (1 - test)):]
    logger.info('Train: %d\tValid: %d\tTest:%d' % (len(train), len(valid), len(test)))
    open('key_train.txt', 'w').writelines([i + '\n' for i in train])
    open('key_dev.txt', 'w').writelines([i + '\n' for i in valid])
    open('key_test.txt', 'w').writelines([i + '\n' for i in test])

def check_wavfile(path, key):
    return os.path.exists('%s/%s.wav' % (path, key))

def phoneme_set_to_dict(phoneme_set):
    phoneme_set = sorted(phoneme_set)
    phoneme_dict = {}
    for i, j in enumerate(phoneme_set):
        if i == 0:
            phoneme_dict['__PAD'] = i
            continue
        if j == '__PAD':
            phoneme_dict[phoneme_set[0]] = i
            continue
        phoneme_dict[j] = i
    return phoneme_dict

if __name__ == '__main__':
    from nicelogger import enable_pretty_logging
    enable_pretty_logging('INFO')
    #enable_pretty_logging('DEBUG')
    import os
    import sys
    from collections import Counter
    import pickle
    import tqdm
    if len(sys.argv) < 1:
        sys.exit(1)

    config = sys.argv[1]
    lines=open('./config/%s/transcript.txt' % config).readlines()
    lines = [i.strip('\n').split('\t') for i in lines]
    phoneme = {}
    phoneme_set = set(['__PAD', ])
    stats = []

    for i in tqdm.tqdm(lines):
        if not os.path.exists('./wav/%s/%s.wav' % (config, i[0])):
            stats.append('无音频')
            continue
        if len(i[1]) < 5:
            stats.append('文本太短')
            continue
        if len(i[1]) > 20:
            stats.append('文本太长')
            continue
        if not re.search(r'[A-Za-z]', i[1]) is None:
            stats.append('文本有字母')
            continue
        phoneme[i[0]] = g2p(i[1])
        logger.debug(phoneme[i[0]])
        phoneme_set.update(list(phoneme[i[0]]))

    #thcoss_phoneme = pickle.load(open('./config/thcoss/char_inputs_dic.pkl', 'rb'))
    #thcoss_phoneme_dict = pickle.load(open('./config/thcoss/char2id_dic.pkl', 'rb'))
    #phoneme.update(thcoss_phoneme)
    #phoneme_set.update(thcoss_phoneme_dict.keys())

    logger.debug(phoneme)

    phoneme_dict = phoneme_set_to_dict(phoneme_set)
    logger.info(phoneme_dict.keys())
    pickle.dump(phoneme, open('./config/%s/phoneme_list.pkl' % config, 'wb'))
    pickle.dump(phoneme_dict, open('./config/%s/phoneme_dict.pkl' % config, 'wb'))
    split_keys(list(phoneme.keys()))
    logger.warning(dict(Counter(stats)))
