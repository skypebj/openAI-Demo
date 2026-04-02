import os
from datetime import datetime
from openai import OpenAI

# ==============================================
# DEBUG 模式：开启详细日志（全程打印执行步骤）
# ==============================================
DEBUG = True

def debug_print(msg):
    if DEBUG:
        print(f"[DEBUG] {msg}")

# ====================== 初始化客户端 ======================
debug_print("开始初始化 OpenAI 客户端")
debug_print(f"从环境变量读取 API_KEY: {'已配置' if os.environ.get('OPENAI_API_KEY') else '缺失'}")
debug_print(f"从环境变量读取 API_BASE: {'已配置' if os.environ.get('OPENAI_API_BASE') else '缺失'}")
debug_print(f"从环境变量读取 MODEL: {os.environ.get('OPENAI_MODEL')}")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE")
)
debug_print("OpenAI 客户端初始化完成")

# ====================== 生成唯一文件名 ======================
def get_unique_filename():
    debug_print("进入文件名生成函数")
    
    date_str = datetime.now().strftime("%y%m%d")
    debug_print(f"当前日期格式化为: {date_str}")
    
    index = 1
    debug_print(f"初始文件序号: {index}")
    
    while True:
        filename = f"{date_str}-{index}.txt"
        debug_print(f"检查文件是否存在: {filename}")
        
        if not os.path.exists(filename):
            debug_print(f"文件不存在，使用该文件名: {filename}")
            return filename
        
        debug_print(f"文件已存在，序号+1: {index} -> {index+1}")
        index += 1

# ====================== 生成并保存早报 ======================
def generate_morning_report():
    debug_print("===== 进入早报生成主函数 =====")
    
    # 最新提示词（你提供的完整版）
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
科学研究：预印本头条、重大科技突破。
商业与产业：巨头动态、商业模式创新、行业格局变化。
文化、社会、科普：有价值的社会观察、科普知识、历史文化、健康常识。
会议：国内重要政治、经济会议。
要求：客观中立、信息密度高，适合提升认知，避免娱乐化碎片化内容。"""

    debug_print("提示词加载完成，长度：%d 字符" % len(prompt))

    try:
        debug_print("开始调用 AI 接口生成内容")
        debug_print(f"使用模型: {os.environ.get('OPENAI_MODEL')}")
        
        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL"),
            messages=[{"role": "user", "content": prompt}]
        )
        debug_print("AI 接口调用成功，开始解析返回结果")

        # 解析内容
        content = response.choices[0].message.content
        debug_print(f"AI 返回内容长度: {len(content)} 字符")
        debug_print(f"返回内容预览: {content[:80]}...")

        # 生成文件名
        filename = get_unique_filename()
        debug_print(f"最终确定保存文件名: {filename}")

        # 写入文件
        debug_print("开始打开文件并写入内容")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        debug_print("文件写入完成，关闭文件")

        debug_print("===== 全部流程执行成功 =====")
        print(f"\n✅ 早报生成完成：{filename}")

    except Exception as e:
        debug_print(f"捕获异常: {type(e).__name__}")
        debug_print(f"异常详情: {str(e)}")
        print(f"\n❌ 执行失败：{e}")

# ====================== 运行 ======================
if __name__ == "__main__":
    debug_print("程序启动，进入主执行入口")
    generate_morning_report()
    debug_print("程序结束")
