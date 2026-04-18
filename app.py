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


# BMI
def bmi_calculator_ui():
    st.subheader(f"{PROGRAM_NAME_ABBREVIATION} - BMI计算器")
    st.divider()

    col1, col2 = st.columns(2)
    height = col1.number_input(
        "身高/米", min_value=0.5, max_value=2.5, step=0.01, format="%.2f"
    )
    weight = col2.number_input(
        "体重/千克", min_value=20, max_value=200, step=1
    )

    if st.button("计算BMI", type="primary"):
        # 结果占位符
        result_placeholder = st.empty()
        advice_placeholder = st.empty()
        ai_placeholder = st.empty()

        result_placeholder.info("🔄 正在计算BMI，请稍候...")
        time.sleep(0.6)

        bmi = weight / (height ** 2)
        if bmi < 18.5:
            category = "偏瘦"
            color = "#1E90FF"
            advice = "＞﹏＜ 建议：增加营养摄入，多吃富含蛋白质的食物，规律作息，适当力量训练。"
        elif 18.5 <= bmi < 24:
            category = "正常"
            color = "#32CD32"
            advice = "(≧ ▽ ≦) 建议：继续保持当前饮食与运动习惯，维持健康体重"
        elif 24 <= bmi < 28:
            category = "超重"
            color = "#FFD700"
            advice = "≡(▔﹏▔)≡ 建议：控制高油高糖饮食，增加有氧运动（跑步、游泳、骑行）。"
        else:
            category = "肥胖"
            color = "#FF6347"
            advice = "(ノ｀Д)ノ 建议：尽快调整饮食结构，坚持规律运动，可咨询医生制定减脂计划。"
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

        # # 显示按钮（三列布局）
        # prompt = f"BMI{bmi:.2f}，{category}，健康建议"
        # c1, c2, c3 = ai_placeholder.columns(3)
        # c1.link_button("Ask Bing", f"https://www.bing.com/search?q={prompt}")       # Ask Bing
        # c2.link_button("Ask AI", f"https://chatgpt.com?q={prompt}")                 # Ask ChatGPT
        # c3.link_button("Ask Google", f"https://www.google.com/search?q={prompt}")   # Ask Google

        # 显示按钮（紧凑）
        prompt = f"BMI{bmi:.2f}，{category}，健康建议"
        ai_placeholder.markdown(f'''
        <div style="display:flex;gap:6px;justify-content:flex-start;margin-top:10px;">
            <a href="https://www.bing.com/search?q={prompt}" target="_blank"><button style="padding:6px 12px;border-radius:6px;border:none;background:#00a0dc;color:white;">Ask Bing</button></a>
            <a href="https://www.google.com/search?q={prompt}" target="_blank"><button style="padding:6px 12px;border-radius:6px;border:none;background:#00a0dc;color:white;">Ask Google</button></a>
            <a href="https://chatgpt.com?q={prompt}" target="_blank"><button style="padding:6px 12px;border-radius:6px;border:none;background:#00a0dc;color:white;">Ask ChatGPT</button></a>
        </div>
        ''', unsafe_allow_html=True)


# 凯撒密码加解密
def encryption(plaintext: str, offset: str) -> str:
    if plaintext == '' and offset == '':
        return 'Vincent says:"ifmmp xpsme"'

    quantity = int(offset) % 26
    ciphertext_list = []

    for char in plaintext:
        if char in LOWER_CASE:
            idx = (LOWER_DICT[char] - 1 + quantity) % 26
            ciphertext_list.append(LOWER_CASE[idx])
        elif char in UPPER_CASE:
            idx = (UPPER_DICT[char] - 1 + quantity) % 26
            ciphertext_list.append(UPPER_CASE[idx])
        else:
            ciphertext_list.append(char)

    ciphertext = ''.join(ciphertext_list)
    return ciphertext


def decryption(ciphertext: str, offset: str) -> str:
    if ciphertext == '':
        return 'hello world'

    quantity = int(offset) % 26
    if quantity == 0:
        return ciphertext

    plaintext_list = []
    for char in ciphertext:
        if char in LOWER_CASE:
            idx = (LOWER_DICT[char] - 1 - quantity) % 26
            plaintext_list.append(LOWER_CASE[idx])
        elif char in UPPER_CASE:
            idx = (UPPER_DICT[char] - 1 - quantity) % 26
            plaintext_list.append(UPPER_CASE[idx])
        else:
            plaintext_list.append(char)

    plaintext = ''.join(plaintext_list)
    return plaintext


def blasting(ciphertext: str) -> str:
    if ciphertext == '':
        return '请输入文本(若输入了文本但仍显示为输入，则请点击重置爆破)'

    plaintext_list = []
    quantity = 1
    for char in ciphertext:
        if char in LOWER_CASE:
            idx = (LOWER_DICT[char] - 1 - quantity) % 26
            plaintext_list.append(LOWER_CASE[idx])
        elif char in UPPER_CASE:
            idx = (UPPER_DICT[char] - 1 - quantity) % 26
            plaintext_list.append(UPPER_CASE[idx])
        else:
            plaintext_list.append(char)

    plaintext = ''.join(plaintext_list)
    return plaintext


def caesar_menu_ui():
    st.subheader(f"{PROGRAM_NAME_ABBREVIATION} - 凯撒密码加解密")
    st.divider()

    # 选项卡切换
    tab1, tab2, tab3 = st.tabs(["加密", "解密", "爆破"])

    # 加密标签页
    plaintext = tab1.text_area("输入明文", placeholder="请输入需要加密的文本...", height=150)
    offset = tab1.text_input("输入偏移值（正数）", placeholder="如：1/5/10")
    if tab1.button("开始加密", type="primary"):
        if not offset.isdigit() and offset != '':
            tab1.error("偏移值必须是纯数字")
        else:
            result = encryption(plaintext, offset)
            tab1.success("加密完成")
            # tab1.write(result)
            tab1.text_area("密文结果", value=result, height=150, disabled=True, placeholder="解密结果将显示在这里...")

    # 解密标签页
    ciphertext = tab2.text_area("输入密文", placeholder="请输入需要解密的文本...", height=150)
    offset_dec = tab2.text_input("输入偏移值（正数）", placeholder="如：1/5/10", key="dec_offset")
    if tab2.button("开始解密", type="primary"):
        if not offset_dec.isdigit():
            tab2.error("偏移值必须是纯数字")
        else:
            result = decryption(ciphertext, offset_dec)
            tab2.success("解密完成")
            # tab2.write(result)
            tab2.text_area("明文结果", value=result, height=150, disabled=True, placeholder="解密结果将显示在这里...")

    # 爆破标签页
    ciphertext_blast = tab3.text_area("输入密文", placeholder="请输入需要爆破的文本...", height=150, key="blast_text")
    # 初始化会话状态
    if 'blast_count' not in st.session_state:
        st.session_state.blast_count = 0
        st.session_state.current_result = ""
        st.session_state.current_ct = ""

    col1, col2 = tab3.columns([3, 1])
    col1.info(f"当前爆破次数：{st.session_state.blast_count}/25")
    reset = col2.button("重置爆破")
    if reset:
        st.session_state.blast_count = 0
        st.session_state.current_result = ""
        st.session_state.current_ct = ""
        st.rerun()

    if tab3.button("开始/继续爆破", type="primary"):
        if st.session_state.blast_count == 0 and st.session_state.current_ct == "":
            if ciphertext_blast == "":
                tab3.error("请先输入密文")
            else:
                st.session_state.current_ct = ciphertext_blast
        if st.session_state.current_ct == "":
            tab3.error("请先输入密文")
        elif st.session_state.blast_count >= 25:
            tab3.warning("已达到理论最大爆破次数（25次）")
        else:
            result = blasting(st.session_state.current_ct)
            st.session_state.current_result = result
            st.session_state.current_ct = result
            st.session_state.blast_count += 1
            # tab3.write(result)
            tab3.text_area("爆破结果", value=result, height=150, disabled=True, placeholder="爆破结果将显示在这里...")
            if st.session_state.blast_count >= 25:
                tab3.warning("已达到理论最大爆破次数（25次）")


# 随机数游戏
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
            r = random.choice(['失败']*6 + ['成功'])
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

        content = st.text_area("编辑选项", st.session_state.imported_content, height=180)
        options = [line.strip() for line in content.splitlines() if line.strip()]

        c1, c2, c3 = st.columns(3)
        spin = c1.button("开始转盘", type="primary", use_container_width=True)
        export = c2.button("导出配置", use_container_width=True)
        import_file = c3.file_uploader("导入.txt", type=["txt"], label_visibility="collapsed")

        result_area = st.empty()

        if export:
            import base64
            b64 = base64.b64encode(content.encode("utf-8")).decode()
            st.markdown(f"""
            <a href="data:text/plain;charset=utf-8;base64,{b64}" download="转盘配置.txt">
            <button style="width:100%;padding:9px;background:#0078d4;color:white;border:none;border-radius:6px">
            📥 点击下载
            </button></a>
            """, unsafe_allow_html=True)

        if import_file:
            try:
                txt = import_file.read().decode("utf-8")
                st.session_state.imported_content = txt
                result_area.success("✅ 导入成功，已覆盖到输入框")
            except:
                result_area.error("❌ 导入失败")

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


# 数学工具
def number_info_ui(parent):
    parent.subheader("N为何数（分析有理数属性）")
    num_input = parent.number_input(
        "输入有理数",
        help="不建议输入单位超过百万的数，否则会产生卡顿",
        value=0.0,
        step=0.1
    )

    if parent.button("分析属性", type="primary"):
        n = num_input
        parent.divider()
        parent.write(f"### {n} 的属性：")

        if n > 0:
            parent.write("是正数")
        elif n == 0:
            parent.write("不是正数也不是负数")
        else:
            parent.write("是负数")

        if n % 1 == 0:
            n_int = int(n)
            if n_int % 2 == 0:
                parent.write("是偶数")
            else:
                parent.write("是奇数")
            parent.write("是整数")
        else:
            parent.write("是小数（分数），不是偶数也不是奇数")

        if n <= 1 or n % 1 != 0:
            parent.write("不是质数也不是合数")
        else:
            n_int = int(n)
            factor_count = 0
            for x in range(1, n_int + 1):
                if n_int % x == 0:
                    factor_count += 1
            if factor_count == 2:
                parent.write("是质数")
            elif factor_count > 2:
                parent.write("是合数")


def lcm_calculator_ui(parent):
    parent.subheader("最小公倍数计算器")
    input_str = parent.text_input("请输入用逗号(英文逗号)分隔的整数", placeholder="如：2,3,4")

    if parent.button("计算最小公倍数", type="primary"):
        try:
            numbers = [int(num.strip()) for num in input_str.split(",") if num.strip()]
            if not numbers:
                parent.error("未输入任何数字")
                return

            numbers_sorted = sorted(numbers)
            parent.write(f"输入数字排序：{numbers_sorted}")

            max_num = numbers_sorted[-1]
            lcm = max_num
            while True:
                if all(lcm % num == 0 for num in numbers):
                    break
                lcm += 1

            parent.success(f"{numbers} 的最小公倍数是：{lcm}")
        except ValueError:
            parent.error("输入无效，请输入整数并用英文逗号分隔")


def common_factors_ui(parent):
    parent.subheader("两数公因数计算器")
    col1, col2 = parent.columns(2)
    a = col1.number_input("输入第一个整数", step=1, value=0)
    b = col2.number_input("输入第二个整数", step=1, value=0)

    if parent.button("计算公因数", type="primary"):
        a_factors = set()
        for c in range(1, abs(a) + 1):
            if a % c == 0:
                a_factors.add(c)

        b_factors = set()
        for c in range(1, abs(b) + 1):
            if b % c == 0:
                b_factors.add(c)

        common = sorted(a_factors.intersection(b_factors))

        parent.write(f"{a} 的因数：{sorted(a_factors)}")
        parent.write(f"{b} 的因数：{sorted(b_factors)}")
        parent.success(f"{a} 和 {b} 的公因数：{common}")


def number_sort_ui(parent):
    parent.subheader("数字排序工具")
    input_str = parent.text_input("请输入用逗号(英文逗号)分隔的整数", placeholder="如：5,2,8,1", key="sort_input")

    if parent.button("排序", type="primary"):
        try:
            numbers = [int(num.strip()) for num in input_str.split(",") if num.strip()]
            if not numbers:
                parent.error("未输入任何数字")
                return

            sorted_nums = sorted(numbers)
            parent.write(f"输入数字：{numbers}")
            parent.success(f"从小到大排序：{sorted_nums}")
        except ValueError:
            parent.error("输入无效，请输入整数并用英文逗号分隔")


def math_tools_menu_ui():
    st.subheader(f"{PROGRAM_NAME_ABBREVIATION} - 数学工具")
    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "N为何数",
        "最小公倍数计算器",
        "两数公因数计算器",
        "数字排序工具"
    ])


    number_info_ui(tab1)
    lcm_calculator_ui(tab2)
    common_factors_ui(tab3)
    number_sort_ui(tab4)


def web_menu_ui():
    st.subheader(f"{PROGRAM_NAME_ABBREVIATION} - 优质网站收录")
    st.divider()
    st.info("提示：此页面为实用网站收录，仅作导航页使用。除特殊标注外，所有网站均为公开网络资源，并非作者创建或运营。使用时请遵守对应网站规则与国家法律法规，风险自负。")
    st.divider()
    with st.expander("娱乐"):
        st.markdown("免费电影：[69美剧](https://69mj.com/)")
        st.markdown("emoji混合：[emojimix](https://tikolu.net/emojimix/)")
        st.markdown("在线钢琴：[自由钢琴-AutoPiano|在线钢琴，键盘钢琴，模拟钢琴，多种乐器选择，好听又好玩](https://www.autopiano.cn/)")

    with st.expander("工具"):
        st.markdown("音乐LRC文件下载：[Music Lyrics LRC files Download](https://www.megalobiz.com/lrc/maker/download-music-lyrics-lrc-generated-files)")
        st.markdown("加解密网页小工具：[RSA加密/解密工具 - 在线RSA加密解密等五种使用场景](https://try8.cn/tool/cipher/rsa)")
        st.markdown("免费心理测试网站：[赛可心理测试](https://m.psyctest.cn/))")
        st.markdown("在线PS：[ps photoshop editor - photoshop image editor](https://ps.ittools.cc/editor/)")
        st.markdown("新闻地图：[China Interactive News Map -china.liveuamap.com](https://china.liveuamap.com/)")
        st.markdown("时光邮局：[时光邮局-给未来的自己写一封信](https://www.hi2future.com/)")
        st.markdown("Adobe破解版下载：[【软件资源长期更新】★.lxtable](https://share.note.youdao.com/ynoteshare/index.html?id=ce9e1c5bde9e69d261e4bd6494c8d148&type=note&_time=1755589394493)")
        st.markdown("MasterGo：[MasterGo](https://mastergo.com/)")
        st.markdown("AI写歌：[suno](https://suno.hzlesu.cn/h5/suno/music.html?self_os=1&platform_id=4&app_id=1186&agency_id=215&channel_id=13682&bd_vid=2045533973130832212&is_buy=1&packet=bdds)")
        st.markdown("片头模板/制作：[Panzoid](https://panzoid.com/)")
        st.markdown("在线PS：[稿定|在线PS](https://ps.gaoding.com/#/)")
        st.markdown("在线设计：[MOCKITT](https://mockitt.com/)")
    with st.expander("其他"):
        st.markdown("编程教程：[菜鸟教程](https://www.runoob.com/)")
        st.markdown("优质网站收录：[lkssite](https://lkssite.vip/)")
        st.markdown("另一个弱一点的优质网站收录：[就是我！(≧∇≦)ﾉ](https://vd3.bdstatic.com/mda-qjcrrsjkbtmeycuv/360p/h264/1728843064552037960/mda-qjcrrsjkbtmeycuv.mp4)")

def about_menu_ui():
    st.subheader(f"{PROGRAM_NAME_ABBREVIATION} - 关于项目")
    st.divider()

    st.markdown("## 项目简介")
    st.write("项目全称：Tools and Games (TAG) V2.0")
    st.write("开发语言：Python")
    st.write("搭建框架：Streamlit")
    st.write("项目类型:多功能实用工具集网页应用")
    st.write("本项目是一款轻量化跨平台网页工具合集，整合日常学习计算、文本加密、趣味随机游戏、实用网站导航等多功能模块，界面简洁易用，操作门槛低，无需安装客户端，浏览器即可打开使用。")

    st.divider()

    st.markdown("## 开发初心")
    st.write("""
    在日常学习与生活中，经常会遇到零散重复的计算需求、文本加密需求、随机选择抽签场景，同时网上各类工具分散杂乱、广告繁多。

    因此我开发了 **TAG 工具集**，整合所有常用小功能到同一个网页里，无多余广告、界面简洁清爽，兼顾学习实用性与休闲趣味性，
    希望用编程做出能真正服务日常、方便自己与他人的轻量化工具。
    """)

    st.divider()

    st.markdown("## 全部功能模块")
    with st.expander("数学工具箱", expanded=False):
        st.write("""
        - BMI健康指数计算器
        - 整数属性分析（正负数、奇偶、质合数判断）
        - 多数字最小公倍数计算
        - 两数公因数全量求解
        - 数字自动排序工具
        """)
    with st.expander("文本加解密", expanded=False):
        st.write("""
        - 凯撒密码自定义偏移加密
        - 凯撒密码对应偏移解密
        - 凯撒密码逐位爆破遍历
        """)
    with st.expander("趣味随机游戏", expanded=False):
        st.write("""
        - 抛瓶子、抛硬币、摇骰子经典随机小游戏
        - 自定义抽签转盘，支持选项自定义编辑
        - 转盘配置文件导入、导出本地保存
        """)
    with st.expander("实用网站导航", expanded=False):
        st.write("""合网络优质公开工具、学习网站、娱乐站点，仅做导航收录
        ##⚠免责声明
        本页面仅为第三方网站导航收录平台。除特殊标注说明外，所有收录网站均为**公开网络资源**，并非作者创建、运营。用户自主访问、使用外部网站所产生的一切行为与后果，由用户自行承担，请严格遵守国家相关法律法规与各平台用户协议。
        """)

    st.divider()

    st.markdown("## 后续更新规划")
    st.write("""
    本项目**不止于比赛参赛作品**，后续将会持续迭代优化：
    - 持续优化各模块交互细节，修复已知问题，完善界面适配
    - 新增更多日常实用工具模块
    - 优化数据本地保存逻辑，提升使用体验
    - 补充更多实用公开资源导航
    """)

    st.divider()

    st.markdown("## 反馈与建议")
    st.write("使用中遇到BUG、想要新增功能、有任何优化建议，都可以通过下方问卷提交：")
    st.write("[点击提交项目反馈](https://forms.office.com/Pages/ResponsePage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAANAAX0z5qdUMU1OTldYUEdYV0xDVEdQWDlINVlRTDJGWi4u)")

    st.divider()

    st.markdown("### 开发者寄语")
    st.caption("开发者：Vincent")

    # 左右列宽 1:3
    col_avatar, col_saying = st.columns([1, 3])

    # 左侧：头像区域
    with col_avatar:
        st.image("VIN.png", width=200)
        st.caption("Vincent")

    # 右侧：寄语文本框
    with col_saying:
        ""
        ""
        "***真正有价值的程序应该是能够服务人类的***"
        "***而非用复杂繁琐的结构与千奇百怪的语法炫技***"

    # ""
    "***Made simple, made useful.***"
    "***One small tool, for your daily life.***"

    # """Give people wonderful tools, and they'll do wonderful things."""


query = st.query_params
page = query.get("page", "home")
def main_ui():
    st.sidebar.header("功能选择")
    menu = {
        "HELLOTAG":"home",
        "随机数游戏":"game",
        "凯撒密码加解密":"caesar",
        "BMI计算器":"bmi",
        "数学工具":"math",
        "优质网站收录":"web",
        "About": "about"
    }
    select_label = st.sidebar.radio("", list(menu.keys()),
                                   index=list(menu.values()).index(page),
                                    label_visibility="collapsed")
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
    elif select_page == "about":
        about_menu_ui()
    else:
        st.title(f"{PROGRAM_NAME} {PROGRAM_VERSION}")
        st.divider()
        st.subheader("HELLOTAG")
        st.write(f"版本：{PROGRAM_VERSION}")
        st.write("包含功能：随机数游戏、凯撒密码加解密、BMI计算器、数学工具")
        st.write("开发者：Vincent")
        st.write("基于 Python,Streamlit 构建的网页版工具集")
        st.divider()

        little_tag = ["临时标注：",
                      "此项目不仅仅是一个比赛作品，而是一个希望能服务大众的工具。按计划将来 Vincent 会继续优化它"]
        text = ""
        for reason in little_tag:
            text += f"- {reason}\n"
        st.warning(text)

# God bless this code works
if __name__ == "__main__":
    main_ui()
