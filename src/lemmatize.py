#!/usr/bin/env python
# coding: utf-8

# add the path of arapy
from __future__ import absolute_import
from __future__ import print_function

import sys

sys.path.insert(0,"/Users/jordanking/Documents/")
import arapy.madamira as mada




mada.transform_sentence_file(["السلطة الفلسطينية تستنكر استمرار سياسة الاغتيالات الاسرائيلية",
                              "السلطة الفلسطينية تستنكر استمرار سياسة الاغتيالات الاسرائيلية",
                              "السلطة الفلسطينية تستنكر استمرار سياسة الاغتيالات الاسرائيلية"], True, True)
