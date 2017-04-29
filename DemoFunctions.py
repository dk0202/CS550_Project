def HW21(x):
    s = 0
    n = 1
    while x > 0:
        s = s + n
        n = n + 2
        x = x - 1
    return


def HW22(A,B):
    x = A
    y = B
    z = 1

    while y > 0:
        if y%2==1:
            y = y - 1
            z = x * z
        else:
            x = x * x
            y = y // 2
        return
