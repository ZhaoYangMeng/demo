import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_event(event, ai_setting, screen, ship, bullets):
    """监视是否有按键被按下"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_setting, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_setting, screen, ship, bullets):
    if len(bullets) < ai_setting.bullet_allowed:
        # 如果未达到子弹上限，创建一颗子弹并将其加入到编组bullets中
        new_bullet = Bullet(ai_setting, screen, ship)
        bullets.add(new_bullet)


def check_keyup_event(event, ship):
    """监视是否有按键被松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_setting, screen,  stats, sb, play_button,  ship,
                 aliens, bullets):
    """监视键盘和鼠标事件"""
    for event in pygame.event.get():
        # 监视是否关闭游戏
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_setting, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 方法get_pos()获得鼠标点击位置的坐标
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_setting, screen, ship, stats, sb, play_button,
                              aliens, bullets, mouse_x, mouse_y)


def update_screen(ai_setting, screen, stats, sb, ship, bullets, aliens,
                  play_button):
    """更新屏幕上的图案，并切换到新屏幕"""
    # 每次循环都重新绘制屏幕
    screen.fill(ai_setting.bg_color)
    # 绘制子弹，飞船，外星人
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 显示得分
    sb.show_score()
    # 只在非活动状态渲染按钮
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_setting, screen, stats, sb,
                   ship, bullets, aliens):
    """更新子弹"""
    # 刷新子弹
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets:
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 用来检测子弹数量
    # print(len(bullets))
    check_bullet_alien_collisions(ai_setting, screen, stats, sb,
                                  ship, bullets, aliens)


def check_bullet_alien_collisions(ai_setting, screen, stats, sb, ship, bullets, aliens):
    """
    检查是否有子弹击中，并删除被击中的外星人,
    第一个布尔值控制子弹，第二个布尔值控制外星人
    """
    collissions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    if collissions:
        for aliens in collissions.values():
            stats.score += ai_setting.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    # 如果没有外星人则删除子弹并新建外星人
    if len(aliens) == 0:
        bullets.empty()
        # 击杀全部外星人则加速
        ai_setting.increase_speed()
        creat_fleet(ai_setting, screen, ship, aliens)
        # 提高等级
        stats.level += 1
        sb.prep_level()


def check_alien_condition(ship, aliens):
    """检查外星人是否与飞船碰撞"""
    if pygame.sprite.spritecollideany(ship, aliens):
        print("Ship hit!!!")


# def update_aliens(aliens):
#     """更新外星人的位置"""
#     aliens.update()


def get_number_alien_x(ai_setting, alien_width):
    """计算一行有多少外星人"""
    available_space_x = ai_setting.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (3 * alien_width)) - 5
    return number_aliens_x


def get_number_alien_row(ai_setting, ship_height, alien_height):
    """计算可显示多少行"""
    available_space_y = (ai_setting.screen_height -
                         (3 * alien_height) - ship_height)
    number_alien_rows = int(available_space_y / (3 * alien_height)) - 2
    return number_alien_rows


def creat_alien(ai_setting, screen, aliens, alien_number, row_number):
    """创建一个外星人"""
    alien = Alien(ai_setting, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 3 * alien_number * alien_width
    alien.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)


def creat_fleet(ai_setting, screen, ship, aliens):
    """创建外星人群"""
    alien = Alien(ai_setting, screen)
    number_aliens_x = get_number_alien_x(ai_setting, alien.rect.width)
    number_aliens_row = get_number_alien_row(ai_setting, ship.rect.height,
                                             alien.rect.height)
    # 创建第一行外星人
    for alien_number in range(number_aliens_x):
        for alien_row in range(number_aliens_row):
            creat_alien(ai_setting, screen, aliens, alien_number, alien_row)


def check_fleet_edges(ai_setting, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_setting, aliens)
            break


def change_fleet_direction(ai_setting, aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_setting.alien_fleet_drop_speed_factor
    ai_setting.fleet_direction *= -1


def update_aliens(ai_setting, stats, sb, screen, ship, aliens, bullets):
    """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
    check_fleet_edges(ai_setting, aliens)
    aliens.update()
    # 检测外星人与飞船碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_setting, stats, sb, screen, ship, aliens, bullets)
    # 检测外星人是否到达边缘
    check_aliens_bottom(ai_setting, stats, sb, screen, ship, aliens, bullets)


def ship_hit(ai_setting, stats, sb, screen, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    # 将飞船生命值减1
    stats.ships_left -= 1
    sb.prep_ships()
    # 判断飞船的生命值
    if stats.ships_left > 0:
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        creat_fleet(ai_setting, screen, ship, aliens)
        ship.center_ship()
        # 暂停一段时间
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_setting, stats, sb, screen, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_setting, stats, sb, screen, ship, aliens, bullets)
            break


def check_play_button(ai_setting, screen, ship, stats, sb, play_button,
                      aliens, bullets, mouse_x, mouse_y):
    """单击play且处于非活动状态时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏初始难度
        ai_setting.initialize_dynamic_settings()
        # 隐藏鼠标
        pygame.mouse.set_visible(False)
        # 重置统计信息
        stats.reset_stats()
        stats.game_active = True
        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并让飞船居中
        creat_fleet(ai_setting, screen, ship, aliens)
        ship.center_ship()


def check_high_score(stats, sb):
    """检查最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
    sb.prep_high_score()
