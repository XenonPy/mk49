import cv2
import pytesseract
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)
driver.click()
image_path = "./tests/test_OCR.png"
image = cv2.imread(image_path)

height, width = image.shape[:2]
cropped_image = image[height//2:height, width//3:2*width//3]

gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

blurred = cv2.GaussianBlur(thresh, (5, 5), 0)

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
text = pytesseract.image_to_string(blurred, config='--psm 6')

text = text.replace('@', '0')

print("Extracted Text:")
print(text)

dataList = text.split(' ')
if len(dataList) != 8:
    print(dataList)
    print(f"Invalid data extracted: Incorrect number of elements ({len(dataList)})")
    exit()
if dataList[7][:3].lower() == 'fps':
    dataList[7] = str(dataList[7])[:3]
else:
    print(dataList)
    print("Invalid data extracted: FPS not found")
    exit()
print(dataList)

data = {
    "ship": dataList[0],
    "speed": dataList[1].replace('kn', ''),
    "headingDegrees": dataList[2].replace('°', ''),
    "longitude": dataList[4].replace('(', '').replace(')', '').replace(',', '').replace('E', '').replace('W', ''),
    "latitude": dataList[5].replace('(', '').replace(')', '').replace(',', '').replace('E', '').replace('W', ''),
    "fps": dataList[6]
}

print(data)
