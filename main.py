import random

import arcade

SPRITE_SCALING_PLAYER = 0.4
SPRITE_SCALING_ENEMY = 0.4
SPRITE_SCALING_LASER = 0.4
PLAYER_COUNT = 3

ENEMY_COUNT = 24
ENEMY_COLS = 6
ENEMY_SCALING_LASER = 0.4

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

BULLET_SPEED = 10


class Enemy(arcade.Sprite):

    dx = 2.5

    def __init__(self, enemy_bullet_list):
        self.dx = Enemy.dx
        self.dy = 12
        self.enemy_bullet_list = enemy_bullet_list

        super().__init__("assets/enemyRed2.png", SPRITE_SCALING_ENEMY)

    def update(self):
        if (self.left < 0 and Enemy.dx < 0) or (self.right > SCREEN_WIDTH and Enemy.dx > 0):
            if -6 < Enemy.dx < 6:
                Enemy.dx *= -1.06
            else:
                Enemy.dx *= -1

        if self.dx != Enemy.dx:
            self.dx = Enemy.dx
            self.center_y -= self.dy

        self.center_x += Enemy.dx
        if random.random() < 0.01 and 5 > len(self.enemy_bullet_list):
            self._shoot()

    def _shoot(self):
        bullet = EnemyBullet()

        bullet.center_x = self.center_x
        bullet.top = self.bottom
        bullet.angle = -180

        self.enemy_bullet_list.append(bullet)


class Bullet(arcade.Sprite):

    def __init__(self):
        super().__init__("assets/laserBlue01.png", SPRITE_SCALING_LASER)

    def update(self):
        self.center_y += BULLET_SPEED
        if self.bottom > SCREEN_HEIGHT:
            self.kill()


class EnemyBullet(arcade.Sprite):

    def __init__(self):
        super().__init__("assets/laserRed01.png", ENEMY_SCALING_LASER)

    def update(self):
        self.center_y -= 4
        if self.top < 0:
            self.kill()


class SpaceInvaders(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Space Invaders")

        self.enemy_list = None
        self.bullet_list = None
        self.player_list = None
        self.player_sprite = None
        self.enemy_bullet_list = None
        self.score = 0

        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.score = 0

        self.player_sprite = arcade.Sprite("assets/playerShip2_blue.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.dx = 0
        self.player_sprite.center_x = 480
        self.player_sprite.center_y = 25
        self.player_list.append(self.player_sprite)
        for n in range(PLAYER_COUNT - 1):
            extra_life = arcade.Sprite("assets/playerShip2_blue.png", SPRITE_SCALING_PLAYER)
            extra_life.dx = 0
            extra_life.center_x = SCREEN_WIDTH - n * 30 - 30
            extra_life.center_y = SCREEN_HEIGHT - 20
            self.player_list.append(extra_life)

        for i in range(ENEMY_COUNT):
            current_row = i // ENEMY_COLS
            current_col = i % ENEMY_COLS

            enemy = Enemy(self.enemy_bullet_list)

            enemy.center_x = 50 + current_col * 85
            enemy.center_y = SCREEN_HEIGHT - (45 + current_row * 60)

            self.enemy_list.append(enemy)

    def on_draw(self):
        arcade.start_render()

        self.enemy_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()
        self.enemy_bullet_list.draw()

        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 20, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        self._shoot()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self._shoot()
        if key == arcade.key.ESCAPE:
            exit()
        if key == arcade.key.MOTION_RIGHT:
            self.player_sprite.dx = 6
        if key == arcade.key.MOTION_LEFT:
            self.player_sprite.dx -= 6

    def on_key_release(self, symbol: int, modifiers: int):
        self.player_sprite.dx = 0

    def _shoot(self):
        if len(self.bullet_list) <= 1:
            bullet = Bullet()

            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top

            self.bullet_list.append(bullet)

    def update(self, delta_time):
        self.enemy_list.update()
        self.bullet_list.update()
        self.enemy_bullet_list.update()
        self.player_list.update()
        for bullet in self.bullet_list:

            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            if len(hit_list) > 0:
                bullet.kill()

            for enemy in hit_list:
                enemy.kill()
                self.score += 10

        for bullet in self.enemy_bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.player_list)
            if len(hit_list) > 0:
                bullet.kill()

            for player in hit_list:
                player.kill()
                if self.player_list:
                    self.player_sprite = self.player_list[-1]
                    self.player_sprite.center_x = 50
                    self.player_sprite.center_y = 25
                    self.player_sprite.scale *= 2
                else:
                    print("GAME OVER")
                    arcade.draw_text(f"GAME OVER", SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT/2, arcade.color.WHITE, 50)
        self.player_sprite.center_x += self.player_sprite.dx


def main():
    window = SpaceInvaders()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
