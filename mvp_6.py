# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 15:54:33 2021

@author: DuttDebr
"""

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
import os
import time
import pandas as pd
s = requests.Session()
a = requests.adapters.HTTPAdapter(max_retries=2)
s.mount("http://", a)
list_comb=['ar/es',
 'bo/es',
 'br/pt',
 'ca/en',
 'ca/fr',
 'lamerica_nsc_carib/en',
 'cl/es',
 'co/es',
 'ec/es',
 'lamerica_nsc_cnt_amer/es',
 'mx/es',
 'py/es',
 'pe/es',
 'pr/es',
 'us/en',
 'uy/es',
 've/es',
 'au/en',
 'cn/zh',
 'hk/en',
 'hk/zh',
 'in/en',
 'id/en',
 'kr/ko',
 'my/en',
 'nz/en',
 'ph/en',
 'sg/en',
 'tw/zh',
 'th/en',
 'vn/en',
 'emea_africa/en',
 'emea_africa/fr',
 'at/de',
 'by/ru',
 'be/fr',
 'be/nl',
 'bg/bg',
 'hr/hr',
 'cz/cs',
 'dk/da',
 'ee/et',
 'fi/fi',
 'fr/fr',
 'de/de',
 'gr/el',
 'hu/hu',
 'ie/en',
 'il/he',
 'it/it',
 'kz/ru',
 'lv/lv',
 'lt/lt',
 'emea_middle_east/ar',
 'emea_middle_east/en',
 'nl/nl',
 'no/no',
 'pl/pl',
 'pt/pt',
 'ro/ro',
 'ru/ru',
 'sa/ar',
 'sa/en',
 'rs/sr',
 'sk/sk',
 'si/sl',
 'za/en',
 'es/es',
 'se/sv',
 'ch/de',
 'ch/fr',
 'tr/tr',
 'ua/ru',
 'ua/uk',
 'uk/en',
 've/en',
 'jp/ja',
 'si/si',
 'rs/rs']

store_list=['mx/es',
            'co/es',
            'br/pt',
            'au/en',
            'id/en',
            'cn/zh',
            'my/en']

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
"hp_design_version"
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
class my_dictionary(dict): 
 
    def __init__(self): 
        self = dict() 
 
    def add(self, key, value): 
        self[key] = value 
dict_metatag=my_dictionary()

def path_extrt(url):
    l1 = url.split("/")
    sc = ""
    fl_nm=""
    for i in l1[5:]:
            fr = i
            sc = sc + "/" + fr
    for i in l1[5:]:
            fr_2 = i
            fl_nm = fl_nm + "_" + fr_2        
    dom = l1[0]+'//'+l1[2]+"/"
    return dom,sc,fl_nm

def tag_extractor(comb):
    token=str(random.randint(0,1000))
    headers = {
                'cache-control': "no-cache",
                'postman-token': token
                }
    url1=path_extrt(url)[0]+comb+path_extrt(url)[1]
    
    try:
        r1=requests.get(url1,headers=headers,timeout=30)
        if r1.status_code==200:
        ###CHECKING IF IT's an Ok URL
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
                        "family"]:
                        dict_metatag1.add(link.get("name"), link.get("content"))
            #print(dict_metatag1, url1)
            return dict_metatag1, url1
                        

        else:
            url1 = path_extrt(url)[0]+re.sub("/","-",comb)+path_extrt(url)[1]
            try:
                r1=requests.get(url1,headers=headers, timeout=30)
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
                                "family"]:
                                dict_metatag1.add(link.get("name"), link.get("content"))
                    #print(dict_metatag1, url1)
                    return dict_metatag1, url1
                else:
                    pass
                
            except:
                pass
            
    except:
        url1 = path_extrt(url)[0]+re.sub("/","-",comb)+path_extrt(url)[1]
        try:
            r1=requests.get(url1,headers=headers, timeout=30)
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
                            "family"]:
                            dict_metatag1.add(link.get("name"), link.get("content"))
                #print(dict_metatag1, url1)
                return dict_metatag1, url1
        except:
            pass
        
def tag_extractor_wrap(cc_ll):
    dict2=my_dictionary()
    try:
        dict2, url=tag_extractor(cc_ll)
        print(cc_ll, dict2)
        try:
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

                    df1.loc[1, col] = url

                elif col=="primary_flag":

                    s=list()

                    for name in ["bu",
                "web_section_id",
                "page_content",
                "segment",
                "lifecycle",
                "user_profile",
                "simple_title"]:

                        s.append(dict2[name]==dict_metatag[name])

                    if all(s):
                        df1.loc[1,col] = 1
                    else:
                        df1.loc[1,col] = 0
                elif col == "status":
                    df1.loc[1, col] = r1.status_code
                elif col == "redirect":

                    if r1.url != url:
                        df1.loc[1, col] = 1
                    else:
                        df1.loc[1, col] = 0

                else:
                    try:

                        df1.loc[1, col]=dict2[col]
                    except:
                        df1.loc[1, col]=""
            return df1
        except:
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

                    df1.loc[1, col] = url

                elif col=="primary_flag":
                    df1.loc[1,col] = 0
                elif col == "status":
                    df1.loc[1, col] = r1.status_code
                elif col == "redirect":

                    if r1.url != url:
                        df1.loc[1, col] = 1
                    else:
                        df1.loc[1, col] = 0

                else:
                    try:

                        df1.loc[1, col]=dict2[col]
                    except:
                        df1.loc[1, col]=""
            
            return df1
    
    except:
        print(cc_ll)
        pass
    
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
    
    
    color = '#C3E6CB' if val =='1' else 'white'
    return 'background-color: %s' % color
def highlight_row(x):
    x=x.to_frame()
    if x['primary_flag'] ==1 & x['secondary_flag']==1:
        return ['background-color: #8AFF33']*15
    else:
        return ['background-color: white']*15 
def highlight_greaterthan(x):
    if (x.Secondary_Flag == '1') & (x.Primary_Flag=='1'):
        return ['background-color: #93d2a2']*df.shape[1]
    else:
        return ['background-color: white']*df.shape[1]    
t1=time.time()
st.set_page_config(layout="wide")
st.title("Meta-tag Validator")
user_input = st.text_input("Master Url goes here",  "")
def download_link(object_to_download, download_filename, download_link_text):
    
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=True)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

url=user_input
t1=time.time()
token=str(random.randint(0,1000))
headers = {
            'cache-control': "no-cache",
            'postman-token': token
            }
try:
   
    r1=requests.get(url,headers=headers,timeout=30)
    if r1.status_code==200:
        htmlcontent = r1.content
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
                    "family"]:
                    dict_metatag.add(link.get("name"), link.get("content"))
        #print(dict_metatag)
        columns=["bu",
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
                    "hp_design_version"]
        for col in metatag_ref.columns:
            if col == "url":
                metatag_ref.loc[1, col] = url
            else:
                try:
                    metatag_ref.loc[1, col]=dict_metatag[col]
                except:
                    metatag_ref.loc[1, col]=""
        try:
            if 'hpweb.2' in dict_metatag['hp_design_version']:
                st.write(metatag_ref)
            else:
                metatag_ref=metatag_ref[columns]
                st.write(metatag_ref)
        except:
            st.write(metatag_ref)
            
        st.write("This is the metatags of:",url,"to be used for reference")
        res=[]
        res2=[]
        bar = st.progress(0)
        latest_iteration = st.empty()
        for i in range(4):
          # Update the progress bar with each iteration.
            l1,l2=i*20,(i+1)*20
            latest_iteration.text(f'Number of URLs: {(i+1)*20}')
            with ThreadPoolExecutor(max_workers=20) as T:
              res = list(T.map(tag_extractor_wrap, list_comb[l1:l2]))
              for row in res:
                df = df.append(row)
              bar.progress((i+1) * 25) 
        df['index'] = list(range(len(df.index)))
        df=df.set_index('index')  
        
        #df=df.set_index('index')  
    
        df=df.fillna("").astype('str')  
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
        cols = df.columns.tolist()
        cols = cols[0:1]+cols[-1:] + cols[2:-1]
        
        df['Primary_Flag']=df.primary_flag
        df['Secondary_Flag']=df.secondary_flag
        st.write('ok')
        try:
            if 'hpweb.1' in dict_metatag['hp_design_version']:
                df=df[col_order]
            else:
                df=df[col_order_1]
        except:
            df=df[col_order]
            
        tmp_download_link = download_link(df, path_extrt(url)[2]+'.csv', 'Click here to download your data!')    
        st.markdown(tmp_download_link, unsafe_allow_html=True)
        
        t2=time.time()
        t=t2-t1
        try:
            if 'hpweb.1' in dict_metatag['hp_design_version']:
                
                st.write('time taken:',t)
                #st.table(df.style.apply(highlight_greaterthan, axis=1).applymap(color_bu, pd.IndexSlice[:,['bu']]))
                st.table(df.style.apply(highlight_greaterthan, axis=1).applymap(color_bu,
                            pd.IndexSlice[:,['bu']]).applymap(color_webs,
                                                              pd.IndexSlice[:,['web_section_id']]).applymap(color_pg,
                                                                                                            pd.IndexSlice[:,['page_content']]).applymap(color_seg,
                                                                                                                                                        pd.IndexSlice[:,['segment']]).applymap(color_lc,
                                                                                                                                                                                              pd.IndexSlice[:,['lifecycle']]).applymap(color_user,pd.IndexSlice[:,['user_profile']]).applymap(color_title,
                                                                                                                                                                                                                                                                                                        pd.IndexSlice[:,['simple_title']]).applymap(color_green_1,
                                                                                                                                                                                                                                                                                                                                                              pd.IndexSlice[:,['sub_bu','analytics_template_name','product_service_name','analytics_section']]).applymap(color_sec_flag,
                                                              pd.IndexSlice[:,['Secondary_Flag']]).applymap(color_prim_flag,
                                                              pd.IndexSlice[:,['Primary_Flag']]))
            else:
                st.write('time taken:',t)
                
                st.table(df.style.apply(highlight_greaterthan, axis=1).applymap(color_bu,
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
                                                                                                                                                            pd.IndexSlice[:,['family']]))
                                                                                                                                              
        except:
            st.write('time taken:',t)
            st.table(df.style.apply(highlight_greaterthan, axis=1).applymap(color_bu,
                            pd.IndexSlice[:,['bu']]).applymap(color_webs,
                                                              pd.IndexSlice[:,['web_section_id']]).applymap(color_pg,
                                                                                                            pd.IndexSlice[:,['page_content']]).applymap(color_seg,
                                                                                                                                                        pd.IndexSlice[:,['segment']]).applymap(color_lc,
                                                                                                                                                                                              pd.IndexSlice[:,['lifecycle']]).applymap(color_user,pd.IndexSlice[:,['user_profile']]).applymap(color_title,
                                                                                                                                                                                                                                                                                                        pd.IndexSlice[:,['simple_title']]).applymap(color_green_1,
                                                                                                                                                                                                                                                                                                                                                              pd.IndexSlice[:,['sub_bu','analytics_template_name','product_service_name','analytics_section']]).applymap(color_sec_flag,
                                                              pd.IndexSlice[:,['Secondary_Flag']]).applymap(color_prim_flag,
                                                              pd.IndexSlice[:,['Primary_Flag']]))

                                                        

            
                                                                                                           

        
    else:
        st.write("master url not working")   
        
except:
    st.write("master url not working")   
