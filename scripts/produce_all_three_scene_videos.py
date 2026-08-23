import asyncio, os, subprocess, shutil
import edge_tts, whisper
import numpy as np
from PIL import Image, ImageDraw, ImageFont

VOICE = "zh-CN-YunyangNeural"
LOGO_PATH = "public/brand/renwork_logo_correct.png"
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
logo_hdr = logo_raw.resize((68, 68), Image.Resampling.LANCZOS)
logo_big = logo_raw.resize((120, 120), Image.Resampling.LANCZOS)

EPISODES = [
    {
        "id": "ep1_training",
        "title": "RenWork 外贸 AI 增长实战营",
        "scene_img": "public/scenes/scene_training_camp.jpg",
        "output_mp4": "renrenyi_series_ep1_training_camp.mp4",
        "text": "为什么外贸老板一定要带团队来参加人人易 AI 外贸增长实战营？\n因为这里不讲假大空的理论，我们全程带电脑、实操跑通真实订单闭环！\n第一模块：企业经验数字化！把工厂目录、技术参数一键装入专属 AI 大脑！\n第二模块：海关真实交易穿透！现场实操锁定正在采购的 R1 级真实大买家！\n第三模块：全场景成交促单！结合历史提单秒级生成 6 国母语定制开发信！\n学员现场收获满满！当天搭建好企业私有知识库，当场挖出北美大买家！\n让每一个外贸业务员，都能像拥有 10 年外贸销冠经验一样高效签单！\n人人易智能科技有限公司，RenWork 外贸增长实战营，全国城市火热开营中！",
        "subs": [
            "为什么外贸老板一定要带团队来参加人人易 AI 外贸增长实战营？",
            "因为这里不讲假大空的理论，我们全程带电脑、实操跑通真实订单闭环！",
            "第一模块：企业经验数字化！把工厂目录、技术参数一键装入专属 AI 大脑！",
            "第二模块：海关真实交易穿透！现场实操锁定正在采购的 R1 级真实大买家！",
            "第三模块：全场景成交促单！结合历史提单秒级生成 6 国母语定制开发信！",
            "学员现场收获满满！当天搭建好企业私有知识库，当场挖出北美大买家！",
            "让每一个外贸业务员，都能像拥有 10 年外贸销冠经验一样高效签单！",
            "人人易智能科技有限公司，RenWork 外贸增长实战营，全国城市火热开营中！"
        ],
        "right_items": [
            ("📚 第一模块：企业经验数字化", "产品参数、工厂目录一键装入 AI 大脑", (56, 189, 248)),
            ("🎯 第二模块：海关真实交易穿透", "实操锁定正在采购的 R1 级真实大买家", (16, 185, 129)),
            ("🤝 第三模块：全场景成交促单", "6 国母语定制开发信，历史提单精准破冰", (249, 115, 22)),
            ("🏆 学员当天实战成果", "搭建企业知识库，当场挖出北美大买家", (168, 85, 247)),
        ]
    },
    {
        "id": "ep2_factory",
        "title": "RenWork 专家入厂指导与增长诊断",
        "scene_img": "public/scenes/scene_factory_mentoring.jpg",
        "output_mp4": "renrenyi_series_ep2_factory_mentoring.mp4",
        "text": "外贸企业买了一堆 AI 软件用不起来？人人易 AI 专家直接入厂实操指导！\n我们深入制造车间、摸清产品样件与材质参数，拒绝空中楼阁！\n第一步：全方位诊断外贸增长瓶颈！精准找出询盘不转化、报价没利润的根本原因！\n第二步：把工厂真实的质检报告、产能优势与定制工艺，一键录入企业专属 AI 知识库！\n第三步：手把手教业务员实操，现场穿透海关真实提单，精准定位海外买家决策人！\n工厂老板直呼：以前听理论摸不着门道，人人易专家现场建好系统，当天就能用！\n从车间生产到海外大客户签单，打造真正属于实体工厂的外贸增长闭环！\n人人易智能科技有限公司，RenWork 专家入厂服务，让中国制造赢在全球！",
        "subs": [
            "外贸企业买了一堆 AI 软件用不起来？人人易 AI 专家直接入厂实操指导！",
            "我们深入制造车间、摸清产品样件与材质参数，拒绝空中楼阁！",
            "第一步：全方位诊断外贸增长瓶颈！精准找出询盘不转化、报价没利润的根本原因！",
            "第二步：把工厂真实的质检报告、产能优势与定制工艺，一键录入企业专属 AI 知识库！",
            "第三步：手把手教业务员实操，现场穿透海关真实提单，精准定位海外买家决策人！",
            "工厂老板直呼：以前听理论摸不着门道，人人易专家现场建好系统，当天就能用！",
            "从车间生产到海外大客户签单，打造真正属于实体工厂的外贸增长闭环！",
            "人人易智能科技有限公司，RenWork 专家入厂服务，让中国制造赢在全球！"
        ],
        "right_items": [
            ("🔍 第一步：诊断增长瓶颈", "询盘不转化、报价没利润的根本原因", (239, 68, 68)),
            ("📋 第二步：录入 AI 知识库", "质检报告、产能优势、定制工艺一键录入", (56, 189, 248)),
            ("🎯 第三步：穿透海关真买家", "手把手教业务员精准定位海外采购决策人", (16, 185, 129)),
            ("💡 老板真实反馈", "现场建好系统，当天就能用！", (245, 158, 11)),
        ]
    },
    {
        "id": "ep3_summit",
        "title": "人人易 AI · RenWork 全国巡回大会",
        "scene_img": "public/scenes/scene_national_tour_summit.jpg",
        "output_mp4": "renrenyi_series_ep3_national_summit.mp4",
        "text": "场场爆满、座无虚席！人人易 AI · RenWork 外贸增长全国巡回大会震撼来袭！\n签到处大排长龙，数百位外贸企业主齐聚一堂，共同见证 AI 外贸新风口！\n大会重磅发布：RenWork 外贸增长操作系统！告别零散拼凑，开启订单闭环增长！\n现场深度揭秘：标杆工厂如何利用 AI 知识库与海关真数据，实现 300% 询盘暴涨！\n从 AI 精准找买家、全媒体内容营销，到 WhatsApp 智能自动化追单全流程打通！\n参会老板纷纷表示：这是听过最落地的外贸 AI 大会，看懂了数字化转型的底层逻辑！\n全国巡回火热进行中，下一站即将抵达您的城市！\n人人易智能科技有限公司，RenWork 全国巡回大会，诚邀全国外贸同仁共赢出海！",
        "subs": [
            "场场爆满、座无虚席！人人易 AI · RenWork 外贸增长全国巡回大会震撼来袭！",
            "签到处大排长龙，数百位外贸企业主齐聚一堂，共同见证 AI 外贸新风口！",
            "大会重磅发布：RenWork 外贸增长操作系统！告别零散拼凑，开启订单闭环增长！",
            "现场深度揭秘：标杆工厂如何利用 AI 知识库与海关真数据，实现 300% 询盘暴涨！",
            "从 AI 精准找买家、全媒体内容营销，到 WhatsApp 智能自动化追单全流程打通！",
            "参会老板纷纷表示：这是听过最落地的外贸 AI 大会，看懂了数字化转型的底层逻辑！",
            "全国巡回火热进行中，下一站即将抵达您的城市！",
            "人人易智能科技有限公司，RenWork 全国巡回大会，诚邀全国外贸同仁共赢出海！"
        ],
        "right_items": [
            ("🔥 场场爆满·座无虚席", "数百位外贸企业主齐聚，见证 AI 新风口", (249, 115, 22)),
            ("🚀 重磅发布操作系统", "告别零散拼凑，开启订单闭环增长", (56, 189, 248)),
            ("📊 标杆案例深度揭秘", "AI 知识库+海关真数据，询盘暴涨 300%", (16, 185, 129)),
            ("🌍 全国巡回火热进行中", "下一站即将抵达您的城市！", (245, 158, 11)),
        ]
    }
]

async def process_all():
    whisper_model = whisper.load_model("base")
    for ep in EPISODES:
        print(f"\n================ 🚀 正在生成：{ep['title']} ================")
        v_raw = f"voice_{ep['id']}_raw.mp3"
        v_mix = f"voice_{ep['id']}_mix.mp3"

        comm = edge_tts.Communicate(ep["text"].strip(), VOICE, rate="+4%")
        await comm.save(v_raw)
        print(f"✨ 语音合成完成: {v_raw}")

        subprocess.run([
            "ffmpeg", "-y", "-i", v_raw,
            "-f", "lavfi", "-i", "anoisesrc=d=70:c=pink:r=44100:a=0.012",
            "-filter_complex",
            "[1:a]volume=0.08,afade=t=in:ss=0:d=1.5,afade=t=out:st=45:d=2[bgm];"
            "[0:a][bgm]amix=inputs=2:duration=first[out]",
            "-map", "[out]", "-c:a", "libmp3lame", "-b:a", "192k", v_mix
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✨ BGM 混合完成: {v_mix}")

        trans_res = whisper_model.transcribe(v_raw, language="zh")
        seg_times = [(s["start"], s["end"]) for s in trans_res["segments"]]
        sub_list = []
        for i, (st, et) in enumerate(seg_times):
            txt = ep["subs"][i] if i < len(ep["subs"]) else trans_res["segments"][i]["text"].strip()
            sub_list.append((st, et, txt))
        print(f"✨ 字幕对齐完成: {len(sub_list)} 条")

        dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", v_mix]
        duration = float(subprocess.run(dur_cmd, stdout=subprocess.PIPE, text=True).stdout.strip())
        total_frames = int(round(duration * FPS))
        print(f"时长: {duration:.2f}s | 帧数: {total_frames}")

        scene_im = Image.open(ep["scene_img"]).convert("RGB").resize((920, 720), Image.Resampling.LANCZOS)

        ff_pipe = subprocess.Popen([
            "ffmpeg", "-y", "-f", "rawvideo", "-vcodec", "rawvideo",
            "-s", f"{W}x{H}", "-pix_fmt", "rgb24", "-r", str(FPS), "-i", "-",
            "-i", v_mix, "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", ep["output_mp4"]
        ], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

        for f_idx in range(total_frames):
            cur_t = f_idx / FPS
            canvas = Image.new("RGB", (W, H), (9, 13, 22))
            draw = ImageDraw.Draw(canvas)
            draw.ellipse([W//2-700,40,W//2+700,650], fill=(16,26,46))
            draw.ellipse([W//2-600,H-450,W//2+600,H-30], fill=(45,22,12))

            draw.rounded_rectangle([40,20,W-40,106], radius=18, fill=(17,24,40), outline=(45,55,78), width=2)
            draw.rounded_rectangle([55,28,135,98], radius=14, fill=(12,18,30), outline=(56,189,248), width=1)
            canvas.paste(logo_hdr, (61,29), logo_hdr)
            draw.text((150,38), "RenWork", font=font(28,True), fill=(255,255,255))
            draw.text((150,70), "人人易智能科技有限公司 · 官方出品", font=font(18,False), fill=(160,175,200))
            draw.rounded_rectangle([W-540,34,W-60,92], radius=14, fill=(234,88,12), outline=(249,115,22), width=2)
            draw.text((W-515,48), f"🔥 {ep['title']}", font=font(21,True), fill=(255,255,255))

            draw.rounded_rectangle([50,130,1010,890], radius=20, fill=(17,24,40), outline=(56,189,248), width=3)
            canvas.paste(scene_im, (70,150))

            draw.rounded_rectangle([1040,130,W-50,890], radius=20, fill=(17,24,40), outline=(245,158,11), width=3)
            draw.text((1070,155), ep["title"], font=font(26,True), fill=(245,158,11))
            for ri, (rtitle, rdesc, rclr) in enumerate(ep["right_items"]):
                ry = 220 + ri * 130
                draw.rounded_rectangle([1060,ry,W-70,ry+110], radius=14, fill=(22,30,48), outline=rclr, width=2)
                draw.text((1085,ry+18), rtitle, font=font(22,True), fill=rclr)
                draw.text((1085,ry+58), rdesc, font=font(18,False), fill=(255,255,255))

            draw.rounded_rectangle([1060,750,W-70,870], radius=16, fill=(22,30,48), outline=(249,115,22), width=2)
            canvas.paste(logo_big, (1080,760), logo_big)
            draw.text((1220,775), "RenWork 外贸增长系统", font=font(22,True), fill=(255,255,255))
            draw.text((1220,815), "让中国制造赢在全球！", font=font(18,False), fill=(245,158,11))

            for st, et, txt in sub_list:
                if st <= cur_t < et:
                    f_sub = font(32,True)
                    bbox = f_sub.getbbox(txt)
                    tw = bbox[2]-bbox[0]
                    th = bbox[3]-bbox[1]
                    sx = (W-(tw+56))//2
                    clr = (245,158,11) if "人人易" in txt or "RenWork" in txt or "第一" in txt or "第二" in txt or "第三" in txt else (255,255,255)
                    draw.rounded_rectangle([sx,920,sx+tw+56,920+th+24], radius=14, fill=(0,0,0,230), outline=(245,158,11), width=2)
                    draw.text((sx+28,920+10), txt, font=f_sub, fill=clr)
                    break

            prog = (f_idx+1)/total_frames
            draw.line([0,H-6,int(W*prog),H-6], fill=(249,115,22), width=6)
            ff_pipe.stdin.write(canvas.tobytes())
            if (f_idx+1)%300==0 or (f_idx+1)==total_frames:
                print(f"[{ep['id']}] {f_idx+1}/{total_frames} ({(f_idx+1)/total_frames*100:.1f}%)")

        ff_pipe.stdin.close()
        ff_pipe.wait()
        print(f"✨ 成功生成：{ep['output_mp4']}")

asyncio.run(process_all())
print("\n🎉🎉🎉 全部 3 集场景视频已成功生成完毕！")
