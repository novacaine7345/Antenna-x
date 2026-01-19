import streamlit as st
import requests
import vswr_gpr_model 
import s11_gpr_model 
import re

previous_msg_value = 0 
OLLAMA_API_URL = "http://localhost:11434/api/chat"  # default Ollama endpoint
st.set_page_config(page_title="Antenna-X", page_icon="", layout="centered")
st.title("Antenna Estimation Chatbot")
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your local AI-powered MSPA estimation assistant. How can I help?"}
    ]
    
st.sidebar.header("Model Settings")
model_name = st.sidebar.text_input("Model name", value="granite4:micro", help="Must be an installed Ollama model.")
temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.7, 0.1)
top_p = st.sidebar.slider("top_p", 0.0, 1.0, 0.9, 0.05)
max_tokens = st.sidebar.number_input("Max tokens (0 = default)", min_value=0, value=0, step=16)
# system_prompt = st.sidebar.text_area(
#     "System prompt (optional)",
#     value="You are a helpful assistant.",
#     help="Sent as a system message at the start of the conversation."
# )

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    # if system_prompt.strip():
    #     st.session_state.messages.append({"role": "system", "content": system_prompt.strip()})
    # st.rerun()
    
#if system_prompt.strip():
    # has_system = any(m["role"] == "system" for m in st.session_state.messages)
    # if not has_system:
    #     st.session_state.messages.insert(0, {"role": "system", "content": system_prompt.strip()})
        
def call_ollama_chat(messages):
    payload = {
        "model": model_name,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
            "top_p": top_p,
        },
    }
    
    if max_tokens > 0:
        payload["options"]["num_predict"] = int(max_tokens)
    try:
        resp = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        return f"Error contacting Ollama API: {e}"
    msg = data.get("message", {})
    content = msg.get("content", "")
    
    if not content:
        return "No content returned from Ollama."
    return content

for m in st.session_state.messages:
    if m["role"] == "system":
        continue
    with st.chat_message("assistant" if m["role"] == "assistant" else "user"):
        st.markdown(m["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    if "vswr" in user_input.lower():
        match = re.search(r"(\d+(\.\d+)?)", user_input)
        if match:
            freq = float(match.group(1)) 
        else:
            freq = None
            
        if freq is None:
            reply = "I could not find a frequency in your request. Please specify, e.g., 'Predict VSWR at 12.5 GHz'."
        else:

            vswr_mean, vswr_std = vswr_gpr_model.predict_vswr(freq)
            context_text = (
                f"The GPR model prediction for VSWR at {freq:.3f} GHz is "
                f"{vswr_mean:.3f} dB with a standard deviation of {vswr_std:.3f} dB."
            )
            llm_messages = st.session_state.messages + [
                {"role": "assistant", "content": context_text},
                {"role": "user", "content": "Explain what this VSWR result means for my antenna performance."}
            ]
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    explanation = call_ollama_chat(llm_messages)
                    # Combine numeric result + explanation
                    reply = context_text + "\n\n" + explanation
                    st.markdown(reply)
    elif "s11" in user_input.lower():
        match = re.search(r"(\d+(\.\d+)?)", user_input)
        if match:
            freq = float(match.group(1))
        else:
            freq = None
            
        if freq is None:
            reply = "I could not find a frequency in your request. Please specify, e.g., 'Predict VSWR at 12.5 GHz'."
        else:
            s11_mean, s11_std = s11_gpr_model.predict_s11(freq)
            context_text = (
                f"The GPR model prediction for sw11 at {freq:.3f} GHz is "
                f"{s11_mean:.3f} dB with a standard deviation of {s11_std:.3f} dB."
            )
            llm_messages = st.session_state.messages + [
                {"role": "assistant", "content": context_text},
                {"role": "user", "content": "Explain what this s11 result means for my antenna performance."}
            ]
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    explanation = call_ollama_chat(llm_messages)
                    reply = context_text + "\n\n" + explanation
                    st.markdown(reply)
    elif ("vswr" and "s11") in user_input.lower():
        match = re.search(r"(\d+(\.\d+)?)", user_input)
        if match:
            freq = float(match.group(1)) 
        else:
            freq = None
            
        if freq is None:
            reply = "I could not find a frequency in your request. Please specify, e.g., 'Predict VSWR at 12.5 GHz'."
        else:

            vswr_mean, vswr_std = vswr_gpr_model.predict_vswr(freq)
            s11_mean, s11_std = s11_gpr_model.predict_s11(freq)
            context_text = (
                f"The GPR model prediction for VSWR at {freq:.3f} GHz is "
                f"{vswr_mean:.3f} dB with a standard deviation of {vswr_std:.3f} dB."
                f"The GPR model prediction for s11 at {freq:.3f} GHz is "
                f"{s11_mean:.3f} dB with a standard deviation of {s11_std:.3f} dB."
            )
            llm_messages = st.session_state.messages + [
                {"role": "assistant", "content": context_text},
                {"role": "user", "content": "Explain what this VSWR and s11 result means for my antenna performance and explain within 1 paragraph without stating how good the performance is"}
            ]
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    explanation = call_ollama_chat(llm_messages)
                    # Combine numeric result + explanation
                    reply = context_text + "\n\n" + explanation
                    st.markdown(reply)
    
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = call_ollama_chat(st.session_state.messages)
                st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})           


