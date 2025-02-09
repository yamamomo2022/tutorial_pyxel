import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
STONE_INTERVAL = 30
START_SCENE = "start"
PLAY_SCENE = "play"

class Stone:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        # 常に1ドット下に移動
        self.y += 1

    def draw(self):
        # 8x8サイズの石として描画（背景色を透過色として指定）
        pyxel.blt(self.x, self.y, 0, 8, 0, 8, 8, pyxel.COLOR_BLACK)

    def is_out_of_screen(self):
        return self.y >= SCREEN_HEIGHT

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="My Game")
        pyxel.mouse(True)
        pyxel.load("my_resource.pyxres")
        pyxel.playm(0, loop=True)
        # 初期シーンはスタートシーン
        self.current_scene = START_SCENE
        pyxel.run(self.update, self.draw)

    def reset_play_scene(self):
        # プレイシーン開始時にプレイヤーや石、その他変数を初期化
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT * 4 // 5
        self.stones = []
        self.is_collision = False
        self.game_over_display_timer = 60

    def update_start_scene(self):
        # スタートシーンではReturnキーでプレイシーンに移行
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.current_scene = PLAY_SCENE
            self.reset_play_scene()

    def update_play_scene(self):
        # 衝突発生中なら、一定時間後にスタートシーンへ戻す
        if self.is_collision:
            if self.game_over_display_timer > 0:
                self.game_over_display_timer -= 1
            else:
                self.current_scene = START_SCENE
            return

        # プレイヤー移動（プレイヤースプライトは16×16と仮定）
        if pyxel.btn(pyxel.KEY_LEFT) and self.player_x > 0:
            self.player_x -= 1
        elif pyxel.btn(pyxel.KEY_RIGHT) and self.player_x < SCREEN_WIDTH - 16:
            self.player_x += 1

        # 一定フレーム間隔で新たな石を生成
        if pyxel.frame_count % STONE_INTERVAL == 0:
            self.stones.append(Stone(pyxel.rndi(0, SCREEN_WIDTH - 8), 0))

        # 各石を更新し、プレイヤーとの衝突判定を実施
        for stone in self.stones.copy():
            stone.update()
            # 矩形同士の当たり判定（石は8×8、プレイヤーは16×16）
            if (stone.x + 8 > self.player_x and stone.x < self.player_x + 16 and
                stone.y + 8 > self.player_y and stone.y < self.player_y + 16):
                self.is_collision = True
            # 画面外に出た石はリストから削除
            if stone.is_out_of_screen():
                self.stones.remove(stone)

    def draw_start_scene(self):
        # 背景をクリアしてスタート画面のメッセージを表示
        pyxel.cls(0)
        pyxel.text(SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10, "Press Return to Start", pyxel.COLOR_YELLOW)

    def draw_play_scene(self):
        pyxel.cls(0)
        # すべての石を描画
        for stone in self.stones:
            stone.draw()
        # プレイヤーを描画（スプライトは16×16と仮定）
        pyxel.blt(self.player_x, self.player_y, 0, 16, 0, 16, 16, pyxel.COLOR_BLACK)
        # 衝突時は「Game Over」を表示
        if self.is_collision:
            pyxel.text(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2, "Game Over", pyxel.COLOR_YELLOW)

    def update(self):
        # 共通の終了処理
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        # 現在のシーンに応じた更新処理を呼び出す
        if self.current_scene == START_SCENE:
            self.update_start_scene()
        elif self.current_scene == PLAY_SCENE:
            self.update_play_scene()

    def draw(self):
        # 現在のシーンに応じた描画処理を呼び出す
        if self.current_scene == START_SCENE:
            self.draw_start_scene()
        elif self.current_scene == PLAY_SCENE:
            self.draw_play_scene()

App()