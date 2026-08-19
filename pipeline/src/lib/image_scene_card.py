#!/usr/bin/env python3
"""Render a branded 16:9 scene card from a real photograph.

The card is intentionally rendered as a single high-resolution image. FFmpeg
adds a subtle Ken Burns motion while the card is held on screen, keeping the
source photograph recognizable and avoiding heavy frame-sequence storage.
"""
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

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


def cover_crop(image, width, height):
    image = image.convert("RGB")
    scale = max(width / image.width, height / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - width) // 2
    top = (resized.height - height) // 2
    return resized.crop((left, top, left + width, top + height))


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
    source = spec["image"]
    output = spec["output"]
    image = cover_crop(Image.open(source), width, height).convert("RGBA")

    # Overall cinematic darkening; the lower panel makes long Chinese copy readable.
    overlay = Image.new("RGBA", (width, height), (12, 5, 3, 72))
    image = Image.alpha_composite(image, overlay)
    panel = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    for y in range(height):
        t = max(0.0, min(1.0, (y - height * 0.40) / (height * 0.60)))
        alpha = int(15 + 165 * t)
        pd.line([(0, y), (width, y)], fill=(18, 7, 5, alpha))
    image = Image.alpha_composite(image, panel)

    draw = ImageDraw.Draw(image, "RGBA")
    gold = rgb(spec.get("gold", "#E0B060"))
    white = rgb(spec.get("white", "#FFFBF5"))
    red = rgb(spec.get("red", "#A0261C"))
    margin_x = int(width * 0.075)

    kicker_font = font(FONT_SANS, 31)
    title_font = font(FONT_DISPLAY, 78)
    subtitle_font = font(FONT_SANS, 35)
    body_font = font(FONT_SANS, 31)
    footer_font = font(FONT_SANS, 23)

    kicker = spec.get("kicker", "")
    title = spec.get("title", "")
    subtitle = spec.get("subtitle", "")
    narration = spec.get("narration", "")

    # Brand mark / section label.
    if kicker:
        draw.rounded_rectangle(
            (margin_x, int(height * 0.10), margin_x + 18, int(height * 0.10) + 52),
            radius=8, fill=(*gold, 255)
        )
        draw.text((margin_x + 34, int(height * 0.10)), kicker, font=kicker_font, fill=(*gold, 255))

    # Main title.
    title_y = int(height * 0.24)
    title_lines = wrap_text(draw, title, title_font, int(width * 0.70))
    for index, line in enumerate(title_lines[:2]):
        draw.text((margin_x, title_y + index * 96), line, font=title_font, fill=(*white, 255), stroke_width=1, stroke_fill=(*red, 160))

    if subtitle:
        sub_y = title_y + max(1, len(title_lines[:2])) * 96 + 16
        draw.text((margin_x, sub_y), subtitle, font=subtitle_font, fill=(*gold, 255))

    # Bottom narration caption: full sentence, wrapped in a readable two/three-line card.
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

    footer = spec.get("footer", "心同共生  ·  ONE HEART · GROWING TOGETHER")
    draw.text((margin_x, height - 52), footer, font=footer_font, fill=(255, 251, 245, 210))
    draw.line((width - margin_x - 220, height - 39, width - margin_x, height - 39), fill=(*gold, 180), width=2)

    os.makedirs(os.path.dirname(output), exist_ok=True)
    image.convert("RGB").save(output, "PNG", optimize=True)


if __name__ == "__main__":
    render(json.load(sys.stdin))
