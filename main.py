import cv2
import sys
import os
import numpy
from PIL import Image
from func.filter import applyFilter
from sphool.Library import getInputData, setOutputData

#Sphool用のライブラリをインポート
#getInputData(x)でx番目の入力ファイルのパスを取得する
#setOutputData(S)でユーザ向けに出力するファイルのパスSを指定する

# 実行
def main():
    imagePath = getInputData(0)
    filterTypePath = getInputData(1)
    filterOptionsPath = getInputData(2)

    file_name = os.path.splitext(os.path.basename(imagePath))[0]
    ext = os.path.splitext(os.path.basename(imagePath))[-1]
    if ext != ".jpg" and ext != ".png" and ext != ".bmp" :
        print(f"以下の拡張子の画像データのみ対応しています。")
        print(f".jpg / .png / .bmp")
        sys.exit(99)


    with open(filterTypePath) as f:
        try:
            filType = str(f.read().strip())
            if filType != "1" and filType != "2" and filType != "3" :
                print(f"フィルタタイプは次のいずれかの数値で指定してください：")
                print(f"1(2値化)")
                print(f"2(Canny edge detection)")
                print(f"3(ラベリング)")
                sys.exit(99)
            else :
                filterType = int(filType)

        except Exception as e:
            print("エラー発生:", e)
            sys.exit(99)

    with open(filterOptionsPath) as f:
        try:
            file_content = f.read()
            if filterType==1 :
                if file_content == "" :
                    print("フィルタタイプが2値化(=1)の場合はフィルタオプションを省略できません")
                    print("2値化のためのフィルタオプションを次の形式で入力してください：")
                    print("<閾値(~255)>, <最大値(~255、閾値より上の値をこの値に変換する)>")
                    print("(例) 120, 255>")
                    sys.exit(99)
                else :
                    filterOptions = list(map(int, file_content.strip().split(',')))
                    if len(filterOptions) < 2 :
                        raise Exception

            elif filterType==2 :
                if file_content == "" :
                    image = numpy.array(Image.open(imagePath))
                    med_val = numpy.median(image)
                    sigma = 0.4
                    min_val = int(max(0, (1.0 - sigma) * med_val))
                    max_val = int(max(255, (1.0 + sigma) * med_val))
                    filterOptions = [min_val, max_val]
                else :
                    filterOptions = list(map(int, file_content.strip().split(',')))
                    if len(filterOptions) < 2 :
                        raise Exception
                     
            else :
                if file_content == "" :
                    print("フィルタタイプがラベリング(=3)の場合はフィルタオプションを省略できません")
                    print("2値化のためのフィルタオプションを次の形式で入力してください：")
                    print("<閾値(~255)>, <最大値(~255、閾値より上の値をこの値に変換する)>")
                    print("(例) 120, 255>")
                    sys.exit(99)
                else :
                    filterOptions = list(map(int, file_content.strip().split(',')))
                    if len(filterOptions) < 2 :
                        raise Exception

        except Exception as e:
            print("フィルタオプションの読み取りエラー発生:", e, "\n")
            if filterType==1 :
                print("フィルタタイプが2値化(=1)の場合、フィルタオプションは次の形式で入力してください：")
                print("<閾値(~255)>, <最大値(~255、閾値より上の値をこの値に変換する)>")
                print("(例) 120, 255>")
            elif filterType==2 :
                print("フィルタタイプがエッジ検出(=2)の場合、フィルタオプションは次の形式で入力してください：")
                print("※フィルタオプションが空欄の場合、σ=0.4、最小値0、最大値255で自動計算を行います")
                print("※最小閾値は微分値より小さくなるように設定してください")
                print("<最小閾値(~255)>, <閾値となる画素値の微分値(~255)>")
                print("(例) 120, 255>")
            else :
                print("フィルタタイプがラベリング(=3)の場合、2値化が必要です。")
                print("2値化のためのフィルタオプションを次の形式で入力してください：")
                print("<閾値(~255)>, <最大値(~255、閾値より上の値をこの値に変換する)>")
                print("(例) 120, 255>")

            sys.exit(99)

    filteredImage = applyFilter(imagePath, filterType, filterOptions)
    outImgPath = file_name + "_filtered" + ext
    cv2.imwrite(outImgPath, filteredImage)
    
    #出力したいファイルのパスを指定する
    setOutputData(outImgPath)

# メイン関数を実行
if __name__ == "__main__":
    main()

