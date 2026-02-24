# 导入streamlit库，用于快速构建网页应用
import streamlit as st
# 导入random库，用于随机数游戏的随机结果生成
import random

# ======================== 全局常量定义 ========================
# 程序全称（用于页面标题、子标题展示）
PROGRAM_NAME = "Tools and Games (TAG)"
# 程序版本号（用于页面标题、首页展示）
PROGRAM_VERSION = "V2.0"
# 程序缩写（用于子标题简化展示）
PROGRAM_NAME_ABBREVIATION = "TAG"

# ======================== 凯撒密码核心数据初始化 ========================
# 生成小写字母列表（a-z）：通过ASCII码转换+列表推导式，避免手动输入
LOWER_CASE = [chr(ord('a') + i) for i in range(26)]
# 生成大写字母列表（A-Z）：逻辑同小写字母，仅起始ASCII码不同（A=65，a=97）
UPPER_CASE = [chr(ord('A') + i) for i in range(26)]
# 构建小写字母到数字的映射字典（a:1, b:2...z:26）：便于快速查询字母位置
LOWER_DICT = {char: idx + 1 for idx, char in enumerate(LOWER_CASE)}
# 构建大写字母到数字的映射字典（A:1, B:2...Z:26）：逻辑同小写字母字典
UPPER_DICT = {char: idx + 1 for idx, char in enumerate(UPPER_CASE)}

# ======================== Streamlit页面全局配置 ========================
st.set_page_config(
    # 设置网页标题：程序全称 + 版本号，便于浏览器标签识别
    page_title=f"{PROGRAM_NAME} {PROGRAM_VERSION}",
    # 网页图标：此处为空，可自定义为emoji（如":🎯:"）或图片链接
    page_icon="",
    # 页面布局：宽屏模式（wide），充分利用浏览器宽度
    layout="wide"
)


# ======================== 1. BMI计算器功能模块 ========================
def bmi_calculator_ui():
    """BMI计算器UI与逻辑函数：负责展示界面、接收输入、计算并展示结果"""
    # 显示BMI计算器子标题：程序缩写 + 功能名，统一视觉风格
    st.subheader(f"{PROGRAM_NAME_ABBREVIATION} - BMI计算器")
    # 添加水平分隔线，分隔标题和输入区域，美化界面
    st.divider()

    # 布局：创建两列输入区域（身高+体重），使界面更紧凑
    col1, col2 = st.columns(2)
    # 第一列：身高输入框（单位：米）
    height = col1.number_input(
        "身高/米",  # 输入框标签
        min_value=0.5,  # 最小值限制：0.5米（符合人类身高范围）
        max_value=2.5,  # 最大值限制：2.5米
        step=0.01,  # 步长：每次增减0.01米（精确到厘米）
        format="%.2f",  # 显示格式：保留2位小数
        help="请输入介于0.5-2.5之间的有效身高"  # 帮助提示：鼠标悬浮时显示
    )
    # 第二列：体重输入框（单位：千克）
    weight = col2.number_input(
        "体重/千克",  # 输入框标签
        min_value=20,  # 最小值限制：20千克（符合人类体重范围）
        max_value=200,  # 最大值限制：200千克
        step=1,  # 步长：每次增减1千克
        help="请输入介于20-200之间的有效体重"  # 帮助提示
    )

    # 创建主色调计算按钮：点击后触发BMI计算逻辑
    if st.button("计算BMI", type="primary"):
        # 核心公式：BMI = 体重(kg) / 身高(m)的平方
        bmi = weight / (height ** 2)

        # 根据BMI值判断体型，并匹配对应颜色（便于视觉区分）
        if bmi < 18.5:
            category = "偏瘦"  # 体型结果
            color = "#1E90FF"  # 深蓝色：对应偏瘦
        elif 18.5 <= bmi < 24:
            category = "正常"  # 体型结果
            color = "#32CD32"  # 绿色：对应正常
        elif 24 <= bmi < 28:
            category = "超重"  # 体型结果
            color = "#FFD700"  # 金色：对应超重
        else:
            category = "肥胖"  # 体型结果
            color = "#FF6347"  # 番茄红：对应肥胖

        # 结果展示区域：添加分隔线，分隔输入和结果
        st.divider()
        # 用HTML自定义样式展示结果：黑色背景+居中+彩色数值，提升视觉效果
        st.markdown(f"""
        <div style="background-color:#000000;padding:20px;border-radius:10px;text-align:center;">
            <h3>BMI指数：<span style="color:{color};font-size:24px;">{bmi:.2f}</span></h3>
            <h3>体型判断：<span style="color:{color};font-size:24px;">{category}</span></h3>
        </div>
        """,
                    # 关键参数：允许解析HTML/CSS（否则会显示原始标签）
                    unsafe_allow_html=True)


# ======================== 2. 凯撒密码功能模块 ========================
def encryption(plaintext: str, offset: str) -> str:
    """
    凯撒密码加密函数：将明文按指定偏移量转换为密文
    :param plaintext: 输入的明文字符串
    :param offset: 偏移值字符串（需转换为整数）
    :return: 加密后的密文字符串
    """
    # 特殊场景：明文和偏移值都为空时，返回预设密文（彩蛋/测试用）
    if plaintext == '' and offset == '':
        return 'TAG says:"ifmmp xpsme"'

    # 计算有效偏移量：转换为整数后取模26（确保偏移量在0-25之间，避免超出字母表范围）
    quantity = int(offset) % 26
    # 初始化密文列表：用于逐个存储加密后的字符，最后拼接为字符串
    ciphertext_list = []

    # 遍历明文中的每个字符，逐个加密
    for char in plaintext:
        # 如果是小写字母：按偏移量计算新字符
        if char in LOWER_CASE:
            # 计算加密后字符的索引：原索引 + 偏移量，取模26保证在字母表内
            idx = (LOWER_DICT[char] - 1 + quantity) % 26
            # 将加密后的字符加入列表
            ciphertext_list.append(LOWER_CASE[idx])
        # 如果是大写字母：逻辑同小写字母，仅使用大写字母表
        elif char in UPPER_CASE:
            idx = (UPPER_DICT[char] - 1 + quantity) % 26
            ciphertext_list.append(UPPER_CASE[idx])
        # 非字母字符（空格、符号等）：直接保留，不加密
        else:
            ciphertext_list.append(char)

    # 将密文字符列表拼接为完整字符串（效率高于循环+拼接）
    ciphertext = ''.join(ciphertext_list)
    # 返回最终密文
    return ciphertext


def decryption(ciphertext: str, offset: str) -> str:
    """
    凯撒密码解密函数：将密文按指定偏移量转换为明文
    :param ciphertext: 输入的密文字符串
    :param offset: 偏移值字符串（需转换为整数）
    :return: 解密后的明文字符串
    """
    # 特殊场景：密文为空时，返回预设明文（彩蛋/测试用）
    if ciphertext == '':
        return 'hello world'

    # 计算有效偏移量：转换为整数后取模26
    quantity = int(offset) % 26
    # 偏移量为0时：密文=明文，直接返回
    if quantity == 0:
        return ciphertext

    # 初始化明文列表：用于逐个存储解密后的字符
    plaintext_list = []
    # 遍历密文中的每个字符，逐个解密
    for char in ciphertext:
        # 如果是小写字母：按偏移量反向计算原字符
        if char in LOWER_CASE:
            idx = (LOWER_DICT[char] - 1 - quantity) % 26
            plaintext_list.append(LOWER_CASE[idx])
        # 如果是大写字母：逻辑同小写字母
        elif char in UPPER_CASE:
            idx = (UPPER_DICT[char] - 1 - quantity) % 26
            plaintext_list.append(UPPER_CASE[idx])
        # 非字母字符：直接保留
        else:
            plaintext_list.append(char)

    # 将明文字符列表拼接为完整字符串
    plaintext = ''.join(plaintext_list)
    # 返回最终明文
    return plaintext


def blasting(ciphertext: str) -> str:
    """
    凯撒密码爆破函数：逐次尝试偏移量解密（无需手动输入偏移值）
    :param ciphertext: 输入的密文字符串
    :return: 单次爆破后的明文字符串
    """
    # 特殊场景：密文为空时，返回提示文本
    if ciphertext == '':
        return '''请输入文本。。。
(若输入了文本但仍显示为输入，则请点击重置爆破)'''

    # 初始化明文列表：存储单次爆破后的字符
    plaintext_list = []
    # 爆破偏移量初始化为1（每次爆破+1，最多25次）
    quantity = 1
    # 遍历密文字符，按当前偏移量解密
    for char in ciphertext:
        if char in LOWER_CASE:
            idx = (LOWER_DICT[char] - 1 - quantity) % 26
            plaintext_list.append(LOWER_CASE[idx])
        elif char in UPPER_CASE:
            idx = (UPPER_DICT[char] - 1 - quantity) % 26
            plaintext_list.append(UPPER_CASE[idx])
        else:
            plaintext_list.append(char)

    # 拼接爆破结果字符串
    plaintext = ''.join(plaintext_list)
    # 返回单次爆破结果
    return plaintext


def caesar_menu_ui():
    """凯撒密码UI函数：负责展示加解密/爆破的界面和交互逻辑"""
    # 显示子标题：程序缩写 + 功能名
    st.subheader(f"{PROGRAM_NAME_ABBREVIATION} - 凯撒密码加解密")
    # 添加水平分隔线
    st.divider()

    # 创建三个选项卡：加密、解密、爆破，实现功能切换
    tab1, tab2, tab3 = st.tabs(["加密", "解密", "爆破"])

    # ======================== 加密标签页 ========================
    # 明文输入文本域：大尺寸输入框，适合多字符输入
    plaintext = tab1.text_area("输入明文", placeholder="请输入需要加密的文本...", height=150)
    # 偏移值输入框：单行输入，提示示例值
    offset = tab1.text_input("输入偏移值（正数）", placeholder="如：1/5/10")
    # 主色调加密按钮：点击触发加密逻辑
    if tab1.button("开始加密", type="primary"):
        # 输入校验：偏移值非空且不是纯数字时，提示错误
        if not offset.isdigit() and offset != '':
            tab1.error("偏移值必须是纯数字！")
        else:
            # 执行加密函数，获取密文结果（移除with spinner，直接执行）
            result = encryption(plaintext, offset)
            # 加密成功提示：绿色对勾+文字
            tab1.success("加密完成！")
            # 直接展示结果（临时查看）
            tab1.write(result)
            # 禁用的文本域：固定展示密文结果，防止误修改
            tab1.text_area("密文结果", value=result, height=150, disabled=True, placeholder="解密结果将显示在这里...")

    # ======================== 解密标签页 ========================
    # 密文输入文本域
    ciphertext = tab2.text_area("输入密文", placeholder="请输入需要解密的文本...", height=150)
    # 偏移值输入框：设置唯一key，避免与加密页输入框冲突
    offset_dec = tab2.text_input("输入偏移值（正数）", placeholder="如：1/5/10", key="dec_offset")
    # 主色调解密按钮
    if tab2.button("开始解密", type="primary"):
        # 输入校验：偏移值不是纯数字时，提示错误
        if not offset_dec.isdigit():
            tab2.error("偏移值必须是纯数字！")
        else:
            # 执行解密函数，获取明文结果
            result = decryption(ciphertext, offset_dec)
            # 解密成功提示
            tab2.success("解密完成！")
            # 直接展示结果
            tab2.write(result)
            # 禁用的文本域：展示明文结果
            tab2.text_area("明文结果", value=result, height=150, disabled=True, placeholder="解密结果将显示在这里...")

    # ======================== 爆破标签页 ========================
    # 密文输入文本域：设置唯一key，避免与其他标签页冲突
    ciphertext_blast = tab3.text_area("输入密文", placeholder="请输入需要爆破的文本...", height=150, key="blast_text")
    # 初始化会话状态：存储爆破次数（页面刷新不丢失）
    if 'blast_count' not in st.session_state:
        st.session_state.blast_count = 0  # 爆破次数初始化为0
        st.session_state.current_result = ""  # 当前爆破结果初始化为空
        st.session_state.current_ct = ""  # 当前待爆破密文初始化为空

    # 布局：两列（显示爆破次数 + 重置按钮）
    col1, col2 = tab3.columns([3, 1])
    # 第一列：显示当前爆破进度（已爆破次数/最大次数25）
    col1.info(f"当前爆破次数：{st.session_state.blast_count}/25")
    # 第二列：重置爆破按钮
    reset = col2.button("重置爆破")
    # 点击重置按钮时：清空会话状态，重置爆破
    if reset:
        st.session_state.blast_count = 0
        st.session_state.current_result = ""
        st.session_state.current_ct = ""
        # 重新运行页面：刷新状态，清空结果
        st.rerun()

    # 主色调爆破按钮：开始/继续爆破
    if tab3.button("开始/继续爆破", type="primary"):
        # 首次爆破：未记录待爆破密文时
        if st.session_state.blast_count == 0 and st.session_state.current_ct == "":
            # 密文为空时提示错误
            if ciphertext_blast == "":
                tab3.error("请先输入密文！")
            else:
                # 记录待爆破密文到会话状态
                st.session_state.current_ct = ciphertext_blast
        # 待爆破密文为空时提示错误
        if st.session_state.current_ct == "":
            tab3.error("请先输入密文！")
        # 爆破次数达到25次（最大理论次数）时提示警告
        elif st.session_state.blast_count >= 25:
            tab3.warning("已达到理论最大爆破次数（25次）！")
        else:
            # 执行爆破函数，获取单次爆破结果
            result = blasting(st.session_state.current_ct)
            # 存储当前爆破结果到会话状态
            st.session_state.current_result = result
            # 将当前结果设为下一次爆破的密文（逐次偏移）
            st.session_state.current_ct = result
            # 爆破次数+1
            st.session_state.blast_count += 1
            # 展示爆破结果
            tab3.write(result)
            # 禁用的文本域：展示爆破结果
            tab3.text_area("爆破结果", value=result, height=150, disabled=True, placeholder="爆破结果将显示在这里...")
            # 达到最大次数时再次提示警告
            if st.session_state.blast_count >= 25:
                tab3.warning("已达到理论最大爆破次数（25次）！")


# ======================== 3. 随机数游戏功能模块 ========================
def game_menu_ui():
    """随机数游戏UI函数：展示抛瓶子/抛硬币/摇色子的界面和逻辑"""
    # 显示子标题
    st.subheader(f"{PROGRAM_NAME_ABBREVIATION} - 随机数游戏")
    # 添加水平分隔线
    st.divider()

    # 创建三个选项卡：对应三种游戏
    tab1, tab2, tab3 = st.tabs(["抛瓶子", "抛硬币", "摇色子"])

    # ======================== 抛瓶子游戏 ========================
    tab1.write("### 抛瓶子游戏")  # 子标题：三级标题，突出游戏名
    # 主色调抛瓶子按钮
    if tab1.button("抛瓶子", type="primary"):
        # 生成随机结果：8次失败+1次成功（模拟低概率成功）
        result = random.choice(['失败'] * 8 + ['成功'])
        # 自定义样式展示结果：黑色背景+居中+大字体
        tab1.markdown(f"""
        <div style="background-color:#000000;padding:20px;border-radius:10px;text-align:center;">
            <h2>结果：{result}</h2>
        </div>
        """, unsafe_allow_html=True)

    # ======================== 抛硬币游戏 ========================
    tab2.write("### 抛硬币游戏")
    # 主色调抛硬币按钮
    if tab2.button("抛硬币", type="primary"):
        # 生成随机结果：正/反（等概率）
        result = random.choice(['正', '反'])
        # 自定义样式展示结果
        tab2.markdown(f"""
        <div style="background-color:#000000;padding:20px;border-radius:10px;text-align:center;">
            <h2>结果：{result}</h2>
        </div>
        """, unsafe_allow_html=True)

    # ======================== 摇色子游戏 ========================
    tab3.write("### 摇色子游戏")
    # 主色调摇色子按钮
    if tab3.button("摇色子", type="primary"):
        # 生成随机结果：1-6（等概率）
        result = random.choice(['1', '2', '3', '4', '5', '6'])
        # 自定义样式展示结果
        tab3.markdown(f"""
        <div style="background-color:#000000;padding:20px;border-radius:10px;text-align:center;">
            <h2>结果：{result}</h2>
        </div>
        """, unsafe_allow_html=True)


# ======================== 4. 数学工具功能模块 ========================
def number_info_ui(parent):
    """
    N为何数功能：分析输入数字的属性（正负、奇偶、质数/合数等）
    :param parent: 父容器（标签页），用于将UI嵌入到指定位置
    """
    # 显示子标题
    parent.subheader("N为何数（分析有理数属性）")
    # 数字输入框：支持小数，步长0.1
    num_input = parent.number_input(
        "输入有理数",
        help="不建议输入单位超过百万的数，否则会产生卡顿",  # 性能提示
        value=0.0,  # 默认值
        step=0.1  # 步长
    )

    # 主色调分析按钮
    if parent.button("分析属性", type="primary"):
        # 将输入值赋值给变量n，简化后续调用
        n = num_input
        # 添加分隔线
        parent.divider()
        # 显示分析标题：当前输入的数字
        parent.write(f"### {n} 的属性：")

        # 判断正负性
        if n > 0:
            parent.write("是正数")
        elif n == 0:
            parent.write("不是正数也不是负数")
        else:
            parent.write("是负数")

        # 判断奇偶性+是否为整数
        if n % 1 == 0:  # 余数为0表示是整数
            n_int = int(n)  # 转换为整数类型
            if n_int % 2 == 0:
                parent.write("是偶数")
            else:
                parent.write("是奇数")
            parent.write("是整数")
        else:
            parent.write("是小数（分数），不是偶数也不是奇数")

        # 判断质数/合数（仅对大于1的整数生效）
        if n <= 1 or n % 1 != 0:
            parent.write("不是质数也不是合数")
        else:
            n_int = int(n)
            factor_count = 0  # 因数计数器
            # 遍历1到n_int，统计因数个数
            for x in range(1, n_int + 1):
                if n_int % x == 0:
                    factor_count += 1
            # 因数个数为2：质数（1和自身）
            if factor_count == 2:
                parent.write("是质数")
            # 因数个数大于2：合数
            elif factor_count > 2:
                parent.write("是合数")


def lcm_calculator_ui(parent):
    """
    最小公倍数计算器：计算多个整数的最小公倍数
    :param parent: 父容器（标签页）
    """
    # 显示子标题
    parent.subheader("最小公倍数计算器")
    # 文本输入框：输入逗号分隔的整数
    input_str = parent.text_input("请输入用逗号(英文逗号)分隔的整数", placeholder="如：2,3,4")

    # 主色调计算按钮
    if parent.button("计算最小公倍数", type="primary"):
        # 异常处理：防止输入非整数导致报错
        try:
            # 分割输入字符串，转换为整数列表（过滤空值）
            numbers = [int(num.strip()) for num in input_str.split(",") if num.strip()]
            # 无有效数字时提示错误
            if not numbers:
                parent.error("未输入任何数字！")
                return

            # 对数字排序，便于后续计算
            numbers_sorted = sorted(numbers)
            parent.write(f"输入数字排序：{numbers_sorted}")

            # 最小公倍数计算逻辑：从最大值开始，逐次+1，找到能被所有数整除的最小值
            max_num = numbers_sorted[-1]
            lcm = max_num
            while True:
                # 检查当前值是否能被所有数字整除
                if all(lcm % num == 0 for num in numbers):
                    break  # 找到最小公倍数，退出循环
                lcm += 1

            # 展示计算结果
            parent.success(f"{numbers} 的最小公倍数是：{lcm}")
        # 输入非整数时捕获异常，提示错误
        except ValueError:
            parent.error("输入无效！请输入整数并用英文逗号分隔！")


def common_factors_ui(parent):
    """
    两数公因数计算器：计算两个整数的所有公因数
    :param parent: 父容器（标签页）
    """
    # 显示子标题
    parent.subheader("两数公因数计算器")
    # 布局：两列输入两个整数
    col1, col2 = parent.columns(2)
    # 第一列：第一个整数输入框
    a = col1.number_input("输入第一个整数", step=1, value=0)
    # 第二列：第二个整数输入框
    b = col2.number_input("输入第二个整数", step=1, value=0)

    # 主色调计算按钮
    if parent.button("计算公因数", type="primary"):
        # 计算第一个数的所有因数：存入集合（自动去重）
        a_factors = set()
        for c in range(1, abs(a) + 1):
            if a % c == 0:
                a_factors.add(c)

        # 计算第二个数的所有因数
        b_factors = set()
        for c in range(1, abs(b) + 1):
            if b % c == 0:
                b_factors.add(c)

        # 求两个因数集合的交集（公因数），并排序
        common = sorted(a_factors.intersection(b_factors))

        # 展示结果：分别显示两个数的因数 + 公因数
        parent.write(f"{a} 的因数：{sorted(a_factors)}")
        parent.write(f"{b} 的因数：{sorted(b_factors)}")
        parent.success(f"{a} 和 {b} 的公因数：{common}")


def number_sort_ui(parent):
    """
    数字排序工具：将输入的整数按从小到大排序
    :param parent: 父容器（标签页）
    """
    # 显示子标题
    parent.subheader("数字排序工具")
    # 文本输入框：设置唯一key，避免冲突
    input_str = parent.text_input("请输入用逗号(英文逗号)分隔的整数", placeholder="如：5,2,8,1", key="sort_input")

    # 主色调排序按钮
    if parent.button("排序", type="primary"):
        # 异常处理：防止输入非整数
        try:
            # 分割输入字符串，转换为整数列表
            numbers = [int(num.strip()) for num in input_str.split(",") if num.strip()]
            # 无有效数字时提示错误
            if not numbers:
                parent.error("未输入任何数字！")
                return

            # 从小到大排序
            sorted_nums = sorted(numbers)
            # 展示原始数字和排序结果
            parent.write(f"输入数字：{numbers}")
            parent.success(f"从小到大排序：{sorted_nums}")
        except ValueError:
            parent.error("输入无效！请输入整数并用英文逗号分隔！")


def math_tools_menu_ui():
    """数学工具总UI函数：整合所有数学工具，展示到对应标签页"""
    # 显示子标题
    st.subheader(f"{PROGRAM_NAME_ABBREVIATION} - 数学工具")
    # 添加水平分隔线
    st.divider()

    # 创建四个选项卡：对应四个数学工具
    tab1, tab2, tab3, tab4 = st.tabs([
        "N为何数",
        "最小公倍数计算器",
        "两数公因数计算器",
        "数字排序工具"
    ])

    # 将每个工具嵌入到对应标签页（传入标签页作为父容器）
    number_info_ui(tab1)
    lcm_calculator_ui(tab2)
    common_factors_ui(tab3)
    number_sort_ui(tab4)


# ======================== 5. 优质网站收录功能模块 ========================
def web_menu_ui():
    """优质网站收录UI函数：展示各类实用网站的导航链接"""
    # 显示子标题
    st.subheader(f"{PROGRAM_NAME_ABBREVIATION} - 优质网站收录")
    # 添加水平分隔线
    st.divider()
    # 提示信息：说明页面用途
    st.info("提示，此页面为实用网站收录，仅作导航页使用。收录的网站并非 Vincent 所创建，使用时")
    # 添加水平分隔线
    st.divider()

    # 创建“娱乐”分类折叠面板：点击展开/收起
    play = st.expander("娱乐")
    # 超链接：格式为「链接名：[显示文本](链接地址)」
    play.markdown("免费电影：[69美剧](https://69mj.com/)")
    play.markdown("emoji混合：[emojimix](https://tikolu.net/emojimix/)")
    play.markdown(
        "在线钢琴：[自由钢琴-AutoPiano|在线钢琴，键盘钢琴，模拟钢琴，多种乐器选择，好听又好玩](https://www.autopiano.cn/)")

    # 创建“工具”分类折叠面板
    tools = st.expander("工具")
    tools.markdown(
        "音乐LRC文件下载：[Music Lyrics LRC files Download](https://www.megalobiz.com/lrc/maker/download-music-lyrics-lrc-generated-files)")
    tools.markdown(
        "加解密网页小工具：[RSA加密/解密工具 - 在线RSA加密解密等五种使用场景](https://try8.cn/tool/cipher/rsa)")
    tools.markdown("免费心理测试网站：[赛可心理测试](https://m.psyctest.cn/)")
    tools.markdown("在线ps：[ps photoshop editor - photoshop image editor](https://ps.ittools.cc/editor/)")
    tools.markdown("新闻地图：[China Interactive News Map -china.liveuamap.com](https://china.liveuamap.com/)")
    tools.markdown("时光邮局：[时光邮局-给未来的自己写一封信](https://www.hi2future.com/)")

    # 直接展示菜鸟教程链接（无折叠面板）
    st.markdown("菜鸟教程：[菜鸟教程 - 学的不仅是技术，更是梦想！](https://www.runoob.com/)")
    # 预留空链接行：便于后续扩展
    st.markdown("：[]()")


# ======================== 主页面/导航模块 ========================
def main_ui():
    """程序主UI函数：负责侧边栏导航、功能切换、首页展示"""
    # 侧边栏：显示导航标题
    st.sidebar.header("功能导航")
    # 侧边栏：创建单选框，选择功能模块
    menu_choice = st.sidebar.radio(
        "请选择功能模块",  # 单选框提示文本
        [
            "HELLOTAG",  # 首页
            "随机数游戏",  # 随机数游戏功能
            "凯撒密码加解密",  # 凯撒密码功能
            "BMI计算器",  # BMI计算器功能
            "数学工具",  # 数学工具功能
            "优质网站收录"  # 网站收录功能
        ]
    )
    # 侧边栏：添加水平分隔线
    st.sidebar.divider()
    # 侧边栏：功能说明，帮助用户了解各模块作用
    st.sidebar.write(
        "功能说明：\n- 随机数游戏：抛瓶子/抛硬币/摇色子\n- 凯撒密码：加解密+爆破功能\n- BMI计算器：计算身体质量指数\n- 数学工具：因数/公倍数/排序等")

    # 根据侧边栏选择，展示对应功能
    if menu_choice == "随机数游戏":
        game_menu_ui()  # 调用随机数游戏UI函数
    elif menu_choice == "凯撒密码加解密":
        caesar_menu_ui()  # 调用凯撒密码UI函数
    elif menu_choice == "BMI计算器":
        bmi_calculator_ui()  # 调用BMI计算器UI函数
    elif menu_choice == "数学工具":
        math_tools_menu_ui()  # 调用数学工具UI函数
    elif menu_choice == "优质网站收录":
        web_menu_ui()  # 调用网站收录UI函数
    else:  # 默认选择HELLOTAG，展示首页
        # 显示程序标题：全称 + 版本号
        st.title(f"{PROGRAM_NAME} {PROGRAM_VERSION}")
        # 添加水平分隔线
        st.divider()
        # 显示首页子标题
        st.subheader("HELLOTAG")
        # 展示程序信息：版本、功能、开发者、技术栈
        st.write(f"版本：{PROGRAM_VERSION}")
        st.write("包含功能：随机数游戏、凯撒密码加解密、BMI计算器、数学工具")
        st.write("开发者：Vincent")
        st.write("基于 Python,Streamlit 构建的网页版工具集")
        # 添加水平分隔线
        st.divider()
        # 零时标注：展示项目说明
        little_tag = ["零时标注：",
                      "此项目不仅仅是一个比赛作品，而是一个希望能服务大众的工具。按计划将来 Vincent 会继续优化它"]
        text = ""  # 初始化标注文本
        # 拼接标注文本为列表格式
        for reason in little_tag:
            text += f"- {reason}\n"
        # 用警告框展示标注文本（黄色背景，醒目）
        st.warning(text)


# ======================== 程序入口 ========================
# 判断是否为主程序运行（而非被导入为模块）
if __name__ == "__main__":
    # 调用主UI函数，启动程序
    main_ui()
