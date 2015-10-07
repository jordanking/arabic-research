#!/usr/bin/env python
# coding: utf-8

# add the path of arapy
from __future__ import absolute_import
from __future__ import print_function

import sys
import StringIO

sys.path.insert(0,"/Users/jordanking/Documents/")
import arapy.madamira as mada

with mada.Madamira() as m:

    out = m.process(["السلطة الفلسطينية تستنكر استمرار سياسة الاغتيالات الاسرائيلية"])

    for doc in out.docs():

        for sent in doc.sentences():
        
            buff = StringIO.StringIO()
            pos_buff = StringIO.StringIO()

            for word in sent.words():
                buff.write(word.lemma())
                buff.write(" ")
                pos_buff.write(word.pos())
                pos_buff.write(" ")

            buff.seek(0)
            pos_buff.seek(0)
            print(buff.read())
            print(pos_buff.read())
            buff.close()
            pos_buff.close()

