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
            '请选择(Please select)',
            self.apps,
            format_func=lambda title: str(title))
        self.app_dict[title]()
        self.changeTitleSize(title_size)
        self.changeOptionsize(option_size)

    
    def changeTitleSize(self,title_size='12px'):
        ChangeWidgetFontSize("请选择(Please select)",title_size)
    
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
def get_emotion(ques,state,message,lang='中文'):
    tips={'中文':["我遇到了一个问题:%s,我的当前心情是%s,请对这种情况做个简单的分析"%(ques,state),'就前面的问题,请给出几条建议(每条建议不超过100个汉字)'],
    'English':["I'm having a problem:%s,My current mood is %s,Please do a simple analysis of this situation"%(ques,state),
    'On the previous question, please give a few suggestions (no more than 200 words each)']}
    msg = tips[lang][0]
    message.append({"role":"user","content":msg})
    res1=chatgpt(message,max_tokens=300,temperature=0.8)
    message.append({"role":"assistant","content":res1})
    msg = tips[lang][1]
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

    tips ={'中文':{'head':'历史人物:sparkling_heart:','char':'历史学家','quest':'你想了解谁?','placeholder':'在此输入姓名','sub1':'开始吧','err':'请首先输入人物姓名','sub2':'了解更多','lab1':'生平简介','lab2':'同时代名人','lab3':'相关影视作品'},
    'English':{'head':'Historical figure:sparkling_heart:','char':'historian','quest':'Who do you want to know?','placeholder':'Ener the name here','sub1':'Start','err':'Please enter the name of the person first',
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
    tips = {'中文':{'head':'情绪支持:sparkling_heart:','char':'心理治疗师','q1':'你遇到了什么问题','p1':'请输入问题','q2':'你当前的心情状态是','p2':'请输入心情',
    'btn':'开始分析','lab1':'请首先输入问题','lab2':'下面是一些简单建议：'},
            'English':{'head':'Emotion Support:sparkling_heart:','char':'psychotherapist','q1':'What problem did you encounter','p1':'Please enter your problem',
             'q2':'Your current state of mood is','p2':'Please enter your mood status',
            'btn':'Start the analysis','lab1':'Please enter the problem first','lab2':'Here are some simple suggestions:'},
    }
    if st.session_state.lang !='中文':
        ll = 'English'
    else:
        ll = '中文'
    st.header(tips[ll]['head'])
    if 'api_key' not in st.session_state or not st.session_state.api_key:
        st.write("请先输入你的chatGPT API Key")
        return
    else:
        openai.api_key = st.session_state.api_key

    ques = st.text_input(tips[ll]['q1'],placeholder=tips[ll]['p1'])
    state = st.text_input(tips[ll]['q2'],placeholder=tips[ll]['p2'])

    if 'emo_analyze' not in st.session_state:
        st.session_state.emo_analyze = False
    
    if st.button(tips[ll]['btn']):
        if not ques or not state:
            st.write(tips[ll]['lab1'])
            return
        message  = [{"role":"system","content":tips[ll]['char']}]
        rtn = get_emotion(ques,state,message,ll)
        st.write(rtn[0])
        st.write(tips[ll]['lab2'])
        st.write(rtn[1])
    return


def get_story():
    st.session_state.story=True

def story():
    st.title("Emma & ChatGPT")    
    
    message  = [{"role":"system","content":"作家"}]

    if 'api_key' not in st.session_state or not st.session_state.api_key:
        st.write("请先输入你的chatGPT API Key")
        return
    else:
        openai.api_key = st.session_state.api_key

    tips = {'中文': {'title': "欢迎来到艾玛的故事会",'lang': "请选择语言种类:",'length': "请输入故事长度",'type': "您想听什么类型的故事?",
    'char': "故事有哪些角色?",'la': "故事发生在什么地方?",'end': "您想要什么样的故事结局?",'btn': "生成故事",'plot':"情节离奇程度"},
    'English': {'title': "Welcome to Emma's Story Club:",'lang': "Please select language",'length': "Please enter the length of the story",'type': "What type of story do you want to hear?",
    'char': "What are the characters in the story?",'la': "Where does the story take place?",'end': "What kind of story ending do you want?",'btn': "Generate story",'plot':"he degree of plot strangeness"},
    '日本語': {'title': "エマの物語クラブへようこそ:",'lang': "言語を選択してください",'length': "物語の長さを入力してください",'type': "どのような種類の物語を聞きたいですか？",
    'char': "物語のキャラクターは何ですか？",'la': "物語はどこで起こりますか？",'end': "どのような物語の結末が欲しいですか？",'btn': "物語を生成する",'plot':"プロットの奇妙さの程度"},
    'Français': {'title': "Bienvenue au club d'histoires d'Emma:",'lang': "Veuillez sélectionner la langue",'length': "Veuillez saisir la longueur de l'histoire",'type': "Quel type d'histoire voulez-vous entendre?",
    'char': "Quels sont les personnages de l'histoire?",'la': "Où se déroule l'histoire?",'end': "Quel genre de fin d'histoire voulez-vous?",'btn': "Générer une histoire",'plot':"Le degré de bizarrerie de l’intrigue."},
    'Deutsch': {'title': "Willkommen im Emma Story Club:",'lang': "Bitte wählen Sie die Sprache",'length': "Bitte geben Sie die Länge der Geschichte ein",'type': "Welche Art von Geschichte möchten Sie hören?",
    'char': "Was sind die Charaktere in der Geschichte?",'la': "Wo findet die Geschichte statt?",'end': "Welche Art von Geschichte Ende wollen Sie?",'btn': "Geschichte generieren",'plot':"Das Maß der Seltsamkeit der Handlung"},
    'русский': {'title': "Добро пожаловать в клуб историй Эммы:",'lang': "Пожалуйста, выберите язык",'length': "Пожалуйста, введите длину истории",'type': "Какой тип истории вы хотите услышать?",
    'char': "Кто герои истории?",'la': "Где происходит история?",'end': "Какой тип конца истории вы хотите?",'btn': "Создать историю",'plot':"Степень необычности сюжета"}}
    
    if 'cont' not in  st.session_state:
        st.session_state.cont = ""

    st.text(st.session_state.cont)

    if 'story' not in st.session_state:
        st.session_state.story=False

    params = {}
    
    if 'lang' not in st.session_state:
        st.session_state.lang='中文'

    lang = st.session_state.lang
    st.header(tips[lang]['title'])
    
    st.subheader(tips[lang]['lang'])
    
    lang = st.session_state.lang
    
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
    tips = {'中文':{'head':'旅游推荐:sparkling_heart:','char':'导游','title':'请选择目的地','destination':['南美洲', '非洲', '欧洲','亚洲','北美洲','大洋洲']},
            'English':{'head':'Travel recommendation:sparkling_heart:','char':'guide','title':'please select a destination','destination':['South America', 'Africa', 'Europe','Asia','North America','Oceania']}
    }
    if st.session_state.lang !='中文':
        ll = 'English'
    else:
        ll = '中文'
    
    st.header(tips[ll]['head'])
    message  = [{"role":"system","content":tips[ll]['char']}]

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

    st.subheader(tips[ll]['title'])
    continent = st.selectbox(
    tips[ll]['title'],
    tips[ll]['destination'], #也可以用元组
    index = 0,label_visibility='collapsed'
    )
    cont ={'中文':["列举%s所有的国家"%(continent),"你要去哪个国家旅游？","国家","你要去哪个地区旅游？","地区",["选择大洲","选择国家","选择地区"]],
    'English':['List all countries in %s'%(continent),"Which country are you traveling to?","Country","Which area are you visiting?","Area",["Select continent","Select Country","Select Area"]]}
    
    st.button(cont[ll][5][0],on_click=choose_continent)
    if st.session_state.continent:
        message.append({"role":"user","content":cont[ll][0]})
        obj = chatgpt(message,max_tokens=500,temperature=0)
        st.write(obj)

        country = st.text_input(cont[ll][1],placeholder=cont[ll][2])
        st.button(cont[ll][5][1],on_click=choose_country)

        if st.session_state.country and country:
            message.pop()
            ct={'中文':"列举%s所有的省(州、邦)"%(country),'English':"List all %s provinces (states)"%(country)}
            message.append({"role":"user","content":ct[ll]})
            obj = chatgpt(message,max_tokens=500,temperature=0)
            st.write(obj)
            area = st.text_input(cont[ll][3],placeholder=cont[ll][4])
            st.button(cont[ll][5][2],on_click=choose_area)
            
            ca={'中文':["列举%s%s有名的名胜古迹"%(country,area),"列举%s%s有名的自然风光"%(country,area),"列举%s%s有名的经典美食"%(country,area),
            "介绍%s%s的交通状况"%(country,area),['名胜古迹','自然风光','经典美食','交通状况']],
            'English':["List the famous places of interest in %s,%s"%(area,country),"List the famous natural scenery of %s,%s"%(area,country),
            "List the famous classics of %s,%s"%(area,country),"Introducing traffic conditions in %s,%s"%(area,country),
            ['Historic sites','Nature scenery','Classic cuisine','Traffic conditions']]
            }
            if st.session_state.area and area:
                message.pop()
                message.append({"role":"user","content":ca[ll][0]})
                res = chatgpt(message,max_tokens=500,temperature=0)
                st.write(ca[ll][4][0])
                st.write(res)

                message.pop()
                message.append({"role":"user","content":ca[ll][1]})
                res = chatgpt(message,max_tokens=500,temperature=0)
                st.write(ca[ll][4][1])
                st.write(res)

                message.pop()
                message.append({"role":"user","content":ca[ll][2]})
                res = chatgpt(message,max_tokens=500,temperature=0)
                st.write(ca[ll][4][2])
                st.write(res)

                message.pop()
                message.append({"role":"user","content":ca[ll][3]})
                res = chatgpt(message,max_tokens=500,temperature=0)
                st.write(ca[ll][4][3])
                st.write(res)
        
                more = st.selectbox(
                '详细了解(Detailed introduction)',
                ca[ll][4], #也可以用元组
                index = 0
                )
                intro = {"中文":"请详细介绍%s%s的%s"%(country,area,more),"English":"Please tell us more about the (%s) of %s,%s"%(more,area,country)}
                message.pop()
                message.append({"role":"user","content":intro[ll]})
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
    tips = {'中文':{'head':'职业选择:sparkling_heart:','char':'职业规划师','form':['兴趣爱好', '技能特长', '价值观'],
            'ph':["你喜欢将时间花在什么上面","可以是写作这样的硬实力，也可以是领导力这样的软实力","选择工作你最看重什么?兴趣、工资、地理位置..."]},
            'English':{'head':'Career options:sparkling_heart:','char':'Career planner','form':['Hobbies','Skill specialties','Values'],
            'ph':["What do you like to spend your time on","It can be hard power like writing or soft power like leadership",
            "What do you value most when choosing a job? Hobbies, salary, place of work..."]}
    }
    if st.session_state.lang !='中文':
        ll = 'English'
    else:
        ll = '中文'
    
    st.header(tips[ll]['head'])

    message  = [{"role":"system","content":tips[ll]['char']}]

    if 'api_key' not in st.session_state or not st.session_state.api_key:
        st.write("请先输入你的chatGPT API Key")
        return
    else:
        openai.api_key = st.session_state.api_key

    interest = st.text_input(tips[ll]['form'][0],placeholder=tips[ll]['ph'][0])        
    skill = st.text_input(tips[ll]['form'][1],placeholder=tips[ll]['ph'][1])
    values = st.text_input(tips[ll]['form'][2],placeholder=tips[ll]['ph'][2])

    if 'career1' not in st.session_state:
        st.session_state.career1=False

    if 'career2' not in st.session_state:
        st.session_state.career2=False

    if 'career3' not in st.session_state:
        st.session_state.career3=False
    
    mm ={"中文":{"btn":["开始规划","重新规划","详细介绍"],"prompt":["兴趣爱好是%s,技能特长是%s,最看重%s,请推荐三种最合适的职业"%(interest,skill,values),
    "兴趣爱好是%s,技能特长是%s,最看重%s,另外给出三种最合适的职业推荐"%(interest,skill,values),"详细介绍这三种职业"]},
    "English":{"btn":["Start planning","Re-plan","Detailed introduction"],"prompt":["The hobby is %s, the skill specialty is %s, the %s is the most important, so please recommend three most suitable occupations"%(interest,skill,values),
    "The hobby is %s, the skill specialty is %s, the %s is the most important, so please recommend three other suitable occupations"%(interest,skill,values),"Detail the three occupations"]}}
    
    msg =mm[ll]['prompt'][0]
    st.button(mm[ll]['btn'][0],on_click=career_plan)
    if st.session_state.career1 and interest and skill and values:
        message.append({"role":"user","content":msg})
        res = chatgpt(message,max_tokens=300,temperature=0.6)
        st.write(res)
    
        msg =mm[ll]['prompt'][1]
        st.button(mm[ll]['btn'][1],on_click=re_plan)
        if st.session_state.career2:
            message.append({"role":"assistant","content":res})
            message.append({"role":"user","content":msg})
            res = chatgpt(message,max_tokens=300,temperature=0.8)
            st.write(res)
        
        st.button(mm[ll]['btn'][2],on_click=career_analyze)
        if st.session_state.career3:
            message.append({"role":"assistant","content":res})
            message.append({"role":"user","content":mm[ll]['prompt'][2]})
            res = chatgpt(message,max_tokens=800,temperature=0.5)
            st.write(res)
        
    return

def writer():
    st.title("Emma & ChatGPT")    

    tips = {'中文':{'head':'作家推荐:sparkling_heart:'},'English':{'head':'Writer recommendation:sparkling_heart:'}}
    if st.session_state.lang !='中文':
        ll = 'English'
    else:
        ll = '中文'
    
    st.header(tips[ll]['head'])

    if 'api_key' not in st.session_state or not st.session_state.api_key:
        st.write("请先输入你的chatGPT API Key")
        return
    else:
        openai.api_key = st.session_state.api_key

    #st.subheader("Will coming soon!")
    ques = st.text_input("What do you want to know?",placeholder="Anythings")
    if ques:
        message  = [{"role":"system","content":'encyclopedia'}]
        message.append({"role":"user","content":ques})
        res = chatgpt(message,max_tokens=800,temperature=0.5)
        st.text_area=res
    return

def science():
    st.title("Emma & ChatGPT")    
    tips = {'中文':{'head':'科学世界:sparkling_heart:'},'English':{'head':'Science World:sparkling_heart:'}}
    if st.session_state.lang !='中文':
        ll = 'English'
    else:
        ll = '中文'
    
    st.header(tips[ll]['head'])
    
    if 'api_key' not in st.session_state or not st.session_state.api_key:
        st.write("请先输入你的chatGPT API Key")
        return
    else:
        openai.api_key = st.session_state.api_key
    
    ques = st.text_input("What do you want to know?",placeholder="Anythings")
    if ques:
        message  = [{"role":"system","content":'encyclopedia'}]
        message.append({"role":"user","content":ques})
        res = chatgpt(message,max_tokens=800,temperature=0.5)
        st.text_area=res
    return

def schedule():
    st.title("Emma & ChatGPT")    
    
    tips = {'中文':{'head':'日程规划:sparkling_heart:'},'English':{'head':'Schedule planning:sparkling_heart:'}}
    if st.session_state.lang !='中文':
        ll = 'English'
    else:
        ll = '中文'
    
    st.header(tips[ll]['head'])

    if 'api_key' not in st.session_state or not st.session_state.api_key:
        st.write("请先输入你的chatGPT API Key")
        return
    else:
        openai.api_key = st.session_state.api_key
    
    ques = st.text_input("What do you want to know?",placeholder="Anythings")
    if ques:
        message  = [{"role":"system","content":'encyclopedia'}]
        message.append({"role":"user","content":ques})
        res = chatgpt(message,max_tokens=800,temperature=0.5)
        st.text_area=res
    return

def demo():
    st.title("Emma & ChatGPT")    

    tips = {'中文':{'head':'使用演示:sparkling_heart:'},'English':{'head':'App demo:sparkling_heart:'}}
    if st.session_state.lang !='中文':
        ll = 'English'
    else:
        ll = '中文'

    st.header(tips[ll]['head'])
    
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

app = MultiApp()

if 'lang' not in st.session_state:
    lang = 'English'
    st.session_state.lang='English'
else:
    lang = st.session_state.lang

if lang !='中文':
    lang = 'English'


menu = {'中文':['使用演示','API Key','历史人物','情绪支持','故事大王','旅游推荐','职业选择','作家推荐','科学世界','日程规划'],
'English':['App Demos','API Key','Historical figure','Emotional support','Storyteller','Travel recommendation','Career options','Writer recommendation','Science World','Schedule planning']}
app.add_app(menu[lang][0], demo)
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