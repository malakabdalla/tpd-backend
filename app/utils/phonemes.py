def make_phonemes(text):
    print("text here ::::::: ", text)
    text = text.replace('^', '<phoneme alphabet="ipa" ph="	ˈeɪ">ˈeɪ</phoneme>')
    # text = text.replace('A', '<phoneme alphabet="ipa" ph="`eɪ">a</phoneme>')
    return text
