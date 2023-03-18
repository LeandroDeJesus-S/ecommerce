def format_money_value(value):
    if not value: return value
    return f'R${value:.2f}'.replace('.', ',')


def get_cart_quantity(cart):
    return sum([i['quantity'] for i in cart.values()])


def amount(value):
    v = []
    for i in value.values():
        if i.get('promotional_quantitative_price'):
            v.append(i['promotional_quantitative_price'])
            continue
        v.append(i['quantitative_price'])
    return sum(v)


def calculate_age(value):
    from datetime import datetime, timedelta
    
    d, m, y = value.day, value.month, value.year
    now = datetime.now()
    age = now.year - y
    
    if now.day < d or now.month < m:
        return age - 1
    return age
    

