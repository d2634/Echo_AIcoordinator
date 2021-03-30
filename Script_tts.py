key_list=["티셔츠"]
patterns=["P09", "P01", "P02", "P10","P03","P04","P11"]
textile=["T123", "T113", "T112", "T124","T118","T125"]
necks=["F33", "F32","F38","F37","F31","F36","F46"]
length= ['L152', 'L151', 'L153', 'L154', 'L148', 'L147', 'L149', 'L150']

text=""
def script_tts(name, price, pat, tex, neck, leng,color,sat,val):
    #color_l=color.split(',')
    text=""
    text="이 제품은 "+name+"입니다. "+"가격은 "+price+"원입니다. "
    

    if pat=='단색':
        text=text+"무늬가 없는"+color_t(color)+" 단색 제품으로 깔끔한 느낌을 줍니다. "

    elif pat=='스트라이프':
        text=text+color_add(color)+"줄무늬가 있는 제품으로 생기있는 느낌을 줍니다. "
    elif pat=='체크':
        text=text+color_add(color)+"체크무늬가 있는 제품으로 단정한 느낌을 줍니다."
    elif pat=='프린트/캐릭터':
        text=text+"앞에 그림이 프린트 되어 있는 제품으로 "
    elif pat=='플라워':
        text=text+color_add(color)+"꽃무늬가 있는 제품으로 화사한 느낌을 줍니다. "
    elif pat=='도트':
        text=text+color_add(color)+"물방울 무늬가 있는 제품으로 귀여운 느낌을 줍니다. "
    elif pat=='레터링':
        text=text+"글자가 써져 있는 제품으로 세련된 느낌을 줍니다. "
    
    text=text+s_v_text(sat,val, color)

    if tex=='면':
        text=text+"소재는 면이고 "
    elif tex=='린넨':
        text=text+"린넨 소재로 통풍이 잘 돼 시원합니다. "
    elif tex=='쉬폰':
        text=text+"쉬폰 소재로 얇고 부드럽습니다. "
    elif tex=='레이스':
        text=text+"레이스가 달려 있고 "
    elif tex=='니트':
        text=text+"따뜻한 니트 소재이고 "
    elif tex=='스팽글':
        text=text+"반짝거리는 스팽글이 달려 있어 화려한 느낌입니다. 다만 스팽글은 세탁시 잘 떨어질 수 있으니 손빨래를 해야 합니다. "

    if neck=='라운드넥':
        text=text+"목 부분이 파이지 않고 둥근 라운드넥입니다. "
    elif neck=='브이넥':
        text=text+"목 부분이 브이모양으로 파여 있습니다. "
    elif neck=='폴로카라':
        text=text+"목 부분이 셔츠같은 카라로 되어 있어 단정해 보입니다. "
    elif neck=='터틀넥':
        text=text+"목을 감싸는 폴라티입니다. "
    elif neck=='후드':
        text=text+"뒤에 모자가 달린 후드제품 입니다. "
    elif neck=='홀터넥':
        text=text+"가슴 부분의 끈을 목 뒤로 묶는 홀터넥제품 입니다. 여름에 시원하게 입기 좋습니다. "
    elif neck=='오프숄더':
        text=text+"어깨가 드러나도록 파여 있는 오프숄더입니다. "
    elif neck=='벨티드':
        text=text+"벨트로 허리를 강조하는 제품입니다. "
    
    if leng=='숏&반팔':
        text=text+"기장이 허리 위로 올라오도록 짧고 소매는 반팔입니다. "
    elif leng=='숏&긴팔':
        text=text+"기장이 허리 위로 올라오도록 짧고 소매는 손목을 가릴 정도의 긴팔입니다. "
    elif leng=='숏&7부':
        text=text+"기장이 허리 위로 올라오도록 짧고 소매는 손목이 보이는 7부입니다. "
    elif leng=='숏&민소매':
        text=text+"기장이 허리 위로 올라오도록 짧고 소매가 없는 민소매입니다. "
    elif leng=='롱&반팔':
        text=text+"기장이 엉덩이를 덮을 정도로 길고 소매는 반팔입니다. "
    elif leng=='롱&긴팔':
        text=text+"기장이 엉덩이를 덮을 정도로 길고 소매는 손목을 가릴 정도의 긴팔입니다. "
    elif leng=='롱&7부':
        text=text+"기장이 엉덩이를 덮을 정도로 길고 소매는 손목이 보이는 7부입니다. "
    elif leng=='롱&7부':
        text=text+"기장이 엉덩이를 덮을 정도로 길고 소매가 없는 민소매입니다. "
    return text

def color_t(color):
    if color=='빨':
        return '빨간색의'
    elif color=='주':
        return '주황색의'
    elif color=='노':
        return '노란색의'
    elif color=='초':
        return '초록색의'
    elif color=='파':
        return '파란색의'
    elif color=='보':
        return '보라색의'
    elif color=='핑':
        return '핑크색의'
    elif color=='검':
        return '검은색의'
    elif color=='회':
        return '회색의'
    elif color=='갈':
        return '갈색의'
    elif color=='흰':
        return '흰색의'
    else:
        return('')

def color_add(color):
    if color=='빨':
        return '빨간'
    elif color=='주':
        return '주황색의'
    elif color=='노':
        return '노란'
    elif color=='초':
        return '초록색의'
    elif color=='파':
        return '파란'
    elif color=='보':
        return '보라색의'
    elif color=='핑':
        return '핑크색의'
    elif color=='검':
        return '검은'
    elif color=='회':
        return '회색의'
    elif color=='흰':
        return '흰'
    else:
        return('')

def s_v_text(s,v, color):
    text1=color_t(color)+""
    if s=='파스텔' and v=='밝':
        text1=text1+" 밝고 옅은 포근한 색상이라 봄에 잘 어울립니다. "
    elif s=='파스텔' and v=='짙':
        text1=text1+" 탁하고 짙은 색상이라 차분한 느낌을 주고 겨울에 잘 어울립니다. "
    elif s=='선명'and v=='밝':
        text1=text1+" 선명하고 밝은 색상이라 생기 있어 보입니다. "
    elif s=='선명'and v=='짙':
        text1=text1+" 어둡고 선명한 색상이라 피부가 더 밝아보입니다. "
    elif s=='탁'and v=='밝':
        text1=text1+" 밝은 색상이지만 탁한 계열이라 밝은 옷을 원하지만 너무 튀지 않는 스타일을 원하시는 분께 추천드립니다."
    elif s=='탁'and v=='짙':
        text1=text1+" 탁하고 어두운 색상이라 차분한 느낌을 주고 겨울에 잘 어울립니다. "
    
    return text1
    

print(script_tts('리바이스 시그니처 티셔츠','30000','단색','면','라운드넥','숏&긴팔','빨','탁','밝'))