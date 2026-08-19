#!/usr/bin/env python3
# 品牌影片逐帧动画渲染器
# 单次调用渲染一个场景的全部帧（背景只算一次，文字按 easing 关键帧动画）
# 动画：标题淡入+上移+缩放、副标题滑入、装饰圆环缓慢扩张、封面缩放进入。
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

FONT_SERIF = "/System/Library/Fonts/Supplemental/Songti.ttc"
FONT_SANS = "/System/Library/Fonts/STHeiti Medium.ttc"
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


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


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


def draw_text(frame, W, text, font, cx, y, fill_rgb, alpha, scale=1.0):
    """把文字（可缩放、带透明度、按中心 x 对齐）画到 frame 上。"""
    if not text or alpha <= 0.0:
        return
    a = int(255 * alpha)
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad = 4
    layer = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.text((pad - bbox[0], pad - bbox[1]), text, font=font, fill=(*fill_rgb, a))
    if scale != 1.0:
        nw = max(1, int(layer.width * scale))
        nh = max(1, int(layer.height * scale))
        layer = layer.resize((nw, nh), Image.LANCZOS)
    ox = int(cx - layer.width / 2)
    oy = int(y - pad * scale)
    frame.alpha_composite(layer, (ox, oy))


def render(scene):
    W = scene["w"]
    H = scene["h"]
    fps = scene["fps"]
    dur = scene["dur"]
    out_dir = scene["out_dir"]
    os.makedirs(out_dir, exist_ok=True)

    top = hexrgb(scene["bg"][0])
    bottom = hexrgb(scene["bg"][1])
    accent = hexrgb(scene.get("accent", "#E0B060"))
    white = (255, 252, 245)

    s = H / 1920.0
    F_KICK = 40 * s
    F_HEAD = 108 * s
    F_HEAD2 = 96 * s
    F_SUB = 46 * s
    F_FOOT = 34 * s

    is_cover = scene.get("is_cover", False)
    single_p = scene.get("single_p")          # 若提供，则只渲染 1 帧并固定在进度 single_p
    N = 1 if single_p is not None else max(1, int(round(fps * dur)))

    # 背景渐变（只算一次）+ 静态装饰环
    base = gradient(W, H, top, bottom).convert("RGBA")

    # 预先准备的字体
    fonts = {}
    for key, path, size in [
        ("kick", FONT_SANS, F_KICK),
        ("head", FONT_SERIF, F_HEAD),
        ("head2", FONT_SERIF, F_HEAD2),
        ("sub", FONT_SANS, F_SUB),
        ("foot", FONT_SANS, F_FOOT),
    ]:
        fonts[key] = load(path, size)

    # 副标题按宽度自适应换行
    subtitle = scene.get("subtitle", "")
    sub_lines = []
    if subtitle:
        probe = ImageDraw.Draw(Image.new("RGBA", (W, H)))
        sf = fonts["sub"]
        sub_lines = wrap(probe, subtitle, sf, W - int(180 * s))

    kicker = scene.get("kicker", "")
    headline = scene.get("headline", "")
    headline2 = scene.get("headline2", "")
    footer = scene.get("footer", "心同共生")

    # 主标题字号自适应（避免超出）
    probe = ImageDraw.Draw(Image.new("RGBA", (W, H)))
    max_w = W - int(180 * s)
    hf, _ = fit(probe, headline, FONT_SERIF, F_HEAD, max_w) if headline else (fonts["head"], F_HEAD)
    h2f, _ = fit(probe, headline2, FONT_SERIF, F_HEAD2, max_w) if headline2 else (fonts["head2"], F_HEAD2)
    fonts["head"] = hf
    fonts["head2"] = h2f

    ring_base = int(min(W, H) * (0.40 if is_cover else 0.34))

    for i in range(N):
        p = single_p if single_p is not None else (i / N)
        frame = base.copy()
        d = ImageDraw.Draw(frame, "RGBA")

        # 装饰圆环：缓慢扩张 + 呼吸透明度
        grow = 1 + 0.04 * ease(p)
        ring_r = int(ring_base * grow)
        cx, cy = W // 2, int(H * (0.42 if is_cover else 0.40))
        ring_alpha = int(46 + 10 * ease(p))
        d.ellipse([cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r],
                  outline=(*accent, ring_alpha), width=max(1, int(2 * s)))

        if is_cover:
            # 封面：主标题缩放进入 + 副题 + 角标
            t = ease(p / 0.45)
            scale = 0.86 + 0.14 * t
            draw_text(frame, W, headline, fonts["head"], W / 2, H * 0.40, white, t, scale)
            draw_text(frame, W, kicker, fonts["kick"], W / 2, H * 0.30, accent, ease(p / 0.30))
            draw_text(frame, W, headline2, fonts["head2"], W / 2, H * 0.56, accent, ease((p - 0.15) / 0.30))
        else:
            # 角标：先淡入
            ka = ease(p / 0.10)
            if kicker:
                draw_text(frame, W, kicker, fonts["kick"], W / 2, H * 0.13, accent, ka)
            # 主标题：淡入 + 上移
            h1a = ease((p - 0.06) / 0.20)
            h1y = H * 0.34 + (1 - h1a) * 50 * s
            draw_text(frame, W, headline, fonts["head"], W / 2, h1y, white, h1a)
            # 第二行：错峰淡入 + 上移
            if headline2:
                h2a = ease((p - 0.14) / 0.20)
                h2y = H * 0.34 + (110 * s) + (1 - h2a) * 40 * s
                draw_text(frame, W, headline2, fonts["head2"], W / 2, h2y, white, h2a)
            # 副标题：底部滑入
            sa = ease((p - 0.40) / 0.25)
            sy = H * 0.72 + (1 - sa) * 30 * s
            for li, ln in enumerate(sub_lines):
                draw_text(frame, W, ln, fonts["sub"], W / 2, sy + li * 56 * s, accent, sa)

        # 底部品牌落款（全程低透明度）
        draw_text(frame, W, footer, fonts["foot"], W / 2, H * 0.90, (255, 255, 255), 0.70)
        # 落款金线
        fy2 = int(H * 0.90 + 46 * s)
        d.line([(W / 2 - 90 * s, fy2), (W / 2 + 90 * s, fy2)], fill=(*accent, 150), width=max(1, int(2 * s)))

        frame.convert("RGB").save(os.path.join(out_dir, f"f{i:04d}.png"))


if __name__ == "__main__":
    render(json.load(sys.stdin))
