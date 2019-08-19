import datetime
import math
import re

from django.utils.html import strip_tags


def count_words(html_string):
    '''

    :param html_string:
    :return:
    '''
    word_string = strip_tags(html_string)
    count = len(re.findall(r'\w', word_string))
    return count

def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count/200.0) # 200 workds per min
    read_time = int(read_time_min)
    return read_time