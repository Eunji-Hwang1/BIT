from flask import Flask, render_template, request, redirect , jsonify
from flask_debugtoolbar import DebugToolbarExtension
from PIL import Image
from diffusers import StableDiffusionPipeline
from auth_token import auth_token
from torch import autocast
import os
from io import BytesIO
import base64
import torch
import urllib.parse
import urllib.request
import stdlist
#import datalist
import std_CompVis
import std_tutorial
import std_img_img
import json
import testimage as tt
from natsort import natsorted

application = Flask(__name__)
application.config["RED"] = 0

client_id = "xOWKTKM4eSgEdm0ioV8M"
client_secret = "8Z3An53CPh"

#메인 사이트 출력
@application.route("/")
def hello():
    std_list = stdlist.load_list()  #이미지 리스트 불러오기
    length=len(std_list)
    photo_list = []

    for f in natsorted(os.listdir('static/img')):
        if 'jpeg' in f:
            photo_list.append(f)
            
    return render_template("simple.html", std_list = std_list, length=length, photo_list=photo_list)


#파일 업로드
@application.route("/upload_done", methods=["POST"])
def upload_done():
    uploaded_file = request.files.get("file") 
    print(uploaded_file)
    if uploaded_file:
        file_path = f'static/uploaded/_{stdlist.Now_idx()}.png'
        uploaded_file.save(file_path)
        return jsonify({'success': True, 'image_path': file_path})
    else:
        return jsonify({'success': False, 'message': 'No image file provided'})

#정보 가져오기, 이미지 생성, 출력
@application.route("/search", methods=["get"])
def create_info():
    data = request.args
    pprompt = data.get("ptext")
    nprompt = data.get("ntext")
    filter = data.get("filter_num")
    
    pencText = urllib.parse.quote(pprompt)  # 번역할 한국어 텍스트를 URL 인코딩
    nencText=urllib.parse.quote(nprompt)
    pdata = "source=ko&target=en&text=" + pencText  # 번역할 텍스트와 번역 언어 설정
    ndata="source=ko&target=en&text=" + nencText 
    url = "https://openapi.naver.com/v1/papago/n2mt"  # 번역 API의 URL
    req = urllib.request.Request(url)  # 변수 이름을 request 대신 req로 변경
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)
    
    #번역
    presponse = urllib.request.urlopen(req, data=pdata.encode("utf-8"))
    presponse_body = presponse.read()
    presult = json.loads(presponse_body.decode('utf-8'))  # JSON 형식으로 파싱
    ptranslated_text = presult['message']['result']['translatedText']  # 번역된 텍스트 추출

    if nprompt==None:
        ntranslated_text=""
    else:
        nresponse = urllib.request.urlopen(req, data=ndata.encode("utf-8"))
        nresponse_body = nresponse.read()
        nresult = json.loads(nresponse_body.decode('utf-8'))  # JSON 형식으로 파싱
        ntranslated_text = nresult['message']['result']['translatedText']  # 번역된 텍스트 추출
    #필터랑 파일 데이터 처리
    if filter=="":
        print("필터를 입력해주세요")

    #필터에 따른 생성모델로 이동
    if(filter=="실사화"):
        std_CompVis.compvis(ptranslated_text, filter)
        situation=tt.test(ptranslated_text, ntranslated_text, filter, "static/testimg/"+ptranslated_text+".jpeg")
    elif(filter=="애니메이션화"):
        std_tutorial.stdv1_5(ptranslated_text, ntranslated_text, filter)     
        situation=tt.test(ptranslated_text, ntranslated_text, filter, "static/testimg/"+ptranslated_text+".jpeg")
    
    if(situation==0):
        image_path = f"static\img\{stdlist.Now_idx()}.jpeg"  # 이미지 파일 경로
        image = Image.open(image_path)  # 이미지를 로드합니다.
        image_data = BytesIO()
        image.save(image_data, format='JPEG')
        encoded_image = base64.b64encode(image_data.getvalue()).decode("utf-8")
    
        # 이미지 URL 생성
        url_encoded_image = urllib.parse.quote(encoded_image)
        image_url = f"data:image/jpeg;base64,{url_encoded_image}"
        stdlist.save(ptranslated_text,ntranslated_text,filter) 
        response_data={"prompt":ptranslated_text}
        image_file=f"img/{stdlist.Now_idx()-1}.jpeg"
        return jsonify(response_data=response_data, image_file=image_file) 
    elif(situation==1):
        return redirect(f"/can't_create/1/?pprompt={pprompt}&nprompt={nprompt}&filter={filter}")
    elif(situation==2):
        return redirect(f"/can't_create/2/?pprompt={ptranslated_text}&nprompt={ntranslated_text}&filter={filter}")

@application.route("/search2", methods=["get"])
def create_info2():
    data = request.args
    pprompt = data.get("ptext")
    image_url=data.get("data_url")
    
    pencText = urllib.parse.quote(pprompt)  # 번역할 한국어 텍스트를 URL 인코딩
    pdata = "source=ko&target=en&text=" + pencText  # 번역할 텍스트와 번역 언어 설정
    url = "https://openapi.naver.com/v1/papago/n2mt"  # 번역 API의 URL
    req = urllib.request.Request(url)  # 변수 이름을 request 대신 req로 변경
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)
    
    #번역
    presponse = urllib.request.urlopen(req, data=pdata.encode("utf-8"))
    presponse_body = presponse.read()
    presult = json.loads(presponse_body.decode('utf-8'))  # JSON 형식으로 파싱
    ptranslated_text = presult['message']['result']['translatedText']  # 번역된 텍스트 추출
    
    #필터에 따른 생성모델로 이동
    std_img_img.img_to_img(ptranslated_text, image_data)
    situation=tt.test(ptranslated_text, "", "", "static/testimg/"+ptranslated_text+".jpeg")
    
    if(situation==0):
        image_path = f"static\img\{stdlist.Now_idx()}.jpeg"  # 이미지 파일 경로
        image = Image.open(image_path)  # 이미지를 로드합니다.
        image_data = BytesIO()
        image.save(image_data, format='JPEG')
        encoded_image = base64.b64encode(image_data.getvalue()).decode("utf-8")
    
        # 이미지 URL 생성
        url_encoded_image = urllib.parse.quote(encoded_image)
        image_url = f"data:image/jpeg;base64,{url_encoded_image}"
        stdlist.save(ptranslated_text,"",filter) 
        response_data={"prompt":ptranslated_text}
        image_file=f"img/{stdlist.Now_idx()-1}.jpeg"
        print(image_file)
        return jsonify(response_data=response_data, image_file=image_file) 
    elif(situation==1):
        return redirect(f"/can't_create/1/?pprompt={pprompt}&nprompt=_&filter=_")
    elif(situation==2):
        return redirect(f"/can't_create/2/?pprompt={ptranslated_text}&nprompt=_&filter=_")


@application.route("/open_result")
def result():
    image_url=request.args.get("image_url")
    return render_template('result.html', photo=image_url)

@application.route("/list")
def list():
    std_list = stdlist.load_list()
    length=len(std_list)
    photo_list = []

    for f in natsorted(os.listdir('static/img')):
        if 'jpeg' in f:
            photo_list.append(f)

    return render_template("simple/simple.html", std_list = std_list, length=length, photo_list=photo_list)

@application.route("/detail_info/<int:index>/")
def detail(index):
    d_info = stdlist.load_std(index)
    pprompt=d_info["pprompt"]
    nprompt=d_info["nprompt"]
    filter=d_info["filter"]

    photo= f"img/{index}.jpeg"
    return render_template("detail_info.html", pprompt=pprompt, nprompt=nprompt, filter=filter, photo=photo)

@application.route("/can't_create/<int:situation>/")
def fail(situation):
    red = application.config.get("RED", 0)
    pprompt=request.args.get("pprompt")
    nprompt=request.args.get("nprompt")
    filter=request.args.get("filter")
    if red==10:
        situation=situation
        application.config["RED"]=0
        return render_template("fail.html", index=situation, pprompt=pprompt, nprompt=nprompt, filter=filter)
    else:
        application.config["RED"]+=1
        situation=3
        return render_template("fail.html", index=situation, pprompt=pprompt, nprompt=nprompt, filter=filter)
    
if __name__ == "__main__":
    application.run(debug=True, use_reloader=True)
