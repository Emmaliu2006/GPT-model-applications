import streamlit as st
import openai
import base64

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
    st.title("Emma & ChatGPT")
    st.header("ChatGPT API Key")
    mykey = st.text_input("请输入你的API Key",placeholder ="sk-")
    st.session_state.api_key = mykey
    ss = st.slider("剧情",0,1,0.6)
    st.write(ss)
    expand = st.expander("� 不知道什么是API Key")
    expand.write('''
    1. OpenAI给用户提供API接口，用户可以在自己或者第三方程序中调用这些接口跟ChatGPT进行交互。\n
    2. 通过不同的API Key来识别用户，以确定本次API接口调用来自哪个用户。\n
    3. 用户需要自行到OpenAI的官网(https://openai.com)上申请自己的API Key，一个用户可以申请多个API Key，并可以随时销毁。\n
    4. 使用ChatGPT的API接口将产生费用，费用与API接口调用使用的token(字数)数量相关。\n
    5. API Key与用户关联，相当于用户使用API接口的密码，请妥善使用和保管，切勿泄露给他人。
    6. 按照OpenAI的使用规则，API key仅限用户自己使用，不得公开共享或与他人共用。''')
    return

@st.cache_data
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

def story():
    st.session_state.story = True


def people():
    st.title("Emma & ChatGPT")
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
    st.title("Emma & ChatGPT")
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


def get_story():
    st.session_state.story=True

def story():
    st.title("Emma & ChatGPT")    
    st.header("故事大王")
    message  = [{"role":"system","content":"作家"}]

    if 'api_key' not in st.session_state or not st.session_state.api_key:
        st.write("请先输入你的chatGPT API Key")
        return
    else:
        openai.api_key = st.session_state.api_key
    tips = {'中文': {'title': "欢迎来到艾玛的故事会",'lang': "请选择语言种类:",'length': "请输入故事长度",'type': "您想听什么类型的故事?",'char': "故事有哪些角色?",'la': "故事发生在什么地方?",'end': "您想要什么样的故事结局?",'btn': "生成故事"},
    'English': {'title': "Welcome to Emma's Story Club:",'lang': "Please select language",'length': "Please enter the length of the story",'type': "What type of story do you want to hear?",'char': "What are the characters in the story?",'la': "Where does the story take place?",'end': "What kind of story ending do you want?",'btn': "Generate story"},
    '日本語': {'title': "エマの物語クラブへようこそ:",'lang': "言語を選択してください",'length': "物語の長さを入力してください",'type': "どのような種類の物語を聞きたいですか？",'char': "物語のキャラクターは何ですか？",'la': "物語はどこで起こりますか？",'end': "どのような物語の結末が欲しいですか？",'btn': "物語を生成する"},
    'Français': {'title': "Bienvenue au club d'histoires d'Emma:",'lang': "Veuillez sélectionner la langue",'length': "Veuillez saisir la longueur de l'histoire",'type': "Quel type d'histoire voulez-vous entendre?",'char': "Quels sont les personnages de l'histoire?",'la': "Où se déroule l'histoire?",'end': "Quel genre de fin d'histoire voulez-vous?",'btn': "Générer une histoire"},
    'Deutsch': {'title': "Willkommen im Emma Story Club:",'lang': "Bitte wählen Sie die Sprache",'length': "Bitte geben Sie die Länge der Geschichte ein",'type': "Welche Art von Geschichte möchten Sie hören?",'char': "Was sind die Charaktere in der Geschichte?",'la': "Wo findet die Geschichte statt?",'end': "Welche Art von Geschichte Ende wollen Sie?",'btn': "Geschichte generieren"},
    'русский': {'title': "Добро пожаловать в клуб историй Эммы:",'lang': "Пожалуйста, выберите язык",'length': "Пожалуйста, введите длину истории",'type': "Какой тип истории вы хотите услышать?",'char': "Кто герои истории?",'la': "Где происходит история?",'end': "Какой тип конца истории вы хотите?",'btn': "Создать историю"}}


    if 'story' not in st.session_state:
        st.session_state.story=False

    params = {}
    
    if 'lang' not in st.session_state:
        st.session_state.lang='中文'

    promot = st.session_state.lang
    st.subheader(tips[promot]['lang'])
    
    lang = st.selectbox('↓↓↓↓',      
        ['中文', 'English', '日本語','Français','Deutsch','русский'], #也可以用元组
        index = 0,label_visibility='collapsed'
        )
    st.session_state.lang=lang
    
    params['length'] = st.number_input(tips[lang]['length'],min_value=100,max_value=1000,value=500)
    params['type'] = st.text_input(tips[lang]['type'])
    params['char'] = st.text_input(tips[lang]['char'])
    params['la'] = st.text_input(tips[lang]['la'])
    params['end'] = st.text_input(tips[lang]['end'])
    params['temp'] = st.select_slider("剧情",0,1,0.6)

    st.button(tips[lang]['btn'],on_click=get_story)

    if st.session_state.story:
        msg ="写一个故事，包含以下要素:{}类型的故事,主角是{},地点在{},故事有一个{}结局".format(params['type'] ,params['char'],params['la'],params['end'])
        if lang != '中文':
            message.append({"role":"user","content":"请把{}翻译成{}".format(msg,lang)})
            msg = chatgpt(message,max_tokens=200,temperature=0)
            message.pop()
        
        message.append({"role":"user","content":msg})
        rtn = chatgpt(message,max_tokens=params["length"],temperature=0.6)
        st.write(rtn)

    return

def choose_continent():
    st.session_state.continent=True

def choose_country():
    st.session_state.country=True

def choose_area():
    st.session_state.area=True


def travel():
    st.title("Emma & ChatGPT")    
    st.header("旅游推荐")
    message  = [{"role":"system","content":"导游"}]

    if 'api_key' not in st.session_state or not st.session_state.api_key:
        st.write("请先输入你的chatGPT API Key")
        return
    else:
        openai.api_key = st.session_state.api_key

    if 'continent' not in st.session_state:
        st.session_state.continent=False

    if 'country' not in st.session_state:
        st.session_state.country=False

    if 'area' not in st.session_state:
        st.session_state.area=False


    continent = st.selectbox(
    '请选择',
    ['南美洲', '非洲', '欧洲','亚洲','北美洲','大洋洲'], #也可以用元组
    index = 0
    )
    
    st.button("选好了",on_click=choose_continent)
    if st.session_state.continent:
        message.append({"role":"user","content":"列举%s所有的国家"%(continent)})
        obj = chatgpt(message,max_tokens=500,temperature=0)
        st.write(obj)

        country = st.text_input("你要去哪个国家旅游？",placeholder="国家")
        st.button("就去这个国家",on_click=choose_country)

        if st.session_state.country and country:
            message.pop()
            message.append({"role":"user","content":"列举%s所有的省(州、邦)"%(country)})
            obj = chatgpt(message,max_tokens=500,temperature=0)
            st.write(obj)
            area = st.text_input("你要去哪个地区旅游？",placeholder="地区")
            st.button("就去这个地区",on_click=choose_area)

            if st.session_state.area and area:
                message.pop()
                message.append({"role":"user","content":"列举%s%s有名的名胜古迹"%(country,area)})
                res = chatgpt(message,max_tokens=500,temperature=0)
                st.write("名胜古迹")
                st.write(res)

                message.pop()
                message.append({"role":"user","content":"列举%s%s有名的自然风光"%(country,area)})
                res = chatgpt(message,max_tokens=500,temperature=0)
                st.write("自然风光")
                st.write(res)

                message.pop()
                message.append({"role":"user","content":"列举%s%s有名的经典美食"%(country,area)})
                res = chatgpt(message,max_tokens=500,temperature=0)
                st.write("经典美食")
                st.write(res)

                message.pop()
                message.append({"role":"user","content":"介绍%s%s的交通状况"%(country,area)})
                res = chatgpt(message,max_tokens=500,temperature=0)
                st.write("交通状况")
                st.write(res)
        
                more = st.selectbox(
                '详细了解',
                ['名胜古迹','自然风光','经典美食','交通状况'], #也可以用元组
                index = 0
                )

                message.pop()
                message.append({"role":"user","content":"请详细介绍%s%s的%s"%(country,area,more)})
                res = chatgpt(message,max_tokens=500,temperature=0)
                st.write(res)

    return

def career_plan():
    st.session_state.career1=  True

def re_plan():
    st.session_state.career2=  True

def career_analyze():
    st.session_state.career3=  True

def career():
    st.title("Emma & ChatGPT")    
    st.header("职业选择")
    message  = [{"role":"system","content":"职业规划师"}]

    if 'api_key' not in st.session_state or not st.session_state.api_key:
        st.write("请先输入你的chatGPT API Key")
        return
    else:
        openai.api_key = st.session_state.api_key

    interest = st.text_input("兴趣爱好",placeholder="你喜欢将时间花在什么上面")        
    skill = st.text_input("技能特长 ",placeholder="可以是写作这样的硬实力，也可以是领导力这样的软实力")
    values = st.text_input("价值观",placeholder="选择工作你最看重什么?兴趣、工资、地理位置...")

    if 'career1' not in st.session_state:
        st.session_state.career1=False

    if 'career2' not in st.session_state:
        st.session_state.career2=False

    if 'career3' not in st.session_state:
        st.session_state.career3=False

    msg ="兴趣爱好是%s,技能特长是%s,最看重%s,给出三种最合适的职业推荐"%(interest,skill,values)
    st.button("开始规划",on_click=career_plan)
    if st.session_state.career1 and interest and skill and values:
        message.append({"role":"user","content":msg})
        res = chatgpt(message,max_tokens=300,temperature=0.6)
        st.write(res)
    
        msg ="兴趣爱好是%s,技能特长是%s,最看重%s,另外给出三种最合适的职业推荐"%(interest,skill,values)
        st.button("重新规划",on_click=re_plan)
        if st.session_state.career2:
            message.append({"role":"assistant","content":res})
            message.append({"role":"user","content":msg})
            res = chatgpt(message,max_tokens=300,temperature=0.8)
            st.write(res)
        
        st.button("详细介绍",on_click=career_analyze)
        if st.session_state.career3:
            message.append({"role":"assistant","content":res})
            message.append({"role":"user","content":"详细介绍这三种职业"})
            res = chatgpt(message,max_tokens=800,temperature=0.5)
            st.write(res)
        
    return

def demo():
    st.title("Emma & ChatGPT")    
    st.header("使用演示")
    video_file = open('demo.mp4', 'rb')
    data  = video_file.read()
    st.video(data)    

    return

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

st.set_page_config(page_title="Emma & ChatGpt",page_icon=":rainbow:", layout="wide",initial_sidebar_state="auto")
#set_background("沙漠3.jpg")

app = MultiApp()
app.add_app("使用演示",demo)
app.add_app("API Key", get_key)
app.add_app("历史人物", people)
app.add_app("情绪支持", emotion)
app.add_app("故事大王", story)
app.add_app("旅游推荐", travel)
app.add_app("职业选择", career)


app.run()