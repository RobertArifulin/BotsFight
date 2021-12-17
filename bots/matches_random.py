import random

if __name__ == "__main__":
    matches, allowed = map(int, input().split())
    print(random.randint(1, allowed))

