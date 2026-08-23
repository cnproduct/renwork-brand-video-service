import asyncio, os, sys, subprocess, shutil
import edge_tts
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

print("================ ChatCut Master Edition: Cinematic Typography & Layout ================")

VOICE = "zh-CN-YunyangNeural"
LOGO_PATH = "public/brand/renwork_logo_correct.png"
if not os.path.exists(LOGO_PATH):
    LOGO_PATH = "public/brand/logo.png"

V_STUDENTS = "Students_listening_to_training_l…_202608200221.mp4"
V_INQUIRING = "customer_are_inquiring_busily_202608200220.mp4"
V_INTENT = "RenWork_B2B_Buyer_Intend_release_202608200214.mp4"
V_CUSTOMS = "自动抓取海关数据.mp4"
V_SOCIAL = "自动运营社媒平台.mp4"

OUTPUT_VIDEO = "renrenyi_renwork_training_cinematic_master.mp4"

W, H, FPS = 1920, 1080, 30

FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

def font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_PATH, size, index=1 if bold else 0)
    except:
        return ImageFont.truetype(FONT_PATH, size)

logo_raw = Image.open(LOGO_PATH).convert("RGBA")
logo_top = logo_raw.resize((56, 56), Image.Resampling.LANCZOS)
logo_big = logo_raw.resize((140, 140), Image.Resampling.LANCZOS)

# 8 Concise, High-Impact Sentences
SENTENCES = [
    "为什么全国外贸老板纷纷走进 RenWork 外贸 AI 增长实战营？",
    "因为这里不讲假大空的理论，全员自带电脑，手把手跑通四大知识库与真实订单闭环！",
    "现场重磅发布全球 B2B 买家真实采购意向，秒级锁定正在采购的 R1 级真实大买家！",
    "结合历史海关提单与邓白氏数据，一键生成 6 国母语定制开发信与精准报价方案！",
    "现场咨询持续火爆！学员当天搭建私有营销大脑，当场收到海外买家高意向回复！",
    "就像 10 年外贸销冠现场指导，大幅提升谈单签单率！",
    "用确定性增长操作系统驱动企业全球业绩倍增，让中国制造赢在全球！",
    "人人易智能科技有限公司 —— RenWork 外贸增长实战营，立即预约全国城市席位！"
]

# Minimalist Hero Badge per Act (Large, Bold, Clean)
HERO_BADGES = [
    {"tag": "🔥 实战营火爆现场", "title": "全员自带电脑 · 现场跑通闭环", "sub": "不讲空洞理论 · 沉淀企业私有 AI 大脑", "color": (56, 189, 248)},
    {"tag": "📚 01 企业经验数字化", "title": "搭建四大知识库 ＋ 业务账", "sub": "产品手册/报价/SOP 一键装入 AI 大脑", "color": (245, 158, 11)},
    {"tag": "🎯 02 全球买家意向发布", "title": "直达 R1 级采购决策人", "sub": "海关真实提单 ＋ 邓白氏秒级穿透", "color": (16, 185, 129)},
    {"tag": "🌐 03 全媒体矩阵触达", "title": "6国母语开发信 ＋ 自动排期", "sub": "结合历史提单精准破冰 · 回复率飙升", "color": (249, 115, 22)},
    {"tag": "🔥 04 现场火爆咨询", "title": "当场收获买家高意向回复", "sub": "学员当天搭建中台 · 当天收到询盘", "color": (239, 68, 68)},
    {"tag": "🤝 05 销冠让步谈判", "title": "10年外贸专家让步策略", "sub": "化解疯狂压价 · 牢牢守住利润底线", "color": (168, 85, 247)},
    {"tag": "🚀 确定性增长操作系统", "title": "驱动企业全球业绩倍增", "sub": "让中国制造赢在全球！", "color": (245, 158, 11)},
    {"tag": "📞 全国城市火热开营", "title": "立即预约实战营席位！", "sub": "人人易智能科技有限公司 · 官方出品", "color": (249, 115, 22)}
]

def get_duration(fpath):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", fpath]
    return float(subprocess.run(cmd, stdout=subprocess.PIPE, text=True).stdout.strip())

async def generate_audio():
    print("\n================ Step 1: Generating Sentence Audio with Yunyang ================")
    seg_files = []
    sub_list = []
    cur_offset = 0.0
    gap = 0.22

    for idx, sentence in enumerate(SENTENCES):
        seg_f = f"temp_cine_voice_{idx}.mp3"
        comm = edge_tts.Communicate(sentence.strip(), VOICE, rate="+4%")
        await comm.save(seg_f)
        seg_dur = get_duration(seg_f)
        
        st = cur_offset
        et = cur_offset + seg_dur
        sub_list.append((st, et, sentence.strip(), idx))
        seg_files.append(seg_f)
        cur_offset = et + gap
        print(f"[{st:.2f}s -> {et:.2f}s] ({seg_dur:.2f}s) {sentence}")

    concat_list_file = "concat_cine.txt"
    with open(concat_list_file, "w") as f:
        for sf in seg_files:
            f.write(f"file '{sf}'\n")
    
    v_concat = "voice_cine_concat.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_file,
        "-c", "copy", v_concat
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    v_mix = "voice_cine_mix.mp3"
    total_audio_dur = cur_offset
    subprocess.run([
        "ffmpeg", "-y", "-i", v_concat,
        "-f", "lavfi", "-i", f"anoisesrc=d={int(total_audio_dur+10)}:c=pink:r=44100:a=0.012",
        "-filter_complex",
        f"[1:a]volume=0.07,afade=t=in:ss=0:d=1.5,afade=t=out:st={max(1, total_audio_dur-2)}:d=2[bgm];"
        "[0:a][bgm]amix=inputs=2:duration=first[out]",
        "-map", "[out]", "-c:a", "libmp3lame", "-b:a", "192k", v_mix
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    duration = get_duration(v_mix)
    print(f"✨ 混合音频就绪：总时长 {duration:.2f}s")
    
    return v_mix, duration, sub_list, seg_files, concat_list_file, v_concat

async def main():
    v_mix, duration, sub_list, seg_files, concat_list_file, v_concat = await generate_audio()
    
    print("\n================ Step 2: Setting Up Cinematic Video Streams ================")
    # Full Screen Main Video: 1920x1080
    frame_bytes_main = W * H * 3
    
    # PIP Floating Card: 540x304 (16:9 ratio, crisp & compact)
    pip_w, pip_h = 540, 304
    frame_bytes_pip = pip_w * pip_h * 3
    
    total_frames = int(round(duration * FPS))
    print(f"总帧数: {total_frames} 帧 @ {FPS} FPS")

    # Pipes for main full-screen backgrounds
    p_students = subprocess.Popen([
        "ffmpeg", "-stream_loop", "-1", "-i", V_STUDENTS,
        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", "-r", str(FPS),
        "-f", "image2pipe", "-vcodec", "rawvideo", "-pix_fmt", "rgb24", "-"
    ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**7)

    p_intent = subprocess.Popen([
        "ffmpeg", "-stream_loop", "-1", "-i", V_INTENT,
        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", "-r", str(FPS),
        "-f", "image2pipe", "-vcodec", "rawvideo", "-pix_fmt", "rgb24", "-"
    ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**7)

    p_inquiring = subprocess.Popen([
        "ffmpeg", "-stream_loop", "-1", "-i", V_INQUIRING,
        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", "-r", str(FPS),
        "-f", "image2pipe", "-vcodec", "rawvideo", "-pix_fmt", "rgb24", "-"
    ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**7)

    # Pipes for PIP live demos
    p_customs = subprocess.Popen([
        "ffmpeg", "-stream_loop", "-1", "-i", V_CUSTOMS,
        "-vf", f"scale={pip_w}:{pip_h}", "-r", str(FPS),
        "-f", "image2pipe", "-vcodec", "rawvideo", "-pix_fmt", "rgb24", "-"
    ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**7)

    p_social = subprocess.Popen([
        "ffmpeg", "-stream_loop", "-1", "-i", V_SOCIAL,
        "-vf", f"scale={pip_w}:{pip_h}", "-r", str(FPS),
        "-f", "image2pipe", "-vcodec", "rawvideo", "-pix_fmt", "rgb24", "-"
    ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**7)

    # Encoder
    ff_pipe = subprocess.Popen([
        "ffmpeg", "-y", "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{W}x{H}", "-pix_fmt", "rgb24", "-r", str(FPS), "-i", "-",
        "-i", v_mix, "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", OUTPUT_VIDEO
    ], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    t_stage1_end = sub_list[1][1]
    t_stage2_end = sub_list[3][1]
    t_stage3_end = sub_list[5][1]

    # Pre-generate top and bottom gradient masks for cinematic contrast
    gradient_top = Image.new("RGBA", (W, 200), (0, 0, 0, 0))
    draw_gt = ImageDraw.Draw(gradient_top)
    for y in range(200):
        alpha = int(220 * (1 - y / 200.0))
        draw_gt.line([(0, y), (W, y)], fill=(9, 13, 22, alpha))

    gradient_bottom = Image.new("RGBA", (W, 260), (0, 0, 0, 0))
    draw_gb = ImageDraw.Draw(gradient_bottom)
    for y in range(260):
        alpha = int(240 * (y / 260.0))
        draw_gb.line([(0, y), (W, y)], fill=(9, 13, 22, alpha))

    print("\n================ Step 3: Rendering Master Cinematic Frames ================")
    for f_idx in range(total_frames):
        cur_t = f_idx / FPS
        
        # Read frames
        raw_students = p_students.stdout.read(frame_bytes_main)
        img_students = Image.frombytes("RGB", (W, H), raw_students) if raw_students else None

        raw_intent = p_intent.stdout.read(frame_bytes_main)
        img_intent = Image.frombytes("RGB", (W, H), raw_intent) if raw_intent else None

        raw_inquiring = p_inquiring.stdout.read(frame_bytes_main)
        img_inquiring = Image.frombytes("RGB", (W, H), raw_inquiring) if raw_inquiring else None

        raw_customs = p_customs.stdout.read(frame_bytes_pip)
        img_customs = Image.frombytes("RGB", (pip_w, pip_h), raw_customs) if raw_customs else None

        raw_social = p_social.stdout.read(frame_bytes_pip)
        img_social = Image.frombytes("RGB", (pip_w, pip_h), raw_social) if raw_social else None

        # 1. Main Background Video (Full Screen 1920x1080)
        if cur_t <= t_stage1_end:
            canvas = img_students.copy() if img_students else Image.new("RGB", (W, H), (9, 13, 22))
        elif cur_t <= t_stage2_end:
            canvas = img_intent.copy() if img_intent else Image.new("RGB", (W, H), (9, 13, 22))
        elif cur_t <= t_stage3_end:
            canvas = img_inquiring.copy() if img_inquiring else Image.new("RGB", (W, H), (9, 13, 22))
        else:
            canvas = img_students.copy() if img_students else Image.new("RGB", (W, H), (9, 13, 22))

        # Convert to RGBA for overlay blending
        canvas = canvas.convert("RGBA")

        # 2. Apply Top and Bottom Gradient Scrims for text contrast
        canvas.alpha_composite(gradient_top, (0, 0))
        canvas.alpha_composite(gradient_bottom, (0, H - 260))

        # 3. Dynamic PIP Video Card (When showing customs or social automation)
        draw = ImageDraw.Draw(canvas)

        if t_stage1_end < cur_t <= t_stage2_end and img_customs:
            # Floating Customs PIP at bottom-right
            pip_x, pip_y = W - pip_w - 60, H - pip_h - 220
            # Dark card backing with glowing border
            draw.rounded_rectangle([pip_x - 6, pip_y - 42, pip_x + pip_w + 6, pip_y + pip_h + 6], radius=16, fill=(12, 18, 30, 240), outline=(16, 185, 129, 255), width=2)
            draw.text((pip_x + 14, pip_y - 32), "🎯 海关真实提单穿透实操演示", font=font(20, True), fill=(16, 185, 129))
            canvas.paste(img_customs, (pip_x, pip_y))

        elif t_stage2_end < cur_t <= t_stage3_end and img_social:
            # Floating Social Automation PIP at bottom-right
            pip_x, pip_y = W - pip_w - 60, H - pip_h - 220
            draw.rounded_rectangle([pip_x - 6, pip_y - 42, pip_x + pip_w + 6, pip_y + pip_h + 6], radius=16, fill=(12, 18, 30, 240), outline=(249, 115, 22, 255), width=2)
            draw.text((pip_x + 14, pip_y - 32), "🚀 6国母语全媒体矩阵自动排期", font=font(20, True), fill=(249, 115, 22))
            canvas.paste(img_social, (pip_x, pip_y))

        # 4. Top-Left Minimalist Glass Pill (Brand Watermark)
        draw.rounded_rectangle([50, 36, 440, 102], radius=20, fill=(12, 18, 30, 225), outline=(56, 189, 248, 180), width=2)
        canvas.paste(logo_top, (64, 41), logo_top)
        draw.text((132, 45), "RenWork", font=font(26, True), fill=(255, 255, 255))
        draw.text((132, 73), "外贸 AI 增长实战营", font=font(16, False), fill=(160, 175, 200))

        # 5. Top-Right / Hero Punchy Kinetic Typography Card (Large, Minimalist, High-Impact)
        # Find current active sentence and its hero badge
        cur_badge = HERO_BADGES[0]
        cur_sentence_text = SENTENCES[0]
        for st, et, txt, sidx in sub_list:
            if st <= cur_t < et:
                cur_badge = HERO_BADGES[sidx] if sidx < len(HERO_BADGES) else HERO_BADGES[-1]
                cur_sentence_text = txt
                break

        # Large Hero Badge Container (Top-Right)
        badge_w, badge_h = 760, 120
        bx, by = W - badge_w - 50, 36
        draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=20, fill=(9, 13, 22, 225), outline=cur_badge["color"], width=2)
        
        # Punchy Big Text (34px bold main title + 20px sub)
        draw.text((bx + 26, by + 18), cur_badge["tag"], font=font(20, True), fill=cur_badge["color"])
        draw.text((bx + 26, by + 48), cur_badge["title"], font=font(34, True), fill=(255, 255, 255))
        draw.text((bx + 26, by + 88), cur_badge["sub"], font=font(18, False), fill=(200, 215, 235))

        # 6. Center-Bottom Cinema-Grade Subtitles (Big 44px Font, Zero-Drift, Crystal Clear)
        for st, et, txt, sidx in sub_list:
            if st <= cur_t < et:
                f_sub = font(44, True)
                bbox = f_sub.getbbox(txt)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                sx = (W - (tw + 72)) // 2
                sy = H - 150
                
                # Dark Glass Pill with Glow Border
                draw.rounded_rectangle([sx, sy, sx + tw + 72, sy + th + 32], radius=18, fill=(0, 0, 0, 235), outline=cur_badge["color"], width=2)
                
                # Subtitle text with keyword color styling
                txt_color = (255, 255, 255)
                draw.text((sx + 36, sy + 14), txt, font=f_sub, fill=txt_color)
                break

        # 7. Thin Neon Progress Bar at very bottom
        prog = (f_idx + 1) / total_frames
        draw.line([0, H - 6, int(W * prog), H - 6], fill=(249, 115, 22), width=6)

        # Convert back to RGB and write
        final_frame = canvas.convert("RGB")
        ff_pipe.stdin.write(final_frame.tobytes())

        if (f_idx + 1) % 300 == 0 or (f_idx + 1) == total_frames:
            print(f"[Cinematic Master] 渲染进度: {f_idx + 1}/{total_frames} ({(f_idx + 1) / total_frames * 100:.1f}%)")

    ff_pipe.stdin.close()
    ff_pipe.wait()

    # Kill pipes
    p_students.kill()
    p_intent.kill()
    p_inquiring.kill()
    p_customs.kill()
    p_social.kill()

    # Cleanup
    for sf in seg_files:
        if os.path.exists(sf): os.remove(sf)
    if os.path.exists(concat_list_file): os.remove(concat_list_file)
    if os.path.exists(v_concat): os.remove(v_concat)

    print(f"\n🎉🎉🎉 电影级极简大字排版大片已成功生成：{OUTPUT_VIDEO}")

asyncio.run(main())
