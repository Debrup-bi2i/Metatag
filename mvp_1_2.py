import streamlit as st
import numpy as np
import pandas as pd
import time
import requests
from requests.exceptions import ConnectionError
from urllib.parse import urlparse, urljoin
import random
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import base64
import re


s = requests.Session()
a = requests.adapters.HTTPAdapter(max_retries=2)
s.mount("http://", a)

df2=pd.DataFrame() 
def f2(x):
    if x==7:
        return 1
    else:    
        return 0
def f1(x):
    if x==4:
        return 1
    else:    
        return 0    
def tag_extractor_n(url1):
    try:
        token=str(random.randint(0,1000))
        headers = {
                    'cache-control': "no-cache",
                    'postman-token': token
                    }
        r1=requests.get(url1,headers=headers)
        if r1.status_code==200:
        
            htmlcontent1 = r1.content
            # print(htmlcontent)
            soup1 = BeautifulSoup(htmlcontent1, "html.parser")
            dict_metatag1 = my_dictionary()
            for link in soup1.find_all("meta"):
                if link.get("name") != None:
                    if link.get("name") in [
                        "bu",
                        "sub_bu",
                        "flag_all",
                        "web_section_id",
                        "page_content",
                        "segment",
                        "lifecycle",
                        "user_profile",
                        "simple_title",
                        "analytics_template_name",
                        "product_service_name",
                        "analytics_section",
                        "hp_design_version",
                        "page_level",
                        "product_type",
                        "family"
                    ]:
                        dict_metatag1.add(link.get("name"), link.get("content"))
            print(dict_metatag1, url1)

            

            df1 = pd.DataFrame(
                columns=(
                    "url",
                    "primary_flag",
                    "redirect",
                    "status",
                    "bu",
                    "web_section_id",
                    "page_content",
                    "segment",
                    "lifecycle",
                    "user_profile",
                    "simple_title",
                    "sub_bu",
                    "analytics_template_name",
                    "product_service_name",
                    "analytics_section",
                    "hp_design_version",
                    "page_level",
                    "product_type",
                    "family"
                )
            )
            for col in df1.columns:

                if col == "url":
                    df1.loc[1, col] = url1
                elif col=="primary_flag":
                    s=list()
                    for name in ["bu",
                "web_section_id",
                "page_content",
                "segment",
                "lifecycle",
                "user_profile",
                "simple_title"]:
                        s.append(dict_metatag1[name]==dict_metatag[name])
                    if all(s):
                        df1.loc[1,col] = 1
                    else:
                        df1.loc[1,col] = 0                        
                 
                elif col == "status":
                    df1.loc[1, col] = r1.status_code
                elif col == "redirect":
                    if r1.url != url1:
                        df1.loc[1, col] = 1
                    else:
                        df1.loc[1, col] = 0
               
                else:
                    try:
                        df1.loc[1, col]=dict_metatag1[col]
                    except:
                        df1.loc[1, col]=""
                            

            return df1

                # df = df.append(df1)
        else:
            pass
    
            time.sleep(1)
    except:
        pass
        
def tag_extractor(url1):
        try:
            token=str(random.randint(0,1000))
            headers = {
                        'cache-control': "no-cache",
                        'postman-token': token
                        }
            r1=requests.get(url1,headers=headers)
            if r1.status_code==200:
            
                htmlcontent1 = r1.content
                # print(htmlcontent)
                soup1 = BeautifulSoup(htmlcontent1, "html.parser")
                dict_metatag1 = my_dictionary()
                for link in soup1.find_all("meta"):
                    if link.get("name") != None:
                        if link.get("name") in [
                            "bu",
                            "sub_bu",
                            "flag_all",
                            "web_section_id",
                            "page_content",
                            "segment",
                            "lifecycle",
                            "user_profile",
                            "simple_title",
                            "analytics_template_name",
                            "product_service_name",
                            "analytics_section",
                        ]:
                            dict_metatag1.add(link.get("name"), link.get("content"))
                print(dict_metatag1, url1)

                

                df1 = pd.DataFrame(
                    columns=(
                        "url",
                        "redirect",
                        "status",
                        "bu",
                        "web_section_id",
                        "page_content",
                        "segment",
                        "lifecycle",
                        "user_profile",
                        "simple_title",
                        "sub_bu",
                        "analytics_template_name",
                        "product_service_name",
                        "analytics_section",
                    )
                )
                for col in df1.columns:

                    if col == "url":
                        df1.loc[1, col] = url1

                    elif col == "status":
                        df1.loc[1, col] = r1.status_code
                    elif col == "redirect":
                        if r1.url != url1:
                            df1.loc[1, col] = 1
                        else:
                            df1.loc[1, col] = 0
                   
                    else:
                        try:
                            df1.loc[1, col]=dict_metatag1[col]
                        except:
                            df1.loc[1, col]=""
                                

                return df1

                    # df = df.append(df1)
            else:
                pass
        
                time.sleep(1)
        except:
            pass        
class my_dictionary(dict): 
 
    def __init__(self): 
        self = dict() 
 
    def add(self, key, value): 
        self[key] = value 
dict_metatag=my_dictionary()
main_url=None        
def path_extrt(url):
    l1 = url.split("/")
    sc = ""
    for i in l1[5:]:
            fr = i
            sc = sc + "/" + fr
    return sc
metatag_ref = pd.DataFrame(
        columns=(
            "url",
            "bu",
            "web_section_id",
            "page_content",
            "segment",
            "lifecycle",
            "user_profile",
            "simple_title",
            "sub_bu",
            "analytics_template_name",
            "product_service_name",
            "analytics_section",
            "hp_design_version",
            "page_level",
            "product_type",
            "family"
            )
            )  
def static_list(path):
    print(path)
    url = "http://www8.hp.com/us/en" + path
    global main_url
    main_url=url
    r = requests.get(url)
    htmlcontent = r.content
    ##print(htmlcontent)
    soup = BeautifulSoup(htmlcontent, "html.parser")

    for link in soup.find_all("meta"):
        if link.get("name") != None:
            if link.get("name") in [
                "bu",
                "sub_bu",
                "web_section_id",
                "page_content",
                "segment",
                "lifecycle",
                "user_profile",
                "simple_title",
                "analytics_template_name",
                "product_service_name",
                "analytics_section",
                "hp_design_version",
                "page_level",
                "product_type",
                "family"
            ]:
                dict_metatag.add(link.get("name"), link.get("content"))
    #print(dict_metatag)
    global workstnlist1
    workstnlist1=set()
    for ur in list_urls:
        vr = ur.split("/")
        sc1 = ""
        for i in vr[:5]:
            fr = i
            sc1 = sc1 + "/" + fr
        workstnlist1.add(sc1[1:] + path)
    global metatag_ref
    for col in metatag_ref.columns:
        if col == "url":
            metatag_ref.loc[1, col] = main_url
        else:
            try:
                metatag_ref.loc[1, col]=dict_metatag[col]
            except:
                metatag_ref.loc[1, col]=""
                        
    return metatag_ref,main_url,workstnlist1,dict_metatag
def input_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return parsed.netloc=='www8.hp.com' and parsed.scheme=='https' and bool(re.search(".html$",parsed.path.split('/')[-1]))
list_urls=['https://www8.hp.com/ar/es/home.html',
 'https://www8.hp.com/bo/es/home.html',
 'https://www8.hp.com/br/pt/home.html',
 'https://www8.hp.com/ca/en/home.html',
 'https://www8.hp.com/ca/fr/home.html',
 'https://www8.hp.com/lamerica_nsc_carib/en/home.html',
 'https://www8.hp.com/cl/es/home.html',
 'https://www8.hp.com/co/es/home.html',
 'https://www8.hp.com/ec/es/home.html',
 'https://www8.hp.com/lamerica_nsc_cnt_amer/es/home.html',
 'https://www8.hp.com/mx/es/home.html',
 'https://www8.hp.com/py/es/home.html',
 'https://www8.hp.com/pe/es/home.html',
 'https://www8.hp.com/pr/es/home.html',
 'https://www8.hp.com/us/en/home.html',
 'https://www8.hp.com/uy/es/home.html',
 'https://www8.hp.com/ve/es/home.html',
 'https://www8.hp.com/au/en/home.html',
 'https://www8.hp.com/cn/zh/home.html',
 'https://www8.hp.com/hk/en/home.html',
 'https://www8.hp.com/hk/zh/home.html',
 'https://www8.hp.com/in/en/home.html',
 'https://www8.hp.com/id/en/home.html',
 'https://www8.hp.com/kr/ko/home.html',
 'https://www8.hp.com/my/en/home.html',
 'https://www8.hp.com/nz/en/home.html',
 'https://www8.hp.com/ph/en/home.html',
 'https://www8.hp.com/sg/en/home.html',
 'https://www8.hp.com/tw/zh/home.html',
 'https://www8.hp.com/th/en/home.html',
 'https://www8.hp.com/vn/en/home.html',
 'https://www8.hp.com/emea_africa/en/home.html',
 'https://www8.hp.com/emea_africa/fr/home.html',
 'https://www8.hp.com/at/de/home.html',
 'https://www8.hp.com/by/ru/home.html',
 'https://www8.hp.com/be/fr/home.html',
 'https://www8.hp.com/be/nl/home.html',
 'https://www8.hp.com/bg/bg/home.html',
 'https://www8.hp.com/hr/hr/home.html',
 'https://www8.hp.com/cz/cs/home.html',
 'https://www8.hp.com/dk/da/home.html',
 'https://www8.hp.com/ee/et/home.html',
 'https://www8.hp.com/fi/fi/home.html',
 'https://www8.hp.com/fr/fr/home.html',
 'https://www8.hp.com/de/de/home.html',
 'https://www8.hp.com/gr/el/home.html',
 'https://www8.hp.com/hu/hu/home.html',
 'https://www8.hp.com/ie/en/home.html',
 'https://www8.hp.com/il/he/home.html',
 'https://www8.hp.com/it/it/home.html',
 'https://www8.hp.com/kz/ru/home.html',
 'https://www8.hp.com/lv/lv/home.html',
 'https://www8.hp.com/lt/lt/home.html',
 'https://www8.hp.com/emea_middle_east/ar/home.html',
 'https://www8.hp.com/emea_middle_east/en/home.html',
 'https://www8.hp.com/nl/nl/home.html',
 'https://www8.hp.com/no/no/home.html',
 'https://www8.hp.com/pl/pl/home.html',
 'https://www8.hp.com/pt/pt/home.html',
 'https://www8.hp.com/ro/ro/home.html',
 'https://www8.hp.com/ru/ru/home.html',
 'https://www8.hp.com/sa/ar/home.html',
 'https://www8.hp.com/sa/en/home.html',
 'https://www8.hp.com/rs/sr/home.html',
 'https://www8.hp.com/sk/sk/home.html',
 'https://www8.hp.com/si/sl/home.html',
 'https://www8.hp.com/za/en/home.html',
 'https://www8.hp.com/es/es/home.html',
 'https://www8.hp.com/se/sv/home.html',
 'https://www8.hp.com/ch/de/home.html',
 'https://www8.hp.com/ch/fr/home.html',
 'https://www8.hp.com/tr/tr/home.html',
 'https://www8.hp.com/ua/ru/home.html',
 'https://www8.hp.com/ua/uk/home.html',
 'https://www8.hp.com/uk/en/home.html',
 'https://www8.hp.com/ve/en/home.html',
 'https://www8.hp.com/jp/ja/home.html',
 'https://www8.hp.com/si/si/home.html',
 'https://www8.hp.com/rs/rs/home.html'
 'https://www8.hp.com/is/is/home.html']
df1 = pd.DataFrame(
    columns=(
        "url",
        "redirect",
        "status",
        "bu",
        "web_section_id",
        "page_content",
        "segment",
        "lifecycle",
        "user_profile",
        "simple_title",
        "sub_bu",
        "analytics_template_name",
        "product_service_name",
        "analytics_section",
    )
)
col_order=["url",
"Primary_Flag",
"Secondary_Flag",
"bu",
"web_section_id",
"page_content",
"segment",
"lifecycle",
"user_profile",
"simple_title",
"sub_bu",
"analytics_template_name",
"product_service_name",
"analytics_section",
]
col_order_1=["url",
"Primary_Flag",
"Secondary_Flag",
"bu",
"web_section_id",
"page_content",
"segment",
"lifecycle",
"user_profile",
"simple_title",
"sub_bu",
"analytics_template_name",
"product_service_name",
"analytics_section",
"hp_design_version",
"page_level",
"product_type",
"family"]
dict_metatag = my_dictionary()
workstnlist1=set()
styler=[]
df = pd.DataFrame(
       columns=(
           "url",
           "primary_flag",
           "secondary_flag",
           "redirect",
           "status",
           "bu",
           "web_section_id",
           "page_content",
           "segment",
           "lifecycle",
           "user_profile",
           "simple_title",
           "sub_bu",
           "analytics_template_name",
           "product_service_name",
           "analytics_section",
           "Primary_Flag",
           "Secondary_Flag",
           )
           )    
# def app_backend(url):
    
#     path=path_extrt(url)

#     static_list(path)
    

#     res = []
#     with ThreadPoolExecutor(max_workers=30) as T:
#         res = list(T.map(tag_extractor, list(workstnlist1)))
       
#     global df,df2#,styler
#     df = pd.DataFrame(
#         columns=(
#             "url",
#             "redirect",
#             "status",
#             "bu",
#             "web_section_id",
#             "page_content",
#             "segment",
#             "lifecycle",
#             "user_profile",
#             "simple_title",
#             "sub_bu",
#             "analytics_template_name",
#             "product_service_name",
#             "analytics_section",
#             )
#             )    
#     for i in res:
        
        
#         df = df.append(i)
        
        
#         # df['primary_flag']=df[['bu', 'web_section_id', 'page_content',
#         #    'segment', 'lifecycle', 'user_profile', 'simple_title']].sum(axis=1)
#         # df['secondary_flag']=df[['sub_bu',
#         #    'analytics_template_name', 'product_service_name', 'analytics_section']].sum(axis=1) 
#         # df['primary_flag']=df['primary_flag'].apply(f2)
#         # df['secondary_flag']=df['secondary_flag'].apply(f1)
#         # df2=df.set_index('url')
#         #styler = df2.style.applymap(color_green)
#     return df,dict_metatag
values=list(metatag_ref.loc[:,'bu':'simple_title'].astype(str))

def color_bu(val):
    
    color ='#C3E6CB' if val == metatag_ref.loc[1,'bu'] else '#e3b468'
    return 'background-color: %s' % color
def color_webs(val):
    
    color ='#C3E6CB' if val == metatag_ref.loc[1,'web_section_id'] else '#e3b468'
    return 'background-color: %s' % color
def color_pg(val):
    
    color ='#C3E6CB' if val == metatag_ref.loc[1,'page_content'] else '#e3b468'
    return 'background-color: %s' % color
def color_seg(val):
    
    color ='#C3E6CB' if val == metatag_ref.loc[1,'segment'] else '#e3b468'
    return 'background-color: %s' % color
def color_lc(val):
    
    color ='#C3E6CB' if val == metatag_ref.loc[1,'lifecycle'] else '#e3b468'
    return 'background-color: %s' % color
def color_user(val):
    
    color ='#C3E6CB' if val == metatag_ref.loc[1,'user_profile'] else '#e3b468'
    return 'background-color: %s' % color
def color_title(val):
    
    color ='#C3E6CB' if val == metatag_ref.loc[1,'simple_title'] else '#e3b468'
    return 'background-color: %s' % color
def color_web(val):
    
    color ='#C3E6CB' if val == metatag_ref.loc[1,'hp_design_version'] else '#e3b468'
    return 'background-color: %s' % color
def color_pl(val):
    
    color ='#C3E6CB' if val == metatag_ref.loc[1,'page_level'] else '#e3b468'
    return 'background-color: %s' % color
def color_type(val):
    
    color ='#C3E6CB' if val == metatag_ref.loc[1,'product_type'] else '#e3b468'
    return 'background-color: %s' % color
def color_fam(val):
    
    color ='#C3E6CB' if val == metatag_ref.loc[1,'family'] else '#e3b468'
    return 'background-color: %s' % color
def color_green(val):
    
    color ='#C3E6CB' if val in list(metatag_ref.iloc[0,].astype(str)) else '#e3b468'
    return 'background-color: %s' % color

def color_green_1(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = '#C3E6CB' if val =="" else '#e3b468'
    return 'background-color: %s' % color
def color_sec_flag(val):
    
    
    color = '#C3E6CB' if val =="1" else 'white'
    return 'background-color: %s' % color
def color_prim_flag(val):
    
    
    color = '#C3E6CB' if val ==1 else 'white'
    return 'background-color: %s' % color
def highlight_row(x):
    x=x.to_frame()
    if x['primary_flag'] ==1 & x['secondary_flag']==1:
        return ['background-color: #8AFF33']*15
    else:
        return ['background-color: white']*15 



# def highlight_primary(s):
    
#     return ['background-color: #8AFF33']*len(s) if s.primary_flag else ['background-color: red']*len(s)
t1=time.time()
st.set_page_config(layout="wide")
st.title("Meta-tag Validator")
user_input = st.text_input("Url goes here",  ""
)

##button addition to invoke the piece of code
def download_link(object_to_download, download_filename, download_link_text):
    
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=True)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

if user_input!="" and input_valid(user_input):
#     app_backend(user_input)

    latest_iteration = st.empty()
    bar = st.progress(0)
    path=path_extrt(user_input)
    url = "http://www8.hp.com/us/en" + path
    if requests.get(url).status_code !=200:
        st.write('master_url not OK!')
    static_list(path)
    if 'hpweb.2' in dict_metatag['hp_design_version']:
        res=[]
        res2=[]
        for i in range(4):
          # Update the progress bar with each iteration.
            l1,l2=i*20,(i+1)*20
            latest_iteration.text(f'Number of URLs: {(i+1)*20}')
            with ThreadPoolExecutor(max_workers=20) as T:
              res = list(T.map(tag_extractor_n, list(workstnlist1)[l1:l2]))
              for row in res:
                df = df.append(row)
              
            bar.progress((i+1) * 25)
            res2.append(res)
        df['index'] = list(range(len(df.index)))
        df=df.set_index('index')  
        
        #df=df.fillna("").astype('str')  
        for i in range(len(df.index)):
            t=list()
            for col in ["sub_bu",
                    "analytics_template_name",
                    "product_service_name",
                    "analytics_section"]:
                    t.append(      
                    df.loc[i,col]=="")
                   
            if all(t):    
                df.loc[i,'secondary_flag']="1"
            else:    
                df.loc[i,'secondary_flag']="0"
        df=df.drop(['status','redirect'], axis = 1)
        # cols = df.columns.tolist()
        # cols = cols[0:1]+cols[-1:] + cols[2:-1]
        
        df['Primary_Flag']=df.primary_flag
        df['Secondary_Flag']=df.secondary_flag
        df = df[col_order_1]
    else:
        metatag_ref=metatag_ref.drop(["page_level",
            "product_type",
            "family"],axis=1)
        res=[]
        res2=[]
        for i in range(4):
          # Update the progress bar with each iteration.
            l1,l2=i*20,(i+1)*20
            latest_iteration.text(f'Number of URLs: {(i+1)*20}')
            with ThreadPoolExecutor(max_workers=20) as T:
              res = list(T.map(tag_extractor_n, list(workstnlist1)[l1:l2]))
              for row in res:
                df = df.append(row)
              
            bar.progress((i+1) * 25)
            res2.append(res)
        df['index'] = list(range(len(df.index)))
        df=df.set_index('index')  
        
        #df=df.fillna("").astype('str')  
        for i in range(len(df.index)):
            t=list()
            for col in ["sub_bu",
                    "analytics_template_name",
                    "product_service_name",
                    "analytics_section"]:
                    t.append(      
                    df.loc[i,col]=="")
                   
            if all(t):    
                df.loc[i,'secondary_flag']="1"
            else:    
                df.loc[i,'secondary_flag']="0"
        df=df.drop(['status','redirect'], axis = 1)
        # cols = df.columns.tolist()
        # cols = cols[0:1]+cols[-1:] + cols[2:-1]
        
        df['Primary_Flag']=df.primary_flag
        df['Secondary_Flag']=df.secondary_flag
        df = df[col_order]
              

    
else:
    st.write('Please Enter a Valid URL!')
    
    
t2=time.time()
t=t2-t1
st.write('Total time to Validate the URL:',round(t,2))
st.write(metatag_ref)
st.write("This is the metatags of:",main_url,"to be used for reference")
st.write("Primary Flag indicates if the first seven metatag matches with the US-English local variant of the webpage.")
st.write("Secondary Flag indicates if the last 4 metatags are empty or non-empty.")
#st.dataframe(df2.style.applymap(color_green),100,50)
tmp_download_link = download_link(df, 'check.csv', 'Click here to download your data!')
st.markdown(tmp_download_link, unsafe_allow_html=True)
#st.table(df)
def highlight_greaterthan(x):
    if (x.Secondary_Flag == '1') & (x.Primary_Flag>0):
        return ['background-color: #93d2a2']*df.shape[1]
    else:
        return ['background-color: white']*df.shape[1]
#st.table(df.style.apply(highlight_greaterthan, axis=1))

if 'hpweb.1' in dict_metatag['hp_design_version']:
    obj=df.style.apply(highlight_greaterthan, axis=1).applymap(color_bu,
                            pd.IndexSlice[:,['bu']]).applymap(color_webs,
                                                              pd.IndexSlice[:,['web_section_id']]).applymap(color_pg,
                                                                                                            pd.IndexSlice[:,['page_content']]).applymap(color_seg,
                                                                                                                                                        pd.IndexSlice[:,['segment']]).applymap(color_lc,
                                                                                                                                                                                              pd.IndexSlice[:,['lifecycle']]).applymap(color_user,pd.IndexSlice[:,['user_profile']]).applymap(color_title,
                                                                                                                                                                                                                                                                                                        pd.IndexSlice[:,['simple_title']]).applymap(color_green_1,
                                                                                                                                                                                                                                                                                                                                                              pd.IndexSlice[:,['sub_bu','analytics_template_name','product_service_name','analytics_section']]).applymap(color_sec_flag,
                                                              pd.IndexSlice[:,['Secondary_Flag']]).applymap(color_prim_flag,
                                                              pd.IndexSlice[:,['Primary_Flag']])

    
else:    
    obj=df.style.apply(highlight_greaterthan, axis=1).applymap(color_bu,
                            pd.IndexSlice[:,['bu']]).applymap(color_webs,
                                                              pd.IndexSlice[:,['web_section_id']]).applymap(color_pg,
                                                                                                            pd.IndexSlice[:,['page_content']]).applymap(color_seg,
                                                                                                                                                        pd.IndexSlice[:,['segment']]).applymap(color_lc,
                                                                                                                                                                                              pd.IndexSlice[:,['lifecycle']]).applymap(color_user,pd.IndexSlice[:,['user_profile']]).applymap(color_title,
                                                                                                                                                                                                                                                                                                        pd.IndexSlice[:,['simple_title']]).applymap(color_green_1,
                                                                                                                                                                                                                                                                                                                                                              pd.IndexSlice[:,['sub_bu','analytics_template_name','product_service_name','analytics_section']]).applymap(color_sec_flag,
                                                              pd.IndexSlice[:,['Secondary_Flag']]).applymap(color_prim_flag,
                                                              pd.IndexSlice[:,['Primary_Flag']]).applymap(color_web,
                                                                                                          pd.IndexSlice[:,['hp_design_version']]).applymap(color_pl,
                                                                                                                                                           pd.IndexSlice[:,['page_level']]).applymap(color_type,
                                                                                                                                                           pd.IndexSlice[:,['product_type']]).applymap(color_fam,
                                                                                                                                                           pd.IndexSlice[:,['family']])
                                                                                                           
st.write(obj)
