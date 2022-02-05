import datetime as dt

from django.conf import settings
from django.template.defaultfilters import slugify


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


def rus_to_engslug_addnow(name):
    # translate используется:
    # так как название рецепта может быть написано кирилицей
    slug = slugify(
        name.translate(
            str.maketrans(settings.DICT_TRANSLIT_RUS_TO_ENGLISH)))
    return f'{slug}_{dt.datetime.utcnow()}'
