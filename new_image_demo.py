import torch
import os
import cv2
from yolo.utils.utils import *
from predictors.YOLOv3 import YOLOv3Predictor
#from predictors.DetectronModels import Predictor
import glob
from tqdm import tqdm
import sys
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import urllib.request


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.cuda.empty_cache()


#YOLO PARAMS
yolo_df2_params = {   "model_def" : "F:\cloth_yolo\Clothing-Detection-master/yolo/df2cfg/yolov3-df2.cfg",
"weights_path" : "F:\cloth_yolo\Clothing-Detection-master/yolo/weights/yolov3-df2_15000.weights",
"class_path":"F:\cloth_yolo\Clothing-Detection-master/yolo/df2cfg/df2.names",
"conf_thres" : 0.5,
"nms_thres" :0.4,
"img_size" : 416,
"device" : device}

yolo_modanet_params = {   "model_def" : "yolo/modanetcfg/yolov3-modanet.cfg",
"weights_path" : "yolo/weights/yolov3-modanet_last.weights",
"class_path":"yolo/modanetcfg/modanet.names",
"conf_thres" : 0.5,
"nms_thres" :0.4,
"img_size" : 416,
"device" : device}


#DATASET
dataset = 'df2'


if dataset == 'df2': #deepfashion2
    yolo_params = yolo_df2_params

if dataset == 'modanet':
    yolo_params = yolo_modanet_params


#Classes
classes = load_classes(yolo_params["class_path"])

#Colors
cmap = plt.get_cmap("rainbow")
colors = np.array([cmap(i) for i in np.linspace(0, 1, 13)])
#np.random.shuffle(colors)



#


model = 'yolo'

if model == 'yolo':
    detectron = YOLOv3Predictor(params=yolo_params)
else:
    detectron = Predictor(model=model,dataset= dataset, CATEGORIES = classes)

#Faster RCNN / RetinaNet / Mask RCNN

Kardi=["long sleeve top","long sleeve outwear"] #가디건
knit=["long sleeve top","short sleeve top","long sleeve outwear"] #니트
vest=["vest","short sleeve top","short sleeve outwear"] #베스트
coat=["long sleeve outwear","long sleeve top"] #코트
jacket=["long sleeve outwear","long sleeve top","short sleeve outwear"] #자켓
blouse=["long sleeve top"] #블라우스
shirt=["long sleeve top"] #셔츠
T_s=["long sleeve top","short sleeve top","sling"] #티셔츠
dress=["short sleeve dress","long sleeve dress","vest dress","sling dress"] #원피스
skirt=["skirt"] #치마
pants=["shorts","trousers"] #바지
suit=["long sleeve outwear","long sleeve top","short sleeve outwear"] #수트
jumper=["long sleeve outwear","long sleeve top","short sleeve outwear"] #점퍼

def get_keylist(word):
    if(word=="가디건"):
        return Kardi
    if(word=="니트"):
        return knit
    if(word=="베스트"):
        return vest
    if(word=="코트"):
        return coat
    if(word=="자켓"):
        return jacket
    if(word=="블라우스"):
        return blouse
    if(word=="셔츠"):
        return shirt
    if(word=="티셔츠"):
        return T_s
    if(word=="원피스"):
        return dress
    if(word=="치마"):
        return skirt
    if(word=="바지"):
        return pants
    if(word=="수트"):
        return suit
    if(word=="점퍼"):
        return jumper

#색추출 퍼센트 구하기
def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    # return the histogram
    return hist

def get_color(h, s, v):
    col_list=[]

    if h>345 and h<360 and s>70 and v>25:
        col_list.append('빨')
    if h>0 and h<15 and s>5 and v >50:
        col_list.append('빨')
    if h>=335 and h<360 and s>5 and s<70 and v >70:
        col_list.append('핑')
    if h>=300 and h<345 and s>5 and v >70:
        col_list.append('핑')
    if h>0 and h<10 and s>5 and s<60 and v >90:
        col_list.append('핑')
    if h>16 and h<50 and s>5 and v >65:
        col_list.append('주')
    if h>=50 and h<70 and s>5 and v >50:
        col_list.append('노')
    if h>=70 and h<165 and s>5 and v >25:
        col_list.append('초')
    if h>=165 and h<255 and s>5 and v >25:
        col_list.append('파')
    if h>255 and h<300 and s>5 and v >25:
        col_list.append('보')
    if h>=300 and h<335 and s>5 and v >25 and v<70:
        col_list.append('보')
    if v <25:
        col_list.append('검')
    if s>0 and s<22 and v >25 and v<85:
        col_list.append('회')
    if h>345 and h<360 and s>5 and s<100 and v >25 and v<50:
        col_list.append('갈')
    if h>20 and h<50 and s>5 and s<43 and v >50 and v<80:
        col_list.append('갈')
    if h>15 and h<50 and s>33 and s<90 and v >30 and v<65:
        col_list.append('갈')
    if s>0 and s<22 and v >75 and v<100:
        col_list.append('흰')
    
    col_set = set(col_list) #집합set으로 변환
    col_list = list(col_set)

    c_string=""
    ind=0
    for col in col_list:
        if ind!=0:
            c_string=c_string+","+col
        else:
            c_string=c_string+col
        ind=ind+1

    return c_string

def get_s(s,v):
    if s>0 and s<43 and v>77 and v<100:
        s_string='파스텔'
    else:
        if s>50:
            s_string='선명'
        else:
            s_string='탁'
    return s_string

def get_v(v):
    if v>67:
        v_string='밝'
    else:
        v_string='짙'
    return v_string

dir="tests"
def cloth_yolo(url,word):
    url='http:'+url
    """path=os.path.join(dir,image)
    print(path)

    img=cv2.imread(path)
    detections=detectron.get_detections(img)"""
    """while(True):
    path = input('img path: ')
    if not os.path.exists(path):
        print('Img does not exists..')
        continue
    img = cv2.imread(path)
    detections = detectron.get_detections(img)"""

    k_list=get_keylist(word)

    resp = urllib.request.urlopen(url)
    img = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    #cv2.imshow("Image", img)
    #cv2.waitKey(0)

    detections = detectron.get_detections(img)
    #print(detections)

    if len(detections) != 0 :
        detections.sort(reverse=False ,key = lambda x:x[4])
        for x1, y1, x2, y2, cls_conf, cls_pred in detections:
                
                #print("\t+ Label: %s, Conf: %.5f" % (classes[int(cls_pred)], cls_conf))           
                
                type=classes[int(cls_pred)]
                if(type not in k_list):
                    continue

                color = colors[int(cls_pred)]
                color = tuple(c*255 for c in color)
                color = (.7*color[2],.7*color[1],.7*color[0])       
                    
                font = cv2.FONT_HERSHEY_SIMPLEX   
            
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                text =  "%s conf: %.3f" % (classes[int(cls_pred)] ,cls_conf)
                
                x=x1
                y=y1
                w=x2-x1
                h=y2-y1
                cv2.rectangle(img,(x1,y1) , (x2,y2) , color,3)

                img_trim = img[y1:y1+h, x1:x1+w]
                #print("y1",y1,"h",h,"x1",x1,"w",w)
                #print(img_trim.shape)
                
                #배경제거 코드
                mask = np.zeros(img.shape[:2],np.uint8)
                bgdModel = np.zeros((1,65),np.float64)
                fgdModel = np.zeros((1,65),np.float64)

                m_rect=(x,y,w,h)
                try:
                    cv2.grabCut(img,mask,m_rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
                except:
                    return []
                    
                mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
                img2 = img*mask2[:,:,np.newaxis]

                #plt.imshow(img2),plt.colorbar(),plt.show()
                
                #색 추출 코드
                if y<0:
                    y=0
                if x<0:
                    x=0
                #print("y:",y,"h:",h,"x",x,"w",w)
                image = img2[y:y+h, x:x+w]
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = image.reshape((image.shape[0] * image.shape[1], 3)) # height, width 통합
                #print(image.shape)

                k = 5 # 예제는 5개로 나누겠습니다
                clt = KMeans(n_clusters = k)
                clt.fit(image)

                """for center in clt.cluster_centers_:
                    print(center)"""
                #print(clt.cluster_centers_)
                
                hist = centroid_histogram(clt)
                print(hist)
                try:
                    maxi=np.max(hist)
                except ValueError:
                    return []
                
                m_index=np.where(hist==maxi)
                #print(m_index)
                m_color=clt.cluster_centers_[m_index][0]

                if(m_color[0]<2 and m_color[1]<2 and m_color[2]<2): #제일 많이 나온 부분이 배경일 때(배경을 패스하고 다음으로)
                    f_hist=np.delete(hist,m_index)
                    try:
                        maxi=np.max(f_hist)
                    except ValueError:
                        return []
                    m_index=np.where(f_hist==maxi)
                    m_color=clt.cluster_centers_[m_index][0]
                    HSV_convert = cv2.cvtColor (np.uint8 ([[m_color]]), cv2.COLOR_RGB2HSV)[0][0]
                    hsv_list=[HSV_convert[0]*2,round(HSV_convert[1]*0.392156),round(HSV_convert[2]*0.392156)]
                    #print(hsv_list)
                    return hsv_list

                #print(m_color[0], m_color[1], m_color[2])
                HSV_convert = cv2.cvtColor (np.uint8 ([[m_color]]), cv2.COLOR_RGB2HSV)[0][0] #rgb를 hsv로
                hsv_list=[HSV_convert[0]*2,round(HSV_convert[1]*0.392156),round(HSV_convert[2]*0.392156)]
                col_string=get_color(hsv_list[0],hsv_list[1],hsv_list[2])
                s_string=get_s(hsv_list[1],hsv_list[2])
                v_string=get_v(hsv_list[2])
                col_list=[]
                col_list.append(col_string)
                col_list.append(s_string)
                col_list.append(v_string)
                #print(hsv_list)
                print(col_list)
                return col_list
                
                """cv2.imwrite('org_trim.jpg', img_trim)
                org_image = cv2.imread('org_trim.jpg')
                cv2.imshow('org_image', org_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()"""
                
                
#print(urllib.request.getproxies())
#cloth_yolo("//item.ssgcdn.com/76/86/29/item/1000059298676_i1_232.jpg","티셔츠")
#cloth_yolo('http://item.ssgcdn.com/12/58/78/item/1000032785812_i1_232.jpg',"티셔츠")