from faker import Faker
from db import db

CATS_COUNT = 10
CATS_NAMES = ['Whiskers', 'Fluffy', 'Mittens', 'Paws', 'Tiger', 'Garfield', 'Snowball', 'Smokey', 'Kitty', 'Socks']
CATS_FEATURES = ['jump', 'run', 'sleep', 'eat', 'play', 'hunt', 'purr', 'scratch', 'climb', 'hide', 'meow', 'lick',
                 'sniff', 'chase', 'nap', 'stretch', 'yawn', 'pounce', 'groom', 'swat', 'stalk', 'cuddle', 'beg',
                 'roll', 'sneak', 'lurk', 'leap', 'snuggle', 'bat', 'flop', 'chatter', 'nuzzle', 'curl', 'twitch',
                 'wiggle', 'chew', 'paw', 'sniff', 'slink', 'stalk', 'swat', 'wag', 'whisk', 'yowl', 'zoom', 'bask',
                 'crouch', 'drape', 'flick', 'hiss', 'lunge', 'nudge', 'plop', 'prowl', 'slink', 'slip', 'snarl',
                 'swish', 'tangle', 'twist', 'writhe', 'yelp', 'bask', 'crouch', 'drape', 'flick']


def populate_cats():
    for i in range(CATS_COUNT):
        cat = {
            "name": CATS_NAMES[i],
            "age": Faker().random_int(min=1, max=20),
            "features": Faker().random_choices(elements=CATS_FEATURES, length=5)
        }
        db().insert_one(cat)
    print(f'{CATS_COUNT} cats added')

if __name__ == '__main__':
    populate_cats()
