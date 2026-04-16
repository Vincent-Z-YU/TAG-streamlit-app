import streamlit as st
import random
import time

# 全局配置与初始化
PROGRAM_NAME = "Tools and Games (TAG)"
PROGRAM_VERSION = "V2.0"
PROGRAM_NAME_ABBREVIATION = "TAG"

# 凯撒密码字母表初始化
LOWER_CASE = [chr(ord('a') + i) for i in range(26)]
UPPER_CASE = [chr(ord('A') + i) for i in range(26)]
LOWER_DICT = {char: idx + 1 for idx, char in enumerate(LOWER_CASE)}
UPPER_DICT = {char: idx + 1 for idx, char in enumerate(UPPER_CASE)}

# Streamlit 页面配置
st.set_page_config(
    page_title=f"{PROGRAM_NAME} {PROGRAM_VERSION}",
    page_icon="",
    layout="wide"
)

# ======================== 1. BMI计算器功能 ========================
def bmi_calculator_ui():
    """BMI计算器"""
    st.subheader(f"{PROGRAM_NAME_ABBREVIATION} - BMI计算器")
    st.divider()

    col1, col2 = st.columns(2)
    height = col1.number_input(
        "身高/米", min_value=0.5, max_value=2.5, step=0.01, format="%.2f"
    )
    weight = col2.number_input(
        "体重/千克", min_value=20, max_value=200, step=1
    )

    # ✅ 按钮固定在上方，结果区域在下方
    if st.button("计算BMI", type="primary"):
        # 结果占位符（在按钮下方）
        result_placeholder = st.empty()
        advice_placeholder = st.empty()
        ai_placeholder = st.empty()

        # 🔄 加载动画显示在按钮下方
        result_placeholder.info("🔄 正在计算BMI，请稍候...")
        time.sleep(0.6)

        # 计算逻辑
        bmi = weight / (height ** 2)
        if bmi < 18.5:
            category = "偏瘦"
            color = "#1E90FF"
            advice = "🍀 建议：增加营养摄入，多吃富含蛋白质的食物，规律作息，适当力量训练。"
        elif 18.5 <= bmi < 24:
            category = "正常"
            color = "#32CD32"
            advice = "✅ 建议：继续保持当前饮食与运动习惯，维持健康体重！"
        elif 24 <= bmi < 28:
            category = "超重"
            color = "#FFD700"
            advice = "⚠️ 建议：控制高油高糖饮食，增加有氧运动（跑步、游泳、骑行）。"
        else:
            category = "肥胖"
            color = "#FF6347"
            advice = "❌ 建议：尽快调整饮食结构，坚持规律运动，可咨询医生制定减脂计划。"

        # 替换结果
        result_placeholder.markdown(f"""
        <div style="background-color:#000;padding:20px;border-radius:10px;text-align:center;">
            <h3>BMI：<span style="color:{color};font-size:24px;">{bmi:.2f}</span></h3>
            <h3>体型：<span style="color:{color};font-size:24px;">{category}</span></h3>
        </div>
        """, unsafe_allow_html=True)

        # 显示建议
        advice_placeholder.subheader("📝 健康建议")
        advice_placeholder.info(advice)

        # # 显示AI按钮（三列布局：Bing, AI, Google）
        # prompt = f"BMI{bmi:.2f}，{category}，健康建议"
        # c1, c2, c3 = ai_placeholder.columns(3)
        # c1.link_button("Ask Bing", f"https://www.bing.com/search?q={prompt}")       # Ask Bing
        # c2.link_button("Ask AI", f"https://chatgpt.com?q={prompt}")                 # Ask ChatGPT
        # c3.link_button("Ask Google", f"https://www.google.com/search?q={prompt}")   # Ask Google

        # 显示建议按钮（紧凑）
        prompt = f"BMI{bmi:.2f}，{category}，健康建议"
        ai_placeholder.markdown(f'''
        <div style="display:flex;gap:6px;justify-content:flex-start;margin-top:10px;">
            <a href="https://www.bing.com/search?q={prompt}" target="_blank"><button style="padding:6px 12px;border-radius:6px;border:none;background:#00a0dc;color:white;">Ask Bing</button></a>
            <a href="https://www.google.com/search?q={prompt}" target="_blank"><button style="padding:6px 12px;border-radius:6px;border:none;background:#00a0dc;color:white;">Ask Google</button></a>
            <a href="https://chatgpt.com?q={prompt}" target="_blank"><button style="padding:6px 12px;border-radius:6px;border:none;background:#00a0dc;color:white;">Ask ChatGPT</button></a>
        </div>
        ''', unsafe_allow_html=True)

# ======================== 2. 凯撒密码加解密功能 ========================
def encryption(plaintext: str, offset: str) -> str:
    if plaintext == '' and offset == '':
        return 'TAG says:"ifmmp xpsme"'
    quantity = int(offset) % 26
    ciphertext = []
    for c in plaintext:
        if c in LOWER_CASE:
            ciphertext.append(LOWER_CASE[(LOWER_DICT[c]-1 + quantity) % 26])
        elif c in UPPER_CASE:
            ciphertext.append(UPPER_CASE[(UPPER_DICT[c]-1 + quantity) % 26])
        else:
            ciphertext.append(c)
    return ''.join(ciphertext)

def decryption(ciphertext: str, offset: str) -> str:
    if ciphertext == '': return 'hello world'
    quantity = int(offset) % 26
    plain = []
    for c in ciphertext:
        if c in LOWER_CASE:
            plain.append(LOWER_CASE[(LOWER_DICT[c]-1 - quantity) % 26])
        elif c in UPPER_CASE:
            plain.append(UPPER_CASE[(UPPER_DICT[c]-1 - quantity) % 26])
        else:
            plain.append(c)
    return ''.join(plain)

def blasting(ciphertext: str) -> str:
    if ciphertext == '':
        return '请输入文本'
    plain = []
    for c in ciphertext:
        if c in LOWER_CASE:
            plain.append(LOWER_CASE[(LOWER_DICT[c]-2) % 26])
        elif c in UPPER_CASE:
            plain.append(UPPER_CASE[(UPPER_DICT[c]-2) % 26])
        else:
            plain.append(c)
    return ''.join(plain)

def caesar_menu_ui():
    st.subheader(f"{PROGRAM_NAME_ABBREVIATION} - 凯撒密码加解密")
    st.divider()
    tab1, tab2, tab3 = st.tabs(["加密", "解密", "爆破"])

    with tab1:
        plaintext = st.text_area("输入明文", height=150)
        offset = st.text_input("偏移值")
        # ✅ 按钮固定在上方
        if st.button("开始加密", type="primary"):
            res_box = st.empty()  # 结果在按钮下方
            res_box.info("🔄 加密中...")
            time.sleep(0.4)
            if not offset.isdigit() and offset != "":
                tab1.error("偏移值必须是数字")
            else:
                res = encryption(plaintext, offset)
            res_box.text_area("密文结果", value=res, disabled=True)

    with tab2:
        ciphertext = st.text_area("输入密文", height=150)
        offset = st.text_input("偏移值", key="dec")
        if st.button("开始解密", type="primary"):
            res_box = st.empty()
            res_box.info("🔄 解密中...")
            time.sleep(0.4)
            if not offset.isdigit():
                tab2.error("偏移值必须是数字")
            else:
                res = decryption(ciphertext, offset)
            res_box.text_area("明文结果", value=res, disabled=True)

    with tab3:
        ciphertext = st.text_area("输入密文", height=150, key="blast")
        if 'blast_count' not in st.session_state:
            st.session_state.blast_count = 0
            st.session_state.current = ""
        st.info(f"爆破次数：{st.session_state.blast_count}/25")
        if st.button("重置爆破"):
            st.session_state.blast_count = 0
            st.session_state.current = ""
            st.rerun()
        if st.button("开始/继续爆破", type="primary"):
            res_box = st.empty()
            res_box.info("🔄 爆破中...")
            time.sleep(0.4)
            if st.session_state.current == "" and ciphertext.strip() == "":
                st.error("请输入密文")
            elif st.session_state.blast_count >= 25:
                st.warning("已达最大次数")
            else:
                if st.session_state.current == "":
                    st.session_state.current = ciphertext
                res = blasting(st.session_state.current)
                st.session_state.current = res
                st.session_state.blast_count += 1
            res_box.text_area("爆破结果", value=res, disabled=True)


# ======================== 3. 随机数游戏功能 ========================
def game_menu_ui():
    st.subheader(f"{PROGRAM_NAME_ABBREVIATION} - 随机数游戏")
    st.divider()
    t1, t2, t3, t4 = st.tabs(["抛瓶子", "抛硬币", "摇色子", "自定义转盘"])

    with t1:
        st.write("### 抛瓶子")
        if st.button("抛瓶子", type="primary", key="bottle"):
            res_box = st.empty()
            res_box.info("🔄 瓶子旋转中...")
            time.sleep(0.5)
            r = random.choice(['失败']*8 + ['成功'])
            res_box.markdown(f"""<div style="background:#000;padding:20px;border-radius:10px;text-align:center;"><h2>结果：{r}</h2></div>""", unsafe_allow_html=True)

    with t2:
        st.write("### 抛硬币")
        if st.button("抛硬币", type="primary", key="coin"):
            res_box = st.empty()
            res_box.info("🔄 硬币翻转中...")
            time.sleep(0.5)
            r = random.choice(['正','反'])
            res_box.markdown(f"""<div style="background:#000;padding:20px;border-radius:10px;text-align:center;"><h2>结果：{r}</h2></div>""", unsafe_allow_html=True)

    with t3:
        st.write("### 摇色子")
        if st.button("摇色子", type="primary", key="dice"):
            res_box = st.empty()
            res_box.info("🔄 骰子滚动中...")
            time.sleep(0.5)
            r = random.choice(['1','2','3','4','5','6'])
            res_box.markdown(f"""<div style="background:#000;padding:20px;border-radius:10px;text-align:center;"><h2>结果：{r}</h2></div>""", unsafe_allow_html=True)

    with t4:
        st.subheader("🎯 自定义转盘")
        st.caption("每行一个选项，空行会自动忽略")

        # 导入后自动回填内容
        if "imported_content" not in st.session_state:
            st.session_state.imported_content = "一等奖\n二等奖\n三等奖\n谢谢参与"

        # 唯一输入框（永远只有一个）
        content = st.text_area("编辑选项", st.session_state.imported_content, height=180)
        options = [line.strip() for line in content.splitlines() if line.strip()]

        # 按钮
        c1, c2, c3 = st.columns(3)
        spin = c1.button("开始转盘", type="primary", use_container_width=True)
        export = c2.button("导出配置", use_container_width=True)
        import_file = c3.file_uploader("导入.txt", type=["txt"], label_visibility="collapsed")

        # 结果区域
        result_area = st.empty()
        # 导出
        if export:
            import base64
            b64 = base64.b64encode(content.encode("utf-8")).decode()
            st.markdown(f"""
            <a href="data:text/plain;charset=utf-8;base64,{b64}" download="转盘配置.txt">
            <button style="width:100%;padding:9px;background:#0078d4;color:white;border:none;border-radius:6px">
            📥 点击下载
            </button></a>
            """, unsafe_allow_html=True)

        # 导入：只覆盖内容，不创建新输入框
        if import_file:
            try:
                txt = import_file.read().decode("utf-8")
                st.session_state.imported_content = txt
                result_area.success("✅ 导入成功！已覆盖到输入框")
            except:
                result_area.error("❌ 导入失败")
        # 转盘
        if spin:
            if not options:
                st.warning("请输入至少一个选项")
            else:
                result_area.info("🔄 转盘中...")
                time.sleep(0.8)
                res = random.choice(options)
                result_area.markdown(f"""
                <div style='background:#000;color:white;padding:24px;border-radius:12px;text-align:center'>
                <h1>🎯 {res}</h1>
                </div>
                """, unsafe_allow_html=True)




# ======================== 4. 数学工具功能 ========================
def number_info_ui(p):
    p.subheader("N为何数")
    n = p.number_input("输入数字", value=0.0)
    if p.button("分析属性", type="primary"):
        res_box = p.empty()
        res_box.info("🔄 分析中...")
        time.sleep(0.4)
        res_box.empty()
        p.write(f"### {n} 的属性")
        if n>0: p.write("正数")
        elif n==0: p.write("零")
        else: p.write("负数")
        if n%1==0:
            i=int(n)
            p.write("偶数" if i%2==0 else "奇数")
            p.write("整数")
        else:
            p.write("小数")
        if n<=1 or n%1!=0:
            p.write("非质非合")
        else:
            i=int(n)
            cnt=sum(1 for x in range(1,i+1) if i%x==0)
            p.write("质数" if cnt==2 else "合数")

def lcm_calculator_ui(p):
    p.subheader("最小公倍数计算器")
    s = p.text_input("用英文逗号分隔")
    if p.button("计算最小公倍数", type="primary"):
        res_box = p.empty()
        res_box.info("🔄 计算中...")
        time.sleep(0.4)
        try:
            nums = [int(x.strip()) for x in s.split(",") if x.strip()]
            m = max(nums)
            while True:
                if all(m%x==0 for x in nums): break
                m+=1
            p.success(f"最小公倍数：{m}")
        except:
            p.error("输入错误")

def common_factors_ui(p):
    p.subheader("两数公因数计算器")
    a = int(p.number_input("数1", 0))
    b = int(p.number_input("数2", 0))
    if p.button("计算公因数", type="primary"):
        res_box = p.empty()
        res_box.info("🔄 计算中...")
        time.sleep(0.4)
        fa = set(x for x in range(1, abs(a)+1) if a % x == 0)
        fb = set(x for x in range(1, abs(b)+1) if b % x == 0)
        common = sorted(fa & fb)
        p.success(f"公因数：{common}")

def number_sort_ui(p):
    p.subheader("数字排序工具")
    s = p.text_input("逗号分隔数字")
    if p.button("排序", type="primary"):
        res_box = p.empty()
        res_box.info("🔄 排序中...")
        time.sleep(0.4)
        try:
            nums = sorted(int(x.strip()) for x in s.split(",") if x.strip())
            p.success(f"结果：{nums}")
        except:
            p.error("格式错误")

def math_tools_menu_ui():
    st.subheader("数学工具")
    t1,t2,t3,t4 = st.tabs(["N为何数","最小公倍数","公因数","排序"])
    number_info_ui(t1)
    lcm_calculator_ui(t2)
    common_factors_ui(t3)
    number_sort_ui(t4)


# ======================== 网站收录 ========================
def web_menu_ui():
    st.subheader("优质网站收录")
    st.divider()
    st.info("提示，此页面为实用网站收录，仅作导航页使用。")
    with st.expander("娱乐"):
        st.markdown("免费电影：[69美剧](sslocal://flow/file_open?url=https%3A%2F%2F69mj.com%2F&flow_extra=eyJsaW5rX3R5cGUiOiJjb2RlX2ludGVycHJldGVyIn0=)")
    with st.expander("工具"):
        st.markdown("在线PS：[稿定](sslocal://flow/file_open?url=https%3A%2F%2Fps.gaoding.com%2F%23%2F&flow_extra=eyJsaW5rX3R5cGUiOiJjb2RlX2ludGVycHJldGVyIn0=)")
    st.markdown("菜鸟教程：https://www.runoob.com/")


# ======================== 主页面 & URL路由 ========================
query = st.query_params
page = query.get("page", "home")

def main_ui():
    st.sidebar.header("功能导航")
    menu = {
        "HELLOTAG":"home",
        "随机数游戏":"game",
        "凯撒密码加解密":"caesar",
        "BMI计算器":"bmi",
        "数学工具":"math",
        "优质网站收录":"web"
    }
    select_label = st.sidebar.radio("选择功能", list(menu.keys()),
                                   index=list(menu.values()).index(page))
    select_page = menu[select_label]

    if select_page != page:
        st.query_params["page"] = select_page
        st.rerun()

    if select_page == "game":
        game_menu_ui()
    elif select_page == "caesar":
        caesar_menu_ui()
    elif select_page == "bmi":
        bmi_calculator_ui()
    elif select_page == "math":
        math_tools_menu_ui()
    elif select_page == "web":
        web_menu_ui()
    else:
        st.title(f"{PROGRAM_NAME} {PROGRAM_VERSION}")
        st.divider()
        st.subheader("HELLOTAG")
        st.write("基于 Python + Streamlit 构建")
        st.write("开发者：Vincent")

if __name__ == "__main__":
    main_ui()
