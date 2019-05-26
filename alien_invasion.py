import pygame
import game_functions as gf
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


def run_game():
    # 初始化并创建一个屏幕对象
    pygame.init()
    ai_setting = Settings()
    screen = pygame.display.set_mode(
        (ai_setting.screen_width, ai_setting.screen_height))
    pygame.display.set_caption('Alien Invasion')

    # 创建一艘飞船
    ship = Ship(ai_setting, screen)
    # 创建一个储存子弹的编组
    bullets = Group()
    # 创建一个储存外星人的编组
    aliens = Group()
    # 创建外星人群
    gf.creat_fleet(ai_setting, screen, ship, aliens)
    # 创建游戏统计信息和记分牌
    stats = GameStats(ai_setting)
    sb = ScoreBoard(ai_setting, screen, stats)
    # 创建按钮
    play_button = Button(ai_setting, screen, "Play")

    # 开始游戏主循环
    while True:
        # 检查鼠标键盘事件
        gf.check_events(ai_setting, screen, stats, sb, play_button, ship,
                        aliens, bullets)
        # 判断游戏是否失败
        if stats.game_active:
            # 更新飞船位置
            ship.update()
            # 更新子弹位置
            gf.update_bullets(ai_setting, screen, stats, sb,
                              ship, bullets, aliens)
            # 更新外星人位置
            gf.update_aliens(ai_setting, stats, sb, screen, ship,
                             aliens, bullets)
            # 检查子弹与外星人的碰撞
            gf.check_bullet_alien_collisions(ai_setting, screen, stats, sb,
                                             ship, bullets, aliens)
            # 检查飞船与外星人的碰撞
            gf.check_alien_condition(ship, aliens)
        # 刷新屏幕
        gf.update_screen(ai_setting, screen, stats, sb, ship, bullets,
                         aliens, play_button)


run_game()
