#!/usr/bin/env python
# coding: utf-8

# ## 형태소 분석기

# In[24]:


# MeCab installation needed
from eunjeon import Mecab
# from eunjeon import Mecab

def do_mecab(text):
    mecab = Mecab()

    me_list=mecab.pos(text)
    after=[]
    for t in me_list:
        if t[1][0] == 'N' or t[1][0] =='V':#s랑 m도 더함
            after.append(t)
    print(after)
    return me_list

# In[25]:


#질문 1-어떤 옷인지
cloth={'가디건':['가디건','카디건'], '스웨터':['스웨터'], '베스트':['베스트','배스트','조끼'], '코트':['코트'],'자켓':['자켓','아우터','외투','재킷'],
       '블라우스':['블라우스','블루스'], '셔츠':['셔츠'], '티셔츠':['티셔츠','티'], '원피스':['원피스','드레스'], '치마':['치마','스커트'], '바지':['바지','팬츠'], '점퍼':['점퍼','잠바']}
u_pat={'단색': ['단색','민무늬','민'], '스트라이프': ['스트라이프','줄무늬'], '체크': ['체크','체크무늬','격자','격자무늬','바둑판무늬','바둑판'], 
       '프린트/캐릭터': ['프린팅','캐릭터','그림'], '플라워': ['플로럴','꽃무늬','꽃','플라워'], '도트': ['땡땡이','도트','점박이','물방울','물방울무늬'],
       '호피': ['호피','호피무늬'], '찢어진청': ['찢'],'레터링': ['레터링','글자','글씨']}
u_mat={'면': ['면'], '린넨': ['린넨','마','마소재'], '데님': ['청', '데님'], '쉬폰': ['쉬폰','하늘하늘','시폰','부드러운'], 
        '레이스': ['레이스'],
       '모직': ['모직','모','모소재'], '니트(스웨터)': ['니트','울','울소재'], '가죽': ['가죽'], '퍼(fur)': ['퍼','모피'],
       '코듀로이': ['코듀로이','골덴'], '트위드': ['트위드'], '패딩': ['패딩','파카']}
u_sty={'라운드넥': ['둥근','라운드'], '브이넥': ['브이'], '폴로카라': ['폴로','카라'],'U넥': ['파인'], '터틀넥': ['폴로','터틀넥','터틀'],
       '사파리/야상': ['야상'], '더플': ['더플','떡볶이'], '후드': ['후드','후디'], '케이프/망토': ['케이프','망토'], '프릴/셔링': ['프릴','주름'],
       '오프숄더': ['오프','숄더'], '벨티드': ['벨트'], 'H라인': ['h','에이치','에이치라인'], 'A라인': ['a','에이라인','에이'], '플레어': ['나풀나풀','나폴나폴','나풀거리'], 
       '뷔스티에': ['뷔스티에','비스티에','뷔스테','뷔스태','비스테','비스태'], '하이웨스트': ['배','하이'], '집업': ['집업','지퍼'], '스키니': ['스키니','붙'],
       '슬림/세미배기': ['슬림','날씬'],
       '일자핏': ['일자', '통자'], '와이드': ['와이드','퍼지','나팔바지','나팔'], '부츠컷': ['부츠컷','부츠'], '레깅스': ['레깅스','쫄쫄이'],  '점프수트/멜빵': ['멜빵','점프수트','점프'],'정장팬츠': ['정장','수트'], '치마바지': ['치마바지']}
u_len={'숏': ['크롭','숏','반'], '숏&반팔': ['크롭','반팔'], '숏&긴팔': ['크롭','숏','긴팔','긴'], '롱': ['롱'], '하프': ['롱'], '숏&7부': ['숏','7','반','칠부','칠보','칠'], '숏&민소매': ['숏','크롭','민소매','나시'], '롱&반팔': ['롱','반팔'],
       '롱&긴팔': ['롱','긴팔'], '롱&7부': ['롱','7','칠부','칠보','칠'], '롱&민소매': ['롱','민소매','나시'], '미니&반팔 원피스': ['미니','반팔'], '미니': ['미니'], '미디': ['중간','미디'], '미니&긴팔 원피스': ['미니','긴팔','긴'],
       '미니&7부 원피스': ['미니','7','칠부','칠보','칠'], '미니&민소매 원피스': ['미니','민소매','나시'], '미니&오프숄더 원피스': ['미니','오프숄더'], '미디&반팔 원피스': ['미디','중간','반팔'], '미디&긴팔 원피스': ['미디','긴팔','긴'],
       '미디&7부 원피스': ['미디','중간','7','칠부','칠보','칠'], '미디&민소매 원피스': ['미디','중간','민소매','나시'], '미디&오프숄더 원피스': ['미디','중간','오프숄더'], '롱&반팔 원피스': ['롱','반팔'], '롱&긴팔 원피스': ['롱','긴팔'],
       '롱&7부 원피스': ['롱','7','칠부','칠보','칠'], '롱&민소매 원피스': ['롱','민소매','나시'], '롱&오프숄더 원피스': ['롱','오프숄더'], '핫팬츠': ['핫팬츠'], '반바지': ['반바지'], '긴바지': ['긴바지','긴'], '7부바지': ['7','칠부','칠보','칠']}
p_compare={'이상': ['이상','비쌌','비싼','높','위'],'이하':['이하','쌌','싼','싸','저렴','아래','낮','밑','이내'],'정도':['정도','쯤','내외','가량'],'대':['대','대로'],}


# In[19]:



def test_n(word,dic,n_after2,final):
    for key, val in dic.items():
        for v in val:
            if v in word:
                if word == v:
                    final.append(key)
                    return (n_after2,final)
                else:
                    r_w=word.replace(v,'')
                    n_after2.append(r_w)
                    final.append(key)
                    return (n_after2,final)
    return (n_after2,final)


# In[20]:


def test_other(word,dic,final):
    for key, val in dic.items():
        for v in val:
            if word == v:
                final.append(key)
                return final
    return final


# In[21]:


def test_len(word,dic,n_after,final):
    for key, val in dic.items():
        for v in val:
            if v in word:
                final.append(key)
                if word != v:
                    r_w=word.replace(v,'')
                    n_after.append(r_w)
            else:
                n_after.append(word)
    return n_after


# In[22]:


def remove_dup(d_list):
    me_set=set(d_list)
    r_d=list(me_set)
    return r_d


# In[26]:


#어떤 옷인지
def Q_1(me_list):
    final=[]
    n_after=[]
    n_after2=[]
    
    for t in me_list:
        if t[1][0] == 'N':
            n_after=test_len(t[0],u_len,n_after,final)
        elif t[1][0] =='V' or t[1][0] =='S' or t[1][0] =='M':#s랑 m도 더함
            final=test_other(t[0],cloth,final)
            final=test_other(t[0],u_pat,final)
            final=test_other(t[0],u_mat,final)
            final=test_other(t[0],u_sty,final)
            final=test_other(t[0],u_len,final)
    
    n_after=remove_dup(n_after)
    #print(n_after)
    for n in n_after:
        (n_after2, final)=test_n(n,cloth,n_after2,final)
        (n_after2, final)=test_n(n,u_pat,n_after2,final)
        (n_after2, final)=test_n(n,u_sty,n_after2,final)
        (n_after2, final)=test_n(n,u_mat,n_after2,final)
        (n_after2, final)=test_n(n,u_len,n_after2,final)
    
    n_after2=remove_dup(n_after2)
    
    if n_after2:
        for n2 in n_after2:
            final=test_other(n2,cloth,final)
            final=test_other(n2,u_pat,final)
            final=test_other(n2,u_sty,final)
            final=test_other(n2,u_mat,final)
            final=test_other(n2,u_len,final)
        print(final)
    
    f_dic={'cloth':[],'pattern':[],'material':[],'style':[],'length':[]}

    for f in final:
        if f in list(cloth.keys()):
            f_dic['cloth'].append(f)
        elif f in list(u_pat.keys()):
            f_dic['pattern'].append(f)
        elif f in list(u_mat.keys()):
            f_dic['material'].append(f)
        elif f in list(u_sty.keys()):
            f_dic['style'].append(f)
        elif f in list(u_len.keys()):
            f_dic['length'].append(f)
    for key, value in list(f_dic.items()):
        if not value:
            del f_dic[key]
    return f_dic


# In[8]:


#가격 질문
def Q_2(me_list):
    num_l=[]
    index=0
    state=""
    for t in me_list:
        if t[1][0] == 'N' or t[1][0] =='V' or t[1][0] =='X':
            if t[1]=='NR':
                if t[0]=='만':
                    if num_l:
                        num_l[index-1]=num_l[index-1]*10000
                    else:
                        num_l.append(10000)
                        index=index+1
            for key, val in p_compare.items():
                for v in val:
                    if v in t:
                        state=key
        elif t[1]=='SN':
            num_l.append(int(t[0]))
            index=index+1
        elif t[1]=='JKB' and t[0]=='대로':
            state='대'
            
    if len(num_l)>1:
        return("사이",num_l)
    else:
        return(state,num_l)

#print(Q_2(me_list))

me_list=do_mecab(u'긴팔 후드 티셔츠 찾아줘')
fin=Q_1(me_list)
#fin=remove_dup(fin)
print("final",fin)
# In[ ]:




