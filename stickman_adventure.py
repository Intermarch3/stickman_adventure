##################################
#                                #
#   name: stickman_adventure_2D  #
#   author: Lucas L              #
#   date: 11/2022                #
#                                #
##################################

import pyxel

"""
TODO:
- ennemies (attaque, affichage, update ...)
- documentation
- creation music et effets musicals
- joueur meur par dega chute
- joueur meur par Bullete ennemies
- bloc floor qui se casse
- initialisation level (bloc casse, ennemies ...)
...
"""

# Constantes
TILE_FLOOR = [(2, 3), (4, 3), (2, 6), (8, 0), (9, 0), (8, 1), (8, 2), (8, 3), (9, 1), (9, 2), (9, 3), (9, 4)]
TILE_WALL = [(4, 3), (8, 1), (8, 2), (8, 3), (9, 1), (9, 2), (9, 3), (9, 4)]
WINDOW_SIZE = 128
HOME_LENGHT = int(23 * 8)
LVL_SIZE = [{
    'lvl': 1,
    'lenght': int(16 * 8),
    'height': int(16 * 8),
    'x': 0,
    'y': int(48 * 8),
    'player_pos': (4, int(14 * 8))
}, {
    'lvl': 2,
    'lenght': int(16 * 8),
    'height': int(16 * 8),
    'x': 0,
    'y': int(48 * 8),
    'player_pos': (4, int(14 * 8))
}, {
    'lvl': 3,
    'lenght': int(16 * 8),
    'height': int(16 * 8),
    'x': 0,
    'y': int(48 * 8),
    'player_pos': (4, int(14 * 8))
}]
KEY_TILE = (6, 1)
DOOR_TILE = [(0, 1), (1, 1)]
ENEMIE_TILE = [16, 16]
PLAYER_SPRITE = {
    "walk": [[0, 0], [16, 0], [24, 0], [16, 8], [24, 8], [24, 0], [0, 0]],
    "jump": [[32, 0], [40, 0], [32, 0], [0, 0]],
    "shoot": [[8, 8], [8, 0], [0, 0]]
}
TEXT_LVL = [{
    "x": (2 * 8) + 3,
    "y": (12 * 8) + 2,
    "txt": "_1_"
}, {
    "x": (8 * 8) + 3,
    "y": (12 * 8) + 2,
    "txt": "_2_"
}, {
    "x": (16 * 8) + 3,
    "y": (12 * 8) + 2,
    "txt": "_3_"
}]


def get_tile(tile_x, tile_y):
    """ Récupere la Title aux coordonné donné """
    return pyxel.tilemap(0).pget(tile_x, tile_y)


class Bullet:
    def __init__(self, x, y, dx=5, dy=0):
        self.dir = dir
        self.dx = dx
        self.dy = dy
        self.x = x
        self.y = y
        self.is_alive = True


    def trajectoire(self):
        self.x += self.dx
        self.y += self.dy


    def draw(self):
        pyxel.rect(self.x, self.y, 1, 1, 8)


class Player:
    """
    class Player qui controle le joueur principal
    - - - - - - - - - -
    parametre:
        sprite_ls: dictionnaire des sprites du joueur en fonction de son statue
    - - - - - - - - - -
    Methode:
        deplacement(): gere les deplacement en fonction des touches presser
        update(): actualise les valeurs (position, direction ...)
        draw(): affiche le joueur
        floor_detection(): detecte si le joueur touche le sol
    
    """
    def __init__(self, sprite_ls):
        """ initialisation des attributs """
        assert type(sprite_ls) == dict
        # attributs de position
        self.x = 4
        self.y = 90
        self.dir = 1
        # attributs de force (vitesse, graviter, ...)
        self.speed = 0.5
        self.jump_force = 3.2
        self.player_dy = 0
        self.player_dx = 0
        # attributs des sprites
        self.sprite_ls = sprite_ls
        # pour la marche
        self.walk_liste = sprite_ls["walk"]
        self.nb_walk = 0
        self.sprite = self.walk_liste[0]
        # pour le saut
        self.jump_liste = sprite_ls["jump"]
        self.nb_jump = 0
        self.on_floor = True
        self.gravity = 0.45 # 0.45
        # pour le tir
        self.shoot_liste = sprite_ls["shoot"]
        self.nb_shoot = 0
        self.shoot = False
        # autre
        self.on_door = False
        self.menu = True
        self.level = 0
        self.vie = True
        self.win_level = False
        self.cam_x = 0
        self.cam_y = 0
        # tire
        self.tire_ls = []
        self.first_bullet = True


    def deplacement(self):
        """ controle des directions du joueur """
        # deplacement à droite
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) and self.x < 124:
            self.player_dx = 1
            self.dir = 1
            if self.nb_walk > len(self.walk_liste) - 1:
                self.nb_walk = 0
            else:
                self.nb_walk += self.speed
        # deplacement à gauche
        elif pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q) and self.x > 0:
            self.player_dx = -1
            self.dir = -1
            if self.nb_walk > len(self.walk_liste) - 1:
                self.nb_walk = 0
            else:
                self.nb_walk += self.speed
        # saut
        if pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.KEY_UP):
            if self.on_floor:
                self.on_floor = False
                self.player_dy = self.jump_force * -1
        if pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_DOWN):
            if self.on_door:
                self.menu = False
        # tir
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btn(pyxel.KEY_V):
            self.shoot = True
            if self.dir == 1:
                x = self.x + 6
            else:
                x = self.x + 2
            if int(self.nb_shoot) == 0 and self.first_bullet:
                self.first_bullet = False
                self.tire_ls.append(Bullet(x, self.y + 1))


    def floor_detection(self):
        """ detecte si le joueur touche le sol """
        # ajustement des coordonné en fonction du level
        if self.level != 0 and self.menu != True:
            y = self.y + LVL_SIZE[self.level - 1]['y'] - self.cam_y
        else:
            y = self.y - self.cam_y
        if self.level != 0:
            x = self.x + LVL_SIZE[self.level - 1]['x'] - self.cam_x
        else:
            x = self.x - self.cam_x
        # ajustement des coordonné en fonction de l'orientation
        left, right = 0, 0
        if self.dir == 1:
            left = -3
        else:
            right = 3
        # detection du sol
        for xi in range(int(x + right), int(x + 8 + left)):
            if self.player_dy > 0:
                if get_tile(int(xi / 8), int((y + 8) / 8)) in TILE_FLOOR:
                    self.on_floor = True
                    self.player_dy = 0
                    self.y = int(self.y / 8) * 8
                    break
                else:
                    self.on_floor = False


    def menu_door_detection(self):
        """ détecte si le joueur est en face d'une porte de niveau """
        for x in range(int((self.x - self.cam_x)/ 8), int((self.x + 8 - self.cam_x) / 8)):
            for y in range(int((self.y - self.cam_y) / 8), int((self.y + 8 - self.cam_y) / 8)):
                if get_tile(x, y) in DOOR_TILE:
                    self.on_door = True
                    for lvl in TEXT_LVL:
                        if self.x - self.cam_x >= lvl['x'] - 3 and self.x - self.cam_x <= lvl['x'] + 5:
                            self.level = int(lvl['txt'].replace("_", ""))
                else:
                    self.on_door = False


    def key_detection(self):
        """ detecte si le joueur attrape la clee du niveau """
        # ajustement des coordonné en fonction du level
        if self.level != 0 and self.menu != True:
            y = self.y + LVL_SIZE[self.level - 1]['y'] - self.cam_y
        else:
            y = self.y - self.cam_y
        if self.level != 0:
            x = self.x + LVL_SIZE[self.level - 1]['x'] - self.cam_x
        else:
            x = self.x - self.cam_x
        for xi in range(int(x), int(x + 8)):
            for yi in range(int(y), int(y + 8)):
                if get_tile(int(xi / 8), int(yi / 8)) == KEY_TILE:
                    if self.win_level != True:
                            self.win_level = True
                            break
                else:
                    self.win_level = False


    def wall_detection(self):
        """ detecte si le joueur touche un mur """
        # ajustement des coordonne en fonction du level
        if self.level != 0 and self.menu != True:
            y = self.y + LVL_SIZE[self.level - 1]['y'] - self.cam_y
        else:
            y = self.y - self.cam_y
        if self.level != 0:
            x = self.x + LVL_SIZE[self.level - 1]['x'] - self.cam_x
        else:
            x = self.x - self.cam_x
        # quand avance a droite
        if self.player_dx > 0:
            for yi in range(int(y), int(y + 8)):
                if get_tile(int((x + 6) / 8), int(yi / 8)) in TILE_WALL:
                    self.player_dx = 0
                    self.x = int(self.x / 8) * 8 + 2
                    break
        # quand avance a gauche
        elif self.player_dx < 0:
            for yi in range(int(y), int(y + 8)):
                if get_tile(int((x + 3) / 8), int(yi / 8)) in TILE_WALL:
                    self.player_dx = 0
                    self.x = int(self.x / 8) * 8 + 5
                    break


    def roof_detection(self):
        """ detecte si le joueur tape sur un bloc par le haut """
        if self.level != 0 and self.menu != True:
            y = self.y + LVL_SIZE[self.level - 1]['y'] - self.cam_y
        else:
            y = self.y - self.cam_y
        if self.level != 0:
            x = self.x + LVL_SIZE[self.level - 1]['x'] - self.cam_x
        else:
            x = self.x - self.cam_x
        # ajustement des coordonné en fonction de l'orientation
        left, right = 0, 0
        if self.dir == 1:
            left = -3
        else:
            right = 3
        # detection du toit
        if self.player_dy < 0:
            for xi in range(int(x + right), int(x + 8 + left)):
                if get_tile(int(xi / 8), int(y / 8)) in TILE_WALL:
                    self.player_dy = 0
                    self.y = int((self.y + 8) / 8) * 8
                    break


    def cam_position(self):
        """ actualisation position caméra """
        # change lenght quand il est dans le menu ou dans un level
        if self.menu:
            lenght = HOME_LENGHT
        else:
            lenght = LVL_SIZE[self.level - 1]['lenght'] - 8
        if self.x > WINDOW_SIZE * 0.8 and 17 + self.x - self.cam_x < lenght:
            self.x = WINDOW_SIZE * 0.8
            self.cam_x -= self.player_dx
        elif self.x < WINDOW_SIZE * 0.2 and self.cam_x < 0:
            self.x = WINDOW_SIZE * 0.2
            self.cam_x -= self.player_dx
        if self.x < - 2:
            self.x = - 2
        if self.x > WINDOW_SIZE - 6:
            self.x = WINDOW_SIZE - 6


    def player_sprite(self):
        """ actualisation des sprite du joueur """
        # quand il marche
        if pyxel.btnp(pyxel.KEY_LEFT, True, True) or pyxel.btnp(pyxel.KEY_RIGHT, True, True):
            self.sprite = self.walk_liste[int(self.nb_walk)]
        else:
            self.sprite = self.walk_liste[0]
        # quand il saute
        if self.on_floor == False:
            if self.nb_jump >= len(self.jump_liste) - 1:
                self.nb_jump = 0
            else:
                self.nb_jump += 0.1
            self.sprite = self.jump_liste[int(self.nb_jump)]
        # quand il tire
        if self.shoot:
            if self.nb_shoot >= len(self.shoot_liste) - 1:
                self.nb_shoot = 0
                self.shoot = False
                self.first_bullet = True
            else:
                self.nb_shoot += 0.1
            self.sprite = self.shoot_liste[int(self.nb_shoot)]


    def end_level(self):
        self.x = 4
        self.y = 90
        self.menu = True


    def update(self, cam_x, cam_y):
        """ 
        actualisation des valeurs et affichage joueur 
        retourne:
            - cam_x: position de la camera en x
            - cam_y: position de la camera en y
        """
        # detection des porte dans le menu
        if self.menu:
            self.menu_door_detection()
        # actualisation des deplacements du joueur
        self.deplacement()
        # actualisation des sprites
        self.player_sprite()
        #actualisation position joueur
        self.x += self.player_dx
        self.y += self.player_dy
        self.cam_x, self.cam_y = cam_x, cam_y
        self.cam_position()
        #actualisation force saut et chute
        self.player_dy = min(self.player_dy + self.gravity, 8)
        #actualisation des colisions
        self.floor_detection()
        self.wall_detection()
        self.roof_detection()
        self.key_detection()
        # actualisation force deplacement gauche droite
        self.player_dx = max(self.player_dx - 1, 0)
        # actualisation des bullets
        i = 0
        for bullet in self.tire_ls:
            bullet.trajectoire()
            if (self.tire_ls[i].x < -100 or self.tire_ls[i].x > 1000) or self.tire_ls[i].is_alive != True:
                self.tire_ls.pop(i)
            i += 1
        return self.cam_x, self.cam_y


    def draw(self):
        """ affichage du joueur """
        pyxel.blt(self.x, self.y, 0, self.sprite[0], self.sprite[1], 8 * self.dir, 8, 0)
        # affichage des balle du joueur
        for bullet in self.tire_ls:
            bullet.draw()


class Ennemie:
    """ ennemie class """
    def __init__(self, x, y, sprite_ls, level):
        self.x = x
        self.y = y
        self.time_to_fire = 0
        self.is_alive = True
        self.dir = 1
        self.gravity = 0.45
        self.level = level
        # attributs de force (vitesse, graviter, ...)
        self.player_dy = 0
        self.player_dx = 0
        # attributs des sprites
        self.sprite_ls = sprite_ls
        # pour le tir
        self.shoot_liste = sprite_ls["shoot"]
        self.nb_shoot = 0
        self.shoot = False
        # autre
        self.cam_x = 0
        self.cam_y = 0
        # tire
        self.tire_ls = []
        self.sprite = []
        self.first_bullet = True
    
    
    def player_sprite(self):
        """ actualisation des sprite du joueur """
        if self.shoot:
            if self.nb_shoot >= len(self.shoot_liste) - 1:
                self.nb_shoot = 0
                self.shoot = False
                self.first_bullet = True
            else:
                self.nb_shoot += 0.1
            self.sprite = self.shoot_liste[int(self.nb_shoot)]
        else:
            self.sprite = [0, 0]


    def deplacement(self):
        y = self.y + LVL_SIZE[self.level - 1]['y'] - self.cam_y
        x = self.x + LVL_SIZE[self.level - 1]['x'] - self.cam_x
        # ajustement des coordonné en fonction de l'orientation
        left, right = 0, 0
        if self.dir == 1:
            left = -3
        else:
            right = 3
        # detection du sol
        for xi in range(int(x + right), int(x + 8 + left)):
            if self.player_dy > 0:
                if get_tile(int(xi / 8), int((y + 8) / 8)) in TILE_FLOOR:
                    self.on_floor = True
                    self.player_dy = 0
                    self.y = int(self.y / 8) * 8
                    break
                else:
                    self.on_floor = False


    def update(self, player_x, player_y):
        self.player_dy = min(self.player_dy + self.gravity, 8)
        self.y += self.player_dy
        self.deplacement()
        self.time_to_fire -= 1
        if self.time_to_fire <= 0:
            dx = player_x - self.x
            dy = player_y - self.y
            sq_dist = dx * dx + dy * dy
            if sq_dist < 60**2:
                dist = pyxel.sqrt(sq_dist)
                self.shoot = True
                if self.dir == 1:
                    x = self.x + 6
                else:
                    x = self.x + 2
                if int(self.nb_shoot) == 0 and self.first_bullet:
                    self.first_bullet = False
                    self.tire_ls.append(Bullet(x, self.y + 1, dx / dist, dy / dist))
                self.time_to_fire = 60
        self.player_sprite()
        i = 0
        for bullet in self.tire_ls:
            bullet.trajectoire()
            if (self.tire_ls[i].x < -100 or self.tire_ls[i].x > 1000) or self.tire_ls[i].is_alive != True:
                self.tire_ls.pop(i)
            i += 1


    def draw(self):
        """ affichage du joueur """
        pyxel.blt(self.x, self.y, 0, self.sprite[0], self.sprite[1], 8 * self.dir, 8, 0)
        # affichage des balle du joueur
        for bullet in self.tire_ls:
            bullet.draw()


class Map:
    """ classe pour les maps """
    def __init__(self):
        """ 
        initialisation de la map 
        parametre:
            - level: level en cours
        """
        self.level = 0
        self.menu = True
        self.cam_x = 0
        self.cam_y = 0


    def draw_menu(self):
        """ affichage du menu """
        # affichage lune
        pyxel.blt(96 + self.cam_x * 0.7, 24, 2, 0, 40, 16, 16, 0)
        # affichage de la map
        pyxel.bltm(self.cam_x, self.cam_y, 0, 0, 0, 256, 256, 0)
        # affichage txt level
        if self.menu:
            for lvl in TEXT_LVL:
                pyxel.text(lvl['x'] + self.cam_x, lvl['y'] + self.cam_y, lvl["txt"], 7)


    def draw_level(self):
        """ affichage du level """
        pyxel.bltm(self.cam_x, self.cam_y, 0, \
                LVL_SIZE[self.level - 1]['x'], LVL_SIZE[self.level - 1]['y'], \
                LVL_SIZE[self.level - 1]['lenght'], LVL_SIZE[self.level - 1]['height'], 0)


    def update(self, menu, level):
        """ actualisation de la map """
        self.menu = menu
        self.level = level


    def draw(self):
        """ affichage de la map """
        if self.menu:
            self.draw_menu()
        else:
            self.draw_level()



class Jeu:
    """
    class Jeu qui actualise le joueur et la fenetre
    - - - - - - - - - - 
    Attributs:
        p: le joueur (Player)
    - - - - - - - - - - 
    Methode:
        update(): actualise le jeu
        draw(): affiche le jeu
    """
    def __init__(self, player):
        """ initialisation du joueur et de la fenetre """
        assert type(player) == Player, "mauvais parametre"
        self.p = player
        self.map = Map()
        self.menu = True
        self.enter_level = True
        self.end_level = False
        self.enemies = []
        pyxel.run(self.update, self.draw)

    # a voire
    def spawn_enemy(self):
        for x in range(LVL_SIZE[self.p.level - 1]['x'], LVL_SIZE[self.p.level - 1]['x'] + LVL_SIZE[self.p.level - 1]['lenght']):
            for y in range(LVL_SIZE[self.p.level - 1]['y'], LVL_SIZE[self.p.level - 1]['y'] + LVL_SIZE[self.p.level - 1]['height']):
                tile = get_tile(x / 8, y / 8)
                if tile == ENEMIE_TILE:
                    self.enemies.append(Ennemie(x * 8, y * 8, self.p.sprite_ls, self.p.level))


    def update(self):
        """ actualisation des elements du jeu """
        # actualisation du joueur et de la position de la camera
        self.map.cam_x, self.map.cam_y = self.p.update(self.map.cam_x, self.map.cam_y)
        # fin d'un level
        if self.p.win_level:
            self.end_level = True
        if self.p.menu:
            self.menu = True
        else:
            self.menu = False
        # actualisation de la map
        self.map.update(self.p.menu, self.p.level)
        # actualisation entrer dans un level
        if self.p.level != 0 and self.menu != True and self.enter_level:
            self.map.cam_x = 0
            self.map.cam_y = 0
            self.enter_level = False
            self.p.x = LVL_SIZE[self.p.level - 1]['player_pos'][0]
            self.p.y = LVL_SIZE[self.p.level - 1]['player_pos'][1]
            self.spawn_enemy()
        if self.end_level:
            self.end_level = False
            self.menu = True
            self.p.end_level()
            self.map.cam_x, self.map.cam_y = 0, 0
            self.enter_level = True
        # update enemies
        for enemie in self.enemies:
            enemie.update(self.p.x, self.p.y)


    def draw(self):
        """ affichage des elements du jeu """
        pyxel.cls(0)
        # affichage de la map
        self.map.draw()
        # affichage du joueur
        self.p.draw()
        # affichage enemies
        for enemie in self.enemies:
            enemie.draw()


if __name__ == '__main__':
    # initialisation fenetre
    pyxel.init(WINDOW_SIZE, WINDOW_SIZE, "STICKMAN ADVENTURE 2D")
    pyxel.mouse(False)
    # importation map, sprite, music
    pyxel.load("stickman_adventure.pyxres")
    # création d'une instance de Jeu
    Jeu(Player(PLAYER_SPRITE))
