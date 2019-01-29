import re
import ast
from .symbols import symbols
from .nicelogger import enable_pretty_logging
from .split_pinyin_sp.split_pinyin import split_pinyin
from .gen_inputs import check_wavfile, g2p, phoneme_set_to_dict, split_keys

# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {k: v for v, k in enumerate(symbols)}
_id_to_symbol = {v: k for v, k in enumerate(symbols)}




def text_to_sequence(text, cleaner_names):
  '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.

    The text can optionally have ARPAbet sequences enclosed in curly braces embedded
    in it. For example, "Turn left on {HH AW1 S S T AH0 N} Street."

    Args:
      text: string to convert to a sequence
      cleaner_names: names of the cleaner functions to run the text through

    Returns:
      List of integers corresponding to the symbols in the text
  '''
  #print(symbols)
  symbols = ast.literal_eval(text)
  sequence = _symbols_to_sequence(text)
  return sequence

def rawtext_to_text(text):
  pinyin = g2p(text).split(' ')
  pinyin = [split_pinyin(i) if not i in '|.!?' else i for i in pinyin]
  symbols = []
  for i in pinyin:
    for j in i:
      if j != '':
        symbols.append(str(j))
  #sequence = _symbols_to_sequence(symbols)
  symbols = str(symbols)
  return symbols

def sequence_to_text(sequence):
  '''Converts a sequence of IDs back to a string'''
  result = ''
  for symbol_id in sequence:
    if symbol_id in _id_to_symbol:
      s = _id_to_symbol[symbol_id]
      result += s
  return result



def _symbols_to_sequence(symbols):
  return [_symbol_to_id[s] for s in symbols if _should_keep_symbol(s)]

def _should_keep_symbol(s):
  return s in _symbol_to_id and s is not '__PAD'


