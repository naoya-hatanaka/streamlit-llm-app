from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os

# アプリの概要・操作説明
st.title("LLM専門家相談アプリ")
st.markdown("""
このアプリは、LLM（大規模言語モデル）に健康の専門家として質問できるWebアプリです。\
下記の手順でご利用ください：

1. 専門家の種類（睡眠 or 運動）を選択
2. 質問内容を入力
3. 送信ボタンを押すと、専門家としてLLMが回答します
""")

# 専門家の選択
expert = st.radio(
	"相談したい専門家を選んでください",
	("睡眠の専門家", "運動の専門家")
)

# 入力フォーム
user_input = st.text_area("質問内容を入力してください", height=100)

# LLM応答関数
def get_llm_response(input_text: str, expert_type: str) -> str:
	if expert_type == "睡眠の専門家":
		system_prompt = "あなたは睡眠の専門家です。健康になるための睡眠について、わかりやすく丁寧にアドバイスしてください。"
	else:
		system_prompt = "あなたは運動の専門家です。健康になるための運動について、わかりやすく丁寧にアドバイスしてください。"

	# OpenAI APIキーは環境変数から取得
	openai_api_key = os.getenv("OPENAI_API_KEY")
	if not openai_api_key:
		return "OpenAI APIキーが設定されていません。"

	llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.7, model_name="gpt-3.5-turbo")
	messages = [
		SystemMessage(content=system_prompt),
		HumanMessage(content=input_text)
	]
	try:
		response = llm(messages)
		return response.content
	except Exception as e:
		return f"エラーが発生しました: {e}"

# 送信ボタン
if st.button("送信"):
	if not user_input.strip():
		st.warning("質問内容を入力してください。")
	else:
		with st.spinner("LLMが回答中..."):
			answer = get_llm_response(user_input, expert)
		st.markdown("#### 回答")
		st.write(answer)