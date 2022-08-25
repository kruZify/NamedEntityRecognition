from fastapi import FastAPI,Request,File,UploadFile,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import docx2txt,re,pytesseract,json
from PyPDF2 import PdfReader
import trainingModel
from model_2 import model_2
from PIL import Image
from trainingModel import Sama
from resume_parserM import resumeP
from face_recog import facer

app=FastAPI()

templates=Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/',response_class=HTMLResponse)
async def simplePost(request:Request):
    return templates.TemplateResponse("home.html",{"request":request})

@app.post('/submitform')
async def convertion(request:Request,f:UploadFile=File(...)):
    try:
        contents= await f.read()
        with open(f.filename,'wb') as L:
            L.write(contents)
    except Exception:
        return {"Message":"File Uploading Problem"}
    fext = ""
    flag = 0
    for i in f.filename:
        if (i == "."):
            flag = 1
        if (flag == 1):
            fext = fext + i
    file_extension = fext
    if (file_extension == '.docx'):
        text = docx2txt.process(f.filename)

        with open("output.txt", "w", encoding="utf-8") as text_file:
            print(text, file=text_file)

    elif (file_extension == '.pdf'):
        a = PdfReader(f.filename)
        s = ""
        n = a.numPages
        for i in range(0, n):
            s += a.getPage(i).extractText()
            with open("output.txt", 'w',encoding="utf-8") as F:
                print(s,file=F)


    elif (file_extension==".jpg" or ".jpeg" or ".png"):
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
        osd = pytesseract.image_to_osd(f.filename, config='--psm 0 -c min_characters_to_try=10')

        # print("[OSD] "+osd)
        rot = re.search('(?<=Rotate: )\d+', osd).group(0)
        print(rot)

        Original_image = Image.open(f.filename)

        angle = int(rot)

        if angle == 180:
            angle = 180 - angle
            print("[ANGLE] " + str(angle))
            rotated_image = Original_image.rotate(angle)
        elif angle == 90:
            angle = angle+90
            print("[ANGLE] " + str(angle))
            rotated_image = Original_image.rotate(angle)
        else:
            rotated_image = Original_image

        config = ('-l eng --oem 1 --psm 3')

        # pytessercat
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
        text = pytesseract.image_to_string(rotated_image, config=config)

        with open("output.txt", "w", encoding='utf-8') as text_file:
            print(text, file=text_file)
    else:
        print("Invalid file")
    mt = ""
    with open("output.txt","r+",encoding= 'utf-8') as G:
        for line in G:
            if not line.isspace():
                mt+=line
    G=open("output.txt","r+",encoding='utf-8')
    G.write(mt)
    G.close()
    H=open("output.txt","r+",encoding='utf-8')
    return templates.TemplateResponse("page2.html",{"request":request,"File":H.read()})

@app.post('/finalpage')
async def modelRun(request:Request):
        model_2.runner(self=model_2)
        with open('output.txt','r+',encoding='utf-8') as F:
            return templates.TemplateResponse("page3.html", {"request": request, "File": F.read()})

@app.get('/datavis')
async def datavis(request:Request):
    return templates.TemplateResponse("datavis.html",{"request":request})

@app.get('/resumeVis')
async def datavis(request:Request):
    return templates.TemplateResponse("resumeVis.html",{"request":request})

@app.post('/update')
async def updateModel(request:Request,sentence:str=Form(...),entity:str=Form(),label:str=Form()):
    k = len(entity)
    ls = []
    n = sentence.find(entity)
    ls.append((n,n+k-1,label))
    k={"text":sentence,"label":ls}
    with open("updateTrainer.json", "r+") as L:
        ls2=json.load(L)
        ls2.append(k)
    with open("updateTrainer.json", "w") as M:
        json.dump(ls2,M)
    Sama.SamaModel(self=trainingModel)
    model_2.runner(self=model_2)

    with open('output.txt', 'r+', encoding='utf-8') as F:
        return templates.TemplateResponse("page3.html", {"request":request,"File": F.read()})

@app.post('/face')
async def face_rec(request:Request,fl:UploadFile=File(...)):
    try:
        contents= await fl.read()
        with open(fl.filename,'wb') as L:
            L.write(contents)
    except Exception:
        return {"Message":"File Uploading Problem"}
    f=facer()
    f.facerReg(fl)
    fext = ""
    flag = 0
    for i in fl.filename:
        if (i == "."):
            flag = 1
        if (flag == 1):
            fext = fext + i
    file_extension = fext
    if (file_extension == '.docx'):
        text = docx2txt.process(fl.filename)

        with open("output2.txt", "w", encoding="utf-8") as text_file:
            print(text, file=text_file)

    elif (file_extension == '.pdf'):
        a = PdfReader(fl.filename)
        s = ""
        n = a.numPages
        for i in range(0, n):
            s += a.getPage(i).extractText()
            with open("output2.txt", 'w', encoding="utf-8") as F:
                print(s, file=F)
    mt = ""
    with open("output2.txt", "r+", encoding='utf-8') as G:
        for line in G:
            if not line.isspace():
                mt += line
    G = open("output2.txt", "r+", encoding='utf-8')
    G.write(mt)
    G.close()
    vals=resumeP.resumer(self=resumeP)
    return vals

