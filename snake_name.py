import pygame
import time
import random

# 初始化 pygame
pygame.init()

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
yellow = (255, 255, 0)

# 设置游戏窗口 - 调整为更大的尺寸
display_width = 800
display_height = 600
dis = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('贪吃蛇游戏')

# 设置游戏时钟
clock = pygame.time.Clock()

# 蛇的大小和速度
snake_block = 15  # 增加蛇的大小
snake_speed = 15

# 设置字体
font_style = pygame.font.SysFont("simhei", 28)  # 增加字体大小
score_font = pygame.font.SysFont("simhei", 38)
title_font = pygame.font.SysFont("simhei", 60)  # 增加标题字体大小
button_font = pygame.font.SysFont("simhei", 32)  # 增加按钮字体大小

# 显示得分
def your_score(score):
    """
    显示当前得分
    
    @param {number} score - 当前得分
    """
    value = score_font.render("得分: " + str(score), True, black)
    dis.blit(value, [10, 10])  # 调整位置

# 绘制蛇
def our_snake(snake_block, snake_list):
    """
    绘制蛇的身体
    
    @param {number} snake_block - 蛇身体方块的大小
    @param {list} snake_list - 包含蛇身体所有部分位置的列表
    """
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])

# 显示消息
def message(msg, color, y_displace=0, size="small"):
    """
    在屏幕上显示消息
    
    @param {string} msg - 要显示的消息
    @param {tuple} color - 消息的颜色
    @param {number} y_displace - Y轴位移
    @param {string} size - 字体大小
    """
    if size == "small":
        mesg = font_style.render(msg, True, color)
    elif size == "medium":
        mesg = score_font.render(msg, True, color)
    elif size == "large":
        mesg = title_font.render(msg, True, color)
    
    text_rect = mesg.get_rect(center=(display_width/2, display_height/2 + y_displace))
    dis.blit(mesg, text_rect)

# 创建按钮
def create_button(text, x, y, width, height, inactive_color, active_color):
    """
    创建一个可点击的按钮
    
    @param {string} text - 按钮文本
    @param {number} x - 按钮X坐标
    @param {number} y - 按钮Y坐标
    @param {number} width - 按钮宽度
    @param {number} height - 按钮高度
    @param {tuple} inactive_color - 未激活时的颜色
    @param {tuple} active_color - 激活时的颜色
    @return {boolean} - 如果按钮被点击则返回True
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(dis, active_color, [x, y, width, height])
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(dis, inactive_color, [x, y, width, height])
    
    text_surf = button_font.render(text, True, black)
    text_rect = text_surf.get_rect(center=(x + width/2, y + height/2))
    dis.blit(text_surf, text_rect)
    
    return False

# 开始界面
def start_screen():
    """
    显示游戏开始界面
    
    @return {boolean} - 用户选择开始游戏返回True，退出返回False
    """
    start = False
    exit_game = False
    
    while not start and not exit_game:
        dis.fill(white)
        message("贪吃蛇游戏", green, -150, "large")
        message("使用方向键控制蛇移动", black, -50)
        message("吃到食物得分增加", black, 0)
        message("撞到墙壁或自己游戏结束", black, 50)
        message("按P键暂停游戏", black, 100)
        
        # 创建开始和退出按钮 - 调整按钮大小和位置
        if create_button("开始游戏", display_width/2 - 150, display_height/2 + 150, 300, 60, green, blue):
            start = True
        
        if create_button("退出游戏", display_width/2 - 150, display_height/2 + 230, 300, 60, red, (255, 100, 100)):
            exit_game = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
        
        pygame.display.update()
        clock.tick(15)
    
    return not exit_game

# 结束界面
def end_screen(score):
    """
    显示游戏结束界面
    
    @param {number} score - 最终得分
    @return {string} - 返回用户选择："restart"重新开始，"quit"退出
    """
    choice = ""
    
    while choice == "":
        dis.fill(white)
        message("游戏结束!", red, -150, "large")
        message(f"最终得分: {score}", black, -50, "medium")
        
        # 创建重新开始和退出按钮 - 调整按钮大小和位置
        if create_button("再玩一次", display_width/2 - 150, display_height/2 + 50, 300, 60, green, blue):
            choice = "restart"
        
        if create_button("退出游戏", display_width/2 - 150, display_height/2 + 130, 300, 60, red, (255, 100, 100)):
            choice = "quit"
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choice = "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    choice = "quit"
                if event.key == pygame.K_c:
                    choice = "restart"
        
        pygame.display.update()
        clock.tick(15)
    
    return choice

# 暂停界面
def pause_game():
    """
    显示游戏暂停界面
    
    @return {boolean} - 如果用户选择继续游戏返回True，退出返回False
    """
    paused = True
    dis.fill(white)
    message("游戏暂停", black, -50, "large")
    message("按C继续或Q退出", black, 30, "medium")
    pygame.display.update()
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        clock.tick(5)
    
    return True

# ... existing code ...

# 游戏主循环
def gameLoop():
    """
    游戏的主循环函数
    """
    # 显示开始界面
    if not start_screen():
        return
    
    game_over = False
    game_close = False
    game_paused = False

    # 初始化蛇的位置
    x1 = display_width / 2
    y1 = display_height / 2

    # 初始化蛇的移动方向
    x1_change = 0
    y1_change = 0

    # 初始化蛇的身体
    snake_List = []
    Length_of_snake = 1

    # 随机生成食物位置 - 修复食物生成逻辑
    foodx = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block

    while not game_over:

        # 游戏结束时的选项界面
        if game_close:
            choice = end_screen(Length_of_snake - 1)
            if choice == "quit":
                game_over = True
            elif choice == "restart":
                return gameLoop()

        # 处理键盘事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:
                    pause_game()

        # 检查是否撞到边界
        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_close = True

        # 更新蛇的位置
        x1 += x1_change
        y1 += y1_change
        dis.fill(white)
        
        # 绘制食物 - 确保食物正确显示
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        
        # 更新蛇的身体
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        
        # 如果蛇的长度超过了应有的长度，删除多余的部分
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 检查是否撞到自己
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # 绘制蛇和分数
        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)
        
        # 绘制暂停按钮
        if create_button("暂停", display_width - 120, 10, 100, 40, yellow, (255, 255, 150)):
            pause_game()

        pygame.display.update()

        # 检查是否吃到食物 - 修复食物碰撞检测
        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            # 生成新的食物位置 - 修复食物生成逻辑
            foodx = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
            # 增加蛇的长度
            Length_of_snake += 1

        # 控制游戏速度
        clock.tick(snake_speed)

    # 退出游戏
    pygame.quit()
    quit()

# ... existing code ...

# 启动游戏
gameLoop()