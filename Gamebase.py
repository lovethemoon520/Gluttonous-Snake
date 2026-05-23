from turtle import *

def square(x,y,size,color_name):
    up()
    goto(x,y)
    down()
    color(color_name)
    begin_fill()

    forward(size)
    left(90)
    forward(size)
    left(90)
    forward(size)
    left(90)
    forward(size)
    left(90)

    end_fill()


def circle_shape(x, y, size, color_name):
    up()
    # 保持居中对齐逻辑
    goto(x + size / 2, y)
    down()
    color(color_name)
    begin_fill()

    # 🔴 关键修改：在这里加上 steps=30 参数
    # 让 Turtle 强行用 30 个小线段去组合这个圆，边缘就会变得非常丝滑！
    circle(size / 2, steps=30)

    end_fill()
    up()
