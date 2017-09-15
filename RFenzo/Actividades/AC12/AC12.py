# with open('chatayudantes.iic2233', 'rb') as file:
#     datos1 = file.read()

# sumas = []
# i = 1
# suma = 0
# for num in datos1:

#     if i % 4 != 0:
#         suma += num
#     else:
#         suma += num
#         x = str(suma).zfill(3)
#         sumas.append(x)
#         suma = 0
#     i += 1


def gen_primes():
    D = {}
    q = 2

    while True:
        if q not in D:
            yield q
            D[q * q] = [q]
        else:
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]
        q += 1


# generator = gen_primes()
# for j in generator:
#     print(j)


# def gen_malv():
#     num = 3
#     while True:
#         if bin(num)[2:].count('1') % 2 == 0:
#             yield num
#         num += 1

# for i in gen_malv():
#     print(i)

x = [1, 2, 3, 4, 5]
y = x[:2]
x = x[2:]
print(x, y)
