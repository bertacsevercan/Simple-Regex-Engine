# write your code here
def check_question_wildcard(regex, inp):
    question_index = regex.index("?")
    char_index_b4_question = question_index - 1
    if regex[char_index_b4_question] == "\\":
        regex = regex.replace(regex[char_index_b4_question], "")
    elif regex[char_index_b4_question] in inp:
        regex = regex.replace(regex[question_index], "")
    else:
        regex = regex.replace(regex[question_index], "")
        regex = regex.replace(regex[char_index_b4_question], "")
    return regex


def check_star_wildcard(regex, inp):
    star_index = regex.index("*")
    char_index_b4_star = star_index - 1
    if regex[char_index_b4_star] == "\\":
        regex = regex.replace(regex[char_index_b4_star], "")
    elif regex[char_index_b4_star] in inp or regex[char_index_b4_star] == "*":
        inp_char_count = inp.count(regex[char_index_b4_star])
        regex = regex.replace(regex[star_index], "")
        regex = regex.replace(regex[char_index_b4_star], regex[char_index_b4_star] * inp_char_count)
    else:
        regex = regex.replace(regex[star_index], "")
        regex = regex.replace(regex[char_index_b4_star], "")
    return regex


def check_plus_wildcard(regex, inp):
    plus_index = regex.index("+")
    char_index_b4_plus = plus_index - 1
    if regex[char_index_b4_plus] == "\\":
        regex = regex.replace(regex[char_index_b4_plus], "")
    elif regex[char_index_b4_plus] in inp or regex[char_index_b4_plus] == ".":
        inp_char_count = inp.count(regex[char_index_b4_plus]) \
            if regex[char_index_b4_plus] != "." else inp.count(inp[regex.index(".")])
        regex = regex.replace(regex[plus_index], "")
        regex = regex.replace(regex[char_index_b4_plus], regex[char_index_b4_plus] * inp_char_count)
    else:
        regex = regex.replace(regex[plus_index], "")
    return regex


def check_letter_by_letter(regex, inp):
    container = []
    if "?" in regex:
        regex = check_question_wildcard(regex, inp)
    elif "*" in regex:
        regex = check_star_wildcard(regex, inp)
    elif "+" in regex:
        regex = check_plus_wildcard(regex, inp)
    if regex in inp:
        return True
    elif regex == ".":
        return True
    if len(regex) > len(inp) and "\\" not in regex:
        return False
    for i in range(len(regex or inp)):
        if regex == "" or regex[i] == ".":
            try:
                if regex[i - 1] == "\\":
                    container.append(regex[i])
            except IndexError:
                container.append(inp[i])
            else:
                container.append(inp[i])
        elif regex.count("\\") == 2:  # edge case: '\\|\'
            return True
        elif regex[i] == "\\":
            continue
        elif inp == "":
            return False
        elif regex[i] == inp[i]:
            container.append(inp[i])
        else:
            continue

    if "".join(container) == inp:
        return True
    else:
        return False


def check_match():
    regex, inp = input().split("|")
    first_char = regex[0] if regex != "" else ""
    last_char = len(regex) - 1
    if first_char == "^" and regex[last_char] == "$":
        if "+" in regex or "*" in regex:
            return check_letter_by_letter(regex[1:last_char], inp)
        return "".join(inp).startswith("".join(regex[1:last_char])) and \
               "".join(inp).endswith("".join(regex[1:last_char]))
    elif first_char == "^":
        if "\\" in regex:
            regex = regex.replace("\\", "")
            return "".join(inp).startswith("".join(regex[1:]))
        elif "." in regex:
            return check_letter_by_letter(regex[1:], inp)
        elif "+" in regex:
            return check_letter_by_letter(regex[1:last_char], inp)
        return "".join(inp).startswith("".join(regex[1:]))
    elif regex != "" and regex[last_char] == "$":
        if "\\" in regex:
            regex = regex.replace("\\", "")
            last_char = len(regex) - 1
            return "".join(inp).endswith("".join(regex[:last_char]))
        elif "." in regex:
            return check_letter_by_letter(regex[:last_char], inp)
        return "".join(inp).endswith("".join(regex[:last_char]))
    else:
        return check_letter_by_letter(regex, inp)


print(check_match())
