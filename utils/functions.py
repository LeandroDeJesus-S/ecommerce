def format_money_value(value):
    return f'R${value:.2f}'.replace('.', ',')


def get_total(cart):
    return sum([i['quantity'] for i in cart.values()])
