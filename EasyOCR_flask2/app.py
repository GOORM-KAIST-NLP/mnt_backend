import os
from flask import Flask, flash, jsonify, request, redirect
from werkzeug.utils import secure_filename
import easyocr
from translator import Translator
from Use_EasyOCR import ocr
from Use_EasyOCR import plt_imshow
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

reader = easyocr.Reader(['ko'], True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
FILE_DIR = 'files'

app = Flask(__name__)

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

translator_obj = Translator()

if not os.path.exists(FILE_DIR):
    os.makedirs(FILE_DIR)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 게시물 요청에 파일 부분이 있는지 확인
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # 사용자가 파일을 선택하지 않으면 브라우저도
        # 파일 이름 없이 빈 부분 제출
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = FILE_DIR + '/' + secure_filename(file.filename)
            file.save(filename)
            parsed = reader.readtext(filename)
            input_text = list(map(lambda x: x[1], parsed))
            print(input_text) #list안에 저장
            inin = '<br/>\n'.join(map(lambda x: x, input_text)) #str형태
            print('-------------------')
            # 파일 업로드 처리
            src_lang = 'ko'
            tgt_lang = 'en'
            output = []
            for i in range(len(input_text)):
                output.append(translator_obj.translate(input_text[i], src_lang, tgt_lang))
            print(output)

            outt = '<br/>\n'.join(map(lambda x: x, output))
            ans = inin + '<br/>' + outt #한글 + 영어(번역)
            print(ans)

            # 글자 인식 상자 생성
            # output : 간판글자를 영어로 번역된 값, filename : 이미지가 있는 경로, parsed: 글자 인식 좌표가 포함된 값
            img, resultName = ocr(output, filename, parsed)

            # 출력 이미지 표시
            plt_imshow(img, figsize=(16,10))

            datas = {}
            datas['text'] = []
            for i in range(len(input_text)):
                datas['text'].append({'korean': input_text[i], 'trans': output[i]})

            datas = json.dumps(datas, ensure_ascii=False)
            datas
            print(datas)

            return (datas)


    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/api', methods=['POST'])
def upload_file_api():
    datas = {}
    datas['text'] = []

        # 게시물 요청에 파일 부분이 있는지 확인
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # 사용자가 파일을 선택하지 않으면 브라우저도
    # 파일 이름 없이 빈 부분 제출
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = FILE_DIR + '/' + secure_filename(file.filename)
        file.save(filename)
        parsed = reader.readtext(filename)
        input_text = list(map(lambda x: x[1], parsed))
        print(input_text) #list안에 저장
        inin = '<br/>\n'.join(map(lambda x: x, input_text)) #str형태
        print('-------------------')
        # 파일 업로드 처리
#        src_lang = 'ko'
#        tgt_lang = 'en'
        src_lang = 'kor'
        tgt_lang = 'eng'
        output = []
        for i in range(len(input_text)):
            output.append(translator_obj.translate(input_text[i], src_lang, tgt_lang))
        print(output)

        outt = '<br/>\n'.join(map(lambda x: x, output))
        ans = inin + '<br/>' + outt #한글 + 영어(번역)
        print(ans)

        # 글자 인식 상자 생성
        # output : 간판글자를 영어로 번역된 값, filename : 이미지가 있는 경로, parsed: 글자 인식 좌표가 포함된 값
        img, resultName = ocr(output, filename, parsed)

        # 출력 이미지 표시
        # plt_imshow(img, figsize=(16,10))

        texts = []
        for i in range(len(input_text)):
            texts.append({
                'original_text': input_text[i], 
                'trans_text': output[i]
            })

        datas['url'] = resultName
        datas['text'] = texts
        datas = json.dumps(datas, ensure_ascii=False)
        return datas

    return datas

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)