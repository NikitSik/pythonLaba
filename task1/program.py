# Запуск:
#   python program.py
# Требуются: Python 3.10+, Pillow (pip install pillow)
"""Main script to render predefined floral turtle compositions and save a screenshot."""

from __future__ import annotations

import turtle
from pathlib import Path
from typing import Tuple

# pylint: disable=missing-function-docstring,missing-class-docstring,missing-module-docstring

try:
    from PIL import Image
except ImportError:  # pragma: no cover - optional dependency handling
    Image = None
    print(
        "Pillow is not installed. Install it with 'pip install pillow' to enable PNG export."
    )

from draw_figure import draw

RGBColor = Tuple[int, int, int]
Position = Tuple[int, int]
CompositionConfig = tuple[int, int, RGBColor, int, Position]

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
PNG_OUTPUT_PATH = Path("task1/screenshot.png")
COMPOSITIONS: tuple[CompositionConfig, ...] = (
    (7, 140, (0, 120, 255), 2, (-260, 60)),
    (10, 110, (255, 105, 0), 3, (0, -20)),
    (3, 160, (60, 200, 120), 4, (260, 80)),
)
COLOR_MODE = 255


_COLOR_MODE_SET = False


def ensure_colormode_255() -> None:
    """Ensure that the turtle module operates in RGB color mode with 255 range."""

    global _COLOR_MODE_SET
    if not _COLOR_MODE_SET:
        turtle.colormode(COLOR_MODE)
        _COLOR_MODE_SET = True


def save_canvas_png(screen: turtle.Screen, path: Path) -> None:
    """Save the current turtle canvas to a PNG file.

    The image is exported via an intermediate EPS file, which is then converted to PNG
    using Pillow. When Pillow is unavailable, the EPS file is kept and a notice is
    printed to the console.

    Args:
        screen: Active turtle screen whose canvas will be exported.
        path: Destination path for the PNG file.
    """

    canvas = screen.getcanvas()
    path.parent.mkdir(parents=True, exist_ok=True)
    eps_path = path.with_suffix(".eps")
    canvas.postscript(file=str(eps_path))

    if Image is None:
        print(
            f"Saved EPS fallback to {eps_path.as_posix()} because Pillow is unavailable."
        )
        return

    with Image.open(eps_path) as image:
        bounding_box = image.getbbox()
        if bounding_box:
            image = image.crop(bounding_box)
        image.save(path, format="PNG")

    if eps_path.exists():
        eps_path.unlink()


def main() -> None:
    """Entry point that draws several flower-like figures and saves the screenshot."""

    ensure_colormode_255()

    screen = turtle.Screen()
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.title("Лабораторная работа №3 – Фиксированные композиции")

    painter = turtle.Turtle()
    painter.speed(0)
    painter.hideturtle()

    for base_elements, size, color, line_width, position in COMPOSITIONS:
        draw(
            painter,
            base_elements=base_elements,
            size=size,
            color=color,
            line_width=line_width,
            position=position,
        )

    screen.update()
    save_canvas_png(screen, PNG_OUTPUT_PATH)
    painter.hideturtle()
    screen.exitonclick()


if __name__ == "__main__":
    main()
