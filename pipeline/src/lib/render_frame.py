#!/usr/bin/env python3
# 用 Pillow 渲染单帧 PNG（背景渐变 + 产品名 + 多语言标题 + CTA）
# 供 05-video.js 调用，再由 ffmpeg 封装成短视频。
import sys
import json

from PIL import Image, ImageDraw, ImageFont

FONTS = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/GeezaPro.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def load_font(size):
    for p in FONTS:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def hex_to_rgb(h):
    h = h.lstrip("#")
    if h.startswith("0x"):
        h = h[2:]
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def fit_font(draw, text, path, size, max_w):
    """把字号降到能放进 max_w 为止。"""
    while size > 16:
        try:
            f = ImageFont.truetype(path, size)
        except Exception:
            return load_font(size), size
        w = draw.textlength(text, font=f)
        if w <= max_w:
            return f, size
        size -= 4
    return load_font(size), size


def wrap_text(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render(cfg):
    W, H = cfg["width"], cfg["height"]
    base = hex_to_rgb(cfg["color"])
    dark = tuple(max(0, c - 70) for c in base)

    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    # 垂直渐变背景
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(base[i] + (dark[i] - base[i]) * t) for i in range(3)))

    product = cfg["product"]
    title = cfg["title"]
    cta = cfg["cta"]
    margin = 80

    # 产品名（最大号，顶部）
    f1, s1 = fit_font(d, product, FONTS[0], 88, W - margin * 2)
    d.text(((W - d.textlength(product, font=f1)) / 2, H * 0.28), product, font=f1, fill=(255, 255, 255))

    # 标题（强调色）
    accent = (255, 209, 102)
    f2, s2 = fit_font(d, title, FONTS[0], 64, W - margin * 2)
    for i, line in enumerate(wrap_text(d, title, f2, W - margin * 2)):
        d.text(((W - d.textlength(line, font=f2)) / 2, H * 0.44 + i * s2 * 1.25), line, font=f2, fill=accent)

    # CTA（底部，带半透明圆角框）
    f3, s3 = fit_font(d, cta, FONTS[0], 48, W - margin * 2)
    pad_x, pad_y = 36, 22
    tw = d.textlength(cta, font=f3)
    x0, y0 = (W - tw) / 2 - pad_x, H * 0.74
    x1, y1 = (W + tw) / 2 + pad_x, y0 + s3 + pad_y * 2
    box = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(box)
    bd.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=(0, 0, 0, 120))
    img = Image.alpha_composite(img.convert("RGBA"), box).convert("RGB")
    d = ImageDraw.Draw(img)
    d.text(((W - tw) / 2, y0 + pad_y), cta, font=f3, fill=(255, 255, 255))

    img.save(cfg["out"], "PNG")


if __name__ == "__main__":
    render(json.load(sys.stdin))
