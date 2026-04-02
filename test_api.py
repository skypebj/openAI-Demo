import os
from datetime import datetime
from openai import OpenAI

# ===================== DEBUG 输出开关 =====================
DEBUG = True

def debug_print(msg):
    if DEBUG:
        print(f"[DEBUG] {msg}")

# ===================== 初始化 AI 客户端 =====================
debug_print("=== 开始初始化 OpenAI 客户端 ===")
api_key = os.environ.get("OPENAI_API_KEY")
api_base = os.environ.get("OPENAI_API_BASE")
model = os.environ.get("OPENAI_MODEL")

debug_print(f"API_KEY: {'已配置' if api_key else '缺失'}")
debug_print(f"API_BASE: {'已配置' if api_base else '缺失'}")
debug_print(f"MODEL: {model if model else '未配置'}")

if not api_key or not api_base or not model:
    debug_print("错误：环境变量缺失")
    exit(1)

client = OpenAI(api_key=api_key, base_url=api_base)
debug_print("=== 客户端初始化完成 ===")

# ===================== 生成唯一文件名 =====================
def get_unique_filename():
    debug_print("生成文件名...")
    date_str = datetime.now().strftime("%y%m%d")
    index = 1
    while True:
        filename = f"{date_str}-{index}.txt"
        if not os.path.exists(filename):
            debug_print(f"使用文件名：{filename}")
            return filename
        debug_print(f"{filename} 已存在，序号+1")
        index += 1

# ===================== 生成早报（你的完整提示词） =====================
def generate_morning_report():
    debug_print("===== 开始生成早报 =====")

    prompt = """请为我整理一份早报，内容专业、客观、简洁，重点突出，结构清晰
第一部分、投资金融领域
要求内容专业、客观、简洁，重点突出，结构清晰，覆盖以下内容：
全球宏观要闻：隔夜国际重要经济数据、央行政策动向、地缘政治对资本市场的影响。
美股及海外市场：隔夜美股三大指数表现、热门板块、重要中概股走势、欧洲 / 亚太主要市场概况。
A 股市场前瞻：昨日 A 股收盘总结、北向资金流向、龙虎榜要点、今日潜在影响市场的重要事件与数据。
新闻联播摘要：最新新闻联播咨询，政策、产业政策、涉及的行业以及企业，重要事件。
行业与板块机会：重点关注金融、消费、科技、新能源、医药、周期等板块的最新政策、产业动态、催化事件。
债券、汇率、大宗商品：美债收益率、人民币汇率、原油、黄金、有色金属等关键品种简要走势。
重要公告与监管动态：证监会、交易所、重要公司业绩预告 / 公告、退市与 IPO 相关信息。
投资策略简要提示：当日市场情绪判断、风险点、值得跟踪的方向，不构成具体买卖建议。
要求：逻辑清晰、数据准确、无冗余内容，适合长期投资者与趋势交易者阅读。

第二部分、泛知识综合新闻
内容覆盖广泛但不杂乱，重点选取有长期价值、认知增量的信息，包括：
国内要闻：重要政策、产业趋势、科技进展、民生与社会热点。
国际动态：全球政治经济、科技竞争、国际合作与重大事件。
科技前沿：人工智能、半导体、新能源、生物医药、航天航空等领域突破。
商业与产业：巨头动态、商业模式创新、行业格局变化。
文化、社会、科普：有价值的社会观察、科普知识、历史文化、健康常识。
会议：国内重要政治、经济会议。
要求：客观中立、信息密度高，适合提升认知，避免娱乐化碎片化内容。"""

    try:
        debug_print("调用 AI 生成...")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            timeout=180
        )

        content = response.choices[0].message.content
        if not content or len(content) < 50:
            debug_print("错误：内容过短")
            return False

        debug_print(f"生成完成，长度：{len(content)} 字符")
        filename = get_unique_filename()

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
            f.flush()

        debug_print(f"文件保存成功：{filename}")
        print(f"✅ 早报生成完成：{filename}")
        return True

    except Exception as e:
        debug_print(f"异常：{str(e)}")
        return False

# ===================== 运行 =====================
if __name__ == "__main__":
    generate_morning_report()
