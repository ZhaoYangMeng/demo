class Settings():
    """存储游戏所需的设置"""

    def __init__(self):
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (255, 255, 255)

        # 飞船设置
        # self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # 子弹设置
        # self.bullet_speed_factor = 1.5
        self.bullet_width = 1200
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 5

        # 外星人设置
        # self.alien_speed_factor = 1
        self.alien_fleet_drop_speed_factor = 40
        # 1表示向右，-1表示向左，不使用left和right是为了避免使用if语句
        # self.fleet_direction = 1

        # 游戏难度递增节奏
        self.speedup_scale = 1.01
        # 游戏得分递增节奏
        self.score_scale = 20

        # 初始化状态
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏难度"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # fleet_direction为1表示向右；为-1表示向左
        self.fleet_direction = 1
        self.alien_points = 10

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.score_scale * self.alien_points)
