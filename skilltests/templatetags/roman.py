from django import template

register = template.Library()


@register.filter
def romanize(arg):
    try:
        arg = int(arg)

        if 0 < arg < 4000:
            pass
        else:
            return None

        digits = {  # Чему равны числа
            1: 'I',
            4: 'IV',
            5: 'V',
            9: 'IX',
            10: 'X',
            40: 'XL',
            50: 'L',
            90: 'XC',
            100: 'C',
            400: 'CD',
            500: 'D',
            900: 'CM',
            1000: 'M'
        }

        result = ''

        for key in sorted(list(digits.keys()), reverse=True):
            while arg >= key:
                result += digits[key]
                arg -= key

        return result
    except:
        return None
