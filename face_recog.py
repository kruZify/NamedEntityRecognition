import fitz
import io,cv2,os
from PIL import Image
from docx2python import docx2python
class facer:
    def facerReg(self,f):
        fext = ""
        flag = 0
        for i in f.filename:
            if (i == "."):
                flag = 1
            if (flag == 1):
                fext = fext + i
        file_extension = fext
        if (file_extension==".pdf"):
            file = f.filename
            pdf_file = fitz.open(file)
            for page_index in range(len(pdf_file)):
                # get the page itself
                page = pdf_file[page_index]
                image_list = page.getImageList()
                # printing number of images found in this page
                if image_list:
                    print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
                else:
                    print("[!] No images found on page", page_index)
                for image_index, img in enumerate(page.getImageList(), start=1):
                    xref = img[0]
                    base_image = pdf_file.extractImage(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    image = Image.open(io.BytesIO(image_bytes))
                    # save it to local disk
                    image.save(open(r"D:\API\fastAPI\NER\faces/image{page_index+1}_{image_index}.{image_ext}","wb"))


        else:
            docx2python(f.filename, 'faces')

        directory = r'D:\API\fastAPI\NER\faces'

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        for filename in os.listdir(directory):
            tempFile=directory+'\\'+filename
            img = cv2.imread(tempFile)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 10)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            path = r'D:\API\fastAPI\NER\faces_Human'
            length = len(faces)
            if(length >= 1):
                cv2.imwrite(os.path.join(path, filename), img)
