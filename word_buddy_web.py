"""
AI 单词助手 - 网页版
把 word_buddy.py 的命令行版搬上网页,用 Streamlit 实现。

跟命令行版的区别:
  - 命令行版用 input() 让你输单词 -> 网页版用输入框
  - 命令版用 print() 显示卡片 -> 网页版直接渲染成带格式的网页
  - 生成卡片的"干活逻辑"(调 AI、存文件、记词表)完全复用命令行版的代码,不重写

运行方法:
    streamlit run word_buddy_web.py
"""
import os
import streamlit as st

# set_page_config 必须是第一条 Streamlit 命令:配置浏览器标签页的标题和图标
st.set_page_config(page_title="AI 单词助手", page_icon="📖")

# ---- 密钥读取:兼容云端和本地两种环境 ----
# 云端(Streamlit Cloud):没有 .env,从后台 secrets 读 key,塞进环境变量,
#   这样下面 import word_buddy 时它就能用 os.getenv 读到。
# 本地(你自己电脑):没有 secrets 会报错,except 跳过,改由 .env 提供。
try:
    os.environ["ZHIPU_API_KEY"] = st.secrets["ZHIPU_API_KEY"]
except Exception:
    pass

# 从命令行版直接借用三个"干活"的函数,不用重写一遍
# 这样以后改提示词、改重试逻辑,只要改 word_buddy.py,网页版自动跟着变
from word_buddy import generate_word_card, save_card, record_word


# ============================================================
# 网页主体
# ============================================================
st.title("📖 AI 单词助手")
st.caption("考研英语单词卡生成器 · 基于智谱 GLM-4-Flash")

# 输入框:相当于命令行版的 input("请输入单词:")
# placeholder 是框里灰色的提示文字,没输入时显示
word = st.text_input("输入一个单词", placeholder="例如:abandon")

# 按钮:点了才会往下走,相当于命令行版里按回车确认
# type="primary" 让按钮变成醒目的蓝色
if st.button("生成学习卡片", type="primary"):
    word = word.strip().lower()  # 去掉首尾空格、统一小写,跟命令行版一致
    if not word:
        st.warning("请先输入一个单词~")
    else:
        # spinner:生成期间显示"正在生成...",跟命令行版的 print("正在生成...") 一个意思
        # with 块结束(生成完)后,转圈提示自动消失
        with st.spinner(f"🤖 正在为【{word}】生成学习卡片..."):
            try:
                card = generate_word_card(word)   # 1. 调 AI 生成(复用命令行版的函数)
                save_card(word, card)             # 2. 存成 output/单词.md
                record_word(word)                 # 3. 记到 wordlist.txt
            except Exception as e:
                # 生成失败(比如网络问题、Key 不对)时,在网页上红色提示,不让程序崩
                st.error(f"生成失败:{e}\n\n👉 检查 API Key 是否正确(本地看 .env 文件,云端看 Streamlit secrets)")
                st.stop()  # 停住,不再往下执行

        # 把 AI 返回的 Markdown 原样渲染成带格式的卡片(标题、粗体、列表都会显示)
        st.markdown(card)
        st.success(f"✅ 已保存到 output/{word}.md")
