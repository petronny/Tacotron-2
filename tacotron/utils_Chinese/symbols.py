
'''
Defines the set of symbols used in text input to the model.

The default is a set of ASCII characters that works well for English or text that has been run
through Unidecode. For other data, you can modify _characters. See TRAINING_DATA.md for details.
'''

symbols = ['__PAD', '2', '3', '4', '5', '1', 'a', 'ai', 'an', 'ang', 'ao', 'b', 'c', 'ch', 'd', 'e', 'ei', 'en', 'eng', 'er', 'f', 'g', 'h', 'i', 'ia', 'ian', 'iang', 'iao', 'ie', 'in', 'ing', 'io', 'iong', 'iou', 'iv', 'ix', 'iy', 'j', 'k', 'l', 'm', 'n', 'ng', 'o', 'ong', 'ou', 'p', 'q', 'r', 'rr', 's', 'sh', 't', 'u', 'ua', 'uai', 'uan', 'uang', 'uei', 'uen', 'ueng', 'uo', 'v', 'van', 've', 'vn', 'x', 'z', 'zh', '|', '。', '！', '？']
