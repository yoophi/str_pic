import os
import re
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont, ImageColor
from flask import Blueprint, send_file, request

__version__ = "0.1.0"

RE_HEX_FULL = re.compile("^[A-F0-9]{6}$", re.IGNORECASE)
RE_HEX_SHORT = re.compile("^[A-F0-9]{3}$", re.IGNORECASE)
DEFAULT_COLORS = {
    "BG": "yellow",
    "TEXT": "black",
    "BORDER": "silver",
}


class DummyImage:
    app = None

    def __init__(self, app=None, **kwargs):
        if app:
            self.init_app(app, **kwargs)

    def init_app(
        self, app, url_prefix="/dummyimage", endpoint="dummyimage", route="dummyimage"
    ):
        app.register_blueprint(
            self.create_blueprint(__name__, endpoint=endpoint, route=route),
            url_prefix=url_prefix,
        )

    def create_blueprint(self, import_name, endpoint="dummyimage", route="dummyimage"):
        bp = Blueprint(
            "dummyimage",
            import_name,
        )
        bp.route("/{route}".format(route=route), endpoint=endpoint)(self.dummyimage)
        bp.route("/{route}/<string:size>".format(route=route), endpoint=endpoint)(
            self.dummyimage
        )

        return bp

    def dummyimage(self, size="320"):
        # default variables
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "DroidSans.ttf")
        font_size = 20

        # get args
        width, height = get_size(size)
        text = request.args.get("text", "%dx%d" % (width, height))
        zoom_text = get_bool(request.args.get('zoom', 'True'))
        draw_border = get_bool(request.args.get('border', 'True'))
        debug = get_bool(request.args.get('debug', 'False'))

        bg_color = get_color(request.args.get("bg_color"), "BG")
        text_color = get_color(request.args.get("text_color"), "TEXT")
        border_color = get_color(request.args.get("border_color"), "BORDER")

        # draw image
        img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(img)

        if zoom_text:
            # if zoom is on
            font_size = 1  # starting font size
            img_fraction = 0.90  # portion of image width you want text width to be

            font = ImageFont.truetype(font_path, font_size)
            while (
                font.getsize(text)[0] < img_fraction * img.size[0]
                and font.getsize(text)[1] < img_fraction * img.size[1]
            ):
                # iterate until the text size is just larger than the criteria
                font_size += 1
                font = ImageFont.truetype(font_path, font_size)
        else:
            font_size = int(request.args.get("fontsize", font_size))
            font = ImageFont.truetype(font_path, font_size)

        render_width, render_height = font.getsize(text)

        draw.text(
            ((width - render_width) / 2, (height - render_height) / 2),
            text,
            font=font,
            fill=text_color,
        )  # put the

        if debug:
            offset_width = (width - render_width) / 2
            offset_height = (height - render_height) / 2
            draw.rectangle(
                (
                    0 + offset_width,
                    0 + offset_height,
                    render_width + offset_width,
                    render_height + offset_height,
                ),
                outline="red",
            )

        if draw_border:
            draw.rectangle((0, 0, width - 1, height - 1), outline=border_color)

        byte_io = BytesIO()
        img.save(byte_io, "PNG")
        byte_io.seek(0)

        return send_file(byte_io, mimetype="image/png")


def get_size(size):
    def match_cube(match):
        w = int(match.group(1))
        return w, w

    def match_width_height(match):
        return int(match.group(1)), int(match.group(2))

    width, height = None, None
    actions = (
        (r"^(\d+)$", match_cube),
        (r"^(\d+)x(\d+)$", match_width_height),
    )

    for regex, action in actions:
        m = re.match(regex, size)
        if m:
            width, height = action(m)
            break

    return width, height


def get_color(value, type):
    """Returns valid color"""
    if value and value.startswith("!"):
        # normalize hex color
        if RE_HEX_FULL.match(value[1:]):
            color = "#%s" % "".join(value[1:]).upper()
        elif RE_HEX_SHORT.match(value[1:]):
            # duplicate short values
            color = "#%s" % "".join(c * 2 for c in value[1:]).upper()
        else:
            # invalid color
            color = DEFAULT_COLORS[type]
        return color
    else:
        # assume literal color. e.g. white, grey69, etc
        value = value if value else DEFAULT_COLORS[type]
        try:
            ImageColor.getrgb(value)
        except ValueError:
            value = DEFAULT_COLORS[type]

        return value


def get_bool(value):
    return value.lower() in ("true", "on", "1")
