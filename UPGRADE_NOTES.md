# 🆙 word_buddy.py 升级说明(v1 -> v2)

升级时间:2026-07-15

---

## 这次升级做了啥

把原来"一进来就只能输一个单词"的小工具,升级成**带菜单的多功能背单词助手**。

### 新增 4 个模式(进来选数字)

| 选项 | 功能 | 说明 |
|---|---|---|
| `[1]` | 生成单词卡(单个) | 和 v1 一样,输一个单词生成一张卡 |
| `[2]` | 批量生成(多个) | **新**。一次输 `abandon, ability, absolute`,自动循环生成,适合一口气攒一批 |
| `[3]` | 复习抽查 | **新**。从已有卡片里随机抽,先显示单词,按回车再"翻面"看完整内容 |
| `[4]` | 查看已学词表 | **新**。列出所有生成过的单词,看自己背了多少 |
| `[q]` | 退出 | -- |

### 其它改进

- **API 失败自动重试 2 次**:网络抖动时不至于直接挂,每词间隔 1 秒重试
- **自动记词表**:每生成一个词,自动追加到 `wordlist.txt`,方便统计进度
- **主菜单驱动**:不再一进来就让你输单词,先选模式

---

## 文件清单(项目目录现在长这样)

```
ai-word-buddy/
├── word_buddy.py            ← 已升级为 v2(主程序)
├── word_buddy_web.py        ← 网页版(Streamlit)
├── word_buddy_v1_backup.py  ← 原版备份(想回退就用它覆盖)
├── requirements.txt
├── .env                     ← 你的 API Key(绝不上传 GitHub)
├── venv/                    ← 虚拟环境
├── output/                  ← 生成的单词卡(.md)
│   └── abandon.md
└── wordlist.txt             ← v2 新增:运行后会自动生成,记录学过的词
```

---

## 怎么跑(和以前一样)

```bash
wsl
cd /mnt/d/Projects/ai-word-buddy
source venv/bin/activate
python word_buddy.py       # 命令行版
streamlit run word_buddy_web.py   # 网页版
```

进来就是菜单,输 `1` / `2` / `3` / `4` 或 `q`。

---

## 想回退到 v1?

```bash
cp word_buddy_v1_backup.py word_buddy.py
```

---

## ⏭️ 回来接着干

1. **我给你逐行讲 v2 新增的代码**(重点:`generate_word_card` 的重试逻辑、`mode_batch` 批量、`mode_review` 复习翻面)
2. 你自己试跑一下:菜单 -> 选 `2` 批量生成几个词 -> 选 `3` 复习
3. 然后**上传 GitHub**(用户名 `zxy-666666666Max`,记得 `.env` 不能传)
