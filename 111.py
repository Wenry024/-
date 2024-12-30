import pygame
import random

# 初始化pygame
pygame.init()

# 设置屏幕大小
screen_width = 1000
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置标题和时钟
pygame.display.set_caption('吃豆人游戏')
clock = pygame.time.Clock()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE=(0,0,255)
# 吃豆人类
class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed = 5
        self.direction = pygame.math.Vector2(0, 0)

    def update(self):
        self.rect.center += self.direction * self.speed

# 鬼魂类
class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, screen_width), random.randint(0, screen_height))
        self.speed = 2
        self.direction = pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))

    def update(self):
        self.rect.center += self.direction * self.speed
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.direction.x *= -1
        if self.rect.top < 0 or self.rect.bottom > screen_height:
            self.direction.y *= -1
# 豆子类
class Bean(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, screen_width), random.randint(0, screen_height))
# 创建精灵组
pacman_group = pygame.sprite.Group()
ghost_group = pygame.sprite.Group()
bean_group=pygame.sprite.Group()

# 创建吃豆人和鬼魂
pacman = Pacman()
pacman_group.add(pacman)

for _ in range(4):
    ghost = Ghost()
    ghost_group.add(ghost)
#创建豆子
for _ in range(20):
   bean= Bean()
bean_group.add(bean)

# 吃豆子个数
collect = 0
# 游戏参数
max_levels = 3
current_level = 1
beans_to_win = 2 # 每个关卡需要吃掉的豆子数量
# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman.direction = pygame.math.Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT:
                pacman.direction = pygame.math.Vector2(1, 0)
            elif event.key == pygame.K_UP:
                pacman.direction = pygame.math.Vector2(0, -1)
            elif event.key == pygame.K_DOWN:
                pacman.direction = pygame.math.Vector2(0, 1)
    # 更新精灵
    pacman_group.update()
    ghost_group.update()

    # 检测碰撞
    for ghost in ghost_group:
        if pygame.sprite.collide_rect(pacman, ghost):
            print("游戏结束")
            running = False
        # 检测吃豆人吃掉豆子
        for bean in bean_group:
            if pygame.sprite.collide_rect(pacman, bean):
                bean_group.remove(bean)
                collect += 1 # 每吃掉一个豆子得分增加1
                bean = Bean()  # 重新生成一个豆子
                bean_group.add(bean)
        # 检测是否完成当前关卡
        if collect >=beans_to_win:
            print(f"恭喜你，通过了第{current_level}关！")
            current_level += 1
            collect=0
            if current_level <= max_levels:
                        # 重新生成豆子，增加难度（例如增加鬼魂数量）
                        bean_group.empty()
                        for _ in range(beans_to_win):
                            bean = Bean()
                            bean_group.add(bean)
                            ghost=Ghost()
                            ghost_group.add(ghost)
                            ghost.speed +=1
            else:
                        print("你已经通过了所有关卡！")
                        running = False
    # 绘制背景和精灵
    screen.fill(BLACK)
    pacman_group.draw(screen)
    ghost_group.draw(screen)
    bean_group.draw(screen)
    font = pygame.font.Font(None, 36)
    text = font.render(f'collect: {collect}', True, WHITE)
    screen.blit(text, (0, 100))
    # 更新屏幕
    pygame.display.flip()

    # 设置帧率
    clock.tick(30)

# 退出游戏
pygame.quit()