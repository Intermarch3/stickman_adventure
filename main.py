import pyxel

"""
A faire:
- colision avec les murs et le sol
- colision avec les portes
- regler probleme de chute
...
"""

# position des sprites en fonction du statue
player_sprite = {
    "walk": [[0, 0], [16, 0], [24, 0], [16, 8], [24, 8], [24, 0], [0, 0]],
    "jump": [[32, 0], [40, 0], [32, 0], [0, 0]],
    "shoot": []
}

TILE_FLOOR = (2, 3)
WINDOW_SIZE = 128
cam_x = 0
cam_y = 0
home_lenght = int(23 * 8)


pyxel.init(WINDOW_SIZE, WINDOW_SIZE, "STICKMAN ADVENTURE")
pyxel.load("assets.pyxres")



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
        self.x = 64
        self.y = 90
        self.dir = 1
        self.floor_y = 105
        # attributs de force (vitesse, graviter, ...)
        self.speed = 0.5
        self.jump_force = 1.5
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


    def floor_detection(self):
        """ detecte si le joueur touche le sol """
        x1 = int(self.x // 8)
        y1 = int((self.y + 1) // 8)
        x2 = int((self.x + 8 - 1) // 8)
        if self.player_dy > 0 and self.y % 8 == 1:
            for xi in range(x1, x2 + 1):
                if get_tile(xi, y1 + 1) == TILE_FLOOR:
                    self.on_floor = True
                    self.nb_jump = 0
                    print("floor")


    def update(self):
        """ actualisation des valeurs et affichage joueur """
        global cam_x, cam_y
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
        # actualisation de la force de chute (graviter)
        if self.y > self.floor_y:
            self.y = self.floor_y
        #actualisation position joueur
        self.x += self.player_dx
        self.y += self.player_dy
        #actualisation position caméra
        if self.x > WINDOW_SIZE * 0.8 and 17 + self.x - cam_x < home_lenght:
            self.x = WINDOW_SIZE * 0.8
            cam_x -= self.player_dx
        elif self.x < WINDOW_SIZE * 0.2 and cam_x < 0:
            self.x = WINDOW_SIZE * 0.2
            cam_x -= self.player_dx
        if self.x < - 2:
            self.x = - 2
        if self.x > WINDOW_SIZE - 6:
            self.x = WINDOW_SIZE - 6
        self.floor_detection()
        #actualisation force deplacement
        self.player_dx = max(self.player_dx - 1, 0)
        self.player_dy = min(self.player_dy + self.gravity, 8)


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
        update(): actualise le joueur et la 
    """
    def __init__(self, player):
        """ initialisation du joueur et de la fenetre """
        self.p = player
        pyxel.run(self.update, self.draw)


    def update(self):
        """ actualisation des elements du jeu """
        # actualisation du joueur
        self.p.update()


    def draw(self):
        """ affichage des elements du jeu """
        pyxel.cls(0)
        # affichage de la map
        pyxel.bltm(cam_x, cam_y, 0, 0, 0, 256, 256)
        # affichage du joueur
        self.p.draw()


if __name__ == '__main__':
    Jeu(Player(player_sprite))
