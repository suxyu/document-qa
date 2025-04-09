# import streamlit as st
# from openai import OpenAI

# # Show title and description.
# st.title("📄 Document question answering")
# st.write(
#     "Upload a document below and ask a question about it – GPT will answer! "
#     "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
# )

# # Ask user for their OpenAI API key via `st.text_input`.
# # Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# # via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
# openai_api_key = st.text_input("OpenAI API Key", type="password")
# if not openai_api_key:
#     st.info("Please add your OpenAI API key to continue.", icon="🗝️")
# else:

#     # Create an OpenAI client.
#     client = OpenAI(api_key=openai_api_key)

#     # Let the user upload a file via `st.file_uploader`.
#     uploaded_file = st.file_uploader(
#         "Upload a document (.txt or .md)", type=("txt", "md")
#     )

#     # Ask the user for a question via `st.text_area`.
#     question = st.text_area(
#         "Now ask a question about the document!",
#         placeholder="Can you give me a short summary?",
#         disabled=not uploaded_file,
#     )

#     if uploaded_file and question:

#         # Process the uploaded file and question.
#         document = uploaded_file.read().decode()
#         messages = [
#             {
#                 "role": "user",
#                 "content": f"Here's a document: {document} \n\n---\n\n {question}",
#             }
#         ]

#         # Generate an answer using the OpenAI API.
#         stream = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=messages,
#             stream=True,
#         )

#         # Stream the response to the app using `st.write_stream`.
#         st.write_stream(stream)


import streamlit as st
from mood_llm import get_prompts
from openai import OpenAI
import time
from mood_llm import generate_custom_file_path
from mood_llm import get_file_paths
from mood_llm import extract_number_from_file_path
from mood_llm import get_final_prompt
import os

# 配置OpenAI客户端
client = OpenAI(base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", api_key="sk-86a9b469ca3447e3ab60f6858591e7bf", timeout=100)


# 默认的任务prompt
default_prompt = "请根据给定的关键词生成相应的任务"

# 页面标题
st.title("舆情分析POC")

# 选择关键词
keyword = st.selectbox("选择一个需要舆情分析的对象", ["杭州卷烟厂","烟草",  "香烟", "浙江中烟"])

# 默认任务prompt
default_prompt = """默认的任务：找出所有直接针对 {keyword} 的负面 或者 正面的帖子或者评论,
只是相关不算直接针对。按照 转发数+评论数+点赞数总和  或者 影响数 排序，
并且按照负面和正面排序。最后基于这些 {keyword} 的相关的帖子和评论，
写一个综述，概括大众对于 {keyword} 的印象，舆论："""

# 显示默认任务prompt，浅灰色
st.markdown(f'<p style="color:grey;">{default_prompt.format(keyword=keyword)}</p>', unsafe_allow_html=True)

# 用户输入自定义任务
user_prompt = st.text_area("如果你对于默认的任务不满意，可以输入自定义任务：", default_prompt.format(keyword=keyword), height=200)


# 创建一个按钮，用户点击后确认输入
if st.button("确认"):
    # 如果用户输入了自定义任务，则覆盖默认任务
    final_prompt = user_prompt if user_prompt != default_prompt.format(keyword=keyword) else default_prompt.format(keyword=keyword)



    # # 用户输入自定义任务prompt
    # user_prompt = st.text_area("输入自定义任务", "", help="如果不输入，自定义任务将会覆盖默认任务")

    # # 判断是否有自定义任务
    # final_prompt = user_prompt if user_prompt else default_prompt

    # 显示当前选择的任务prompt
    #st.write(f"最终任务提示: {final_prompt}")

    # 流式输出结果
    #st.write("正在生成任务...")
    # 这里你可以调用你的算法逻辑处理`keyword`和`final_prompt`，然后输出结果
    st.write(f"最终任务：{final_prompt} \n\n\n 针对关键词: {keyword} 的生成结果：")
    print("final_prompt:",final_prompt)
    print("keyword:",keyword)

    prompts = get_prompts(final_prompt,keyword)

    page_no =0
    for prompt in prompts:
        page_no +=1
        messages = [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(
            model="deepseek-r1-distill-qwen-32b",
            messages=messages,
            stream=True
        )

        # 初始化Streamlit的流式输出
        #st.title("正在生成结果...")
        response_placeholder = st.empty()  # 用于实时输出结果

        # 初始化变量
        reasoning_content = ""
        content = ""
        with st.spinner(f"正在筛选微博搜索 {keyword} 第{page_no}页 的相关内容..."):
            with st.empty():
                #st.write(f"正在筛选微博搜索 {keyword} 第{page_no}页 的相关内容...")
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

        st.empty()  # 清除之前的输出





            
        files_paths = get_file_paths(keyword)
        file_path = files_paths[0]
        p = extract_number_from_file_path(file_path)
        file_path = generate_custom_file_path(file_path, f"temp_{keyword}_{p}.txt")

        with open(file_path, 'w', encoding='utf-8') as temp_file:
            temp_file.write(content)


    final_prompt_full = get_final_prompt(final_prompt, keyword,pages="all",time_range="all")

    
    # 创建消息结构
    messages = [{"role": "user", "content": final_prompt_full}]

    # 进行OpenAI API请求并开启流式输出
    response = client.chat.completions.create(
        model="deepseek-r1-distill-qwen-32b",
        messages=messages,
        stream=True
    )

    # 初始化Streamlit的流式输出
    st.title("信息筛选完成，综合分析全部相关信息的最终结果：")
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


    filtered_file_path = files_paths[0]
    print(filtered_file_path)
    def get_folder_path(file_path):
        """
        从文件路径中提取所在文件夹的相对路径。
        
        :param file_path: str, 文件的相对路径或绝对路径
        :return: str, 文件夹的相对路径
        """
        return os.path.dirname(file_path)
    
    folder_path = get_folder_path(filtered_file_path)
    print("folder_path:",folder_path)
    temp_full_file_path = os.path.join("data", keyword, f"temp_{keyword}_full.txt")
    print("temp_full_file_path:", temp_full_file_path)
    
    if os.path.exists(temp_full_file_path):
        with open(temp_full_file_path, 'r', encoding='utf-8') as file:
            full_content = file.read()
            print("full_content:",full_content)
            st.markdown(f"<h2>相关的微博帖子原文：</h2>\n{full_content}", unsafe_allow_html=True)
    else:
        st.error("未找到文件 temp_{keyword}_full.txt")


    



