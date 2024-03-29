#!/usr/bin/env python

import easyocr

def get_easyocr_results(img_path, lang_list):
    reader = easyocr.Reader(lang_list) # this needs to run only once to load the model into memory
    return reader.readtext(img_path)
