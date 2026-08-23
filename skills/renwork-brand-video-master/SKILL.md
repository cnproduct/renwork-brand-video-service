---
name: renwork-brand-video-master
description: "RenWork 品牌视觉与企业级短视频/宣传片全自动生产总控技能。融合人人易官方品牌视觉系统（BrandVisual System）与 ChatCut/Video-Use 广播级视频混剪引擎，支持全画幅电影级排版、云扬配音、逐句毫秒级音字硬对齐、动态实操画中画与高转化视频号文案生成。"
---

# RenWork Brand Video Master (品牌视觉与视频生产全能总控技能)

本技能专为 **人人易智能科技有限公司（rrenn.com）旗下 RenWork 外贸增长操作系统** 定制，将【品牌视觉规范】与【广播级视频智能装配】打包为一体化生产管线，可在任何新对话中一键调度生成符合出版级标准的 1080P/4K 品牌宣传片、实战营混剪、功能演示与获客短视频。

---

## 🎨 第一部分：RenWork 品牌视觉系统规范 (Brand Visual DNA)

### 1. 企业主体与官方信息
* **企业官方全称**：`人人易智能科技有限公司`（严禁使用任何未经授权的缩写或繁体）
* **核心产品/系统**：`RenWork 外贸增长操作系统`
* **官方域名**：`rrenn.com` / `www.rrenn.com`
* **官方正确 Logo 资产**：
  * 路径：`public/brand/renwork_logo_correct.png`（橙色几何火箭 A 标 ＋ 蓝色星芒与圆眼）
  * 头部水印徽标：56×56 / 68×68 RGBA
  * 尾帧品牌大标：120×120 / 140×140 RGBA

### 2. 标准品牌色彩体系 (Color Palette)
| 色彩名称 | HEX 代码 | RGB 色值 | 应用场景 |
| :--- | :--- | :--- | :--- |
| **活力主橙 (Primary Orange)** | `#EA580C` / `#F97316` | `(234, 88, 12)` / `(249, 115, 22)` | 底部进度条、核心 CTA、强调高亮 |
| **深邃暗夜蓝 (Dark Slate Navy)**| `#090D16` / `#111827` | `(9, 13, 22)` / `(17, 24, 40)` | 背景基底、毛玻璃卡片、抗眩光遮罩 |
| **东盟科技青 (ASEAN Cyan)** | `#38BDF8` | `(56, 189, 248)` | 品牌边框发光、数据流、科技标签 |
| **增长金 (Growth Gold)** | `#F59E0B` | `(245, 158, 11)` | 字幕核心关键词高亮、意向大单徽标 |
| **成交绿 (Emerald Green)** | `#10B981` | `(16, 185, 129)` | 海关真买家标签、数据穿透演示框 |
| **赋能紫 (Empower Purple)** | `#A855F7` | `(168, 85, 247)` | 销冠谈判模型、企业知识大脑 |

### 3. 排版与大字版式准则 (Typography & Layout)
* **全画幅满屏 (Full-Bleed Canvas)**：采用 1920×1080 满屏真实动态视频，坚决杜绝右侧密集堆砌小字信息板。
* **极简 Top-Right Hero 徽标**：
  * 每屏仅保留 1 组强冲击力大字：`[ 20px 动态分类标签 ]` ＋ `[ 34px 加粗主标题 ]` ＋ `[ 18px 辅助说明 ]`。
* **特大加粗胶囊字幕 (Large Subtitle)**：
  * 字号固定为 **44px 加粗特大字体**，居中浮动于 `H - 150px` 位置。
  * 外衬半透明高透黑色胶囊底框（透明度 0.85 ＋ 2px 呼吸发光边框），确保在手机端一眼看清。
* **灵动悬浮画中画 (Floating PIP)**：
  * 尺寸固定为 **540×304 (16:9)**，悬浮于右下角，带有深色圆角发光框，展现海关提单与社媒自动发布实操。

---

## 🎙️ 第二部分：全球锁定播音员与音频标准

* **全局唯一默认主播**：**云扬 (`zh-CN-YunyangNeural`)**
* **语速参数**：`rate="+4%"`（轻快、有力、极具商业信服力）
* **音调与音量**：`pitch="+0Hz"`, `volume="+0%"`
* **背景音乐 (BGM)**：科技环境合成器音效，带 1.5s 柔和淡入、2.0s 淡出，人声播放期间自动侧链压限（Ducking -18dB）。

---

## ⚡ 第三部分：ChatCut 毫秒级音字硬同步算法 (Zero-Drift Pipeline)

**严禁使用 Whisper 语音识别直接生成字幕**（会导致繁体字与识别错别字）。必须采用以下**逐句物理测量法**：

1. **台词列表硬编码**：编写严格纯简体中文台词列表 `SENTENCES = [...]`。
2. **逐句独立 TTS 合成**：循环每句文本单独生成 `temp_voice_{idx}.mp3`。
3. **`ffprobe` 物理测量时长**：精准探测该句音频的实际绝对秒数 $d_i$。
4. **时间戳严格锁定**：
   $$Start_i = Offset,\quad End_i = Offset + d_i,\quad Offset = End_i + 0.22s$$
5. **音频物理拼接 (Concat)** ＋ **BGM 混合**。
6. **帧渲染器时间轴绑定**：当当前播放时间 $t \in [Start_i, End_i)$ 时，显示第 $i$ 句 44px 纯简体字幕并高亮对应关键词。

---

## 💻 第四部分：一键可运行的生产脚本标准模板

在任何项目中调用本模板，即可直接生成 1080P 极简大字混剪大片：

```python
import asyncio, os, subprocess
import edge_tts
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

def get_duration(fpath):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", fpath]
    return float(subprocess.run(cmd, stdout=subprocess.PIPE, text=True).stdout.strip())

# 逐句生成音频与时间轴
async def build_audio_and_timeline(sentences, voice_prefix):
    seg_files, sub_list = [], []
    cur_offset = 0.0
    gap = 0.22
    for idx, sentence in enumerate(sentences):
        seg_f = f"{voice_prefix}_{idx}.mp3"
        comm = edge_tts.Communicate(sentence.strip(), VOICE, rate="+4%")
        await comm.save(seg_f)
        seg_dur = get_duration(seg_f)
        sub_list.append((cur_offset, cur_offset + seg_dur, sentence.strip(), idx))
        seg_files.append(seg_f)
        cur_offset += seg_dur + gap

    concat_file = f"{voice_prefix}_concat.txt"
    with open(concat_file, "w") as f:
        for sf in seg_files: f.write(f"file '{sf}'\n")

    v_concat = f"{voice_prefix}_concat.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file, "-c", "copy", v_concat], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    v_mix = f"{voice_prefix}_mix.mp3"
    total_dur = cur_offset
    subprocess.run([
        "ffmpeg", "-y", "-i", v_concat,
        "-f", "lavfi", "-i", f"anoisesrc=d={int(total_dur+10)}:c=pink:r=44100:a=0.012",
        "-filter_complex", f"[1:a]volume=0.07,afade=t=in:ss=0:d=1.5,afade=t=out:st={max(1, total_dur-2)}:d=2[bgm];[0:a][bgm]amix=inputs=2:duration=first[out]",
        "-map", "[out]", "-c:a", "libmp3lame", "-b:a", "192k", v_mix
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return v_mix, get_duration(v_mix), sub_list, seg_files, concat_file, v_concat
```

---

## 📱 第五部分：微信视频号高转化文案标准框架

每次生成视频后，自动产出配套发布物料：
1. **15 字严格连续黄金标题**（例：`外贸AI实战营现场带电脑跑闭环`）
2. **痛点钩子直击正文**（为什么全国外贸老板纷纷带团队走进人人易...）
3. **结构化四大模块成果**（全员实操 / 数据穿透 / 6国母语 / 销冠谈判）
4. **官方背书与 CTA**（人人易智能科技有限公司 / rrenn.com）
5. **高权重标签矩阵**（`#RenWork #外贸AI增长实战营 #海关数据 #AI数字员工`）
