import streamlit as st
import openai
import base64
import streamlit.components.v1 as components


class MultiApp:
    def __init__(self):
        self.apps = []
        self.app_dict = {}

    def add_app(self, title, func):
        #title = title + " :point_left:"
        if title not in self.apps:
            self.apps.append(title)
            self.app_dict[title] = func

    def run(self,title_size="18px",option_size='12px'):
        title = st.sidebar.radio(
            '请选择',
            self.apps,
            format_func=lambda title: str(title))
        self.app_dict[title]()
        self.changeTitleSize(title_size)
        self.changeOptionsize(option_size)

    
    def changeTitleSize(self,title_size='12px'):
        ChangeWidgetFontSize("请选择",title_size)
    
    def changeOptionsize(self,option_size='12px'):
        for x in self.apps:
            ChangeWidgetFontSize(x,option_size)

def ChangeWidgetFontSize(wgt_txt, wch_font_size = '12px'):
    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('*'), i;
                    for (i = 0; i < elements.length; ++i) { if (elements[i].innerText == |wgt_txt|) 
                        { elements[i].style.fontSize='""" + wch_font_size + """';} } </script>  """

    htmlstr = htmlstr.replace('|wgt_txt|', "'" + wgt_txt + "'")
    components.html(f"{htmlstr}", height=0, width=0)
    


def get_key():
    st.title("Emma & ChatGPT")
    st.header("ChatGPT API Key")
    
    if "api_key" not in st.session_state:
        ph="sk-"
    else:
        ph = st.session_state.api_key
    
    mykey = st.text_input("请输入你的API Key",placeholder =ph)
    if mykey:
        st.session_state.api_key = mykey
    st.write("---") 
    if 'lang' not in st.session_state:
            st.session_state.lang='中文'

    langs = {'中文': "请选择语言种类:",'English': "Please select language",'日本語': "言語を選択してください", 'Français': "Veuillez sélectionner la langue",
    'Deutsch':"Bitte wählen Sie die Sprache",'русский': "Пожалуйста, выберите язык"}

    prompt = st.session_state.lang
    st.subheader(langs[prompt])
    c=dict(zip(list(langs.keys()),[x for x in range(len(langs))]))
    lang = st.selectbox('↓↓↓↓', c.keys(), index = c[prompt],label_visibility='collapsed' )
    st.session_state.lang=lang
    if st.button("OK"):
        st.session_state.lang=lang
    
    st.write("---") 
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
def get_info(pname,message,lang='中文'):
    tips={'中文':["%s是哪个国家哪个年代的人,他的生卒时间"%(pname),'简单介绍一下这个人物的生平'],
    'English':['What country and era was %s from, and what were his birth and death dates?'%(pname),'Briefly introduce the life of this character']}
    msg = tips[lang][0]
    message.append({"role":"user","content":msg})
    res1=chatgpt(message,max_tokens=100,temperature=0)
    message.append({"role":"assistant","content":res1})
    msg =  tips[lang][1]
    message.append({"role":"user","content":msg})
    res2=chatgpt(message,max_tokens=500,temperature=0)
    return res1,res2
    

@st.cache_data
def get_more(people,message,lang='中文'):
    tips={'中文':["与%s同时代的名人有哪些"%(people),"%s出现在哪些影视作品中"%(people)],
    'English':['What are the famous figures of the same era as %s'%(people),'Which film and television works does %s appear in'%(people)]}
    msg = tips[lang][0]
    message.append({"role":"user","content":msg})
    res1=chatgpt(message,max_tokens=200,temperature=0)
    message.append({"role":"assistant","content":res1})
    msg = tips[lang][1]
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

    tips ={'中文':{'head':'历史人物','char':'历史学家','quest':'你想了解谁?','placeholder':'在此输入姓名','sub1':'开始吧','err':'请首先输入人物姓名','sub2':'了解更多','lab1':'生平简介','lab2':'同时代名人','lab3':'相关影视作品'},
    'English':{'head':'Historical figure','char':'historian','quest':'Who do you want to know?','placeholder':'Ener the name here','sub1':'Start','err':'Please enter the name of the person first',
    'sub2':'Know more','lab1':'Brief introduction','lab2':'Contemporary celebrities','lab3':'Related film and television works'}}
    st.title("Emma & ChatGPT")
    if 'api_key' not in st.session_state or not st.session_state.api_key:
        st.write("请先输入你的chatGPT API Key")
        return
    else:
        openai.api_key = st.session_state.api_key

    if st.session_state.lang !='中文':
        ll = 'English'
    else:
        ll = '中文'

    st.header(tips[ll]['head'])
    message  = [{"role":"system","content":tips[ll]["char"]}]
    st.subheader(tips[ll]['quest'])
    pname  = st.text_input(tips[ll]['quest'],placeholder =tips[ll]["placeholder"],label_visibility="collapsed")

    if 'click_start' not in st.session_state:
        st.session_state.click_start = False 

    if 'click_more' not in st.session_state:
        st.session_state.click_more = False 
    
    st.button(tips[ll]['sub1'],on_click=info_click)
    if  st.session_state.click_start:
        if not pname:
            st.write(tips[ll]["err"])
            return
        rtn = get_info(pname,message,ll)
        st.write(rtn[0])
        st.subheader(tips[ll]['lab1'])
        st.write(rtn[1])

        st.button(tips[ll]['sub2'],on_click=more_click)
        if st.session_state.click_more:
            message.pop()
            rtn = get_more(pname,message,ll)
            st.subheader(tips[ll]['lab2'])
            st.write(rtn[0])
            st.subheader(tips[ll]['lab3'])
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

    tips = {'中文': {'title': "欢迎来到艾玛的故事会",'lang': "请选择语言种类:",'length': "请输入故事长度",'type': "您想听什么类型的故事?",
    'char': "故事有哪些角色?",'la': "故事发生在什么地方?",'end': "您想要什么样的故事结局?",'btn': "生成故事",'plot':"情节离奇程度"},
    'English': {'title': "Welcome to Emma's Story Club:",'lang': "Please select language",'length': "Please enter the length of the story",'type': "What type of story do you want to hear?",
    'char': "What are the characters in the story?",'la': "Where does the story take place?",'end': "What kind of story ending do you want?",'btn': "Generate story"},
    '日本語': {'title': "エマの物語クラブへようこそ:",'lang': "言語を選択してください",'length': "物語の長さを入力してください",'type': "どのような種類の物語を聞きたいですか？",
    'char': "物語のキャラクターは何ですか？",'la': "物語はどこで起こりますか？",'end': "どのような物語の結末が欲しいですか？",'btn': "物語を生成する"},
    'Français': {'title': "Bienvenue au club d'histoires d'Emma:",'lang': "Veuillez sélectionner la langue",'length': "Veuillez saisir la longueur de l'histoire",'type': "Quel type d'histoire voulez-vous entendre?",
    'char': "Quels sont les personnages de l'histoire?",'la': "Où se déroule l'histoire?",'end': "Quel genre de fin d'histoire voulez-vous?",'btn': "Générer une histoire"},
    'Deutsch': {'title': "Willkommen im Emma Story Club:",'lang': "Bitte wählen Sie die Sprache",'length': "Bitte geben Sie die Länge der Geschichte ein",'type': "Welche Art von Geschichte möchten Sie hören?",
    'char': "Was sind die Charaktere in der Geschichte?",'la': "Wo findet die Geschichte statt?",'end': "Welche Art von Geschichte Ende wollen Sie?",'btn': "Geschichte generieren"},
    'русский': {'title': "Добро пожаловать в клуб историй Эммы:",'lang': "Пожалуйста, выберите язык",'length': "Пожалуйста, введите длину истории",'type': "Какой тип истории вы хотите услышать?",
    'char': "Кто герои истории?",'la': "Где происходит история?",'end': "Какой тип конца истории вы хотите?",'btn': "Создать историю"}}
    
    if 'cont' not in  st.session_state:
        st.session_state.cont = ""

    st.text(st.session_state.cont)

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
    
    
    params['length'] =  st.slider(tips[lang]['length'],min_value=300,max_value=1000,value=600)
    
    params['type'] = st.text_input(tips[lang]['type'])
    params['char'] = st.text_input(tips[lang]['char'])
    params['la'] = st.text_input(tips[lang]['la'])
    params['end'] = st.text_input(tips[lang]['end'])
    params['plot'] =  st.slider(tips[lang]['plot'],min_value=0.0,max_value=1.0,value=0.6)
    

    st.button(tips[lang]['btn'],on_click=get_story)

    if st.session_state.story:
        msg ="写一个故事，包含以下要素:{}类型的故事,主角是{},地点在{},故事有一个{}结局".format(params['type'] ,params['char'],params['la'],params['end'])
        if lang != '中文':
            message.append({"role":"user","content":"请把{}翻译成{}".format(msg,lang)})
            msg = chatgpt(message,max_tokens=200,temperature=0)
            message.pop()
        
        message.append({"role":"user","content":msg})
        rtn = chatgpt(message,max_tokens=params["length"],temperature=0.6)
        #st.write(rtn)
        st.session_state.cont = rtn

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

def writer():
    st.title("Emma & ChatGPT")    
    st.header("作家推荐")

    return

def science():
    st.title("Emma & ChatGPT")    
    st.header("科学世界")
    st.write(':sunny:')
    return

def schedule():
    st.title("Emma & ChatGPT")    
    st.header("日程规划")
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
if 'lang' not in st.session_state:
    lang = '中文'
else:
    lang = st.session_state.lang

if lang !='中文':
    lang = 'English'


menu = {'中文':['使用演示','API Key','历史人物','情绪支持','故事大王','旅游推荐','职业选择','作家推荐','科学世界','日程规划'],
'English':['App Demos','API Key','Historical figure','Emotional support','Storyteller','Travel recommendation','Career options','Writer recommendation','Science World','Schedule planning']}
app.add_app(menu[lang][0],demo)
app.add_app(menu[lang][1], get_key)
app.add_app(menu[lang][2], people)
app.add_app(menu[lang][3], emotion)
app.add_app(menu[lang][4], story)
app.add_app(menu[lang][5], travel)
app.add_app(menu[lang][6], career)
app.add_app(menu[lang][7], writer)
app.add_app(menu[lang][8], science)
app.add_app(menu[lang][9], schedule)
app.run('32px','24px')