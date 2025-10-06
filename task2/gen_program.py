# Запуск:
#   python gen_program.py --seed 42
# Требуются: Python 3.10+, Pillow (pip install pillow)
"""Batch generator of random turtle compositions saved as PNG files."""

from __future__ import annotations

import argparse
import random
import sys
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

CURRENT_DIR = Path(__file__).resolve().parent
TASK1_DIR = CURRENT_DIR.parent / "task1"
if str(TASK1_DIR) not in sys.path:
    sys.path.insert(0, str(TASK1_DIR))

import turtle

from draw_figure import draw

RGBColor = Tuple[int, int, int]
Position = Tuple[int, int]

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
OUTPUT_DIR = Path("task2/out")
SCREENSHOT_PATH = Path("task2/screenshot.png")
IMAGE_COUNT = 100
COLOR_MODE = 255
BASE_ELEMENTS_RANGE = (3, 15)
LINE_WIDTH_RANGE = (1, 5)
SIZE_RANGE = (80, 180)
POSITION_LIMIT_X = 450
POSITION_LIMIT_Y = 300


_COLOR_MODE_SET = False


def ensure_colormode_255() -> None:
    """Ensure that the turtle module operates in RGB color mode with 255 range."""

    global _COLOR_MODE_SET
    if not _COLOR_MODE_SET:
        turtle.colormode(COLOR_MODE)
        _COLOR_MODE_SET = True


def save_canvas_png(screen: turtle.Screen, path: Path) -> None:
    """Save the current turtle canvas to a PNG file or EPS fallback."""

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


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the generator script."""

    parser = argparse.ArgumentParser(
        description="Generate random turtle flower compositions and save them as images."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Seed for the random number generator to ensure reproducibility.",
    )
    return parser.parse_args()


def generate_parameters(rng: random.Random) -> dict[str, object]:
    """Generate a random set of drawing parameters for one composition."""

    base_elements = rng.randint(*BASE_ELEMENTS_RANGE)
    size = rng.randint(*SIZE_RANGE)
    color = (rng.randint(0, 255), rng.randint(0, 255), rng.randint(0, 255))
    line_width = rng.randint(*LINE_WIDTH_RANGE)

    max_x = max(POSITION_LIMIT_X - size, 0)
    max_y = max(POSITION_LIMIT_Y - size, 0)
    position = (
        rng.randint(-max_x, max_x),
        rng.randint(-max_y, max_y),
    )

    return {
        "base_elements": base_elements,
        "size": size,
        "color": color,
        "line_width": line_width,
        "position": position,
    }


def main() -> None:
    """Generate a batch of random turtle drawings and save them to disk."""

    args = parse_args()
    if args.seed is not None:
        random.seed(args.seed)

    rng = random.Random()
    if args.seed is not None:
        rng.seed(args.seed)

    ensure_colormode_255()

    screen = turtle.Screen()
    screen.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    screen.title("Лабораторная работа №3 – Случайная генерация")
    screen.tracer(0, 0)

    artist = turtle.Turtle()
    artist.speed(0)
    artist.hideturtle()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    last_parameters: dict[str, object] | None = None

    for index in range(1, IMAGE_COUNT + 1):
        artist.clear()
        artist.penup()
        artist.home()
        artist.pendown()

        parameters = generate_parameters(rng)
        last_parameters = parameters

        print(
            f"[{index:03d}] base_elements={parameters['base_elements']} size={parameters['size']} "
            f"color={parameters['color']} line_width={parameters['line_width']} "
            f"position={parameters['position']}"
        )

        draw(artist, **parameters)
        screen.update()
        save_canvas_png(screen, OUTPUT_DIR / f"img_{index:03d}.png")

    if last_parameters is not None:
        screen.update()
        save_canvas_png(screen, SCREENSHOT_PATH)

    artist.hideturtle()
    screen.bye()


if __name__ == "__main__":
    main()
