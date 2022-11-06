import requests
from selectolax.parser import HTMLParser
import json
import time
import csv
import os

os.remove('yandex-pars.csv') #удаляем т.к. файл дописывается с каждым запуском программы

def wtite_csv(filename, data): #функция для создания csv файла
    fieldnames = ['address', 'rooms', 'type', 'floors_total', 'building_type', 'floor', 'area', 'kitchen', 'balcony','metro','renovation', 'price']
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter = ';')
        writer.writerow(data)

def get_offers(response): #функция получения списка объявлений
        response.encoding = 'utf-8'
        html = response.text

        tree = HTMLParser(html)
        script = tree.css_first('script[id="initial_state_script"]').text() 
        script = script[23:-1] #срезаем лишние символы чтобы остался чистый json

        data = json.loads(script)
        try:
            page_number = data['routing']['locationBeforeTransitions']['query']['page']
        except:
            page_number = 0

        offers = data['map']['offers']['points']

        for offer in offers:
       
            address = offer['location']['geocoderAddress']
        
            try:
                rooms = offer['roomsTotal'] #количество комнат
            except:
                rooms = 'студия'
        
            type = offer['flatType'] #вторичка(старый) или новостройка(новый)
            if type == 'SECONDARY':
                type = 'старый'
            if type in('NEW_FLAT', 'NEW_SECONDARY'):
                type = 'новый'
        
            floors_total = offer['floorsTotal'] #всего этажей           
        
            try:
                building_type = offer['building']['buildingType'] #материал дома
                if building_type == 'BRICK':
                    building_type = 'кирпич'
                if building_type in('BLOCK','MONOLIT_BRICK','MONOLIT'):
                    building_type = 'монолит'
                if building_type == 'PANEL':
                    building_type = 'панельный'
            except:
                building_type = ''
        
            floor = str(offer['floorsOffered']).replace('[', '').replace(']','') #этаж на котором квартира

            area = offer['area']['value'] #площадь квартиры
        
            try:
                kitchen = offer['kitchenSpace']['value']            
            except:
                kitchen = ''

            try:
                balcony = offer['house']['balconyType'] #тип балкона
                if balcony in('BALCONY', 'TWO_BALCONY', 'LOGGIA', 'TWO_LOGGIA'):
                    balcony = 'есть'
            except:
                balcony = 'нет'        
        
            try:
                renovation = offer['apartment']['renovation']
                if renovation in('COSMETIC_DONE', 'EURO'):
                    renovation = 'муниципальный ремонт'
                if renovation in('NEEDS_RENOVATION', 'NON_GRANDMOTHER', 'CLEAN'):
                    renovation = 'без отделки'
                if renovation in('PRIME_RENOVATION', 'DESIGNER_RENOVATION'):
                    renovation = 'современный ремонт'
            except:
                renovation = ''

            try:
                metro = offer['location']['metro']['timeToMetro']
            except:
                metro = ''

            price = offer['price']['value']

            print(address, rooms, type, floors_total, building_type, floor, area, kitchen, balcony, metro, renovation, price, sep='; ') #для проверки
        
            data_offer = {
                'address':address, 
                'rooms':rooms, 
                'type':type,
                'floors_total':floors_total,
                'building_type':building_type,
                'floor':floor,
                'area':area,
                'kitchen':kitchen,
                'balcony':balcony,
                'metro':metro,
                'renovation':renovation,
                'price':price
            }
           
            #print(data_offer) #для проверки 

            write_csv('yandex-pars.csv', data_offer)         
          
        return page_number 
  
def main():
    
    page = 1

    while True:
        params = (
            ('page', page),
        )

        url = 'https://realty.ya.ru/moskva/kupit/kvartira/'
        response = requests.get(url, params=params)
        page_number = get_offers(response)

        if int(page_number) < page:
            break
        page += 1
        sleep(randint(2,5))

if __name__ == '__main__':
    main()
