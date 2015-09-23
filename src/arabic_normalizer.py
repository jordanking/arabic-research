# -*- coding: utf-8 -*-

import re
import sys
import codecs


def main():
    with codecs.open(sys.argv[1], 'r', "utf-8") as infile:
        with codecs.open(sys.argv[2], 'w', "utf-8") as outfile:
            for line in infile:
                line = normalizeArabic(line)
                # line = removeVowels(line)
                # line = transString(line)
                # if len(line.split(' ')) == 4 or ':' in line:
                #     outfile.write(line)

def normalizeArabic(text):
    text = re.sub(ur'[إأٱآا]', ur'ا', text)

    text = re.sub(ur'ى', ur'ي', text)
    text = re.sub(ur'ؤ', ur'ء', text)
    text = re.sub(ur'ئ', ur'ء', text)

    text = re.sub(ur'-', ur'', text)

    return(text)

def removeVowels(text):
    noise = re.compile(u""" ّ | # Tashdid
                            َ | # Fatha
                            ً | # Tanwin Fath
                            ُ | # Damma
                            ٌ | # Tanwin Damm
                            ِ | # Kasra
                            ٍ | # Tanwin Kasr
                            ْ | # Sukun
                            ـ # Tatwil/Kashida
                            """, re.VERBOSE)
    text = re.sub(noise, '', text)
    return text

def transString(string, reverse=0):
    '''Given a Unicode string, transliterate into Buckwalter. To go from
    Buckwalter back to Unicode, set reverse=1'''

    buck2uni = {"'": u"\u0621", # hamza-on-the-line
                "|": u"\u0622", # madda
                ">": u"\u0623", # hamza-on-'alif
                "&": u"\u0624", # hamza-on-waaw
                "<": u"\u0625", # hamza-under-'alif
                "}": u"\u0626", # hamza-on-yaa'
                "A": u"\u0627", # bare 'alif
                "b": u"\u0628", # baa'
                "p": u"\u0629", # taa' marbuuTa
                "t": u"\u062A", # taa'
                "v": u"\u062B", # thaa'
                "j": u"\u062C", # jiim
                "H": u"\u062D", # Haa'
                "x": u"\u062E", # khaa'
                "d": u"\u062F", # daal
                "*": u"\u0630", # dhaal
                "r": u"\u0631", # raa'
                "z": u"\u0632", # zaay
                "s": u"\u0633", # siin
                "$": u"\u0634", # shiin
                "S": u"\u0635", # Saad
                "D": u"\u0636", # Daad
                "T": u"\u0637", # Taa'
                "Z": u"\u0638", # Zaa' (DHaa')
                "E": u"\u0639", # cayn
                "g": u"\u063A", # ghayn
                "_": u"\u0640", # taTwiil
                "f": u"\u0641", # faa'
                "q": u"\u0642", # qaaf
                "k": u"\u0643", # kaaf
                "l": u"\u0644", # laam
                "m": u"\u0645", # miim
                "n": u"\u0646", # nuun
                "h": u"\u0647", # haa'
                "w": u"\u0648", # waaw
                "Y": u"\u0649", # 'alif maqSuura
                "y": u"\u064A", # yaa'
                "F": u"\u064B", # fatHatayn
                "N": u"\u064C", # Dammatayn
                "K": u"\u064D", # kasratayn
                "a": u"\u064E", # fatHa
                "u": u"\u064F", # Damma
                "i": u"\u0650", # kasra
                "~": u"\u0651", # shaddah
                "o": u"\u0652", # sukuun
                "`": u"\u0670", # dagger 'alif
                "{": u"\u0671", # waSla
    }

    # For a reverse transliteration (Unicode -> Buckwalter), a dictionary
    # which is the reverse of the above buck2uni is essential.

    uni2buck = {}

    # Iterate through all the items in the buck2uni dict.
    for (key, value) in buck2uni.iteritems():
            # The value from buck2uni becomes a key in uni2buck, and vice
            # versa for the keys.
            uni2buck[value] = key

    if not reverse:     
        for k,v in buck2uni.iteritems():
            string = string.replace(v,k)

    else:     
        for k,v in buck2uni.iteritems():
            string = string.replace(k,v)

    return string

if __name__ == '__main__':
    main()