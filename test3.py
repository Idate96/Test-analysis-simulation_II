

def func(v):
    xtab = []
    ytab = []
    for i in range(v):
        x = i*i #square
        y = (i-1)*i**2
        xtab.append(x)
        ytab.append(y)

    return xtab+ytab

print(func(10))
