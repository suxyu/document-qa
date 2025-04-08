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

# 默认的任务prompt
default_prompt = "请根据给定的关键词生成相应的任务"

# 页面标题
st.title("舆情分析POC")

# 选择关键词
keyword = st.selectbox("选择一个需要舆情分析的对象", ["杭州卷烟厂","烟草", "烟草行业", "香烟", "浙江中烟"])

# 默认任务prompt
default_prompt = """默认的任务：找出所有直接针对 {keyword} 的负面 或者 正面的帖子或者评论,
只是相关不算直接针对。按照 转发数+评论数+点赞数总和  或者 影响数 排序，
并且按照负面和正面排序。最后基于这些 {keyword} 的相关的帖子和评论，
写一个综述，概括大众对于 {keyword} 的印象，舆论："""

# 显示默认任务prompt，浅灰色
st.markdown(f'<p style="color:grey;">{default_prompt.format(keyword=keyword)}</p>', unsafe_allow_html=True)

# 用户输入自定义任务
user_prompt = st.text_area("如果你对于默认的任务不满意，可以输入自定义任务：", default_prompt.format(keyword=keyword), height=200)

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


