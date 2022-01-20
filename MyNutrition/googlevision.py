import io
import os
import cv2
from google.cloud import vision
from google.cloud.vision_v1 import types
import numpy as np
import difflib
import pandas as pd
import re


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="striking-yen-304208-d708784c1463.json"
client = vision.ImageAnnotatorClient()

def ocr(imagepath):
    #image = cv2.imread('/workspace/MyNutrition/static/img/26.jpeg')
    image = cv2.imread(imagepath)
    origin = image.copy()

    r = 800.0/image.shape[0]
    dim = (int(image.shape[1]*r),800)
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3), 0)
    edged = cv2.Canny(gray, 75, 200)

    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*peri, True)

        if len(approx)==4:
            screenCnt = approx
            break

    cv2.drawContours(image, [screenCnt], -1, (0,255,0), 2)

    def order_points(pts):
        rect = np.zeros((4, 2), dtype="float32")

        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis = 1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect

    rect = order_points(screenCnt.reshape(4, 2)/r)
    (topLeft, topRight, bottomRight, bottomLeft) = rect

    w1 = abs(bottomRight[0] - bottomLeft[0])
    w2 = abs(topRight[0] - topLeft[0])
    h1 = abs(topRight[1] - bottomRight[1])
    h2 = abs(topLeft[1] - bottomLeft[1])

    maxWidth = max([w1, w2])
    maxHeight = max([h1, h2])

    dst = np.float32([[0,0], [maxWidth-1,0], [maxWidth-1, maxHeight-1], [0, maxHeight-1]])

    M = cv2.getPerspectiveTransform(rect, dst)

    warped = cv2.warpPerspective(origin, M, (maxWidth, maxHeight))
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    warped = cv2.adaptiveThreshold(warped, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 10)

    cv2.imwrite("scanned.jpeg", warped)

    file_name = os.path.join(os.path.dirname("__file__"), "scanned.jpeg")

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image,image_context={"language_hints": ["ko","en"]})
    labels = response.text_annotations

    labellist=labels[0].description.replace(',','')
    labellist=labellist.split('\n')
    print('labellist: ', labellist)

    words = ["열량","탄수화물","단백질","식이섬유","단백질","지방","콜레스테롤","나트륨","칼슘","철","마그네슘","인","칼륨","망간","셀레늄","비타민 B6","비타민 E","비타민 C","비타민 B12","리보플라빈","나이아신","비타민 K","엽산","비타민 A"]
    def get_exact_words(input_str):
        exact_words = difflib.get_close_matches(input_str,words,n=1,cutoff=0.5)
        if len(exact_words)>0:
            return exact_words[0]
        else:
            return input_str

    labellist = ' '.join(labellist)
    string = labellist.split(' ')
    exact = [get_exact_words(word) for word in string]
    exact = ' '.join(exact).split()
    print("exact: ", exact)

    e, p, fat, carbo, fiber, cal, iron, mg, pho, pot, s, zinc, mn, sel, vb6, ve, vk, vb12, ribo, nia, vc, fol, va = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    
    for word in exact:
        if 'kcal' in word:
            e = ''.join(re.findall("\\d+", exact[exact.index(word)]))
            if e is '':
                e = ''.join(re.findall("\\d+", exact[exact.index(word)-1]))
        if '단백질' in word:
            p = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '지방' in word:
            fat = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '탄수화물' in word:
            carbo = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '식이섬유' in word:
            fiber = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '나트륨' in word:
            s = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '비타민 C' in word:
            vc = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '비타민 K' in word:
            vk = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '칼슘' in word:
            cal = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '철' in word:
            iron = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '마그네슘' in word:
            mg = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '칼륨' in word:
            pot = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '아연' in word:
            zinc = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '망간' in word:
            mn = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '셀레늄' in word:
            sel = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '비타민 B6' in word:
            vb6 = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '비타민 E' in word:
            ve = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '비타민 B12' in word:
            vb12 = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '리보플라빈' in word:
            ribo = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '나이아신' in word:
            nia = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '엽산' in word:
            fol = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))
        if '비타민 A' in word:
            va = ''.join(re.findall("\d*\.\d+|\d+", exact[exact.index(word)+1]))

    df = pd.DataFrame(columns=['Energy','Protein','Fat','Carbohydrate','Dietary_Fiber','Calcium','Iron','Magnesium','Phosphorus','Potassium','Sodium','Zinc','Manganese','Selenium','Vitamin_B6','Vitamin_E','Vitamin_K','Vitamin_B12','Riboflavin','Niacin','Total_Vitamin_C','Folate','Vitamin_A'])

    new_data = {
        'Energy' : e,
        'Protein' : p,
        'Fat' : fat,
        'Carbohydrate' : carbo,
        'Dietary_Fiber' : fiber,
        'Calcium' : cal,
        'Iron' : iron,
        'Magnesium' : mg,
        'Phosphorus' : pho,
        'Potassium' : pot,
        'Sodium' : s,
        'Zinc' : zinc,
        'Manganese' : mn,
        'Selenium' : sel,
        'Vitamin_B6' : vb6,
        'Vitamin_E' : ve,
        'Vitamin_K' : vk,
        'Vitamin_B12' : vb12,
        'Riboflavin' : ribo,
        'Niacin' : nia,
        'Total_Vitamin_C' : vc,
        'Folate' : fol,
        'Vitamin_A' : va
    }
    df = df.append(new_data, ignore_index=True)
    df=df.fillna(0)
    df=df.astype(float)

    return df