import numpy as np
import cv2

# フィルタの種類に応じた処理を行う
def applyFilter(imagePath, filterType, filterOptions):
    # 画像の読み込み
    image = cv2.imread(imagePath)
    # グレースケール変換
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if filterType == 1:
        # 2値化
        _, filteredImage = cv2.threshold(grayImage, filterOptions[0], filterOptions[1], cv2.THRESH_BINARY)

    elif filterType == 2:
        # Canny edge detection
        filteredImage = cv2.Canny(grayImage, filterOptions[0], filterOptions[1])

    elif filterType == 3:
        # ラベリング
        # 2値化
        _, binaryImage = cv2.threshold(grayImage, filterOptions[0], filterOptions[1], cv2.THRESH_BINARY)

        # ラベリング
        _, labels = cv2.connectedComponents(binaryImage)

        # ラベリング結果の正規化と視覚化
        label_hue = np.uint8(179 * labels / np.max(labels))
        blank_ch = 255 * np.ones_like(label_hue)
        labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
        labeled_img[label_hue==0] = 0
        filteredImage = labeled_img
    else :
        #これ以外の場合(例外)の検出はmain側で実施するため、ここでは特に何も実施しない
        pass
    
    return filteredImage