# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 11:10:21 2021

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
from flask import Flask, request, render_template,jsonify
app = Flask(__name__)
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



class my_dictionary(dict): 
 
    def __init__(self): 
        self = dict() 
 
    def add(self, key, value): 
        self[key] = value 
dict_metatag=my_dictionary()

def path_extrt(url):
    fr=""
    sc=""
    fl_nm=""
    pattern=r"^https://[a-zA-Z0-9]+\.[hp]+\.com/[a-z]+\-[a-z]+"
    pat=r"^https://[a-zA-Z0-9]+\.[hp]+\.com/"
    pattern1=r"^https://[a-zA-Z0-9]+\.[hp]+\.com/[a-z]+\/[a-z]+"
    pat1=r"^https://[a-zA-Z0-9]+\.[hp]+\.com/"
    pattern2=r"^https://www.omen.com/[a-z]+\/[a-z]+"
    pat2=r"^https://www.omen.com/"
    if re.search(pattern,url):
        fr=re.findall(pattern,url)[0]
        sc=re.sub(fr, "",url)
        fr=re.findall(pat,url)[0]
    elif re.search(pattern1,url):
        fr=re.findall(pattern1,url)[0]
        sc=re.sub(fr, "",url)
        fr=re.findall(pat1,url)[0]
    elif re.search(pattern2, url):
        fr=re.findall(pattern2,url)[0]
        sc=re.sub(fr, "",url)
        fr=re.findall(pat2,url)[0]
    fl_nm=fr+sc
    fl_nm=fl_nm.replace("/","_").replace('.',"").replace(':',"")
       
    return fr,sc,fl_nm

    
metatag_ref = pd.DataFrame(
        columns=(
            "master_url",
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

columns=[   "master_url",
                            "bu",
                            "web_section_id",
                            "page_content",
                            "segment",
                            "lifecycle",
                            "user_profile",
                            "hp_design_version",
                            "simple_title",
                            "analytics_template_name",
                            "product_service_name",
                            "analytics_section",
                            "sub_bu",
                            ]
columns1=[   "master_url",
                            "bu",
                            "web_section_id",
                            "page_content",
                            "segment",
                            "lifecycle",
                            "user_profile",
                            "hp_design_version",
                            "simple_title",
                            "page_level",
                            "product_type",
                            "family",
                            "analytics_template_name",
                            "product_service_name",
                            "analytics_section",
                            "sub_bu",
                            ]


def tag_extractor(comb,url):
    """
    
    Parameters
    ----------
    comb : combination of locale.
    Returns
    -------
    dict_metatag1 :  A dictionary with all the 
    required metatags from the respective page.
    url1 : The url requested for.
    r1.url : The url, from where response is coming from
    """
    

    token=str(random.randint(0,1000))
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                'cache-control': "no-cache",
                'postman-token': token
                }
    url1=path_extrt(url)[0]+comb+path_extrt(url)[1]
    print(url1)
    try:
        r1=requests.get(url1,headers=headers,timeout=30)
        print(url1)
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
            print(dict_metatag1, url1)
            return dict_metatag1, url1, r1.url
                        

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
                    return dict_metatag1, url1, r1.url
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
                return dict_metatag1, url1, r1.url
        except:
            pass
##configure the log file        
def tag_extractor_wrap(cc_ll,master_url):
    """
    
    Parameters
    ----------
    cc_ll : combination of locale variant.
    Returns
    -------
    df1 : uses folder_tag_extractor as a intermediate function and wraps the 
    metatags within a dataframe.
    """
    dict2=my_dictionary()
    try:
        dict2, url, url2=tag_extractor(cc_ll,master_url)
        print(cc_ll, dict2)
        try:
            df1 = pd.DataFrame(
                columns=(
                    "url",
                    "primary_flag",
                    "redirect",
                    "redirected_url",
                   # "status",
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
                
                elif col == "redirect":

                    if url2 != url:
                        df1.loc[1, col] = 1
                    else:
                        df1.loc[1, col] = 0
                elif col=="redirected_url":
                    df1.loc[1,col]=url2
                else:
                    try:

                        df1.loc[1, col]=dict2[col]
                    except:
                        df1.loc[1, col]=""
            print(df1)
            return df1
        except:
            df1 = pd.DataFrame(
                columns=(
                    "url",
                    "primary_flag",
                    "redirect",
                    "redirected_url",
                   # "status",
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
                
                elif col == "redirect":

                    if url2!= url:
                        df1.loc[1, col] = 1
                    else:
                        df1.loc[1, col] = 0
                elif col=="redirected_url":
                    df1.loc[1,col]=url2
                else:
                    try:

                        df1.loc[1, col]=dict2[col]
                    except:
                        df1.loc[1, col]=""
            
            return df1
    
    except:
        print(cc_ll)
        pass
df = pd.DataFrame()
text1=""
def do_something(text1):
   url = text1
   token=str(random.randint(0,1000))
   headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',

                    'cache-control': "no-cache",
                    'postman-token': token
                    }
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
        metatag_ref = pd.DataFrame(
        columns=(
            "master_url",
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
       
        print(dict_metatag)
        for col in metatag_ref.columns:
                    if col == "master_url":
                        metatag_ref.loc[1, col] = url
                    else:
                        try:
                            metatag_ref.loc[1, col]=dict_metatag[col]
                        except:
                            metatag_ref.loc[1, col]=""
        #             try:
        #                 if 'hpweb.2' in dict_metatag['hp_design_version']:
        #                     metatag_ref=metatag_ref.to_json()
        #                     return metatag_ref
        #                 else:
        #                     metatag_ref=metatag_ref[columns]
        #                     metatag_ref=metatag_ref[columns1].to_json()
        #                     return(metatag_ref)
        #             except:
        #                 metatag_ref=metatag_ref[columns].to_json()
        #                 return(metatag_ref)
        metatag_ref=metatag_ref.to_json()  
        global res
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
        #fr, sc=path_extrt(url)[0],path_extrt(url)[1]
        try:
            print('start',url)
            # with ThreadPoolExecutor(max_workers=20) as T:
            #     res = list(T.map(tag_extractor_wrap, list_comb, url))
            #     for row in res:
            #         df = df.append(row)
            for i in list_comb[0:5]:
                res=tag_extractor_wrap(i, url)
                print('final df',res)
                df=df.append(res)
            #print(df)
            #df=df.to_json()
            print('end',df)
            df['index'] = list(range(len(df.index)))
            df=df.set_index('index')
            df=df.to_json(orinet='index')
        except Exception as error:
            print('exception')
            print(error)
        #print(df)    
   return metatag_ref,df
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/join', methods=['GET','POST'])

def my_form_post():
    text1 = request.form['text1']
    word = request.args.get('text1')
    combine, df = do_something(text1)
    result = {
        "output": combine,
        "output2": df
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)
if __name__ == '__main__':
    app.run(debug=True)
