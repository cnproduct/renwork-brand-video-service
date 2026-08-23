import asyncio, os, sys, subprocess, shutil
import edge_tts
import numpy as np
from PIL import Image, ImageDraw, ImageFont

print("================ ChatCut Master V2: Complete 5-Video Mashup (Zero Repetition) ================")

VOICE = "zh-CN-YunyangNeural"
LOGO_PATH = "public/brand/renwork_logo_correct.png"
if not os.path.exists(LOGO_PATH):
    LOGO_PATH = "public/brand/logo.png"

# All 5 Real Event Video Assets
V_SPEAKER = "讲师激情演讲，学员认真听讲，反应热烈_202608200321.mp4"
V_STUDENTS = "Students_listening_to_training_l…_202608200221.mp4"
V_INTENT = "RenWork_B2B_Buyer_Intend_release_202608200214.mp4"
V_INTERACTION = "大家积极互动_202608200321.mp4"
V_INQUIRING = "customer_are_inquiring_busily_202608200220.mp4"

# 2 PIP Demo Videos
V_CUSTOMS = "自动抓取海关数据.mp4"
V_SOCIAL = "自动运营社媒平台.mp4"

OUTPUT_VIDEO = "renrenyi_renwork_training_cinematic_v2.mp4"

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

# 8 Distinct Hero Badges (One Unique Visual per Sentence)
HERO_BADGES = [
    {"tag": "🔥 实战营火爆开讲", "title": "讲师实战教学 · 反应空前热烈", "sub": "拒绝假大空 · 聚焦外贸真实业务痛点", "color": (56, 189, 248), "video_key": "speaker"},
    {"tag": "💻 01 企业经验数字化", "title": "全员自带电脑 · 现场跑通闭环", "sub": "产品参数/质检/SOP 一键装入 AI 大脑", "color": (245, 158, 11), "video_key": "students"},
    {"tag": "🎯 02 全球买家意向发布", "title": "锁定 R1 级真实采购决策人", "sub": "海关真实提单 ＋ 邓白氏秒级穿透", "color": (16, 185, 129), "video_key": "intent"},
    {"tag": "🌐 03 全媒体矩阵触达", "title": "6国母语开发信 ＋ 自动排期", "sub": "结合历史提单精准破冰 · 回复率飙升", "color": (249, 115, 22), "video_key": "intent"},
    {"tag": "🤝 04 现场深度互动研讨", "title": "全员积极互动 · 当场出海获客", "sub": "学员当天建大脑 · 当场收到买家意向回复", "color": (239, 68, 68), "video_key": "interaction"},
    {"tag": "💡 05 销冠让步谈判模型", "title": "10年外贸专家让步谈判策略", "sub": "化解疯狂压价 · 牢牢守住利润底线", "color": (168, 85, 247), "video_key": "inquiring"},
    {"tag": "🚀 确定性增长操作系统", "title": "驱动企业全球业绩确定性倍增", "sub": "打造属于中国实体制造的专属外贸引擎！", "color": (245, 158, 11), "video_key": "speaker"},
    {"tag": "📞 全国城市火热开营", "title": "立即预约企业实战营席位！", "sub": "人人易智能科技有限公司 · 官方出品", "color": (249, 115, 22), "video_key": "interaction"}
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
        seg_f = f"temp_v2_voice_{idx}.mp3"
        comm = edge_tts.Communicate(sentence.strip(), VOICE, rate="+4%")
        await comm.save(seg_f)
        seg_dur = get_duration(seg_f)
        
        st = cur_offset
        et = cur_offset + seg_dur
        sub_list.append((st, et, sentence.strip(), idx))
        seg_files.append(seg_f)
        cur_offset = et + gap
        print(f"[{st:.2f}s -> {et:.2f}s] ({seg_dur:.2f}s) {sentence}")

    concat_list_file = "concat_v2.txt"
    with open(concat_list_file, "w") as f:
        for sf in seg_files:
            f.write(f"file '{sf}'\n")
    
    v_concat = "voice_v2_concat.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_file,
        "-c", "copy", v_concat
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    v_mix = "voice_v2_mix.mp3"
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
    
    print("\n================ Step 2: Setting Up 5 Multi-Scene Video Streams ================")
    frame_bytes_main = W * H * 3
    pip_w, pip_h = 540, 304
    frame_bytes_pip = pip_w * pip_h * 3
    
    total_frames = int(round(duration * FPS))
    print(f"总帧数: {total_frames} 帧 @ {FPS} FPS")

    # Launch 5 main video pipes
    def make_main_pipe(vpath):
        return subprocess.Popen([
            "ffmpeg", "-stream_loop", "-1", "-i", vpath,
            "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", "-r", str(FPS),
            "-f", "image2pipe", "-vcodec", "rawvideo", "-pix_fmt", "rgb24", "-"
        ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**7)

    def make_pip_pipe(vpath):
        return subprocess.Popen([
            "ffmpeg", "-stream_loop", "-1", "-i", vpath,
            "-vf", f"scale={pip_w}:{pip_h}", "-r", str(FPS),
            "-f", "image2pipe", "-vcodec", "rawvideo", "-pix_fmt", "rgb24", "-"
        ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**7)

    p_speaker = make_main_pipe(V_SPEAKER)
    p_students = make_main_pipe(V_STUDENTS)
    p_intent = make_main_pipe(V_INTENT)
    p_interaction = make_main_pipe(V_INTERACTION)
    p_inquiring = make_main_pipe(V_INQUIRING)

    p_customs = make_pip_pipe(V_CUSTOMS)
    p_social = make_pip_pipe(V_SOCIAL)

    # Encoder
    ff_pipe = subprocess.Popen([
        "ffmpeg", "-y", "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{W}x{H}", "-pix_fmt", "rgb24", "-r", str(FPS), "-i", "-",
        "-i", v_mix, "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", OUTPUT_VIDEO
    ], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

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

    print("\n================ Step 3: Rendering Non-Repetitive Master Mashup ================")
    for f_idx in range(total_frames):
        cur_t = f_idx / FPS
        
        # Read frames from all 5 main streams
        raw_speaker = p_speaker.stdout.read(frame_bytes_main)
        img_speaker = Image.frombytes("RGB", (W, H), raw_speaker) if raw_speaker else None

        raw_students = p_students.stdout.read(frame_bytes_main)
        img_students = Image.frombytes("RGB", (W, H), raw_students) if raw_students else None

        raw_intent = p_intent.stdout.read(frame_bytes_main)
        img_intent = Image.frombytes("RGB", (W, H), raw_intent) if raw_intent else None

        raw_interaction = p_interaction.stdout.read(frame_bytes_main)
        img_interaction = Image.frombytes("RGB", (W, H), raw_interaction) if raw_interaction else None

        raw_inquiring = p_inquiring.stdout.read(frame_bytes_main)
        img_inquiring = Image.frombytes("RGB", (W, H), raw_inquiring) if raw_inquiring else None

        # Read frames from PIP streams
        raw_customs = p_customs.stdout.read(frame_bytes_pip)
        img_customs = Image.frombytes("RGB", (pip_w, pip_h), raw_customs) if raw_customs else None

        raw_social = p_social.stdout.read(frame_bytes_pip)
        img_social = Image.frombytes("RGB", (pip_w, pip_h), raw_social) if raw_social else None

        # Identify current sentence and badge
        cur_badge = HERO_BADGES[0]
        cur_sidx = 0
        for st, et, txt, sidx in sub_list:
            if st <= cur_t < et:
                cur_badge = HERO_BADGES[sidx] if sidx < len(HERO_BADGES) else HERO_BADGES[-1]
                cur_sidx = sidx
                break

        # Dynamically select background video based on sentence (NO REPETITION)
        v_key = cur_badge["video_key"]
        if v_key == "speaker":
            canvas = img_speaker.copy() if img_speaker else Image.new("RGB", (W, H), (9, 13, 22))
        elif v_key == "students":
            canvas = img_students.copy() if img_students else Image.new("RGB", (W, H), (9, 13, 22))
        elif v_key == "intent":
            canvas = img_intent.copy() if img_intent else Image.new("RGB", (W, H), (9, 13, 22))
        elif v_key == "interaction":
            canvas = img_interaction.copy() if img_interaction else Image.new("RGB", (W, H), (9, 13, 22))
        elif v_key == "inquiring":
            canvas = img_inquiring.copy() if img_inquiring else Image.new("RGB", (W, H), (9, 13, 22))
        else:
            canvas = img_speaker.copy() if img_speaker else Image.new("RGB", (W, H), (9, 13, 22))

        canvas = canvas.convert("RGBA")
        canvas.alpha_composite(gradient_top, (0, 0))
        canvas.alpha_composite(gradient_bottom, (0, H - 260))

        draw = ImageDraw.Draw(canvas)

        # Dynamic PIP Video Card (When showing customs or social automation in Sentences 3 & 4)
        if cur_sidx == 2 and img_customs:
            pip_x, pip_y = W - pip_w - 60, H - pip_h - 220
            draw.rounded_rectangle([pip_x - 6, pip_y - 42, pip_x + pip_w + 6, pip_y + pip_h + 6], radius=16, fill=(12, 18, 30, 240), outline=(16, 185, 129, 255), width=2)
            draw.text((pip_x + 14, pip_y - 32), "🎯 海关真实提单穿透实操演示", font=font(20, True), fill=(16, 185, 129))
            canvas.paste(img_customs, (pip_x, pip_y))

        elif cur_sidx == 3 and img_social:
            pip_x, pip_y = W - pip_w - 60, H - pip_h - 220
            draw.rounded_rectangle([pip_x - 6, pip_y - 42, pip_x + pip_w + 6, pip_y + pip_h + 6], radius=16, fill=(12, 18, 30, 240), outline=(249, 115, 22, 255), width=2)
            draw.text((pip_x + 14, pip_y - 32), "🚀 6国母语全媒体矩阵自动排期", font=font(20, True), fill=(249, 115, 22))
            canvas.paste(img_social, (pip_x, pip_y))

        # Top-Left Minimalist Glass Pill (Brand Watermark)
        draw.rounded_rectangle([50, 36, 440, 102], radius=20, fill=(12, 18, 30, 225), outline=(56, 189, 248, 180), width=2)
        canvas.paste(logo_top, (64, 41), logo_top)
        draw.text((132, 45), "RenWork", font=font(26, True), fill=(255, 255, 255))
        draw.text((132, 73), "外贸 AI 增长实战营", font=font(16, False), fill=(160, 175, 200))

        # Top-Right Hero Kinetic Typography Card (Large 34px Title + 20px Tag)
        badge_w, badge_h = 760, 120
        bx, by = W - badge_w - 50, 36
        draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=20, fill=(9, 13, 22, 225), outline=cur_badge["color"], width=2)
        draw.text((bx + 26, by + 18), cur_badge["tag"], font=font(20, True), fill=cur_badge["color"])
        draw.text((bx + 26, by + 48), cur_badge["title"], font=font(34, True), fill=(255, 255, 255))
        draw.text((bx + 26, by + 88), cur_badge["sub"], font=font(18, False), fill=(200, 215, 235))

        # Center-Bottom 44px Subtitles
        for st, et, txt, sidx in sub_list:
            if st <= cur_t < et:
                f_sub = font(44, True)
                bbox = f_sub.getbbox(txt)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                sx = (W - (tw + 72)) // 2
                sy = H - 150
                draw.rounded_rectangle([sx, sy, sx + tw + 72, sy + th + 32], radius=18, fill=(0, 0, 0, 235), outline=cur_badge["color"], width=2)
                draw.text((sx + 36, sy + 14), txt, font=f_sub, fill=(255, 255, 255))
                break

        # Bottom Neon Progress Bar
        prog = (f_idx + 1) / total_frames
        draw.line([0, H - 6, int(W * prog), H - 6], fill=(249, 115, 22), width=6)

        final_frame = canvas.convert("RGB")
        ff_pipe.stdin.write(final_frame.tobytes())

        if (f_idx + 1) % 300 == 0 or (f_idx + 1) == total_frames:
            print(f"[Cinematic V2] 渲染进度: {f_idx + 1}/{total_frames} ({(f_idx + 1) / total_frames * 100:.1f}%)")

    ff_pipe.stdin.close()
    ff_pipe.wait()

    # Kill pipes
    p_speaker.kill()
    p_students.kill()
    p_intent.kill()
    p_interaction.kill()
    p_inquiring.kill()
    p_customs.kill()
    p_social.kill()

    # Cleanup
    for sf in seg_files:
        if os.path.exists(sf): os.remove(sf)
    if os.path.exists(concat_list_file): os.remove(concat_list_file)
    if os.path.exists(v_concat): os.remove(v_concat)

    print(f"\n🎉🎉🎉 全新 5 场景不重复混剪大片已成功生成：{OUTPUT_VIDEO}")

asyncio.run(main())
