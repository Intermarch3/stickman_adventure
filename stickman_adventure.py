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
- documentation
- bonus: 
    - music  et ecran victoire derniere clee
    - music shoot
"""

# variables globales et constantes
TILE_FLOOR = [(2, 3), (4, 3), (2, 6), (5, 2), (6, 2)]
TILE_WALL = [(4, 3), (5, 2), (6, 2)]
BREAK_BLOC_TILE = (6, 2)
WINDOW_SIZE = 128
HOME_LENGHT = int(23 * 8)
LVL_SIZE = [{
    'lvl': 1,
    'lenght': int(16 * 8),
    'height': int(16 * 8),
    'x': 0,
    'y': int(48 * 8),
    'player_pos': (4, int(14 * 8)),
    'enemie_pos': [[115, 70], [1, 35]],
    'breakeable_bloc': []
}, {
    'lvl': 2,
    'lenght': int(16 * 8),
    'height': int(16 * 8),
    'x': int(24 * 8),
    'y': int(48 * 8),
    'player_pos': (int(4), int(14 * 8)),
    'enemie_pos': [[2, 72], [119, 112], [18, 32], [62, 32]],
    'breakeable_bloc': []
}, {
    'lvl': 3,
    'lenght': int(16 * 8),
    'height': int(16 * 8),
    'x': int(48 * 8),
    'y': int(48 * 8),
    'player_pos': (4, int(14 * 8)),
    'enemie_pos': [[112, 112], [88, 80], [2, 48], [59, 56], [56, 32], [86, 16]],
    'breakeable_bloc': []
}]
KEY_TILE = (6, 1)
DOOR_TILE = [(0, 1), (1, 1)]
TRAMPO_TILE = (5, 2)
PLAYER_SPRITE = {
    "walk": [[0, 0], [16, 0], [24, 0], [16, 8], [24, 8], [24, 0], [0, 0]],
    "jump": [[32, 0], [40, 0], [32, 0], [0, 0]],
    "shoot": [[8, 8], [8, 0], [0, 0]]
}
ENEMIE_SPRITE = {
    'shoot': [[16, 16], [8, 16]],
    'idle': [0, 16]
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
    """ 
    Récupere la Title aux coordonné donné 
    args:
        tile_x (int): coordonné x de la tile
        tile_y (int): coordonné y de la tile
    return:
        (int, int): coordonné de la tile dans le tileset
    """
    return pyxel.tilemap(0).pget(tile_x, tile_y)


def cleanup_list(list):
    """
    netttoie une liste en supprimant les elements a detruire
    args:
        list (list): liste a nettoyer
    return:
        (list): liste nettoyé
    """ 
    i = 0
    while i < len(list):
        elem = list[i]
        if elem.is_alive:
            i += 1
        else:
            list.pop(i)
    return list


class Bullet:
    """
    class qui represente une balle tiré par un joueur ou ennemie
    parametres:
        x (int): coordonné x de la balle
        y (int): coordonné y de la balle
        dx (int): vitesse de deplacement de la balle sur l'axe x
        dy (int): vitesse de deplacement de la balle sur l'axe y
    methodes:
        trajectoire(): deplace la balle (actualise sa position)
        draw(): affiche la balle

    """
    def __init__(self, x, y, dx, dy=0):
        """ initialise les attributs de la classe """
        self.dx = dx
        self.dy = dy
        self.x = x
        self.y = y
        self.is_alive = True


    def trajectoire(self):
        """ deplace la balle (actualise sa position) """
        self.x += self.dx
        self.y += self.dy


    def draw(self):
        """ affiche la balle """
        pyxel.rect(self.x, self.y, 1, 1, 9)


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
        menu_door_detection(): detecte si le joueur touche la porte d'un level
        key_detection(): detecte si le joueur touche une clef
        break_bloc(): detruit un bloc cassable
        update_help_txt(): actualise le texte d'aide
        update_warn_txt(): actualise le texte d'avertissement
        warn(): affiche un texte d'avertissement
        help(): affiche un texte d'aide
        wall_detection(): detecte si le joueur touche un mur
        roof_detection(): detecte si le joueur touche le plafond
        cam_position(): actualise la position de la camera
        player_sprite(): actualise le sprite du joueur
        end_level(): gere la fin d'un level
        reset_txt(): remet a zero les textes d'aide et d'avertissement
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
        self.jump_force = 3.5
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
        self.nb_bullet = 100
        self.bullet_ls = []
        self.first_bullet = True
        # autre
        self.on_door = False
        self.menu = True
        self.level = 0
        self.vie = True
        self.fall = False
        self.win_level = False
        self.acces_level = 1
        self.cam_x = 0
        self.cam_y = 0
        self.breaking_bloc = []
        self.nb_break_bloc = 0
        self.mute = False
        # txt
        self.help_txt = ""
        self.warn_txt = ""
        self.help_txt_time = 0
        self.warn_txt_time = 0


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
            if self.on_door and self.level <= self.acces_level:
                self.menu = False
            elif self.on_door != True:
                self.warn("Not in front of door")
            elif self.level > self.acces_level:
                self.warn("No access")
        # tir
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btn(pyxel.KEY_V):
            self.shoot = True
            if self.dir == 1:
                x = self.x + 6
            else:
                x = self.x + 2
            if int(self.nb_shoot) == 0 and self.first_bullet:
                if self.nb_bullet > 0:
                    self.first_bullet = False
                    self.nb_bullet -= 1
                    self.bullet_ls.append(Bullet(x, self.y + 1, 2 * self.dir, 0))
                else:
                    self.warn("No bullet [R] to reset")
        # reset
        if pyxel.btn(pyxel.KEY_R) and self.menu == False:
            self.vie = False


    def floor_detection(self):
        """ detecte si le joueur touche le sol """
        # ajustement des coordonné en fonction du level
        if self.level != 0 and self.menu != True:
            y = self.y + LVL_SIZE[self.level - 1]['y'] - self.cam_y
        else:
            y = self.y - self.cam_y
        if self.level != 0 and self.menu != True:
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
            if get_tile(int(xi / 8), int((y + 8) / 8)) == TRAMPO_TILE:
                        self.player_dy = -7
                        self.on_floor = False
                        break
            if self.player_dy > 0:
                if get_tile(int(xi / 8), int((y + 8) / 8)) in TILE_FLOOR:
                    self.on_floor = True
                    self.player_dy = 0
                    self.y = int(self.y / 8) * 8
                    if get_tile(int(xi / 8), int((y + 8) / 8)) == BREAK_BLOC_TILE:
                        self.breaking_bloc.append([int(x / 8), int((y + 8) / 8), 30])
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
                            self.help("[DOWN] btn to enter level")
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
        # detection de la clee
        for xi in range(int(x), int(x + 8)):
            for yi in range(int(y), int(y + 8)):
                if get_tile(int(xi / 8), int(yi / 8)) == KEY_TILE:
                    if self.win_level != True:
                            self.win_level = True
                            self.acces_level = self.level + 1
                            break
                else:
                    self.win_level = False


    def break_bloc(self):
        """ casse les blocs cassable ou actualise le temps de casse """
        i = 0
        for bloc in self.breaking_bloc:
            if bloc[2] > 0:
                bloc[2] = bloc[2] - 1
            else:
                pyxel.tilemap(0).pset(bloc[0], bloc[1], (6, 3))
                self.breaking_bloc.pop(i)
                self.nb_break_bloc += 1
            i += 1


    def update_help_txt(self):
        """ actualise le texte d'aide """
        if self.help_txt_time > 0:
            self.help_txt_time -= 1
        elif self.help_txt_time <= 0 and self.help_txt != "":
            self.help_txt = ""


    def update_warn_txt(self):
        """ actualise le texte d'alerte """
        if self.warn_txt_time > 0:
            self.warn_txt_time -= 1
        elif self.warn_txt_time <= 0 and self.warn_txt != "":
            self.warn_txt = ""


    def warn(self, txt):
        """ affiche un texte d'alerte """
        self.warn_txt = txt
        self.warn_txt_time = 50
    

    def help(self, txt):
        """ affiche un texte d'aide """
        self.help_txt = txt
        self.help_txt_time = 50


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
        # ajustement des coordonne en fonction du level
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
        # actualisation de la position de la caméra en x
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
        """ reset valeur a la fin du level """
        self.x = 4
        self.y = 90
        self.menu = True
        self.help_txt = ""
        self.help_txt_time = 0


    def reset_txt(self):
        """ reset les textes """
        self.help_txt = ""
        self.warn_txt = ""
        self.warn_txt_time = 0
        self.help_txt_time = 0


    def update(self, cam_x, cam_y, mute):
        """ 
        actualisation des valeurs du joueur
        args:
            cam_x (int): position de la caméra en x
            cam_y (int): position de la caméra en y
            mute (bool): si le son est activer/desactiver
        retourne:
            - cam_x: position de la camera en x
            - cam_y: position de la camera en y
        """
        self.mute = mute
        # txt actualisation
        self.update_warn_txt()
        self.update_help_txt()
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
        self.break_bloc()
        # actualisation force deplacement gauche droite
        self.player_dx = max(self.player_dx - 1, 0)
        # actualisation des bullets
        for bullet in self.bullet_ls:
            bullet.trajectoire()
            if (bullet.x < -20 or bullet.x > 200):
                bullet.is_alive = False
        # suppresion des bullet inutile
        self.bullet_ls = cleanup_list(self.bullet_ls)
        if self.player_dy >= 6:
            self.fall = True
        if self.fall and self.on_floor:
            self.vie = False
            self.fall = False
        # actualisation nombre balle restante pour l'affichage
        if self.menu != True:
            self.help("Bullet:" + str(self.nb_bullet))
        return self.cam_x, self.cam_y


    def draw(self):
        """ affichage du joueur """
        pyxel.blt(self.x, self.y, 0, self.sprite[0], self.sprite[1], 8 * self.dir, 8, 0)
        # affichage des balle du joueur
        for bullet in self.bullet_ls:
            bullet.draw()


class Ennemie:
    """ 
    ennemie class 
    attributs:
        x (int): position en x
        y (int): position en y
        sprite_ls (list): liste de sprite de l'ennemie
        level (int): niveau ou se trouve l'ennemie
    methodes:
        update(): actualisation des valeurs de l'ennemie
        draw(): affichage de l'ennemie
        deplacement(): deplacement et collision de l'ennemie sur l'axe y
        player_sprite(): actualisation des sprite de l'ennemie
    """
    def __init__(self, x, y, sprite_ls, level):
        """ initialisation des valeurs de l'ennemie """
        # attributs de position
        self.x = x
        self.y = y
        self.dir = 1
        # attributs de force (vitesse, graviter, ...)
        self.gravity = 0.45
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
        self.level = level
        self.is_alive = True
        # tire
        self.bullet_ls = []
        self.sprite = []
        self.first_bullet = True
        self.time_to_fire = 0


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
            self.sprite = self.sprite_ls['idle']


    def deplacement(self):
        """ deplacement et collision de l'ennemie sur l'axe y """
        # changement des coordonnés en fonction du level
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
        """ actualisation des valeurs de l'ennemie """
        # actualisation des valeurs de deplacement
        self.player_dy = min(self.player_dy + self.gravity, 8)
        self.y += self.player_dy
        self.deplacement()
        # actualisation de la mecanique de tire
        self.time_to_fire -= 1
        if self.time_to_fire <= 0:
            dx = player_x - self.x
            dy = player_y - self.y
            sq_dist = dx * dx + dy * dy
            if sq_dist < 40**2 and dy < 15:
                try:
                    self.dir = int(dx / abs(dx))
                except:
                    pass
                dist = pyxel.sqrt(sq_dist)
                self.shoot = True
                if self.dir == 1:
                    x = self.x + 6
                else:
                    x = self.x + 2
                if int(self.nb_shoot) == 0 and self.first_bullet:
                    self.first_bullet = False
                    self.bullet_ls.append(Bullet(x, self.y + 1, (dx / dist) * 1.5, (dy / dist) * 1.5))
                self.time_to_fire = 70
        # actualisation des sprites
        self.player_sprite()
        # actualisation des bullets
        for bullet in self.bullet_ls:
            bullet.trajectoire()
            if bullet.x < -100 or bullet.x > 1000:
                bullet.is_alive = False
        self.bullet_ls = cleanup_list(self.bullet_ls)


    def draw(self):
        """ affichage du joueur """
        pyxel.blt(self.x, self.y, 0, self.sprite[0], self.sprite[1], 8 * self.dir, 8, 0)
        # affichage des balle du joueur
        for bullet in self.bullet_ls:
            bullet.draw()


class Map:
    """ 
    classe pour les maps
    methodes:
        draw(): affichage de la bonne map
        draw_menu(): affichage du menu
        draw_level(): affichage du level
    """
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
        # affichage du menu
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
        """ 
        actualisation de la map 
        args:
            menu (bool): bool pour savoir si on est dans le menu
            level (int): level en cours
        """
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
        p (Player): une instance du joueur
    - - - - - - - - - - 
    Methode:
        update(): actualise le jeu
        draw(): affiche le jeu
        spawn_enemy(): spawn les ennemie du niveau
        player_bullet_detection(): detection des collision bullets du joueur sur les ennemies
        enemy_bullet_detection(): detection des collision bullets des ennemies sur le joueur
        get_break_bloc(): fait un inventaire des blocs cassable du niveau
        set_break_bloc(): repositionne les bloc cassable du niveau en cours
        display_help_txt(): affiche le text d'aide
        display_warn_txt(): affiche le text d'avertissement
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
        self.first_enter_level = [True, True, True]
        self.help_txt_pos = [3, 3]
        self.warn_txt_pos = [3, 10]
        self.mute = False
        self.time_mute = 15
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)


    def spawn_enemy(self):
        """ spawn les ennemie du niveau """
        for x, y in LVL_SIZE[self.p.level - 1]['enemie_pos']:
            self.enemies.append(Ennemie(x, y, ENEMIE_SPRITE, self.p.level))


    def player_bullet_detection(self):
        """ detection des collision bullets du joueur sur les ennemies """
        for bullet in self.p.bullet_ls:
            for enemie in self.enemies:
                if abs(bullet.x - (enemie.x + 3)) < 3 and abs(bullet.y - (enemie.y + 3)) < 4:
                    if not self.mute:
                        pyxel.play(3, 10)
                    enemie.is_alive = False
                    bullet.is_alive = False


    def enemie_bullet_detection(self):
        """ detection des collision bullets des ennemies sur le joueur """
        for enemie in self.enemies:
            for bullet in enemie.bullet_ls:
                if abs(bullet.x - (self.p.x + 3)) < 3 and abs(bullet.y - (self.p.y + 4)) < 4:
                    self.p.vie = False

    
    def get_break_bloc(self):
        """ fait un inventaire des blocs cassable du niveau """
        global LVL_SIZE
        x = LVL_SIZE[self.p.level - 1]['lenght'] + LVL_SIZE[self.p.level - 1]['x']
        y = LVL_SIZE[self.p.level - 1]['height'] + LVL_SIZE[self.p.level - 1]['y']
        for xi in range(LVL_SIZE[self.p.level - 1]['x'], x):
            for yi in range(LVL_SIZE[self.p.level - 1]['y'], y):
                if get_tile(int(xi / 8), int(yi / 8)) == BREAK_BLOC_TILE:
                    LVL_SIZE[self.p.level - 1]['breakeable_bloc'].append([int(xi / 8), int(yi / 8)])


    def set_break_bloc(self):
        """ repositionne les bloc cassable du niveau en cours """
        for bloc in LVL_SIZE[self.p.level - 1]['breakeable_bloc']:
            pyxel.tilemap(0).pset(bloc[0], bloc[1], BREAK_BLOC_TILE)


    def display_help_txt(self):
        """ affiche le text d'aide """
        pyxel.text(self.help_txt_pos[0], self.help_txt_pos[1], self.p.help_txt, 7)


    def display_warning_txt(self):
        """ affiche le text d'avertissement """
        pyxel.text(self.warn_txt_pos[0], self.warn_txt_pos[1], self.p.warn_txt, 8)


    def update(self):
        """ actualisation des elements du jeu """
        # tant que le joueur n'a pas gagner tous les niveaux
        if self.p.acces_level < len(LVL_SIZE) + 1:
            # actualisation son et music
            self.time_mute -= 1
            if self.time_mute < 0:
                if pyxel.btn(pyxel.KEY_M) and self.mute:
                    self.mute = False
                    pyxel.playm(0, loop=True)
                    self.time_mute = 15
                elif pyxel.btn(pyxel.KEY_M) and not self.mute:
                    self.mute = True
                    self.time_mute = 15
            if self.mute:
                pyxel.stop()
            # bullet detection
            self.player_bullet_detection()
            self.enemie_bullet_detection()
            # help txt
            if len(LVL_SIZE[self.p.level - 1]['breakeable_bloc']) > 0 and \
            self.p.nb_break_bloc >= len(LVL_SIZE[self.p.level - 1]['breakeable_bloc']):
                self.p.help("[R] to reset lvl")
            # actualisation du joueur et de la position de la camera
            self.map.cam_x, self.map.cam_y = self.p.update(self.map.cam_x, self.map.cam_y, self.mute)
            # fin d'un level
            if self.p.win_level:
                self.end_level = True
            if self.p.menu:
                self.menu = True
            else:
                self.menu = False
            # actualisation de la map
            self.map.update(self.p.menu, self.p.level)
            # actualisation quand le joueur meurt
            if self.p.vie != True:
                self.enter_level = True
                self.p.vie = True
                self.p.breaking_bloc = []
                self.p.bullet_ls = []
                self.p.nb_break_bloc = 0
                if not self.mute:
                    pyxel.play(3, 9)
            # actualisation entrer dans un level
            if self.p.level != 0 and self.menu != True and self.enter_level:
                self.p.nb_bullet = len(LVL_SIZE[self.p.level - 1]['enemie_pos']) + 2
                self.p.reset_txt()
                if self.first_enter_level[self.p.level - 1]:
                    self.get_break_bloc()
                    self.first_enter_level[self.p.level - 1] = False
                self.enemies = []
                self.map.cam_x = 0
                self.map.cam_y = 0
                self.set_break_bloc()
                self.enter_level = False
                self.p.x = LVL_SIZE[self.p.level - 1]['player_pos'][0]
                self.p.y = LVL_SIZE[self.p.level - 1]['player_pos'][1]
                self.spawn_enemy()
            # actualisation fin d'un level
            if self.end_level:
                self.end_level = False
                self.menu = True
                self.p.end_level()
                self.map.cam_x, self.map.cam_y = 0, 0
                self.enter_level = True
                self.enemies = []
                self.p.nb_bullet = 100
            # update enemies
            for enemie in self.enemies:
                enemie.update(self.p.x, self.p.y)
            self.enemies = cleanup_list(self.enemies)


    def draw(self):
        """ affichage des elements du jeu """
        pyxel.cls(0)
        # tant que le joueur n'a pas gagner tous les niveaux
        if self.p.acces_level < len(LVL_SIZE) + 1:
            # affichage de la map
            self.map.draw()
            # affichage du joueur
            self.p.draw()
            # affichage enemies
            for enemie in self.enemies:
                enemie.draw()
            # display txt
            self.display_help_txt()
            self.display_warning_txt()
        else:
            pyxel.rect(0, 0, 255, 255, 1)
            pyxel.text(40, 55, "Victoire !!!", 7)
            pyxel.text(10, 65, "[ECHAP] pour quitter le jeu", 13)


if __name__ == '__main__':
    # initialisation fenetre
    pyxel.init(WINDOW_SIZE, WINDOW_SIZE, "| STICKMAN ADVENTURE 2D |")
    pyxel.mouse(False)
    # importation map, sprite, music
    pyxel.load("stickman_adventure.pyxres")
    # création d'une instance de Jeu
    Jeu(Player(PLAYER_SPRITE))
