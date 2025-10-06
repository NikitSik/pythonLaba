"""Utility for drawing floral compositions with turtle graphics."""

from __future__ import annotations

import turtle
from typing import Tuple

RGBColor = Tuple[int, int, int]
Point = Tuple[int, int]


def draw(
    t: turtle.Turtle,
    *,
    base_elements: int = 7,
    size: int = 120,
    color: RGBColor = (0, 120, 255),
    line_width: int = 2,
    position: Point = (0, 0),
) -> None:
    """Draw a floral-like composition consisting of repeated petal elements.

    Each petal is made of two symmetric arcs placed around the center to mimic a rosette
    structure. The function leaves the screen open for the caller, positions the turtle
    before drawing, and hides it after the composition is completed.

    Args:
        t: Instance of :class:`turtle.Turtle` that performs drawing operations.
        base_elements: Number of petal elements to draw. Supported range is from 3 to 15.
        size: Radius of the arcs that form a petal, controlling the petal size.
        color: RGB color for the pen. Values are expected to be in the range 0..255.
        line_width: Line thickness for petal outlines. Supported range is from 1 to 5.
        position: Coordinates of the composition center relative to the canvas origin.

    Returns:
        None.

    Raises:
        ValueError: If ``base_elements`` or ``line_width`` are outside the supported range.
    """

    if not 3 <= base_elements <= 15:
        raise ValueError("Parameter 'base_elements' must be in range 3..15.")
    if not 1 <= line_width <= 5:
        raise ValueError("Parameter 'line_width' must be in range 1..5.")

    original_state = (t.isdown(), t.position(), t.heading())

    t.penup()
    t.goto(position)
    t.pendown()
    t.pensize(line_width)
    t.pencolor(*color)

    rotation_angle = 360 / base_elements

    for index in range(base_elements):
        t.setheading(rotation_angle * index)
        _draw_petal(t, size)

    t.hideturtle()

    was_down, original_position, original_heading = original_state
    t.penup()
    t.goto(original_position)
    t.setheading(original_heading)
    if was_down:
        t.pendown()


def _draw_petal(turtle_instance: turtle.Turtle, size: int) -> None:
    """Draw a single petal consisting of two mirrored circular arcs.

    Args:
        turtle_instance: Turtle used for drawing.
        size: Radius of the arcs forming the petal.

    Returns:
        None.
    """

    start_position = turtle_instance.position()
    start_heading = turtle_instance.heading()
    was_down = turtle_instance.isdown()

    turtle_instance.penup()
    turtle_instance.forward(size)
    turtle_instance.pendown()
    turtle_instance.left(60)
    turtle_instance.circle(size, 120)
    turtle_instance.left(120)
    turtle_instance.circle(size, 120)

    turtle_instance.penup()
    turtle_instance.goto(start_position)
    turtle_instance.setheading(start_heading)
    if was_down:
        turtle_instance.pendown()
