import pyautogui
import pytesseract
import cv2
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

if __name__ == '__main__':
    screenshot = pyautogui.screenshot('screen.png')

    img = cv2.imread('C:\\dev\\VoiceAssistant2\\screen.png')

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, binary_result = cv2.threshold(img, 85, 255, cv2.THRESH_BINARY)
    #
    # cv2.imshow("binary", binary_result)
    # cv2.waitKey(0)
    # Up-sample
    # # TODO fix accuracy

    text = pytesseract.image_to_data(binary_result, lang="eng", output_type=Output.DICT)

    data = {}
    for i in range(len(text['line_num'])):
        txt = text['text'][i]
        block_num = text['block_num'][i]
        line_num = text['line_num'][i]
        top, left = text['top'][i], text['left'][i]
        width, height = text['width'][i], text['height'][i]
        if not (txt == '' or txt.isspace()):
            tup = (txt, left, top, width, height)
            if block_num in data:
                if line_num in data[block_num]:
                    data[block_num][line_num].append(tup)
                else:
                    data[block_num][line_num] = [tup]
            else:
                data[block_num] = {}
                data[block_num][line_num] = [tup]

    line_data = {}
    idx = 0
    for _, b in data.items():
        for _, l in b.items():
            line_data[idx] = l
            idx += 1
    line_idx = 1
    for _, line in line_data.items():
        for item in line:
            name, x, y = item[0], item[1], item[2]
            if name == 'View':
                pyautogui.click(x, y)
            print(f'Line {line_idx} {name} {x} {y}')

        line_idx += 1

    # # 2
    # x, y = pyautogui.locateCenterOnScreen("edit.jpg", confidence=0.9)
    # pyautogui.moveTo(x, y, duration=0.1)
    # pyautogui.leftClick()
