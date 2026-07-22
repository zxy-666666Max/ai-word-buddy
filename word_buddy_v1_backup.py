"""
AI 单词助手 v1 - 考研英语单词学习卡片生成器
基于智谱 GLM-4-Flash 免费大模型
使用方法:
    python word_buddy.py
"""
import os
import sys
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ZHIPU_API_KEY")

if not API_KEY or "在这里粘贴" in API_KEY:
    print("❌ 错误:还没设置智谱 API Key")
    print("👉 请打开 .env 文件,把 ZHIPU_API_KEY 替换成你的真实 Key")
    print("👉 获取地址:https://bigmodel.cn -> 右上角头像 -> API Keys")
    sys.exit(1)

client = OpenAI(
    api_key=API_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/",
)

PROMPT_TEMPLATE = """你是一位专业的考研英语词汇教学助手。请为单词 "{word}" 生成一份考研级别的学习卡片。
严格按以下 Markdown 格式输出,不要加任何多余的解释或前言:
# 📖 {word}
**音标**:/在这里写国际音标/
**词性 · 中文**:词性缩写. 常见中文含义(1-3 个)
## 📚 词根词缀
用 1-2 句话说明词根拆解和含义推导逻辑。
## 📝 例句
1. 一句地道的英文例句(考研难度)
   (这句话的中文翻译)
2. 另一句英文例句
   (中文翻译)
## 🧠 记忆技巧
用谐音、联想、故事等有趣的方式帮助记忆(1-2 句,要生动)。
## 🔗 相关词
- **同义词**:word1, word2, word3
- **反义词**:word1, word2
- **常见搭配**:短语 1, 短语 2
## ⭐ 考研考点
简述这个词在考研真题中的高频考法或易错点(1-2 句)。
"""

def generate_word_card(word: str) -> str:
    """调用智谱 GLM-4-Flash 生成单词卡片。"""
    prompt = PROMPT_TEMPLATE.format(word=word)
    print(f"🤖 正在为【{word}】生成学习卡片...")
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content

def save_card(word: str, content: str) -> Path:
    """把生成的卡片保存到 output/ 目录。"""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    file_path = output_dir / f"{word}.md"
    file_path.write_text(content, encoding="utf-8")
    return file_path

def main() -> None:
    print("=" * 50)
    print("📖 AI 单词助手 · 考研版")
    print("   模型:智谱 GLM-4-Flash(免费)")
    print("=" * 50)
    print("输入英文单词,AI 帮你生成学习卡片")
    print("输入 'quit' 或 'q' 退出\n")
    while True:
        word = input("请输入单词:").strip().lower()
        if word in ("quit", "q", ""):
            print("👋 再见,加油背单词!")
            break
        try:
            card = generate_word_card(word)
            file_path = save_card(word, card)
            print(f"\n✅ 生成成功!已保存到:{file_path}\n")
            print(card)
            print("\n" + "=" * 50 + "\n")
        except Exception as e:
            print(f"❌ 出错了:{e}")
            print("👉 检查一下 .env 里的 API Key 是不是填对了\n")

if __name__ == "__main__":
    main()
