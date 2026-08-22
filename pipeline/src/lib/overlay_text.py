#!/usr/bin/env python3
"""Render a transparent text overlay (kicker/title/subtitle) for video scenes.

Output is a 1920x1080 RGBA PNG with only the text elements drawn, so ffmpeg can
composite it over a real video clip with the `overlay` filter.
"""
import json
import sys
from PIL import Image, ImageDraw, ImageFont

FONT_DISPLAY = "/System/Library/Fonts/Supplemental/Songti.ttc"
FONT_SANS = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_UNICODE = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"


def font(path, size):
    for candidate in (path, FONT_UNICODE):
        try:
            return ImageFont.truetype(candidate, int(size))
        except Exception:
            pass
    return ImageFont.load_default()


def rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def wrap_text(draw, text, fnt, max_width):
    lines, current = [], ""
    for char in text:
        candidate = current + char
        if current and draw.textlength(candidate, font=fnt) > max_width:
            lines.append(current)
            current = char
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def render(spec):
    width = int(spec.get("width", 1920))
    height = int(spec.get("height", 1080))
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    gold = rgb(spec.get("gold", "#C9A227"))
    white = rgb(spec.get("white", "#FFFBF5"))
    red = rgb(spec.get("red", "#9A2626"))
    margin_x = int(width * 0.075)

    kicker_font = font(FONT_SANS, 31)
    title_font = font(FONT_DISPLAY, 78)
    subtitle_font = font(FONT_SANS, 35)
    body_font = font(FONT_SANS, 31)

    kicker = spec.get("kicker", "")
    title = spec.get("title", "")
    subtitle = spec.get("subtitle", "")
    narration = spec.get("narration", "")

    # Kicker with gold accent bar
    if kicker:
        draw.rounded_rectangle(
            (margin_x, int(height * 0.10), margin_x + 18, int(height * 0.10) + 52),
            radius=8, fill=(*gold, 255)
        )
        draw.text((margin_x + 34, int(height * 0.10)), kicker, font=kicker_font, fill=(*gold, 255))

    # Title
    title_y = int(height * 0.24)
    title_lines = wrap_text(draw, title, title_font, int(width * 0.70))
    for index, line in enumerate(title_lines[:2]):
        draw.text((margin_x, title_y + index * 96), line, font=title_font, fill=(*white, 255), stroke_width=1, stroke_fill=(*red, 160))

    if subtitle:
        sub_y = title_y + max(1, len(title_lines[:2])) * 96 + 16
        draw.text((margin_x, sub_y), subtitle, font=subtitle_font, fill=(*gold, 255))

    # Bottom narration caption card
    if narration:
        body_lines = wrap_text(draw, narration, body_font, int(width * 0.78))
        body_lines = body_lines[:3]
        line_height = 48
        box_h = len(body_lines) * line_height + 42
        box_y = height - int(height * 0.18) - box_h
        box_x = margin_x
        box_w = width - margin_x * 2
        draw.rounded_rectangle((box_x, box_y, box_x + box_w, box_y + box_h), radius=18, fill=(12, 5, 3, 180), outline=(*gold, 130), width=2)
        for index, line in enumerate(body_lines):
            draw.text((box_x + 26, box_y + 18 + index * line_height), line, font=body_font, fill=(*white, 255))

    img.save(spec["output"], "PNG")


if __name__ == "__main__":
    render(json.load(sys.stdin))