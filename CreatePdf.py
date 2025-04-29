from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4, portrait
from tkinter import filedialog
import os
from datetime import datetime

# 入力ファイルと出力PDFのパス
output_pdf = "output.pdf"

# PDFを生成
def create_pdf(input_file, output_pdf):
    # 日本語フォントを登録
    platform = os.name
    if platform == "posix":
        pdfmetrics.registerFont(TTFont("IPAexGothic", "/usr/share/fonts/OTF/ipag.ttf"))

    # Canvasオブジェクトを作成
    c = canvas.Canvas(output_pdf, pagesize=portrait(A4))
    c.setFont("IPAexGothic", 12)  # 日本語フォントを設定

    xStartPosition = 50  # X座標の初期位置
    yStartPosition = 750 # Y座標の初期位置
    xEndPosition = 550   # X座標の終了位置
    lineSpaceace = 30  # 行間隔
    twoRowFlag=False

    # テキストファイルを読み込む
    with open(input_file, "r", encoding="utf-8") as file:
        yPosition = yStartPosition
        prev_yPosition = yStartPosition
        for line in file:
            thLength=5# 単語判定基準文字数
            
            text = line.strip()
            
            isEnglish=False
            if text[0].isalpha() or text[0].isdigit():
                isEnglish=True
                
            if isEnglish:
                thLength*=2
                
            tmp_xStartPosition=xStartPosition
            tmp_xEndPosition=xEndPosition
            
            prev_twoRowFlag=twoRowFlag
            if len(text) <= thLength:
                twoRowFlag=True
                if prev_twoRowFlag:
                    # tmp_xStartPosition=400
                    tmp_xStartPosition=tmp_xStartPosition*1.5+ (xEndPosition-xStartPosition)/2
                    yPosition =prev_yPosition
                else:
                    # tmp_xEndPosition=200
                    tmp_xEndPosition=tmp_xStartPosition*0.5+ (xEndPosition-xStartPosition)/2
            else:
                twoRowFlag=False
                
            # PDFにテキストを描画
            prev_yPosition=yPosition
            c.drawString(tmp_xStartPosition, yPosition, text)
            yPosition -= lineSpaceace  # 次の行のY座標を調整
            c.line(tmp_xStartPosition, yPosition, tmp_xEndPosition, yPosition)  # 横線を引く
            yPosition -= lineSpaceace  # 次の行のY座標を調整
            
            if prev_twoRowFlag and twoRowFlag:
                prev_twoRowFlag=False
                twoRowFlag=False
            if yPosition < lineSpaceace*2:
                yPosition = yStartPosition
                c.showPage()
            
    # PDFを保存
    c.save()

# 実行
if __name__ == "__main__":
    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    inputPath = filedialog.askopenfilename(filetypes = [("","*")],initialdir = desktop_dir)
    print("inputPath:", inputPath)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    outputPath =os.path.join(os.path.dirname(inputPath), f"output_{timestamp}.pdf")
    print("outputPath:", outputPath)
    
    if inputPath and outputPath:
        create_pdf(inputPath, outputPath)