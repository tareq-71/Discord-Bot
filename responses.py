import random


def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == '?Hello':
        return 'Hi'

    if p_message == 'roll':
        return str(random.randint(1, 6))

    if p_message == '@iizam bot':
        return 'what'

    if p_message == 'niz':
        return 'biz'

    if p_message == 'iizam bot':
        return 'yes'
    if p_message == 'aymen':
        return 'business major'
    if p_message == 'yazen':
        return 'is fake'
    if p_message == 'daddy':
        return 'ozmin'
