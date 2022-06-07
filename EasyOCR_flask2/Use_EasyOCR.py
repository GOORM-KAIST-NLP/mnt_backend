from matplotlib import pyplot as plt
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from datetime import datetime

# 이미지 보이기
def plt_imshow(img=None, figsize=(8 ,5)):
    
    plt.figure(figsize=figsize)

    if type(img) == list:

        for i in range(len(img)):
            if len(img[i].shape) <= 2:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_GRAY2RGB)
            else:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_BGR2RGB)

            plt.subplot(1, len(img), i + 1), plt.imshow(rgbImg)
            plt.xticks([]), plt.yticks([])

        plt.show()
    else:
        if len(img.shape) < 3:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        plt.imshow(rgbImg)
        plt.xticks([]), plt.yticks([])
        plt.show()


# 폰트
def putText(cv_img, text, x, y, color=(0, 0, 0), font_size=22):

    # Colab이 아닌 Local에서 수행 시에는 gulim.ttc 를 사용하면 됩니다.
    # font = ImageFont.truetype("fonts/gulim.ttc", font_size)
    # font = ImageFont.truetype('/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf', font_size)
    img = Image.fromarray(cv_img)
    
    draw = ImageDraw.Draw(img)
    draw.text((x, y), text, fill=color)

    cv_img = np.array(img)
    
    return cv_img


def ocr(outt, img, results):

    image = cv2.imread(img, cv2.IMREAD_COLOR)
    
    i = 0
    # loop over the results
    for (bbox, text, prob) in results:

        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))

        # 추출한 영역에 사각형을 그리고 인식한 글자를 표기합니다.
        cv2.rectangle(image, tl, br, (0, 255, 0), 2)
        image = putText(image, outt[i], tl[0], tl[1] - 60, (0, 255, 0), 50)
        i += 1
    
    fileName = datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + '_result_img.jpg'

    cv2.imwrite('./static/' + fileName, image)

    return image, fileName
