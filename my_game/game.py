import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="My Game")
        pyxel.mouse(True)
        self.number = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if 30 <= pyxel.mouse_x <= 50 and 60 <= pyxel.mouse_y <= 70:
                self.number -= 1
            elif 110 <= pyxel.mouse_x <= 130 and 60 <= pyxel.mouse_y <= 70:
                self.number += 1
 
    def draw(self):
        pyxel.cls(pyxel.COLOR_DARK_BLUE)
        pyxel.text(70, 60, f"{self.number}", pyxel.COLOR_PEACH)
        pyxel.text(30, 60, "-", pyxel.COLOR_WHITE)
        pyxel.text(110, 60, "+", pyxel.COLOR_WHITE)

App()