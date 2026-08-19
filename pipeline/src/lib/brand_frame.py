#!/usr/bin/env python3
# 品牌场景帧渲染器：渐变背景 + 金线装饰 + 宋体大标题 + 黑体副标题
# 分辨率自适应（9:16 竖屏 / 16:9 横屏），字号按画布高度等比缩放。
import json
import sys

from PIL import Image, ImageDraw, ImageFont

FONT_SERIF = "/System/Library/Fonts/Supplemental/Songti.ttc"   # 宋体（标题）
FONT_SANS = "/System/Library/Fonts/STHeiti Medium.ttc"         # 黑体（副标题/角标）
FONT_UNI = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"


def load(path, size):
    try:
        return ImageFont.truetype(path, int(size))
    except Exception:
        return ImageFont.truetype(FONT_UNI, int(size))


def hexrgb(h):
    h = h.lstrip("#")
    if h.startswith("0x"):
        h = h[2:]
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def gradient(W, H, top, bottom):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return img


def fit(draw, text, font_path, size, max_w):
    size = int(size)
    while size > 12:
        f = load(font_path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f, size
        size -= 2
    return load(font_path, 12), 12


def center(draw, text, font, y, fill, W):
    w = draw.textlength(text, font=font)
    draw.text(((W - w) / 2, y), text, font=font, fill=fill)


def wrap(d, text, font, max_w):
    lines, cur = [], ""
    for ch in text:
        if d.textlength(cur + ch, font=font) <= max_w:
            cur += ch
        else:
            lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines[:3]


def render(scene):
    W = scene["w"]
    H = scene["h"]
    top = hexrgb(scene["bg"][0])
    bottom = hexrgb(scene["bg"][1])
    accent = hexrgb(scene.get("accent", "#E0B060"))

    # 字号基准：以 1920 高度为参考等比缩放
    s = H / 1920.0
    F_KICK = 40 * s
    F_HEAD = 108 * s
    F_HEAD2 = 96 * s
    F_SUB = 46 * s
    F_FOOT = 34 * s

    img = gradient(W, H, top, bottom)
    d = ImageDraw.Draw(img, "RGBA")

    # 装饰大圆环（月/印章意象，低透明度）
    ring_r = int(min(W, H) * 0.34)
    ring_cx, ring_cy = W // 2, int(H * 0.40)
    d.ellipse(
        [ring_cx - ring_r, ring_cy - ring_r, ring_cx + ring_r, ring_cy + ring_r],
        outline=(*accent, 40),
        width=max(2, int(2 * s)),
    )

    margin = int(90 * s)
    max_w = W - margin * 2

    # 顶部角标 + 两侧短线
    kicker = scene.get("kicker", "")
    if kicker:
        kf = load(FONT_SANS, F_KICK)
        kw = d.textlength(kicker, font=kf)
        ky = int(H * 0.13)
        center(d, kicker, kf, ky, accent, W)
        line_gap = kw / 2 + 40 * s
        ly = ky + int(26 * s)
        d.line([(W / 2 - line_gap, ly), (W / 2 - line_gap - 60 * s, ly)], fill=(*accent, 160), width=max(1, int(2 * s)))
        d.line([(W / 2 + line_gap, ly), (W / 2 + line_gap + 60 * s, ly)], fill=(*accent, 160), width=max(1, int(2 * s)))

    # 主标题
    headline = scene.get("headline", "")
    hf, hs = fit(d, headline, FONT_SERIF, F_HEAD, max_w)
    hy = H * 0.34
    center(d, headline, hf, hy, (255, 252, 245), W)

    # 第二行标题
    headline2 = scene.get("headline2", "")
    if headline2:
        h2f, _ = fit(d, headline2, FONT_SERIF, F_HEAD2, max_w)
        center(d, headline2, h2f, hy + hs * 1.45, (255, 252, 245), W)

    # 副标题
    subtitle = scene.get("subtitle", "")
    if subtitle:
        sf, ss = fit(d, subtitle, FONT_SANS, F_SUB, max_w)
        lines = wrap(d, subtitle, sf, max_w)
        sy = H * 0.72
        for i, ln in enumerate(lines):
            center(d, ln, sf, sy + i * ss * 1.4, accent, W)

    # 底部品牌落款 + 金线
    footer = scene.get("footer", "心同共生")
    ff = load(FONT_SANS, F_FOOT)
    fy = int(H * 0.90)
    center(d, footer, ff, fy, (255, 255, 255, 180), W)
    fy2 = fy + int(46 * s)
    d.line([(W / 2 - 90 * s, fy2), (W / 2 + 90 * s, fy2)], fill=(*accent, 160), width=max(1, int(2 * s)))

    img.save(scene["out"], "PNG")


if __name__ == "__main__":
    render(json.load(sys.stdin))
