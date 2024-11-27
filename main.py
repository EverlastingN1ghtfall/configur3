def crash_handler(err: str):
    print(err)
    exit(-1)

def check_name(name: str) -> bool:
    name = name.rstrip(' ')
    if name.isalpha() and name.isupper():
        return True
    return False

def mas_split(line: str) -> list:
    counts = {
        "Strs": 0,
        "Mases": -1
    }
    buff = ""
    out = []
    for i in line:
        if i == ',' and counts["Strs"] == 0 and counts["Mases"] == 0:
            out.append(buff)
            buff = ""
        else:
            buff += i
        if i == '"':
            if counts["Strs"] == 1:
                counts["Strs"] = 0
            else:
                counts["Strs"] = 1
        elif i == '{' and counts["Strs"] == 0:
            counts["Mases"] += 1
        elif i == '}' and counts["Strs"] == 0:
            counts["Mases"] -= 1
    if buff != "":
        out.append(buff)
    return out

class Solution:
    vars = []

    def __init__(self, lines: str):
        self.data = lines.splitlines()

        self.reader()

    def check_string(self, content: str, ind: int) -> bool:
        if content[1] != '"':
            err = f'''Invalid syntax. Expected " after @. Line {ind+1}: '{self.data[ind]}' '''
            crash_handler(err)
        if content[-1] != '"':
            err = f'''Invalid syntax. Missing closing ". Line {ind+1}: '{self.data[ind]}' '''
            crash_handler(err)
        return True

    def check_numeral(self, content: str, ind: int) -> bool:
        if not content.isdigit():
            err = f"Invalid syntax. Invalid numeral: '{content}'. Line {ind+1}: '{self.data[ind]}'"
            crash_handler(err)
        return True




    def mas_handler(self, add_to: list, content: str, ind: int) -> int:
        contains = content.split(',')
        i = 0
        cur_line = ind
        while i < len(contains):
            contains[i] = contains[i].lstrip(' ').rstrip(' ')
            new_line = self.content_handler(add_to, contains[i], cur_line, "")
            if contains[i][0] == '{':
                closing_ind = -1
                for j in range(i, len(contains)):
                    if contains[j].find
            elif contains[i][0] == '$':


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

    def content_handler(self, add_to: list, content: str, ind: int, name: str) -> int:
        name = name.lstrip(' ').rstrip(' ')
        if name != "" and not check_name(name):
            err = f"Invalid variable name (line {ind+1}): '{name}'"
            crash_handler(err)
        content = content.lstrip(' ').rstrip(' ')
        if content[0] == '@':
            if self.check_string(content, ind):
                content = content[2:-1]
                if name != "":
                    add_to.append({"type": "str", "name": name, "content": content})
                else:
                    add_to.append({"type": "str", "content": content})
                return ind
        elif content[0].isdigit():
            if self.check_numeral(content, ind):
                if name != "":
                    add_to.append({"type": "int", "name": name, "content": int(content)})
                else:
                    add_to.append({"type": "int", "content": int(content)})
                return ind
        elif content[0] == '{':
            add_to.append({"type": "mas", "name": name, "content": []})

            ind_end = self.mas_handler(add_to[-1]["content"], content, ind)
            return ind_end

    def reader(self) -> None:
        i = 0
        while i < len(self.data):
            # print(self.data[i])
            if self.data[i] == "<!--":
                i = self.comment_handler(i)
            elif self.data[i][0].isalpha():
                line = self.data[i]
                col_ind = line.find(':')
                if col_ind == -1:
                    err = f"Invalid syntax. Should be assignment, but : was not found. Line {i+1}: '{line}'"
                    crash_handler(err)

                name, content = line.split(':')
                self.content_handler(self.vars, content, i, name)
            i += 1


if __name__ == "__main__":
    path = "test_file.txt"
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()

    sol = Solution(data)
    print(sol.vars)