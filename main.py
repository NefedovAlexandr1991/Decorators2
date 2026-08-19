import csv
import re
from decorators import logger

phone_pattern = re.compile(
    r"(\+7|8)?\s*\(?"
    r"(\d{3})\)?[\s-]*"
    r"(\d{3})[\s-]*"
    r"(\d{2})[\s-]*"
    r"(\d{2})"
    r"(?:\s*\(?доб\.?\s*(\d+)\)?)?"
)

@logger('main.log')
def format_phone(phone):
    if not phone:
        return ""

    match = phone_pattern.search(phone)

    if not match:
        return phone

    result = (
        f"+7({match.group(2)})"
        f"{match.group(3)}-"
        f"{match.group(4)}-"
        f"{match.group(5)}"
    )

    if match.group(6):
        result += f" доб.{match.group(6)}"

    return result

@logger('main.log')
def find_doubles(contacts_list):
    i = 0
    numbers = []
    while i < len(contacts_list):
        for index, item in enumerate(contacts_list):
            if contacts_list[i][0] == item[0] and contacts_list[i][1] == item[1] and i != index:
                x = (i , index)
                numbers.append(x)
        i = i + 1
    new = []
    for item in numbers:
        new.append(sorted(item))
    i = 0
    while i < len(new):
        for index, item in enumerate(new):
            if new[i] == item and i != index:
                new.pop(i)
        i = i + 1
    return new

@logger('main.log')
def del_doubles(numbers, contacts_list):
    #for item0 in numbers:
    for index, item in enumerate(contacts_list[numbers[0]]):
        if item == '':
            contacts_list[numbers[0]][index] = contacts_list[numbers[1]][index]
    contacts_list.pop(numbers[1])
    return contacts_list


with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
phones = []
for item in contacts_list:
    fio = " ".join(item[:3])
    text = fio.split()
    if text[0]:
        item[0] = text[0]
    if len(text) > 1:
        item[1] = text[1]
    if len(text) > 2:
        item[2] = text[2]
for item in contacts_list:
    if item[5]!='':
        item[5] = format_phone(item[5])

new_list = find_doubles(contacts_list)
i = 0
length_of_doubles = len(new_list)
while i < length_of_doubles:
    contact_list = del_doubles(new_list[0], contacts_list)
    new_list = find_doubles(contacts_list)
    i = i + 1

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)