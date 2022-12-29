# test variable-length keyword arguments
def test(a, b, **c):
    print(a, b, c)


test(1, 2, c1=3, c2=4, c3=5)
