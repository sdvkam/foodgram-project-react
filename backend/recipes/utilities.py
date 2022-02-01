def make_dict_tranlit():
    dict_tranlit = {}
    ru = 'a-b-v-g-d-e-yo-zh-z-i-j-k-l-m-n-o-p-r-s-t-u-f-h-c-ch-sh-sh-y-e-yu-ya'
    list_tranlit_eng = ru.split('-')
    list_tranlit_eng.append(None)  # for 'ь' and 'ъ' symbols
    list_tranlit_eng.append(None)
    for counter, value in enumerate('абвгдеёжзийклмнопрстуфхцчшщыэюяьъ'):
        dict_tranlit[value] = list_tranlit_eng[counter]
    for counter, value in enumerate('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯЬЪ'):
        dict_tranlit[value] = list_tranlit_eng[counter]
    return dict_tranlit
