import streamlit as st
import openai

class MultiApp:
    def __init__(self):
        self.apps = []
        self.app_dict = {}

    def add_app(self, title, func):
        if title not in self.apps:
            self.apps.append(title)
            self.app_dict[title] = func

    def run(self):
        title = st.sidebar.radio(
            '请选择',
            self.apps,
            format_func=lambda title: str(title))
        self.app_dict[title]()

def get_key():
    st.title("艾玛 & ChatGPT")
    st.header("ChatGPT API Key")
    mykey = st.text_input("请输入你的API Key",placeholder ="sk-")
    st.session_state.api_key = mykey
    return

def chatgpt(message,max_tokens=100,temperature=0):
    rsp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        max_tokens=max_tokens,
        temperature = temperature
    )
    return rsp.get("choices")[0]["message"]["content"]

@st.cache_data
def get_info(pname,message):
    msg = "%s是哪个国家哪个年代的人,他的生卒时间"%(pname)
    message.append({"role":"user","content":msg})
    res1=chatgpt(message,max_tokens=100,temperature=0)
    message.append({"role":"assistant","content":res1})
    msg = "简单介绍一下这个人物的生平)"
    message.append({"role":"user","content":msg})
    res2=chatgpt(message,max_tokens=500,temperature=0)
    return res1,res2
    

@st.cache_data
def get_more(people,message):
    msg = "与%s同时代的名人有哪些"%(people)
    message.append({"role":"user","content":msg})
    res1=chatgpt(message,max_tokens=200,temperature=0)
    message.append({"role":"assistant","content":res1})
    msg = "%s出现在哪些影视作品中"%(people)
    message.append({"role":"user","content":msg})
    res2=chatgpt(message,max_tokens=500,temperature=0)
    return res1,res2

@st.cache_data
def get_emotion(ques,state,message):
    msg = "我遇到了一个问题:%s,我的当前心情是%s,请对这种情况做个简单的分析"%(ques,state)
    message.append({"role":"user","content":msg})
    res1=chatgpt(message,max_tokens=300,temperature=0.8)
    message.append({"role":"assistant","content":res1})
    msg = "就前面的问题,请给出几条建议(每条建议不超过100个汉字)"
    message.append({"role":"user","content":msg})
    res2=chatgpt(message,max_tokens=800,temperature=0.8)
    return res1,res2

def info_click():
    st.session_state.click_start = True

def more_click():
    st.session_state.click_more = True

def emo_analyze():
    st.session_state.emo_analyze = True


def people():
    st.title("艾玛 & ChatGPT")
    st.header("历史人物")
    if 'api_key' not in st.session_state or not st.session_state.api_key:
        st.write("请先输入你的chatGPT API Key")
        return
    else:
        openai.api_key = st.session_state.api_key

    message  = [{"role":"system","content":"历史学家"}]
    st.subheader("你想了解谁")
    pname  = st.text_input("",placeholder ="在此输入姓名")

    if 'click_start' not in st.session_state:
        st.session_state.click_start = False 

    if 'click_more' not in st.session_state:
        st.session_state.click_more = False 
    
    st.button("开始吧",on_click=info_click)
    if  st.session_state.click_start:
        if not pname:
            st.write("请首先输入人物姓名")
            return
        rtn = get_info(pname,message)
        st.write(rtn[0])
        st.write("%s的生平简介"%(pname))
        st.write(rtn[1])

        st.button("了解更多",on_click=more_click)
        if st.session_state.click_more:
            message.pop()
            rtn = get_more(pname,message)
            st.write("同时代名人")
            st.write(rtn[0])
            st.write("相关影视作品")
            st.write(rtn[1])    
    return

def emotion():
    st.title("艾玛 & ChatGPT")
    st.header("情绪支持")
    if 'api_key' not in st.session_state or not st.session_state.api_key:
        st.write("请先输入你的chatGPT API Key")
        return
    else:
        openai.api_key = st.session_state.api_key

    ques = st.text_input("你遇到了什么问题:",placeholder="请输入问题")
    state = st.text_input("你当前的心情状态是:",placeholder="请输入心情")

    if 'emo_analyze' not in st.session_state:
        st.session_state.emo_analyze = False
    
    if st.button("开始分析"):
        if not ques or not state:
            st.write("请首先输入问题")
            return
        message  = [{"role":"system","content":"心理治疗师"}]
        rtn = get_emotion(ques,state,message)
        st.write(rtn[0])
        st.write("下面是一些简单建议：")
        st.write(rtn[1])
    return

def story():
    st.title("艾玛 & ChatGPT")    
    st.header("故事大王")
    if 'api_key' not in st.session_state or not st.session_state.api_key:
        st.write("请先输入你的chatGPT API Key")
        return
    else:
        openai.api_key = st.session_state.api_key
    return

app = MultiApp()
app.add_app("API Key", get_key)
app.add_app("历史人物", people)
app.add_app("情绪支持", emotion)
app.add_app("故事大王", story)
app.run()