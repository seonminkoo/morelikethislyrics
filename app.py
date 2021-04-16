import streamlit as st
import pandas as pd
import numpy as np
import SessionState

DATA_PATH = "C:/Users/thekoo/python_da/ailab/data/final_table_rm.csv"
@st.cache
def load_data():
    data = pd.read_csv(DATA_PATH)
    
    print(data.head())
    return data

def find_song(data, user_input):
    src = str(user_input)
    res = data.loc[data['title'].str.contains(src)]
    
    if len(res) == 0:
        st.markdown("**해당 곡이 존재하지 않습니다.**")
    
    return res

def similar_song(nb): #검색할 곡의 neighbor 값 받아서 df로 return
    #st.write(nb)
    #tmp = nb[1:-1]
    #tmp = tmp.replace(',', '')
    #tmp = list(tmp.split())
    #tmp = list(map(int, tmp))
    
    df1 = data.loc[data['Unnamed: 0'] == nb]
    
    
    #for t in tmp[1:]:
     #   df2 = data.loc[data['song_id'] == t]
      #  df1 = pd.concat([df1, df2])
    
    return df1

st.title('가사 기반 추천곡 검색')

data = load_data()
#if st.checkbox('Show raw data'):
#    st.write(data)

row1_0, row1_1 = st.beta_columns([5, 1])
l1, l2, l3, right  = st.beta_columns([1, 1, 1.4, 3.5])
col1, co12 = st.beta_columns(2)

ss = SessionState.get(i=0)

with row1_0:
    source = st.text_input("")
    search = find_song(data, source)
    
    if len(search) > 1 and len(search) != 14575:
        st.write(search[['artist', 'title']])

with row1_1:
    st.write("\n")
    st.write("\n")
    if st.button("SEARCH"):
        st.write("")

with l3:
    if len(search) == 1:
        btn = st.button("<\n 이전 추천곡")
        if btn:
            if ss.i == 0:
                st.write("**첫 번째 곡입니다!**")
                btn = False
            else:
                ss.i -= 1
                st.write(ss.i)
                btn = False

with right:
    if len(search) == 1:
        btn = st.button(">\n 다음 추천곡")
        if btn:
            if ss.i == 4:
                ss.i = 0
                #st.write(ss.i)
                btn = False
            else:
                ss.i += 1
                #st.write(ss.i)
                btn = False
        
with col1: 
    st.subheader("")
    if len(search) == 1:
        st.write("가수: " + "**" + str(search.iloc[0,4]) + "**" )
        st.write("제목: " + "**" + str(search.iloc[0,3]) + "**" )
        st.text_area(' ', value= search.iloc[0,2], height = 300)
        
with co12: 
    st.subheader("")
    if len(search) == 1:
        # st.write(search.iloc[0,-1])
        nb = search.iloc[0, 9+ss.i]
        #similar = similar_song(nb)
        similar = data.loc[data['Unnamed: 0'] == nb]
        
        artist = st.write("가수: " + "**" + str(similar.iloc[0,4]) + "**" )
        title = st.write("제목: " + "**" + str(similar.iloc[0,3]) + "**" )
        lyrics = st.text_area(' ', value = similar.iloc[0,2], height = 300)
         