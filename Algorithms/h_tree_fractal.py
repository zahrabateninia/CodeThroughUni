#!/usr/bin/env python3

#  a recursive drawing using the turtle library, making a fractal pattern of letter H shapes

import turtle

def draw_H(n, x, y, size, t):
    """Recursively draw an H fractal pattern."""
    if n == 0:
        return

    # Draw the central H
    t.penup()
    t.goto(x - size/2, y)
    t.pendown()
    t.forward(size)

    t.right(90)
    t.penup()
    t.goto(x + size/2, y + size/2)
    t.pendown()
    t.forward(size)

    t.penup()
    t.goto(x - size/2, y + size/2)
    t.pendown()
    t.forward(size)

    t.left(90)

    # Recursive calls for 4 endpoints
    draw_H(n-1, x + size/2, y + size/2, size/2, t)
    draw_H(n-1, x - size/2, y + size/2, size/2, t)
    draw_H(n-1, x + size/2, y - size/2, size/2, t)
    draw_H(n-1, x - size/2, y - size/2, size/2, t)

def main():
    screen = turtle.Screen()
    alex = turtle.Turtle()
    alex.speed(0)  # Fastest drawing

    draw_H(5, 0, 0, 300, alex)  

    screen.mainloop()

if __name__ == "__main__":
    main()


# n is the recursion depth (how many layers of Hs you draw).

# (x, y) is the center where the current H will be drawn.

# size is how big the current H will be.

# t is the turtle (the pen that draws).