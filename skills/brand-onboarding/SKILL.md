---
name: brand-onboarding
description: 企业品牌档案首次建档与版本化管理技能。负责导入企业Logo、标准色、字体、品牌故事、核心优势与禁忌语体系，输出符合 Schema 规范的标准化 BrandProfile。
---

# 企业品牌建档技能 (Brand Onboarding)

`brand-onboarding` 负责为企业创建、更新并沉淀长期可调用的数字品牌档案（Brand Profile）。任何新企业使用 RenWork 内容生产前，只需完成一次建档，后续所有战役与图文生成将自动继承其专属品牌基因。

---

## 建档输入要素

1. **企业基础信息**：企业名称（中英文）、官方网址、所属行业、主营产品线；
2. **视觉识别系统 (VI)**：
   - 品牌主色 (Primary HEX)、辅助色 (Secondary/Accent)、深浅背景色；
   - 字体体系（标题字体 Display、正文字体 Sans、代码/数据字体 Mono）；
   - 官方矢量 Logo（SVG 或高清透明 PNG），包括常规彩色版、单色版与反白版；
3. **品牌声音与语调 (Brand Voice & Tone)**：
   - 品牌原型（如：行业开拓者 Innovator、可靠制造业工匠 Craftsman、全球供应链伙伴 Trusted Partner）；
   - 核心语调关键词（如：权威、严谨、创新、务实、敏捷）；
   - 标语口号（中英文 Slogan）；
4. **合规与禁忌红线 (Compliance & Guardrails)**：
   - 严禁使用的词汇（如未经许可的绝对化用语、竞争对手对比禁词等）；
   - 强制附加声明与商标版权标识。

---

## 执行步骤

### 步骤 1：收集或解析企业现有资产
从用户提供的公司官网、宣传册（PDF/Word）、现有 `brand_spec.json` 或设计源文件中提取品牌色彩与核心定位。

### 步骤 2：生成并校验 BrandProfile 数据
根据 `schemas/brand-profile.schema.json` 构造结构化 JSON，并使用本地 Token MCP 验证色彩对比度（WCAG AA/AAA）：

```json
{
  "profile_id": "bp_naike_2026",
  "company_id": "naike_group",
  "version": "1.0.0",
  "brand_name": "耐科实业 (NAIKE Group)",
  "brand_name_en": "NAIKE Outdoor & Leisure Industrial Co.",
  "tagline": "全球顶级户外用品与定制箱包智造商",
  "tagline_en": "Precision Manufacturing for Global Outdoor Brands",
  "industry": "outdoor_and_lifestyle",
  "target_markets": ["North America", "Europe", "Australia", "Middle East"],
  "colors": {
    "primary": "#0D9488",
    "primary_light": "#14B8A6",
    "primary_dark": "#0F766E",
    "secondary": "#F59E0B",
    "bg_dark": "#0B131E",
    "bg_light": "#F8FAFC",
    "card_dark": "#132030",
    "text_primary": "#FFFFFF",
    "text_secondary": "#94A3B8"
  },
  "typography": {
    "font_sans": "'Inter', 'PingFang SC', sans-serif",
    "font_display": "'Plus Jakarta Sans', sans-serif"
  },
  "voice_tone": {
    "primary_archetype": "Reliable Industrial Leader",
    "tone_keywords": ["Professional", "Sustainable", "Engineering-grade", "Responsive"],
    "prohibited_expressions": ["100% cheapest", "No.1 in China without certificate"]
  }
}
```

### 步骤 3：持久化保存
将档案持久化至工作区 `.renwork/brands/<company_id>/brand-profile.json`，并注册至工作区 `brand_spec.json`。
