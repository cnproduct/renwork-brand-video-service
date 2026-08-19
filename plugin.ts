import { tool } from "@opencode-ai/plugin";
import { z } from "zod";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import path from "node:path";
import fs from "node:fs";

// RenWork 品牌视觉系统与视频生成服务 —— OpenCode 插件
// 暴露品牌视频生成、封面、TTS 与品牌配色提取工具。
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PIPELINE = path.resolve(__dirname, "pipeline", "src");

function run(command: string, args: string[], input?: string) {
  const result = spawnSync(command, args, { input, encoding: "utf8" });
  if (result.status !== 0) {
    throw new Error(result.stderr || `${command} failed`);
  }
  return result.stdout;
}

function resolveNode(script: string) {
  return path.join(PIPELINE, "agents", script);
}

export default async function plugin() {
  return {
    tool: {
      // 1. 中文语音合成（默认云扬男声，edge-tts）
      synthesize_tts: tool({
        description:
          "用 Edge TTS 合成中文语音。默认 zh-CN-YunyangNeural（云扬男声）、语速 +4%、音调 +0Hz。返回音频文件路径。",
        args: {
          text: z.string().describe("要合成的中文文本"),
          voice: z
            .string()
            .optional()
            .describe("语音名称，默认 zh-CN-YunyangNeural"),
          rate: z.string().optional().describe("语速，默认 +4%"),
          pitch: z.string().optional().describe("音调，默认 +0Hz"),
          out: z.string().optional().describe("输出 mp3 路径（可选）"),
        },
        async execute({ text, voice, rate, pitch, out }, context) {
          const output =
            out ||
            path.join(context.worktree, "tts-output.mp3");
          run(
            "python3",
            [
              "-m", "edge_tts", "-t", text,
              "-v", voice || "zh-CN-YunyangNeural",
              "--rate", rate || "+4%",
              "--pitch", pitch || "+0Hz",
              "--write-media", output,
            ],
          );
          return {
            output: `语音已生成：${output}`,
            metadata: { file: output, voice: voice || "zh-CN-YunyangNeural" },
          };
        },
      }),

      // 2. 品牌配色提取（从图片提取主色/辅助色，WCAG 对比度校验）
      extract_brand_palette: tool({
        description:
          "从一张图片提取品牌主色与辅助色，并计算关键色对的 WCAG 对比度。返回 HEX 色板与对比度报告。",
        args: {
          image: z.string().describe("图片的绝对路径或工作区相对路径"),
        },
        async execute({ image }, context) {
          const abs = path.isAbsolute(image)
            ? image
            : path.join(context.worktree, image);
          if (!fs.existsSync(abs)) throw new Error(`图片不存在：${abs}`);
          const py = `
import json
from PIL import Image
from collections import Counter
def lum(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    r,g,b=f(r),f(g),f(b); return 0.2126*r+0.7152*g+0.0722*b
def ratio(a,b):
    la,lb=lum(a),lum(b); hi,lo=max(la,lb),min(la,lb); return round((hi+0.05)/(lo+0.05),2)
im=Image.open(${JSON.stringify(abs)}).convert('RGB'); im.thumbnail((200,200))
q=[(r//32*32,g//32*32,b//32*32) for r,g,b in im.getdata()]
c=Counter(q); total=sum(c.values())
pal=[('#%02X%02X%02X'%rgb, round(cnt/total*100,1)) for rgb,cnt in c.most_common(6)]
print(json.dumps({'palette':pal,'wcag_sample':{'primary_on_white': ratio(pal[0][0] if pal else '#000000', '#FFFFFF')}}))
`;
          const out = run("python3", ["-c", py]);
          return out;
        },
      }),

      // 3. 生成品牌介绍片（真实场景图 + 连贯旁白 + 字幕 + BGM）
      generate_brand_video: tool({
        description:
          "生成心同共生品牌介绍片（1920x1080 横版）。基于真实场景图 + 连贯旁白 + 字幕 + 背景音乐，使用默认云扬配音。返回成片路径。",
        args: {
          outputName: z
            .string()
            .optional()
            .describe("输出文件名，默认 心同共生-真实场景介绍片-横版.mp4"),
        },
        async execute({ outputName }) {
          const script = resolveNode("09-xintong-intro.js");
          const env = {
            ...process.env,
            ...(outputName ? { XINTONG_OUTPUT_NAME: outputName } : {}),
          };
          const result = spawnSync("node", [script], { env, encoding: "utf8" });
          if (result.status !== 0) throw new Error(result.stderr || "视频生成失败");
          const line = result.stdout
            .split("\n")
            .map((s) => s.trim())
            .filter((s) => s.startsWith("✅ 成片："))
            .pop();
          const file = line ? line.replace("✅ 成片：", "").trim() : "";
          return { output: result.stdout, metadata: { file } };
        },
      }),

      // 4. 给视频添加可见封面（避免发送后第一帧黑场）
      add_video_cover: tool({
        description:
          "给现有视频添加 4 秒可见品牌封面，避免分享后第一帧是黑场。返回带封面视频路径。",
        args: {
          video: z.string().describe("要加封面的视频绝对路径或工作区相对路径"),
        },
        async execute({ video }, context) {
          const abs = path.isAbsolute(video)
            ? video
            : path.join(context.worktree, video);
          if (!fs.existsSync(abs)) throw new Error(`视频不存在：${abs}`);
          const script = resolveNode("10-add-cover.js");
          const env = { ...process.env, XINTONG_COVER_SOURCE: abs };
          const result = spawnSync("node", [script], { env, encoding: "utf8" });
          if (result.status !== 0) throw new Error(result.stderr || "封面添加失败");
          return result.stdout;
        },
      }),
    },
  };
}
