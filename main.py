import re


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

def check_sorting_mas(mas: list) -> bool:
    for i in mas:
        if i["type"] != "int":
            err = "Runtime exception. Sorting lists with data types, other than integer, is not supported."
            crash_handler(err)
    return True

def export_int(record: dict, depth: int = 1) -> str:
    if record["name"] != "":
        to_write = '\t' * depth + '"' + record["name"] + '": ' + str(record["content"]) + ', '
    else:
        to_write = str(record["content"]) + ", "
    return to_write

def export_string(record: dict, depth: int = 1) -> str:
    if record["name"] != "":
        to_write = '\t' * depth + '"' + record["name"] + '": "' + record["content"] + '", '
    else:
        to_write = '"' + record["content"] + '", '
    return to_write

def export_dict(record: dict, depth: int = 1):
    if record["name"] != "":
        to_write = '\t' * depth + '"' + record["name"] + '": {\n'
    else:
        to_write = '{\n'
    for i in record["content"]:
        if i["type"] == "int":
            to_write += export_int(i, depth + 1) + '\n'
        elif i["type"] == "str":
            to_write += export_string(i, depth + 1) + '\n'
        elif i["type"] == "mas":
            to_write += export_mas(i, depth + 1) + '\n'
        elif i["type"] == "dict":
            to_write += export_dict(i, depth + 1) + '\n'
    to_write = to_write[:-3] + '\n' + '\t' * depth + '}, '
    return to_write

def export_mas(record: dict, depth: int = 1) -> str:
    if record["name"] != "":
        to_write = '\t' * depth + '"' + record["name"] + '": ['
    else:
        to_write = '['
    for i in record["content"]:
        if i["type"] == "int":
            to_write += export_int(i)
        elif i["type"] == "str":
            to_write += export_string(i)
        elif i["type"] == "mas":
            to_write += export_mas(i)
        elif i["type"] == "dict":
            to_write += export_dict(i)
    to_write = to_write[:-2] + '], '
    return to_write

class Solution:
    vars = []

    def __init__(self, lines: str) -> None:
        self.data = lines.splitlines()

        self.reader()

    def find_mas(self, name: str, type: str) -> int:
        for i in range(len(self.vars)):
            var = self.vars[i]
            var_name = var["name"]
            var_type = var["type"]
            if var_name == name and var_type == type:
                return i
        return -1

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
        if not re.fullmatch("-?[0-9]+", content):
            err = f"Invalid syntax. Invalid numeral: '{content}'. Line {ind+1}: '{self.data[ind]}'"
            crash_handler(err)
        return True

    def check_comas(self, start: int, end: int) -> None:
        cur_line = start + 1
        while cur_line < end:
            line = self.data[cur_line]
            line = line.rstrip(' ')
            if line == "" or line[-1] == '[' or line.find(':') == -1:
                cur_line += 1
                continue
            if line[-1] != ',':
                err = f"Invalid syntax. Expected ','. Line {cur_line+1}: '{line}'"
                crash_handler(err)

            cur_line += 1

    def mas_handler(self, add_to: list, content: str, ind: int) -> int:
        contains = mas_split(content)
        contains[0] = contains[0][1:]
        shift = -1
        i = 0
        cur_line = ind
        while i < len(contains):
            el = contains[i].lstrip(' ').rstrip(' ')
            if i == len(contains) - 1 and el != "$[":
                if el[-2:] == ");":
                    shift = -3
                    el = el[:-2]
                el = el[:-1]
            new_line = self.content_handler(add_to, el, cur_line, "")
            if cur_line != new_line:
                i = 1
                cur_line = new_line
                contains = mas_split(self.data[new_line])
            i += 1

        if contains[-1][shift] != '}':
            err = "Syntax error. Missing closing" + f". Line {cur_line+1}: '{self.data[cur_line]}'"
            crash_handler(err)

        return cur_line

    def dict_handler(self, add_to: list, ind: int) -> int:
        cur_line = ind + 1
        while cur_line < len(self.data):
            line = self.data[cur_line].lstrip('\t ')
            if line == "":
                cur_line += 1
                continue
            if line[0] == ']':
                self.check_comas(ind, cur_line)
                return cur_line
            col = line.find(':')
            if col == -1:
                err = f"Syntax error. Expected ':'. Line {cur_line+1}: '{self.data[cur_line]}'"
                crash_handler(err)

            name, content = line[:col], line[col+1:]
            name = name.lstrip(' ').rstrip(' ')
            content = content.rstrip(' ')
            if content[-1] == ',':
                content = content[:-1]
            if name == "":
                err = f"Naming error. Name can not be empty. Line {cur_line+1}: '{self.data[cur_line]}'"
                crash_handler(err)
            cur_line = self.content_handler(add_to, content, cur_line, name)

            cur_line += 1

        err = f"Invalid syntax. No ']' was found for dict started on line {ind+1}"
        crash_handler(err)

    def comment_handler(self, ind: int) -> int: # returns line index where comment ends
        comment = []
        for i in range(ind + 1, len(self.data)):
            if "-->" in self.data[i]:
                if self.data[i] != "-->":
                    err = f"Invalid syntax. Closing symbol (-->) should be on a separate line. Line {i+1}: '{self.data[i]}'"
                    crash_handler(err)

                self.vars.append({"type": "comment", "data": comment})
                return i
            else:
                comment.append(self.data[i])

        err = f"Closing symbol for <!-- (line {ind+1}) not found"
        crash_handler(err)

    def check_op(self, content: str, ind: int) -> bool:
        if content[0] != '|' or content[-1] != '|':
            err = f"Syntax error. Missing '|'. Line {ind+1}: '{self.data[ind]}'"
            crash_handler(err)
        if content.count('|') > 2:
            err = f"Syntax error. Too many '|'. Line {ind+1}: '{self.data[ind]}'"
            crash_handler(err)
        add = content.count('+')
        sub = content.count('-')
        mult = content.count('*')
        if add + sub + mult > 1:
            err = f"Syntax error. Unrecognized operator. Line {ind+1}: '{self.data[ind]}'"
            crash_handler(err)
        if add + sub + mult == 0:
            if not re.fullmatch("(\|sort\([A-Z]+\)\|)", content):
                err = f"Syntax error. Unrecognized operator/invalid variable name (sort?). Line {ind + 1}: '{self.data[ind]}'"
                crash_handler(err)
        return True

    def content_handler(self, add_to: list[dict], content: str, ind: int, name: str) -> int:
        if name != "" and not check_name(name):
            err = f"Invalid variable name (line {ind+1}): '{name}'"
            crash_handler(err)

        content = content.lstrip(' ').rstrip(' ')
        if content[0] == '@':
            if self.check_string(content, ind):
                content = content[2:-1]

                add_to.append({"type": "str", "name": name, "content": content})
                return ind

        elif content[0].isdigit() or content[0] == '-':
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
            return ind_end

        elif content[0] == '|':
            if self.check_op(content, ind):
                content = content[1:-1]
                if content.find("sort(") != -1:
                    for_sorting = content[5:-1]
                    index = self.find_mas(for_sorting, "mas")
                    if index == -1:
                        err = f"Runtime exception. Variable {for_sorting} was not find or has wrong data type. Line {ind+1}: '{self.data[ind]}'"
                        crash_handler(err)
                    for_sorting = self.vars[index]["content"].copy()
                    if check_sorting_mas(for_sorting):
                        for_sorting.sort(key=lambda x: x["content"])

                    add_to.append({"type": "mas", "name": name, "content": for_sorting})
                else:
                    if content.find('+') != -1:
                        symb = '+'
                    elif content.find('*') != -1:
                        symb = '*'
                    elif content.find('-') != -1:
                        symb = '-'
                    else:
                        symb = "how"
                    l, r = content.split(symb)
                    l = l.lstrip(' ').rstrip(' ')
                    r = r.lstrip(' ').rstrip(' ')

                    if not l.isdigit():
                        index = self.find_mas(l, "int")
                        if index == -1:
                            err = f"Runtime exception. Variable {l} was not find or has wrong data type. Line {ind+1}: '{self.data[ind]}'"
                            crash_handler(err)
                        l = self.vars[index]["content"]
                    else:
                        l = int(l)
                    if not r.isdigit():
                        index = self.find_mas(r, "int")
                        if index == -1:
                            err = f"Runtime exception. Variable {r} was not find or has wrong data type. Line {ind+1}: '{self.data[ind]}'"
                            crash_handler(err)
                        r = self.vars[index]["content"]
                    else:
                        r = int(r)

                    if symb == "+":
                        result = l + r
                    elif symb == "*":
                        result = l * r
                    elif symb == '-':
                        result = l - r
                    else:
                        result = "HOW"
                    add_to.append({"type": "int", "name": name, "content": result})

                return ind

        else:
            err = f"Runtime Exception. Unhandled line content: {content}. Line {ind+1}: '{self.data[ind]}'"
            crash_handler(err)

    def reader(self) -> None:
        i = 0
        while i < len(self.data):
            # print(self.data[i])
            if self.data[i] != "":
                if self.data[i] == "<!--":
                    i = self.comment_handler(i)

                elif self.data[i][0] == '(':
                    line = self.data[i]
                    line = line[1:].lstrip(' ').rstrip(' ')
                    if line[0:3] != "def":
                        err = f"Invalid syntax. Incorrect constant declaration1. Line {i+1}: '{self.data[i]}'"
                        crash_handler(err)

                    line = line[3:].lstrip(' ')
                    spc = line.find(' ')
                    if spc == -1:
                        err = f"Invalid syntax. Incorrect constant declaration2. Line {i + 1}: '{self.data[i]}'"
                        crash_handler(err)
                    name, content = line[:spc], line[spc+1:]
                    content = content.lstrip(' ').rstrip(' ')
                    if content.find("$[") == -1:
                        content = content[:-2]

                    name = name.rstrip(' ')
                    if name == "":
                        err = f"Naming error. Name can not be empty. Line {i+1}: '{self.data[i]}'"
                        crash_handler(err)

                    i = self.content_handler(self.vars, content, i, name)
                    line = self.data[i].rstrip(' ')
                    if line[-2:] != ");":
                        err = f"Invalid syntax. Incorrect constant declaration3. Line {i + 1}: '{self.data[i]}'"
                        crash_handler(err)

                else:
                    err = f"Runtime Exception. Unhandled line content. Line {i + 1}: '{self.data[i]}'"
                    crash_handler(err)

            # print(type(i), i)
            i += 1

    def export_to_json(self, output_path: str) -> None:
        f = open(output_path, 'w', encoding='utf-8')
        f.write("{\n")
        for i in range(len(self.vars)):
            rec = self.vars[i]
            if rec["type"] == "int":
                to_write = export_int(rec) + '\n'
            elif rec["type"] == "str":
                to_write = export_string(rec) + '\n'
            elif rec["type"] == "mas":
                to_write = export_mas(rec) + '\n'
            elif rec["type"] == "dict":
                to_write = export_dict(rec) + '\n'

            if i != len(self.vars) - 1 and rec["type"] != "comment":
                f.write(to_write)
        f.write(to_write[:-3] + '\n}')
        f.close()


if __name__ == "__main__":
    path = "test_hard_mases.txt"
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()

    sol = Solution(data)
    print(sol.vars)
    sol.export_to_json("output.json")