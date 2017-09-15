# def int_to_bytes(x):
#     return x.to_bytes((x.bit_length() + 7) // 8, 'big')

# def int_from_bytes(xbytes):
#     return int.from_bytes(xbytes, 'big')
import os
from random import shuffle


def chunks_gen(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def one_filter(canal):
    new = bytearray()
    chunk_nuevo_anterior = None
    for chunk_antiguo in chunks_gen(canal, 2):
        chunk_antiguo = int.from_bytes(chunk_antiguo, 'little')

        if chunk_nuevo_anterior == None:
            chunk_nuevo_anterior = chunk_antiguo
        else:
            chunk_nuevo_anterior = int((chunk_antiguo+chunk_nuevo_anterior)/2)

        new += chunk_nuevo_anterior.to_bytes(2, 'little')
    return new


def n_filter(canal, n):
    if n != 0:
        new = one_filter(canal)
        return n_filter(new, n-1)
    else:
        return canal


def get_bps(file):
    return int(int.from_bytes(file[34:36], 'little')/8)


def get_channels(file, bps):
    canal1 = bytearray()
    canal2 = bytearray()
    i = 0
    for chunk in chunks_gen(file[44:], bps):
        if i % 2 == 0:
            canal1 += chunk
        else:
            canal2 += chunk
        i += 1
    return canal1, canal2


# def ecualizar(path, freq, n):

#     with open(path, 'rb') as f:

#         file = bytearray(f.read())
#         # modificar frecuencia
#         new = int(int.from_bytes(file[24:28], 'little')*freq)
#         file[24:28] = new.to_bytes(4, 'little')

#         # bps = get_bps(file)
#         # # obtener canales
#         # canal1, canal2 = get_channels(file, bps)
#         # # aplicar filtro
#         # canal1_final = n_filter(canal1, n)
#         # canal2_final = n_filter(canal2, n)

#         # # for i in range(5000, 5020):
#         # #     print(canal1[i], canal1_final[i])

#         # # unir canales modificados al file
#         # new_file = file[:44]  # header
#         # for i in range(len(canal1)):
#         #     new_file += canal1_final[bps*i:bps*i+bps]
#         #     new_file += canal2_final[bps*i:bps*i+bps]

#     return file


def ecualizar(path, freq, n_veces):
    with open(path, 'rb') as archivo:
        file = bytearray(archivo.read())
        new = int(int.from_bytes(file[24:28], 'little')*freq)
        file[24:28] = new.to_bytes(4, 'little')
        bps = get_bps(file)

        canal = 0
        for i in range(n_veces):
            new_back_chunk_1 = int(int.from_bytes(
                file[44: 44 + bps], "little"))
            new_back_chunk_2 = int(
                int.from_bytes(file[44 + bps: 44 + 2 * bps], "little"))

            for b in range(len(file)):
                if b >= 44 and b % bps == 0:
                    canal += (canal + 1) % 2
                    aux = int(int.from_bytes(file[b: b + bps],
                                             "little"))
                    if canal == 0:
                        file[b: b + bps] = ((new_back_chunk_1 +
                                             aux)//2).to_bytes(bps, "little")
                        new_back_chunk_1 = int(int.from_bytes(file[b: b + bps],
                                                              "little"))
                    else:
                        file[b: b + bps] = ((new_back_chunk_2 +
                                             aux)//2).to_bytes(bps, "little")
                        new_back_chunk_2 = int(int.from_bytes(file[b: b + bps],
                                                              "little"))
    return file
