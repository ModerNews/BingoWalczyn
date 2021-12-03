from random import choices


def generate_bingo(filepath: str, *, width: int = 5, height: int = 5, encoding: str = 'utf8') -> list[list[str]]:
    bingo = []
    with open(filepath, 'r', encoding=encoding) as file:
        data = file.read().split('\n')
    for i in range(height):
        temp = choices(data, k=width)
        bingo.append(temp)
        for item in temp:
            data.remove(item)

    return bingo


def check_winner(bingo: list[list[int]], *, width: int = 5, height: int = 5) -> bool:
    # horizontal
    for line in bingo:
        if all([1 == n for n in line]):
            return True

    # vertical
    for i in range(len(bingo)):
        if all(line[i] == 1 for line in bingo):
            return True

    # diagonal
    if all(bingo[i][i] == 1 for i in range(len(bingo))):
        return True
    if all(bingo[i][i] == 1 for i in range(len(bingo)-1, -1, -1)):
        return True

    # none
    return False
