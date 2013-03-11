DENOMINATIONS = {1, 5, 2, 10, 20, 50, 100}


def calculate_coins(amount):
    if amount < 0:
        raise ValueError
    stotinki = round(amount * 100)
    coins = {x: 0 for x in DENOMINATIONS}

    for denomination in sorted(DENOMINATIONS, reverse=True):
        coins[denomination] += stotinki // denomination
        stotinki %= denomination

    return coins
