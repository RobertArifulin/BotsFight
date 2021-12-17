import random

if __name__ == "__main__":
    matches, allowed = map(int, input().split())

    if matches % (allowed + 1) == 0:
        print(random.randint(1, allowed))
    else:
        print(matches % (allowed + 1))
