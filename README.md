# Dust Front RTS — 简体中文汉化补丁

为 [Dust Front RTS Demo](https://store.steampowered.com/app/2933200/Dust_Front_RTS/) 提供简体中文界面翻译，覆盖全部 680 条本地化文本（单位、建筑、技能、教程、设置等）。

## 安装方法

1. 从 [Releases](../../releases) 页面下载最新版本的 `resources.assets`
2. 备份游戏原文件：
   ```
   <游戏目录>\Dust Front RTS_Data\resources.assets
   ```
3. 将下载的 `resources.assets` 覆盖到同一位置
4. 启动游戏，在**设置 → 语言**中选择 **Chinese**

> 游戏路径（Steam）：
> `在steam游戏列表右击-管理-浏览本地文件-双击文件夹Dust Front RTS_Data 进入-将下载的resources.assets复制并覆盖-启动游戏-选择中文`

## 还原原版

将备份的原文件复制回去即可。

## 开发者 / 重新打补丁

游戏更新后，需要用新版游戏文件重新打补丁：

```bash
# 依赖：Python 3.12+ 和 UnityPy
pip install UnityPy

# 将新版游戏文件复制到项目目录下对应位置，然后运行：
python patch_zh.py
```

生成的 `resources.assets` 位于 `Dust Front RTS Demo/Dust Front RTS_Data/` 目录。

## 翻译覆盖范围

| 类别 | 条目数 |
|------|--------|
| 杂项 / 提示 | ~30 |
| 单位 | ~80 |
| 建筑 | ~70 |
| 技能 / 支援 | ~50 |
| 主义 / 升级 / 装备 | ~90 |
| 设置 / 界面 | ~40 |
| 教程 | ~50 |
| 任务 / 剧情 | ~20 |

## 兼容版本

| 游戏版本 | 补丁版本 | 状态 |
|----------|----------|------|
| Demo (2025-06) | v1.0.0 | ✅ 可用 |

## License

翻译内容以 [CC0](https://creativecommons.org/publicdomain/zero/1.0/) 发布。
