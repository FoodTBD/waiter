import easyocr

def get_easyocr_results():
    reader = easyocr.Reader(['ch_tra','en']) # this needs to run only once to load the model into memory
    return reader.readtext('hing_lung_test.png')
