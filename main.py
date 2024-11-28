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
        "Mases": 0
    }
    if line[0] == '{':
        counts["Mases"] -= 1
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
    consts = []

    def __init__(self, lines: str) -> None:
        self.data = lines.splitlines()

        self.reader()

    def check_string(self, content: str, ind: int) -> bool:
        if content[1] != '"':
            err = f'''Invalid syntax. Expected " after @. Line {ind+1}: '{self.data[ind]}' '''
            crash_handler(err)
        if content[-1] != '"':
            err = f'''Invalid syntax. Missing closing ". Line {ind+1}: '{self.data[ind]}' '''
            crash_handler(err)
        if content.count('"') > 2:
            err = f'''Invalid syntax. Too many ". Line {ind+1}: '{self.data[ind]}' '''
            crash_handler(err)
        return True

    def check_numeral(self, content: str, ind: int) -> bool:
        if not content.isdigit():
            err = f"Invalid syntax. Invalid numeral: '{content}'. Line {ind+1}: '{self.data[ind]}'"
            crash_handler(err)
        return True

    def mas_handler(self, add_to: list, content: str, ind: int) -> int:
        contains = mas_split(content)
        contains[0] = contains[0][1:]
        i = 0
        cur_line = ind
        while i < len(contains):
            el = contains[i].lstrip(' ').rstrip(' ')
            if i == len(contains) - 1:
                el = el[:-1]
            new_line = self.content_handler(add_to, el, cur_line, "")
            if cur_line != new_line:
                i = 1
                cur_line = new_line
                contains = mas_split(self.data[new_line])
            i += 1

        if contains[-1][-1] != '}':
            err = "Syntax error. Could not find }" + f". Line {cur_line+1}: '{self.data[cur_line]}'"
            crash_handler(err)

        return cur_line

    def dict_handler(self, add_to: list, ind: int) -> int:


    def comment_handler(self, ind: int) -> int: # returns line index where comment ends
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
        if name != "" and not check_name(name):
            err = f"Invalid variable name (line {ind+1}): '{name}'"
            crash_handler(err)

        content = content.lstrip(' ').rstrip(' ')
        if content[0] == '@':
            if self.check_string(content, ind):
                content = content[2:-1]

                add_to.append({"type": "str", "name": name, "content": content})
                return ind

        elif content[0].isdigit():
            if self.check_numeral(content, ind):
                add_to.append({"type": "int", "name": name, "content": int(content)})
                return ind

        elif content[0] == '{':
            add_to.append({"type": "mas", "name": name, "content": []})

            ind_end = self.mas_handler(add_to[-1]["content"], content, ind)
            return ind_end

        elif content == '$[':
            add_to.append({"type": "dict", "name": name, "content": []})

            ind_end = self.dict_handler(add_to[-1]["content"], ind)

        elif content[0] == '|':
            todo_const_hander = 0
        else:
            err = f"Runtime Exception. Unhandled line/content. Line {ind+1}: '{self.data[ind]}'"
            crash_handler(err)

    def reader(self) -> None:
        i = 0
        while i < len(self.data):
            # print(self.data[i])
            if self.data[i] != "":
                if self.data[i] == "<!--":
                    i = self.comment_handler(i)

                elif self.data[i][0].isalpha():
                    line = self.data[i]
                    col_ind = line.find(':')
                    if col_ind == -1:
                        err = f"Invalid syntax. Should be assignment, but : was not found. Line {i+1}: '{line}'"
                        crash_handler(err)

                    cln = line.find(':')
                    name, content = line[:cln], line[cln+1:]
                    name = name.rstrip(' ')
                    if name == "":
                        err = f"Naming error. Name can not be empty. Line {i+1}: '{self.data[i]}'"
                        crash_handler(err)

                    i = self.content_handler(self.vars, content, i, name)

                elif self.data[i][0] == '(':
                    line = self.data[i]
                    line = line[1:].lstrip(' ').rstrip(' ')
                    if line[1:4] != "def":
                        err = f"Invalid syntax. Incorrect constant decloration. Line {i+1}: '{self.data[i]}'"
                        crash_handler(err)

                    line = line[3:].lstrip(' ')
                    spc = line.find(' ')
                    name, content = line[:spc], line[spc+1:]

                    name = name.rstrip(' ')
                    if name == "":
                        err = f"Naming error. Name can not be empty. Line {i+1}: '{self.data[i]}'"
                        crash_handler(err)

                    i = self.content_handler(self.consts, content, i, name)
                    line = self.data[i].rstrip(' ')
                    if line[-2:] != ");":
                        err = f"Invalid syntax. Incorrect constant decloration. Line {i+1}: '{self.data[i]}'"
                        crash_handler(err)

            # print(type(i), i)
            i += 1


if __name__ == "__main__":
    path = "test_basic1.txt"
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()

    sol = Solution(data)
    print(sol.vars)