import streamlit as st
from openai import OpenAI
import time


# 配置OpenAI客户端
client = OpenAI(base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", api_key="sk-86a9b469ca3447e3ab60f6858591e7bf", timeout=100)

# 默认帖子内容
content = """
#帖子：
[#北大港大毕业生卷完学历卷烟厂#]【[#烟厂一线员工谈学历浪费#]：工资并没有网上传得那么高】近日，多地烟草公司发布了2024年大学生招聘拟录用名单。九派新闻梳理发现，多家烟草企业都进行了扩招，例如河南中烟的“一线生产操作岗”招聘了169人，较2023年增加53人。并且，越来越多的名校生、硕博生涌入烟厂 包括一线生产操作岗 浙江中烟杭州、宁波两地的生产技术操作岗拟录取了123人，其中不乏来自北京大学、香港大学、悉尼大学等国内外名校毕业生；济南卷烟厂招聘95名应届生，包括3名博士研究生。管理岗和一线操作岗有明显工资差异吗？名校生是否更容易入职管理岗？1月7日，湖北某烟厂的一线员工告诉九派新闻，他们厂2024年招聘的学历要求从专科提高到了本科，“管理岗的学历要求更高一些，操作岗只要求本科，但进厂后操作岗人员也有晋升管理岗的通道。”至于名校生是否更容易入职管理岗，他表示，这是报考阶段的选择，只要通过网申，后续不论学历，只看笔试、面试成绩。蚌埠卷烟厂2024年的招录名单也显示，有浙大的硕士被录到设备维修岗，也有双非院校的学生被录到管理技术岗位，营销岗位则录用了2名动画、戏剧专业的硕士，报考时的选岗十分重要。该员工还称，近几年烟厂招聘都是根据各部门缺员人数进行招聘，数量确实比之前多一点，“近期招聘的员工还有武汉大学毕业的，公司在高质效发展，职工素质能力在提高，这是令人高兴的事”。[@九派新闻] [九派新闻的微博视频]
影响总数：12
"""

# 生成的 prompt
prompt = f"""
仔细浏览下面微博帖子和对应的评论：
{content}

找出所有直接针对 “杭州卷烟厂” 的负面 或者 正面的帖子或者评论, 只是相关不算直接针对。按照 转发数+评论数+点赞数总和  或者 影响数 排序，并且按照负面和正面排序。 最后基于这些杭州卷烟厂的相关的帖子和评论，写一个综述，概括大众对于杭州卷烟厂的印象，舆论：
"""

# 创建消息结构
messages = [{"role": "user", "content": prompt}]

# 进行OpenAI API请求并开启流式输出
response = client.chat.completions.create(
    model="deepseek-r1-distill-qwen-32b",
    messages=messages,
    stream=True
)

# 初始化Streamlit的流式输出
st.title("流式输出演示")
response_placeholder = st.empty()  # 用于实时输出结果

# 初始化变量
reasoning_content = ""
content = ""

with st.empty():
    # 流式输出部分
    for chunk in response:
        # 处理推理内容
        if chunk.choices[0].delta.reasoning_content:
            reasoning_content += chunk.choices[0].delta.reasoning_content
            response_placeholder.markdown(f"**推理过程：**\n{reasoning_content}")
        
        # 处理生成内容
        if chunk.choices[0].delta.content:
            content += chunk.choices[0].delta.content
            response_placeholder.markdown(f"**生成内容：**\n{content}")

        time.sleep(0.1)

response_placeholder.empty()  # 用于实时输出结果

# 当推理内容流式输出完成后，停留在页面上
if reasoning_content:
    st.markdown(f"**最终推理过程：**\n{reasoning_content}")

# 当生成内容流式输出完成后，停留在页面上
if content:
    st.markdown(f"**最终生成内容：**\n{content}")