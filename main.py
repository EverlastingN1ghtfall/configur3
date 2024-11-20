def crash_handler(err: str):
    print(err)
    exit(-1)

def check_name(name: str) -> bool:
    name = name.rstrip(' ')
    if name.isalpha() and name.isupper():
        return True
    return False


class Solution:
    vars = []

    def __init__(self, lines: str):
        self.data = lines.splitlines()

        self.reader()

    def comment_handler(self, ind: int) -> int:
        comment = []
        for i in range(ind + 1, len(self.data)):
            if "-->" in self.data[i]:
                if self.data[i] != "-->":
                    err = f"Closing symbol (-->) should be on a separate line. Line {i+1}: '{self.data[i]}'"
                    crash_handler(err)

                self.vars.append({"type": "comment", "data": comment})
                return i
            else:
                comment.append(self.data[i])

        err = f"Closing symbol for <!-- (line {ind+1}) not found"
        crash_handler(err)


    def reader(self) -> None:
        i = 0
        while i < len(self.data):
            print(self.data[i])
            if self.data[i] == "<!--":
                i = self.comment_handler(i)
            elif self.data[i][0].isalpha():
                line = self.data[i]
                col_ind = line.find(':')
                if col_ind == -1:
                    err = f"Invalid syntax. Should be assignment, but : was not found. Line {i+1}: '{line}'"
                    crash_handler(err)

                name, content = line.split(':')
                if not check_name(name):
                    err = f"Invalid variable name (line {i+1}): '{name}'"
                    crash_handler(err)
                content_handler(content)
            i += 1


if __name__ == "__main__":
    path = "test_file.txt"
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()

    sol = Solution(data)
    print(sol.vars)