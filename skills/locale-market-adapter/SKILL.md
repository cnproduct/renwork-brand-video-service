---
name: locale-market-adapter
description: 多国目标市场深度本地化适配技能。负责将营销内容与视觉风格根据北美、欧洲、中东、东南亚、日韩等目标市场的语言习惯、商务语调、度量衡单位、宗教文化禁忌与排版格式进行深度重构。
---

# 多国市场本地化适配技能 (Locale Market Adapter)

`locale-market-adapter` 坚决杜绝生硬的机器直翻。本技能将同一核心营销主张，按全球不同贸易国家与文化背景进行**商务心理、文化禁忌、技术标准与度量衡的深度本土化重构**。

---

## 全球主要外贸市场适配矩阵

### 1. 北美市场 (North America: US, CA)
- **商务语调**：直接高效、注重投资回报率 (ROI) 与施工省工（Labor-saving）；
- **技术规范**：优先使用英制单位（inches, feet, lbs, sq.ft），引用 ASTM, ANSI, UL, FDA 认证；
- **排版风格**：粗体关键数据突出，CTA 明确直接（“Get Quote in 24h” / “Order Sample”）。

### 2. 欧洲市场 (Europe: DE, FR, UK, IT)
- **商务语调**：严谨客观、高度重视环保可持续性（Sustainability, Eco-friendly, Carbon Footprint）；
- **技术规范**：公制单位（mm, cm, kg, m²），重点标注 CE, REACH, RoHS, ISO14001, GRS 认证；
- **文化禁忌**：避免夸大式吹嘘（如“World's best”），讲求实验室权威检测数据支持。

### 3. 中东与海湾国家 (Middle East: UAE, Saudi Arabia, Qatar)
- **商务语调**：尊重礼仪、推崇宏伟奢华工程与地标建筑品质；
- **沟通偏好**：极度偏好 **WhatsApp 商务直连**与图册速递；
- **排版与语言**：支持阿拉伯语阿文 RTL（从右至左）排版，主视觉偏好明亮、大理石/天然石材金色光泽感；
- **禁忌规避**：严格规避当地宗教敏感图案与颜色禁忌。

### 4. 东南亚市场 (Southeast Asia: VN, TH, ID, MY, PH)
- **商务语调**：务实亲切、关注性价比、起订量（MOQ）灵活性与快速交付；
- **环境特性**：强调抗高温高湿、防霉变、防潮与耐磨特性；
- **沟通偏好**：WhatsApp, Zalo, WeChat 快速即时沟通。

### 5. 日韩市场 (Japan & South Korea)
- **商务语调**：极度严谨礼貌、注重细节做工公差、微米级品质与包装完好度；
- **技术规范**：引用 JIS / KS 认证标准，包装采用多层防刮保护说明；
- **语言细节**：使用规范的日韩商务敬语体系。

---

## 本地化输出格式

在 `content_item.json` 中，每篇内容均包含本地化字段：

```json
{
  "locale_adaptation": {
    "target_market": "US_NorthAmerica",
    "unit_system": "imperial",
    "adapted_measurements": "24\" x 6\" x 0.8\" (approx. 600x150mm)",
    "adapted_certifications": "ASTM C615 / C97 Laboratory Certified",
    "cultural_notes": "Emphasized labor-saving interlocking benefit for high US contractor wage environment."
  }
}
```
