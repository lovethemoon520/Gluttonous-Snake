# -----引用数据库与函数-----
from turtle import *
from Gamebase import square, circle_shape
from random import randrange, choice
from time import sleep

# -----定义变量-----
apple_x = 0
apple_y = 0
apple_type = "normal"
apple_color = "red"
snake = [[0, 0], [10, 0], [20, 0], [30, 0], [40, 0], [50, 0]]

# 新增变量：药水数量，开局送 1 瓶保底
potions = 1

# 随机生成 2 堵连续的墙
walls = []
for _ in range(2):
    while True:
        wx = randrange(-200, 160, 10)
        wy = randrange(-190, 160, 10)
        current_wall = [[wx, wy], [wx + 10, wy], [wx + 20, wy]]

        is_safe = True
        for block in current_wall:
            if block in snake:
                is_safe = False
                break
            if block in walls:
                is_safe = False
                break
            if block[1] == 0 and 0 <= block[0] <= 120:
                is_safe = False
                break

        if is_safe:
            walls.extend(current_wall)
            break

aim_x = 10
aim_y = 0
is_dead = False


# -----定义函数-----
def change(x, y):
    global aim_x, aim_y
    if aim_x != -x or aim_y != -y:
        aim_x = x
        aim_y = y


def inside_map():
    if -200 <= snake[-1][0] <= 180 and -190 <= snake[-1][1] <= 190:
        return True
    else:
        return False


def inside_snake():
    for n in range(len(snake) - 1):
        if snake[n][0] == snake[-1][0] and snake[n][1] == snake[-1][1]:
            return True
    return False


def restart():
    global snake, aim_x, aim_y, is_dead, potions
    if is_dead:
        snake = [[0, 0], [10, 0], [20, 0], [30, 0], [40, 0], [50, 0]]
        aim_x = 10
        aim_y = 0
        potions = 1  # 重开游戏也重置为 1 瓶药水
        generate_apple()
        is_dead = False
        gameLoop()


def generate_apple():
    global apple_x, apple_y, apple_type, apple_color
    while True:
        apple_x = randrange(-200, 180, 10)
        apple_y = randrange(-190, 160, 10)
        if [apple_x, apple_y] in walls:
            continue
        if [apple_x, apple_y] in snake:
            continue
        break

    apple_type = choice(["normal"] * 7 + ["gold"] * 2 + ["poison"] * 1)
    if apple_type == "normal":
        apple_color = "red"
    elif apple_type == "gold":
        apple_color = "gold"
    elif apple_type == "poison":
        apple_color = "purple"


# --- 新增：手动按 R 键主动刷新苹果的函数 ---
def refresh_apple():
    global potions, is_dead
    # 只有游戏没结束、手头有药水、且当前确实是毒苹果时才允许刷新
    if not is_dead and potions > 0 and apple_type == "poison":
        potions -= 1  # 消耗一瓶药水
        generate_apple()  # 重新生成苹果
        # 刷新画面让计分板和苹果立刻更新
        clear_and_draw()


def gameLoop():
    global apple_x, apple_y, aim_x, aim_y, snake, is_dead, potions

    snake.append([snake[-1][0] + aim_x, snake[-1][1] + aim_y])

    if snake[-1][0] != apple_x or snake[-1][1] != apple_y:
        snake.pop(0)
    else:
        if apple_type == "gold":
            snake.insert(0, [snake[0][0], snake[0][1]])
            snake.insert(0, [snake[0][0], snake[0][1]])
            potions += 1  # 吃到金苹果，药水奖励 +1
        elif apple_type == "poison":
            if len(snake) > 4:
                snake.pop(0)
                snake.pop(0)
            else:
                is_dead = True
        generate_apple()

    if (not inside_map()) or inside_snake() or ([snake[-1][0], snake[-1][1]] in walls) or is_dead:
        square(snake[-1][0], snake[-1][1], 10, "red")
        up()
        goto(0, -20)
        color("red")
        write("Game Over!\n按空格键重新开始", align="center", font=("黑体", 20, "bold"))
        update()
        is_dead = True
        return

    # 把渲染画面独立出来，方便按R键时随时调用
    clear_and_draw()

    score = len(snake) - 6
    delay = max(50, 200 - score * 10)
    ontimer(gameLoop, delay)
    update()


# --- 新增：独立出来的渲染绘制函数 ---
def clear_and_draw():
    clear()
    square(-210, -200, 410, "black")
    square(-200, -190, 390, "white")

    # 计分板：显示得分与药水数量
    up()
    goto(0, 180)
    color("black")
    score = len(snake) - 6
    write(f"当前得分: {score}   🧪药水储备: {potions}", align="center", font=("黑体", 14, "normal"))

    for w in walls:
        square(w[0], w[1], 10, "black")

    circle_shape(apple_x, apple_y, 10, apple_color)

    for n in range(len(snake) - 1):
        square(snake[n][0], snake[n][1], 10, "#0088ff")

    square(snake[-1][0], snake[-1][1], 10, "orange")
    update()


def show_rules():
    clear()
    up()
    color("black")

    goto(0, 120)
    write(" 贪 吃 蛇 大 升 级 ", align="center", font=("黑体", 22, "bold"))

    goto(0, 80)
    write("【 游 戏 规 则 】", align="center", font=("黑体", 14, "bold"))

    goto(0, 40)
    write("1. 使用 WSAD 或 方向键 控制蛇移动", align="center", font=("黑体", 12, "normal"))

    goto(-140, 10)
    write("2. ", align="left", font=("黑体", 12, "normal"))
    circle_shape(-120, 12, 10, "red")
    up()

    goto(-105, 10)
    color("black")
    write("红苹果 +1分  | ", align="left", font=("黑体", 12, "normal"))
    circle_shape(15, 12, 10, "gold")
    up()

    goto(30, 10)
    color("black")
    write("金苹果 +3分", align="left", font=("黑体", 12, "normal"))

    goto(-140, -20)
    write("3. ", align="left", font=("黑体", 12, "normal"))
    circle_shape(-120, -18, 10, "purple")
    up()

    goto(-105, -20)
    color("black")
    write("毒苹果 -2分 (过短会直接导致失败)", align="left", font=("黑体", 12, "normal"))

    # 6. 第四行：黑色墙壁 (y=-50)
    goto(-140, -50)
    write("4. 撞击 ", align="left", font=("黑体", 12, "normal"))
    square(-85, -48, 10, "black")
    up()

    goto(-70, -50)
    color("black")
    write("黑色墙壁 或 边界 游戏结束", align="left", font=("黑体", 12, "normal"))

    # 🔴【核心修改】将秘籍拆成两行，并且左对齐（y=-75 和 y=-95）
    # 第一行：说明怎么获得药水
    goto(-140, -75)
    color("darkgreen")
    write("⭐ 秘籍：吃金苹果  可以获得1瓶药水", align="left", font=("黑体", 11, "bold"))
    # 在文字中间留出的空隙里，用画圆函数画出金色的圆圈
    circle_shape(13, -73, 10, "gold")
    up()

    # 第二行：说明怎么使用药水
    goto(-140, -95)
    color("darkgreen")
    write("   按【R】键可消耗1瓶药水随机刷新毒苹果", align="left", font=("黑体", 11, "bold"))

    # 7. 底部提示语 (顺延向下平移到 y=-130，防止和文字重叠)
    goto(0, -130)
    color("blue")
    write("确认了解规则后，请按【空格键】开始游戏", align="center", font=("黑体", 13, "bold"))

    update()


def start_game():
    clear()
    generate_apple()

    onkey(lambda: change(0, 10), "w")
    onkey(lambda: change(0, 10), "W")
    onkey(lambda: change(0, -10), "s")
    onkey(lambda: change(0, -10), "S")
    onkey(lambda: change(-10, 0), "a")
    onkey(lambda: change(-10, 0), "A")
    onkey(lambda: change(10, 0), "d")
    onkey(lambda: change(10, 0), "D")

    onkey(lambda: change(0, 10), "Up")
    onkey(lambda: change(0, -10), "Down")
    onkey(lambda: change(-10, 0), "Left")
    onkey(lambda: change(10, 0), "Right")

    # 🔴 新增：绑定 R 键用来刷新毒苹果
    onkey(refresh_apple, "r")
    onkey(refresh_apple, "R")

    onkey(restart, "space")
    gameLoop()


# -----主程序-----
setup(420, 420, 0, 0)
title("贪吃蛇")
hideturtle()
tracer(False)

listen()
onkey(start_game, "space")

show_rules()

done()