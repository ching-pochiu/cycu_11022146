def print_right(text):
    """
    將字串右對齊，使其最後一個字元位於第 40 個欄位。

    參數：
        text (str): 要列印的字串。
    """
    length = len(text)
    spaces = 40 - length
    if spaces > 0:
        print(" " * spaces + text)
    else:
        print(text)

print_right("Monty")
print_right("Python's")
print_right("Flying Circus")