sizes = {'Chau': 150, 'Hernan': 110, 'Franky': 110,
         'Tower': 200, 'Nexo': 150, 'Inhibidor': 150,
         'Tienda': 150, 'MinionN': 50, 'MinionG': 80}

original = {'Chau': 140, 'Hernan': 170, 'Franky': 260,
            'Tower': 450, 'Nexo': 500, 'Inhibidor': 700,
            'Tienda': 500, 'MinionN': 50, 'MinionG': 60}


def diag_size(original):
    return original*2**0.5

real_size = {'Chau': diag_size(sizes['Chau']),
             'Hernan': diag_size(sizes['Hernan']),
             'Franky': diag_size(sizes['Franky']),
             'MinionN': diag_size(sizes['MinionN']),
             'MinionG': diag_size(sizes['MinionG']),
             'Tower': sizes['Tower'], 'Nexo': sizes['Nexo'],
             'Inhibidor': sizes['Inhibidor'],
             'Tienda': sizes['Tienda']}

porcent = {'Chau': sizes['Chau']/original['Chau'],
           'Hernan': sizes['Hernan']/original['Hernan'],
           'Franky': sizes['Franky']/original['Franky'],
           'Tower': sizes['Tower']/original['Tower'],
           'Nexo': sizes['Nexo']/original['Nexo'],
           'Inhibidor': sizes['Inhibidor']/original['Inhibidor'],
           'Tienda': sizes['Tienda']/original['Tienda'],
           'MinionN': sizes['MinionN']/original['MinionN'],
           'MinionG': sizes['MinionG']/original['MinionG']}

# es el tamaño de la imagen en la que realmente debe topar

area_real = {'Tower': (200*porcent['Tower'], 298*porcent['Tower']),
             'Nexo': (280*porcent['Nexo'], 380*porcent['Nexo']),
             'Inhibidor': (300*porcent['Inhibidor'], 550*porcent['Inhibidor']),
             'Tienda': (270*porcent['Tienda'], 240*porcent['Tienda']),

             'MinionN': (50*porcent['MinionN'], 50*porcent['MinionN']),
             'MinionG': (40*porcent['MinionG'], 40*porcent['MinionG']),
             'Chau': (100*porcent['Chau'], 100*porcent['Chau']),
             'Hernan': (120*porcent['Hernan'], 120*porcent['Hernan']),
             'Franky': (230*porcent['Franky'], 230*porcent['Franky'])}


def get_offset(nombre):
    if nombre in ['Tower', 'Nexo', 'Inhibidor']:
        return ((real_size[nombre]-104)/2, 0)
    elif nombre in ['MinionN', 'MinionG']:
        return ((real_size[nombre]-54)/2, 0)
    else:
        return ((real_size[nombre]-104)/2, 0)


offsets = {'Chau': get_offset('Chau'), 'Hernan': get_offset('Hernan'),
           'Franky': get_offset('Franky'), 'Tower': get_offset('Tower'),
           'Nexo': get_offset('Nexo'), 'Inhibidor': get_offset('Inhibidor'),
           'Tienda': get_offset('Tienda'), 'MinionN': get_offset('MinionN'),
           'MinionG': get_offset('MinionG')}


def get_vertices(nombre):
    x, y = area_real[nombre]
    esq1 = ((real_size[nombre]-x)/2, (real_size[nombre]-y)/2)
    esq2 = (esq1[0]+x, esq1[1])
    esq3 = (esq1[0], esq1[1]+y)
    esq4 = (esq1[0]+x, esq1[1]+y)
    return [esq1, esq2, esq3, esq4]

vertices = {'Tower': get_vertices('Tower'),
            'Nexo': get_vertices('Nexo'),
            'Inhibidor': get_vertices('Inhibidor'),
            'Tienda': get_vertices('Tienda'),

            'MinionN': get_vertices('MinionN'),
            'MinionG': get_vertices('MinionG'),
            'Chau': get_vertices('Chau'),
            'Hernan': get_vertices('Hernan'),
            'Franky': get_vertices('Franky')}


parametros = {'Tienda': {'buy_range': 50},
              }

items = {"Arma de mano": [5, "damage", 2],
         "Arma de distancia": [5, "attack_range", 2],
         "Botas": [5, "move_speed", 2],
         "Baculo": [7, "sa_cooldown", 2],
         "Armadura": [5, "armor",  2],
         "Earthstone": [10, "random attribute", 6]}

tot_life = {'Tower': 250, 'Inhibidor': 600, 'Nexo': 1200}
