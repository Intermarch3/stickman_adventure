##################################
#                                #
#   name: stickman_adventure_2D  #
#   author: Lucas L              #
#   date: 11/2022                #
#                                #
##################################

import pyxel


"""
A faire:
- colision avec les murs et le sol dans les level
- affichage ennemie
...
"""

# Constantes
TILE_FLOOR = [(2, 3), (4, 3)]
WINDOW_SIZE = 128
HOME_LENGHT = int(23 * 8)
LVL_SIZE = [{
    'lvl': 1,
    'lenght': int(16 * 8),
    'height': int(16 * 8),
    'x': 0,
    'y': int(48 * 8),
    'player_pos': (4, int(14 * 8))
}]
DOOR_TILE = [(0, 1), (1, 1)]
PLAYER_SPRITE = {
    "walk": [[0, 0], [16, 0], [24, 0], [16, 8], [24, 8], [24, 0], [0, 0]],
    "jump": [[32, 0], [40, 0], [32, 0], [0, 0]],
    "shoot": []
}
TEXT_LVL = [{
    "x": (2 * 8) + 3,
    "y": (12 * 8) + 2,
    "txt": "_1_"
},
{
    "x": (8 * 8) + 3,
    "y": (12 * 8) + 2,
    "txt": "_2_"
},
{
    "x": (16 * 8) + 3,
    "y": (12 * 8) + 2,
    "txt": "_3_"
}]


def get_tile(tile_x, tile_y):
    """ Récupere la Title aux coordonné donné """
    return pyxel.tilemap(0).pget(tile_x, tile_y)


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
        self.jump_force = 3
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
        self.gravity = 0.5
        # statue
        self.on_door = False
        self.menu = True
        self.level = 0


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


    def floor_detection(self):
        """ detecte si le joueur touche le sol """
        if get_tile(int(self.x / 8), int((self.y + 8) / 8)) in TILE_FLOOR:
            self.on_floor = True
            self.player_dy = 0
            self.y = int(self.y / 8) * 8

    def menu_door_detection(self):
        """ détecte si le joueur est en face d'une porte de niveau """
        for x in range(int(self.x / 8), int((self.x + 8) / 8)):
            for y in range(int(self.y / 8), int((self.y + 8) / 8)):
                if get_tile(x, y) in DOOR_TILE:
                    self.on_door = True
                    for lvl in TEXT_LVL:
                        if self.x >= lvl['x'] - 3 and self.x <= lvl['x'] + 5:
                            self.level = int(lvl['txt'].replace("_", ""))
                else:
                    self.on_door = False


    # voire si fonctionne
    def wall_detection(self):
        """ detecte si le joueur touche un mur """
        if get_tile(int((self.x + 8) / 8), int(self.y / 8)) == TILE_FLOOR:
            self.player_dx = 0
            self.x = int(self.x / 8) * 8
    

    def cam_position(self, cam_x, cam_y):
        """ actualisation position caméra """
        # change lenght quand il est dans le menu ou dans un level
        if self.menu:
            lenght = HOME_LENGHT
        else:
            lenght = LVL_SIZE[0]['lenght'] - 8
        if self.x > WINDOW_SIZE * 0.8 and 17 + self.x - cam_x < lenght:
            self.x = WINDOW_SIZE * 0.8
            cam_x -= self.player_dx
        elif self.x < WINDOW_SIZE * 0.2 and cam_x < 0:
            self.x = WINDOW_SIZE * 0.2
            cam_x -= self.player_dx
        if self.x < - 2:
            self.x = - 2
        if self.x > WINDOW_SIZE - 6:
            self.x = WINDOW_SIZE - 6
        return cam_x, cam_y


    def update(self, cam_x, cam_y):
        """ 
        actualisation des valeurs et affichage joueur 
        retourne:
            - cam_x: position de la camera en x
            - cam_y: position de la camera en y
        """
        self.menu_door_detection()
        # actualisation des deplacements du joueur
        self.deplacement()
        # actualisation des sprites du joueur quand il marche
        if pyxel.btnp(pyxel.KEY_LEFT, True, True) or pyxel.btnp(pyxel.KEY_RIGHT, True, True):
            self.sprite = self.walk_liste[int(self.nb_walk)]
        else:
            self.sprite = self.walk_liste[0]
        # actualisation des sprites du joueur quand il saute
        if self.on_floor == False:
            if self.nb_jump >= len(self.jump_liste) - 1:
                self.nb_jump = 0
            else:
                self.nb_jump += 0.1
            self.sprite = self.jump_liste[int(self.nb_jump)]
        #actualisation position joueur
        self.x += self.player_dx
        self.y += self.player_dy
        cam_x, cam_y = self.cam_position(cam_x, cam_y)
        #actualisation force deplacement
        self.player_dx = max(self.player_dx - 1, 0)
        self.player_dy = min(self.player_dy + self.gravity, 8)
        #actualisation detection du sol
        self.floor_detection()
        return cam_x, cam_y


    def draw(self):
        """ affichage du joueur """
        pyxel.blt(self.x, self.y, 0, self.sprite[0], self.sprite[1], 8 * self.dir, 8, 0)


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
        self.p = player
        self.menu = True
        self.cam_x = 0
        self.cam_y = 0
        self.level = 0
        self.enter_level = True
        pyxel.run(self.update, self.draw)


    def update(self):
        """ actualisation des elements du jeu """
        # actualisation du joueur
        self.cam_x, self.cam_y = self.p.update(self.cam_x, self.cam_y)
        if self.menu:
            self.menu = self.p.menu
        if self.level == 0:
            self.level = self.p.level
        elif self.level != 0 and self.menu != True and self.enter_level:
            self.enter_level = False
            self.p.x, self.p.y = LVL_SIZE[self.level - 1]['player_pos'][0], LVL_SIZE[self.level - 1]['player_pos'][1]


    def draw(self):
        """ affichage des elements du jeu """
        pyxel.cls(0)
        if self.menu:
            # affichage lune
            pyxel.blt(96 + self.cam_x * 0.7, 24, 2, 0, 40, 16, 16, 0)
            # affichage de la map
            pyxel.bltm(self.cam_x, self.cam_y, 0, 0, 0, 256, 256, 0)
            # affichage txt level
            if self.menu:
                for lvl in TEXT_LVL:
                    pyxel.text(lvl['x'] + self.cam_x, lvl['y'] + self.cam_y, lvl["txt"], 7)
            # affichage du joueur
            self.p.draw()
        elif self.level != 0 and self.menu != True:
            pyxel.bltm(0, 0, 0, LVL_SIZE[self.level - 1]['x'], LVL_SIZE[self.level - 1]['y'], LVL_SIZE[self.level - 1]['lenght'], LVL_SIZE[self.level - 1]['height'], 0)
            self.p.draw()


if __name__ == '__main__':
    # initialisation fenetre
    pyxel.init(WINDOW_SIZE, WINDOW_SIZE, "STICKMAN ADVENTURE 2D")
    # importation map, sprite, music
    pyxel.load("stickman_adventure.pyxres")
    # création d'une instance de Jeu
    Jeu(Player(PLAYER_SPRITE))
