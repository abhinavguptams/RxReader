import cv2
import pytesseract
from bs4 import BeautifulSoup
from helper import call_openai_api
import requests


def image_to_text(image_path):

    try:
        # Load the image using OpenCV
        image = cv2.imread(image_path)

        # Preprocess the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Perform OCR using Tesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        text = pytesseract.image_to_string(thresh)

        response={}

        #find diseases from text
        find_disease=find_the_disease(text)
        diseases=find_disease.split('\n')
        if len(diseases)>8:
            diseases=diseases[0:8]
        response["disease"]=diseases

        #find medicines from text
        find_medicine=find_the_medicine(text)
        medicines=find_medicine.split('\n')
        response["medicine"]=medicines



        find_names=find_the_medicine_name(find_medicine)

        #find buying options for medicines
        names=find_names.split('\n')
        suggest_options = []
        for name in names:
            suggest_options= suggest_options + find_the_buying_options_online("buy" + name + "in Inida")


        response["links_to_buy_medicines"]=suggest_options

        return response
    except:
        return "Rate Limiting Error: Azure Open AI subscription for hackathon has rate limiter so if someone else also has called this API within last 30 sec then you will see this error. Please wait for 30 sec and retry"


def find_the_buying_options_online(find_medicine):
    str=[]
    results = 3
    page = requests.get(f"https://www.google.com/search?q={find_medicine}&num={results}")
    soup = BeautifulSoup(page.content, "html")
    links = soup.findAll("a")
    for link in links :
        link_href = link.get('href')
        if "url?q=" in link_href and not "webcache" in link_href:
            temp= link.get('href').split("?q=")[1].split("&sa=U")[0]
            if "google" in  temp :
                continue

            if "1mg" in temp or "apollo" in temp or "meds" in temp or "mart" in temp:
                str.append(link.get('href').split("?q=")[1].split("&sa=U")[0])

    return str
    

def find_the_disease(text):
    try: 
        output=call_openai_api("Identify disease from the following text also tell precautions to take for that disease return answer in a unordered list",text)
        response=output
        return response
    except:
        raise Exception("Rate Limtiing Error")


def find_the_medicine(text):
    try: 
        output=call_openai_api("Identify list of medicines from the following text also tell precautions to take with these medicines return answer in an unordered list with precaution listed with medicine.",text)
        response=output
        return response
    except:
        raise Exception("Rate Limtiing Error")

def find_the_medicine_name(text):
    try:
        output=call_openai_api("Identify list of medicines from the following text return answer in a unordered list.",text)
        response=output
        return response
    except:
        raise Exception("Rate Limtiing Error")
    


