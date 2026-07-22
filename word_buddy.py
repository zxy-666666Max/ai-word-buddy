"""
AI 单词助手 v2 - 考研英语单词学习卡片生成器
基于智谱 GLM-4-Flash 免费大模型

相比 v1 的新功能:
  [1] 生成单词卡(单个)        -- 和 v1 一样,输一个单词生成一张卡
  [2] 批量生成(多个)          -- 一次输多个单词,自动循环生成
  [3] 复习抽查                -- 从已生成的卡片里随机抽,先看单词再翻面
  [4] 查看已学词表            -- 列出所有生成过的单词
  [q] 退出

其它改进:
  - API 调用失败会自动重试 2 次(应对网络抖动)
  - 每个生成的单词自动记到 wordlist.txt,方便统计进度
  - 主菜单驱动,不再是一进来就只让你输单词

使用方法:
    python word_buddy.py
"""
import os
import sys
import random
import time
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# ============================================================
# 配置区:加载密钥、连接智谱、准备文件夹
# ============================================================
load_dotenv()
API_KEY = os.getenv("ZHIPU_API_KEY")

# 如果没填 Key,或还是占位符,就提示用户去填,然后退出
if not API_KEY or "在这里粘贴" in API_KEY:
    print("❌ 错误:还没设置智谱 API Key")
    print("👉 请打开 .env 文件,把 ZHIPU_API_KEY 替换成你的真实 Key")
    print("👉 获取地址:https://bigmodel.cn -> 右上角头像 -> API Keys")
    sys.exit(1)

# 用 OpenAI 兼容方式连接智谱(智谱的接口和 OpenAI 长得一样,所以能用同一个库)
client = OpenAI(
    api_key=API_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/",
)

# 卡片保存的文件夹;不存在就建一个
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# 词表文件:记录所有生成过的单词,一行一个
WORDLIST_FILE = Path("wordlist.txt")

# 给 AI 的提示词模板:{word} 会被替换成用户输入的单词
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


# ============================================================
# 核心功能:生成、保存、记录
# ============================================================
def generate_word_card(word: str, max_retries: int = 2) -> str:
    """调用智谱 GLM-4-Flash 生成单词卡片。

    如果调用失败(比如网络抖动),会自动重试 max_retries 次,
    每次间隔 1 秒。全都失败了就把最后一次的错误抛出去。
    """
    prompt = PROMPT_TEMPLATE.format(word=word)
    print(f"🤖 正在为【{word}】生成学习卡片...")
    last_error = None
    # range(1, max_retries + 2):首次尝试 + 重试次数 = 共 max_retries+1 次
    for attempt in range(1, max_retries + 2):
        try:
            response = client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            last_error = e
            if attempt <= max_retries:
                print(f"   ⚠️ 第 {attempt} 次失败({e}),1 秒后重试...")
                time.sleep(1)
            else:
                # 重试次数用完,把错误抛给上一层处理
                raise
    # 理论上走不到这里,保险起见
    raise last_error


def save_card(word: str, content: str) -> Path:
    """把生成的卡片保存到 output/ 目录,文件名就是单词.md"""
    file_path = OUTPUT_DIR / f"{word}.md"
    file_path.write_text(content, encoding="utf-8")
    return file_path


def record_word(word: str) -> None:
    """把单词追加记到 wordlist.txt,已经记过就不重复记。"""
    existing = set()
    if WORDLIST_FILE.exists():
        # 读出所有已记录的词,放进集合(集合自动去重)
        existing = set(WORDLIST_FILE.read_text(encoding="utf-8").split())
    if word not in existing:
        # "a" 模式 = 追加,不会覆盖原内容
        with open(WORDLIST_FILE, "a", encoding="utf-8") as f:
            f.write(word + "\n")


def generate_one(word: str) -> bool:
    """生成单个单词卡片的完整流程:调用API -> 保存 -> 记录词表。

    成功返回 True,失败返回 False(不会让程序崩,方便批量里继续下一个)。
    """
    try:
        card = generate_word_card(word)
        file_path = save_card(word, card)
        record_word(word)
        print(f"\n✅ 生成成功!已保存到:{file_path}\n")
        print(card)
        print("\n" + "=" * 50 + "\n")
        return True
    except Exception as e:
        print(f"❌ 出错了:{e}")
        print("👉 检查一下 .env 里的 API Key 是不是填对了\n")
        return False


# ============================================================
# 四种模式
# ============================================================
def mode_single() -> None:
    """模式 1:一个一个输单词生成卡片。"""
    print("\n📝 单词卡生成(输 q 返回菜单)")
    while True:
        word = input("请输入单词:").strip().lower()
        if word in ("quit", "q", ""):
            break
        generate_one(word)


def mode_batch() -> None:
    """模式 2:一次输多个单词,用逗号或空格隔开,批量生成。"""
    print("\n📚 批量生成:输入多个单词,用逗号或空格隔开")
    print("例:abandon, ability, absolute")
    raw = input("请输入单词列表:").strip()
    if not raw:
        return
    # 把逗号统一换成空格,再按空格切分,顺便去掉空字符串和首尾空格
    words = [w.strip().lower() for w in raw.replace(",", " ").split() if w.strip()]
    print(f"\n📋 共 {len(words)} 个单词,开始生成...\n")
    success = 0
    for i, word in enumerate(words, 1):
        print(f"[{i}/{len(words)}] ", end="")
        if generate_one(word):
            success += 1
    print(f"\n🎉 批量完成!成功 {success}/{len(words)}")


def mode_review() -> None:
    """模式 3:从 output/ 已有卡片里随机抽,先显示单词,按键后再翻面看完整内容。"""
    # glob("*.md") = 找出 output 文件夹下所有 .md 文件
    cards = list(OUTPUT_DIR.glob("*.md"))
    if not cards:
        print("\n📭 还没有卡片,先去生成几个吧!\n")
        return
    print(f"\n🧠 复习模式(共 {len(cards)} 张卡,按回车翻面,n 跳过,q 退出)")
    random.shuffle(cards)  # 打乱顺序,每次复习顺序都不一样
    for card_path in cards:
        word = card_path.stem  # stem = 文件名去掉 .md 后缀
        content = card_path.read_text(encoding="utf-8")
        print(f"\n🔤 单词:{word}")
        cmd = input("按回车看完整卡片(n 跳过 / q 退出):").strip().lower()
        if cmd == "q":
            break
        elif cmd == "n":
            continue
        print("\n" + content)
        input("\n(回车继续下一张)")
    print("\n👋 复习结束\n")


def mode_wordlist() -> None:
    """模式 4:列出所有生成过的单词。"""
    if not WORDLIST_FILE.exists():
        print("\n📭 还没生成过单词\n")
        return
    words = WORDLIST_FILE.read_text(encoding="utf-8").split()
    print(f"\n📖 已学单词(共 {len(words)} 个):")
    for i, w in enumerate(words, 1):
        print(f"  {i:>3}. {w}")
    print()


# ============================================================
# 主菜单
# ============================================================
def main() -> None:
    print("=" * 50)
    print("📖 AI 单词助手 v2 · 考研版")
    print("   模型:智谱 GLM-4-Flash(免费)")
    print("=" * 50)
    while True:
        print("\n请选择模式:")
        print("  [1] 生成单词卡(单个)")
        print("  [2] 批量生成(多个)")
        print("  [3] 复习抽查")
        print("  [4] 查看已学词表")
        print("  [q] 退出")
        choice = input("你的选择:").strip().lower()
        if choice == "1":
            mode_single()
        elif choice == "2":
            mode_batch()
        elif choice == "3":
            mode_review()
        elif choice == "4":
            mode_wordlist()
        elif choice in ("quit", "q"):
            print("👋 再见,加油背单词!")
            break
        else:
            print("❓ 没这个选项,请输 1 / 2 / 3 / 4 或 q")


if __name__ == "__main__":
    main()
