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


class Bingo:
    def __init__(self, *, content: list[list[int]] = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]):
        self._content: list[list[int]] = content

    def __repr__(self):
        return repr(self._content)

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return len(self._content)

    def __getitem__(self, item):
        return self._content[item]

    def check_winner(self, *, width: int = 5, height: int = 5) -> bool:
        # horizontal
        for line in self:
            if all([1 == n for n in line]):
                return True

        # vertical
        for i in range(len(self)):
            if all(line[i] == 1 for line in self):
                return True

        # diagonal
        if all(self[i][i] == 1 for i in range(len(self))):
            return True
        if all(self[i][i] == 1 for i in range(len(self) - 1, -1, -1)):
            return True

        # none
        return False
