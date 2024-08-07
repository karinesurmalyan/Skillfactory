from django import template


register = template.Library()


BAD_WORDS = ['some', 'words']


@register.filter()
def censor(word):
    for i in BAD_WORDS:
        word = word.replace(i[1:], '*' * (len(i[1:]) - 1) + i[-1])
    return word
