def count_spam(number):
    count = 0
    if number <= 0:
        return count
    while number % 3 == 0:
        count += 1
        number //= 3
    return count

def prepare_meal(number):
    spam_count = count_spam(number)
    has_eggs = number != 0 and number % 5 == 0
    spams = ' '.join(['spam'] * spam_count)
    if spam_count and has_eggs:
        return spams + ' and eggs'
    elif spam_count and not has_eggs:
        return spams
    elif spam_count == 0 and has_eggs:
        return 'eggs'
    else:
        return ''
