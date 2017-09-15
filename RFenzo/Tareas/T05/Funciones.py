from Datos import sizes
from numpy import pi, arctan
from math import degrees, sin, cos, radians


def get_bot_pos(tipo, size, pos_inicial):
    x, y = size
    pos = pos_inicial[tipo]
    return (x-pos[0]-sizes[tipo], y-pos[1]-sizes[tipo])


def dot_inside_area(punto, center, size):
    x, y = punto
    xf, yf = center
    cond1 = x > xf-size[0]/2 and x < xf+size[0]/2
    cond2 = y > yf-size[1]/2 and y < yf+size[1]/2

    if cond1 and cond2:
        return True
    return False


def proyectile_pos(pto1, pto2, size):
    diag = (size**2 + size**2)**0.5
    x1, y1 = 0.5*pto1[0], 0.5*pto1[1]
    x2, y2 = 0.5*pto2[0], 0.5*pto2[1]
    return (x1+x2-diag/2, y1+y2-diag/2)


def distancia(pto1, pto2):
    return ((pto1[0]-pto2[0])**2+(pto1[1]-pto2[1])**2)**0.5


def closest_distance(vertices1, vertices2):
    x = []
    for i in range(4):
        for j in range(4):
            x.append(distancia(vertices1[i], vertices2[j]))
    return min(x)


def move_vertices(vertices, pos_actual):
    x, y = pos_actual
    moved = []
    for vertex in vertices:
        moved.append((vertex[0]+x, vertex[1]+y))
    return moved


def item_to_text(nombre, x):
    if nombre == 'Baculo':
        return nombre+'\n\nPrice: {} points\nEffect: {} - {}'.format(*x)
    elif nombre == 'Earthstone':
        return nombre+'\n\nPrice: {} points\nEffect: {} +- {}'.format(*x)
    return nombre+'\n\nPrice: {} points\nEffect: {} + {}'.format(*x)


def nearest(list, my_v):
    dist = [(n, closest_distance(obj.vertices, my_v))
            for n, obj in enumerate(list)]
    return sorted(dist, key=lambda x: x[1])


def get_angle(vertices_obj, vertices):
    op = []
    for i in range(4):
        dists = [(pto, vertices[i], distancia(pto, vertices[i]))
                 for pto in vertices_obj]
        mini = min(dists, key=lambda x: x[2])
        op.append(mini)

    minimo = min(op, key=lambda x: x[2])
    pto, pto2, d = minimo

    x, y = pto2
    if pto[0]-x == 0:
        angle = 0
    else:
        angle = abs(arctan((y-pto[1])/(x-pto[0])))

    if pto[0] > x and pto[1] < y:
        angle = 2*pi-angle
    elif pto[0] < x and pto[1] < y:
        angle += pi
    elif pto[0] < x and pto[1] > y:
        angle = pi - angle

    return d, radians(360-(180+degrees(angle)) % 360)


def angle_mouse(center_obj, centro):

    x, y = centro
    if center_obj[0]-x == 0:
        angle = 0
    else:
        angle = abs(arctan((y-center_obj[1])/(x-center_obj[0])))

    if center_obj[0] > x and center_obj[1] < y:
        angle = 2*pi-angle
    elif center_obj[0] < x and center_obj[1] < y:
        angle += pi
    elif center_obj[0] < x and center_obj[1] > y:
        angle = pi - angle

    return radians(360-(180+degrees(angle)) % 360)
