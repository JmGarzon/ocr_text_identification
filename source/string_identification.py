#!/usr/bin/env python3


import re

def analyze_file():
    """ This function extracts meaningful information from the OCR gotten for a recepit type 1
        The information is looked for in the following order:
        1. Store ID.
        2. Store Address.
        3. Transaction ID.
        4. Cashier ID.
        5. Date.
        6. Ammount charged.
    """

    store_id_pattern = re.compile(r'(?<=S\w{4})(?:\s*#)(\d{5})')
    store_address_pattern = re.compile(r'([\d\w\s,]+\d{5})')
    transaction_id_pattern = re.compile(r'(?<=T\w{10})(?:\s*#)(\d{6})')
    cashier_id_pattern = re.compile(r'(?:\s*#)(\d{8})')
    date_pattern = re.compile(r'((?:\d+/?){3}\s*\d+:\d+\s*\w{2})')
    total_pattern = re.compile(r'(?<=T\w{4})(?:\s*(\d+\.?\d+))')

    tags_list = ("store_id", "store_address", "transaction_id", "cashier_id", "date", "total")
    pattern_list = [store_id_pattern, store_address_pattern, transaction_id_pattern, cashier_id_pattern, date_pattern, total_pattern]
    information_found = []
    current_pattern_index = 0

    with open("../input/OCR_Ticket.txt", "r", encoding="utf-16") as file:

        previous_pattern_excess = ""

        for line in file:
            previous_pattern_excess = previous_pattern_excess.replace("\n", " ")
            line = previous_pattern_excess + line
            previous_pattern_excess = ""

            pattern_found = re.search(pattern_list[current_pattern_index], line)
            if pattern_found:
                current_pattern_index += 1
                information_found.append(pattern_found.group(1))
                previous_pattern_excess = line[pattern_found.end():]
            else:
                previous_pattern_excess = line
                continue

            if current_pattern_index == 6:
                break

        if current_pattern_index == 6:
            print("All items found")
        else:
            print("The last {} items were not found".format(6-current_pattern_index))

        file.close()

        re.purge()
        data_caught = {tag:information_found.pop(0) for tag in tags_list}

        return data_caught

if __name__ == '__main__':
    print(analyze_file())