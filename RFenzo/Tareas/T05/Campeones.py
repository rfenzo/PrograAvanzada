from Funciones import closest_distance


def freeze(team_enemigo, hero):
    for thread in team_enemigo:
        thread.freeze = 10
    hero.sa_time = 0
    hero.mygame.sa_request(hero)


def earthquake(team_enemigo, hero):
    for thread in team_enemigo:
        d = closest_distance(hero.vertices, thread.vertices)
        if d <= 70:
            if thread.tipo in ['Tower', 'Nexo', 'Inhibidor']:
                thread.receive_dmg(thread)

            elif d <= 30:
                pos_t = thread.center
                pos_h = hero.center
                dist = (30*5/2)/(2**0.5)
                if pos_t[0] >= pos_h[0] and pos_t[1] >= pos_h[1]:
                    thread.pos = (pos_t[0]+dist, pos_t[1]+dist)
                elif pos_t[0] >= pos_h[0] and pos_t[1] < pos_h[1]:
                    thread.pos = (pos_t[0]+dist, pos_t[1]-dist)
                elif pos_t[0] < pos_h[0] and pos_t[1] < pos_h[1]:
                    thread.pos = (pos_t[0]-dist, pos_t[1]-dist)
                else:
                    thread.pos = (pos_t[0]-dist, pos_t[1]+dist)
    hero.mygame.sa_request(hero)
    hero.sa_time = 0


def lifesteal(target, hero):
    d = closest_distance(hero.vertices, target.vertices)
    if d <= hero.attack_range:
        target.downlife = 5
        hero.uplife = 5
        hero.sa_time = 0
        hero.mygame.sa_request(hero)
    else:
        hero.waiting_sa = True
        hero.left_click(target)


Chau = {'tipo': 'Chau', 'special_attack': freeze, 'sa_cooldown': 30,
        'move_speed': 30*3, 'damage': 5, 'attack_speed': 10,
        'attack_range': 40,
        'tot_life': 500, 'armor': 0, 'respawn': 10}

Hernan = {'tipo': 'Hernan', 'special_attack': earthquake, 'sa_cooldown': 40,
          'move_speed': 10*5, 'damage': 20, 'attack_speed': 4,
          'attack_range': 5, 'tot_life': 666, 'armor': 0, 'respawn': 10}

Franky = {'tipo': 'Franky', 'special_attack': lifesteal, 'sa_cooldown': 20,
          'move_speed': 15*5, 'damage': 10, 'attack_speed': 5,
          'attack_range': 5,
          'tot_life': 800, 'armor': 0, 'respawn': 10}
