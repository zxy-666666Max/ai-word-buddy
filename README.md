# 📖 AI Word Buddy · AI 单词助手

> 一个基于 AI 的考研英语单词学习助手,自动为每个单词生成:音标、词根、例句、记忆技巧、考研考点等,帮助高效记忆。

作者:AI 专业大一学生 · 目标:厦门大学研究生 🎯

## ✨ 功能特色

- 🤖 **AI 驱动** - 调用智谱 GLM-4-Flash 大模型,生成高质量学习内容
- 📝 **考研专项** - 所有内容针对考研词汇设计,附考研真题考点
- 🧠 **多维记忆** - 词根、例句、谐音、联想,一网打尽
- 💾 **自动存档** - 每个单词一份 Markdown 卡片,可打印可复习
- 🆓 **完全免费** - 使用智谱 GLM-4-Flash 永久免费额度
- ⚡ **零门槛** - 输入单词即用,3 秒出结果

## 🖼 效果预览

输入单词 `abandon`,AI 生成:

```markdown
# 📖 abandon

**音标**:/əˈbændən/
**词性 · 中文**:v. 放弃、抛弃、离弃

## 📚 词根词缀
a-(离开)+ band(约束、控制)-> 脱离控制 -> 抛弃、放弃

## 📝 例句
1. He abandoned his car in the snow.
   (他把车丢在雪地里就走了。)
2. Don't abandon your dreams because of temporary failure.
   (别因一时的失败就放弃梦想。)

...
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/你的用户名/ai-word-buddy.git
cd ai-word-buddy
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key

在项目根目录创建 `.env` 文件(或复制 `.env.example`):

```
ZHIPU_API_KEY=你的智谱API_Key
```

免费获取智谱 API Key:[bigmodel.cn](https://bigmodel.cn) -> 右上角头像 -> API Keys

### 4. 运行

#### 命令行版
```bash
python word_buddy.py
```

#### 网页版(Streamlit)
```bash
streamlit run word_buddy_web.py
```

## 🛠 技术栈

- **Python 3.10+**
- **智谱 GLM-4-Flash**(免费大模型 API)
- **python-dotenv**(环境变量管理)
- **openai SDK**(通用大模型客户端)
- **Streamlit**(网页版界面)

## 📌 未来计划

- [x] 支持批量生成单词(多个一起)
- [x] 复习抽查模式
- [x] 网页版本,浏览器直接使用(Streamlit)
- [ ] 支持批量导入单词表(CSV / TXT)
- [ ] 生成 Anki 卡片格式,一键导入 Anki
- [ ] 集成 TTS 语音朗读功能
- [ ] 微信小程序版

## 📄 License

MIT License · 欢迎 Star ⭐ 和 Fork 🍴
