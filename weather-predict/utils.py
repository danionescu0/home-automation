def print_headline(text: str):
    header = ''
    for i in range(0, len(text)):
        header += '#'
    print(header)
    print (text.ljust(100, ' '))
    print(header)
    print()