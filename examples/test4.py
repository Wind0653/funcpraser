# test variable-length arguments
def test(a, b, *c):
    print(a, b, c)


test(1, 2, 3, 4, 5)
