import pygame.font
from pygame.sprite import Group
from ship import Ship


class ScoreBoard():
    """显示得分信息"""
    def __init__(self, ai_setting, screen, stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_setting = ai_setting
        self.stats = stats
        # 显示得分信息的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont("arial", 36)
        # 准备初始等级、初始得分和最高分图像
        self.prep_level()
        self.prep_score()
        self.prep_high_score()
        self.prep_ships()

    def prep_score(self):
        """将得分转换为渲染的图像"""
        rounded_score = round(self.stats.score, -1)  # 将得分圆整到最近的10的倍数，下同
        score_str = "{:,}".format(rounded_score)  # 添加用逗号表示的千分位分隔符，下同
        # score_str = str(self.stats.score)
        self.score_image = self.font.render('score : ' + score_str, True, self.text_color,
                                            self.ai_setting.bg_color)

        # 将记分牌放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = self.screen_rect.top

    def prep_high_score(self):
        """将最高分转换为渲染的图像"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render('high score : ' + high_score_str, True, self.text_color,
                                                 self.ai_setting.bg_color)

        # 将最高分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def prep_level(self):
        """将等级转换为渲染的图像"""
        self.level_image = self.font.render('level : ' + str(self.stats.level), True, self.text_color,
                                            self.ai_setting.bg_color)

        # 将等级放在屏幕顶部左端
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = 50

    def prep_ships(self):
        """显示余下的飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_setting, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """显示图像"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # 绘制飞船
        self.ships.draw(self.screen)
