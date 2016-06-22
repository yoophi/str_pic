from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from flask import Flask, send_file

app = Flask(__name__)


@app.route('/pic/<int:width>/<int:height>/<string:txt>')
def x(width, height, txt):
    text_color = "black"
    bg_color = "yellow"

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    fontsize = 1  # starting font size
    img_fraction = 0.90 # portion of image width you want text width to be

    font = ImageFont.truetype("Arial.ttf", fontsize)
    while font.getsize(txt)[0] < img_fraction * img.size[0] and font.getsize(txt)[1] < img_fraction * img.size[1]:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype("Arial.ttf", fontsize)

    render_width, render_height = font.getsize(txt)

    draw.text((
        (width - render_width) / 2,
        (height - render_height) / 2
    ), txt, font=font, fill=text_color)  # put the

    offset_width = (width - render_width) / 2
    offset_height = (height - render_height) / 2
    draw.rectangle((0 + offset_width, 0 + offset_height, render_width + offset_width, render_height + offset_height),
                   outline="pink")

    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)

    return send_file(byte_io,
                     mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True, port=8001)
