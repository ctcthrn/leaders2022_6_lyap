import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
import re
import csv
import array as arr
import xlrd
from cryptography.fernet import Fernet

st.experimental_name = st.sidebar.text_input('Введите логин:')
st.experimental_user = st.sidebar.text_input('Введите свой e-mail:')
st.sidebar.button("Войти")


def convert_df(df):
    return df.to_csv().encode('utf-8')


if re.match("[^@]+@[^@]+\.[^@]+", st.experimental_user):

    #Начало основной проги
    st.write("""Добро пожаловать на сервис для определения 
    рыночной стоимости недвижемости!
    """)

    st.header('Укажите желаемые параметры квартиры:')

    form = st.form(key='my-form')
    place_1 = form.text_input('Укажите адрес:')
    rooms_1 = form.selectbox('Укажите количество комнат:', ('','Студия','1','2','3','4','5','6','7+'))
    segment_1 = form.selectbox('Укажите сегмент:', ('','Новый', 'Современный', 'Старый'))
    floors_1 = form.slider('Укажите количество этажей в доме', 1, 100)
    walls_material_1 = form.selectbox('Укажите материал', ('Кирпич', 'Панель','Монолит',''))
    current_floor_1 = form.slider('Введите желаемый этаж', 1, 100)
    square_1 = form.slider('Укажите площадь квартиры:', 1, 100)
    kitchen_1 = form.slider('Укажите площадь кухни:', 1, 100)
    balcony_1 = form.selectbox('Укажите наличие балкона/лоджии', ('Есть','Нет',''))
    metro_min_1 = form.slider('Удаленность от метро в минутах', 1, 60)
    flat_condition_1 = form.selectbox('Укажите состояние', ('Без отделки','Муниципальный ремонт', 'Современный ремонт',''))
    price_1 = form.text_input('Укажите цену:')

    submit = form.form_submit_button('Импортировать')

    st.write('Нажмите "Импортировать" для отправки данных')

    if submit:
        st.write(f'hello {place_1}')
        print(place_1)

        #print(names['Состоние'])
        pl=str(place_1)

        r=str(rooms_1)
        print('Введите сегмент: ')
        seg=str(segment_1)
        print('Введите этажность дома: ')
        fl=str(floors_1)
        if fl=='':
            fl=int(0)
        print('Введите материал стен: ')
        w_m=str(walls_material_1)
        print('Введите этаж расположения: ')
        c_fl=str(current_floor_1)
        if c_fl=='':
            c_fl=int(0)
        print('Введите площадь квартиры: ')
        sq=str(square_1)
        if sq=='':
            sq=int(0)
        print('Введите площадь кухни: ')
        kit=str(kitchen_1)
        if kit=='':
            kit=int(0)
        print('Наличие балкона: ')
        bal=str(balcony_1)
        print('Удаленность от станции метро в минутах: ')
        metro=str(metro_min_1)
        if metro=='':
            metro=int(0)
        print('Состояние квартиры: ')
        flat_cond=str(flat_condition_1)
        print('Введите цену: ')
        money=str(price_1)
        if money=='':
            money=int(0)
        article_read=pd.read_csv('C:\Project_flat\probnik.csv', delimiter = ';', 
                    names=['place', 'rooms', 'segment', 'floors', 'walls_material', 'current_floor', 
                        'square', 'kitchen', 'balcony', 'metro_min', 'flat_condition', 'price'])
        #загрузка файла на сервер
        #!wget https://pythonru.com/downloads/pandas_tutorial_read.csv
        pd.set_option('display.max_columns', None)

        article_read_copy=article_read.copy(deep=True)

        if pl!='':
            article_read=article_read[article_read['place'].str.contains(pl,case=False)==True]

        if r!='':
            article_read=article_read[article_read['rooms']==r]

        if seg!='':
            article_read=article_read[article_read['segment'].str.contains(seg,case=False)==True]


        if fl!=0:
            article_read=article_read[article_read['floors']==int(fl)]

        if w_m!='':
            article_read=article_read[article_read['walls_material'].str.contains(w_m,case=False)==True]

        #Копируем полученный Data frame в новый, в который будем отбирать возможные варианты
        article_an=article_read.copy(deep=True)

        if c_fl!=0:
            article_read=article_read[article_read['current_floor']==int(c_fl)]
        
        if sq!=0:
            article_read=article_read[article_read['square']==int(sq)]
            sq_an_min=int(sq)*(1-0.3)
            sq_an_max=int(sq)*(1+0.2)
            article_an=article_an[(article_an['square']>sq_an_min) & (article_an['square']<sq_an_max)]


        if kit!=0:
            article_read=article_read[article_read['kitchen']==int(kit)]
            kit_min=int(kit)*(1-0.3)
            kit_max=int(kit)*(1+0.3)
            article_an=article_an[(article_an['kitchen']>kit_min) & (article_an['kitchen']<kit_max)]


        if bal!='':
            article_read=article_read[article_read['balcony'].str.contains(bal,case=False)==True]

        if metro!=0:
            article_read=article_read[article_read['metro_min']==int(metro)]
            t_min=1.0 # Минимальное расстояние до метро
            t_max=int(metro)*2 # Максимальное расстояние до метро - в 2 раза больше заданного 
            article_an=article_an[(article_an['metro_min']>=t_min) & (article_an['metro_min']<=t_max)]


        if flat_cond!='':
            article_read=article_read[article_read['flat_condition'].str.contains(flat_cond,case=False)==True]

        if money!=0:
            article_read=article_read[article_read['price']==int(money)]



        print('\n Результат поиска идеала: ')
        print(article_read)
        n=len(article_read)

        #объединение двух frame
        if (len(article_read)==0) & (len(article_an)>0):
            #article_an.to_excel('import.xlsx', index=False)
            article_an.to_csv(r'C:\Project_flat\import.csv',index=False)
        if (len(article_read)>0) and ((len(article_an)>0)):
            res=pd.concat([article_read, article_an], ignore_index=True)
            res=res.drop_duplicates()
            lenth=len(article_an)
            mas = []
            type(mas)
            mas_rem=[]
            type(mas_rem)
            k_torg=0
            k_bal=0
            k_cond=0
            k_fl=0
            k_kit=0
            k_metro=0
            k_sq=0
            k_an=0
            pr_k_rem=1
            sum=0
            for index,row in res.iterrows():
                k_torg=-4.5 # Коэффициент на торг
                k_all_correction=0
                if index>n:
                    #расчет корректировки на этаж расположения квартиры
                    if (row.current_floor==int(1)):
                        if (res['current_floor'].loc[res.index[0]]==res['floors'].loc[res.index[0]]):
                                k_fl=3.2
                        else:
                            if res['current_floor'].loc[res.index[0]]==1:
                                k_fl=0
                            else:
                                k_fl=7.5
                    else:
                        if (row.current_floor==row.floors):
                            if (res['current_floor'].loc[res.index[0]]==res['floors'].loc[res.index[0]]):
                                k_fl=0
                            else:
                                if res['current_floor'].loc[res.index[0]]==1:
                                    k_fl=-3.1
                                else:
                                    k_fl=4.2
                        else:
                            if (res['current_floor'].loc[res.index[0]]==res['floors'].loc[res.index[0]]):
                                k_fl=-4
                            else:
                                if res['current_floor'].loc[res.index[0]]==1:
                                    k_fl=-7
                                else:
                                    k_fl=0
                    #расчет корректировки на площадь кухни
                    if (row.kitchen<7):
                        if res['kitchen'].loc[res.index[0]]<7:
                            k_kit=0
                        else:
                            if res['kitchen'].loc[res.index[0]]>10:
                                k_kit=9
                            else:
                                k_kit=3
                    else:
                        if (row.kitchen<10):
                            if res['kitchen'].loc[res.index[0]]<7:
                                k_kit=-2.9
                            else:
                                if res['kitchen'].loc[res.index[0]]>10:
                                    k_kit=5.8
                                else:
                                    k_kit=0
                        else:
                            if res['kitchen'].loc[res.index[0]]<7:
                                k_kit=-8.3
                            else:
                                if res['kitchen'].loc[res.index[0]]>10:
                                    k_kit=0
                                else:
                                    k_kit=-5.5
                    #расчет корректировки на наличие балкона
                    if (row.balcony=='нет')|(row.balcony=='Нет'):
                        if (res['balcony'].loc[res.index[0]]=='нет')|(res['balcony'].loc[res.index[0]]=='Нет'):
                            k_bal=0
                        else:
                            k_bal=5.3
                    else:
                        if (res['balcony'].loc[res.index[0]]=='нет')|(res['balcony'].loc[res.index[0]]=='Нет'):
                            k_bal=-5
                        else:
                            k_bal=0

                    #расчет корректировки на состояние отделки
                    if (row.flat_condition=='Без отделки')|(row.flat_condition=='без отделки'):
                        if (res['flat_condition'].loc[res.index[0]]=='Без отделки')|(res['flat_condition'].loc[res.index[0]]=='без отделки'):
                            k_cond=0
                        else:
                            if (res['flat_condition'].loc[res.index[0]]=='Муниципальный ремонт')|(res['flat_condition'].loc[res.index[0]]=='муниципальный ремонт'):
                                k_cond=13400
                            else:
                                k_cond=20100
                    else:
                        if (row.flat_condition=='Муниципальный ремонт')|(row.flat_condition=='муниципальный ремонт'):
                            if (res['flat_condition'].loc[res.index[0]]=='Без отделки')|(res['flat_condition'].loc[res.index[0]]=='без отделки'):
                                k_cond=-13400
                            else:
                                if (res['flat_condition'].loc[res.index[0]]=='Муниципальный ремонт')|(res['flat_condition'].loc[res.index[0]]=='муниципальный ремонт'):
                                    k_cond=0
                                else:
                                    k_cond=6700
                        else:
                            if (res['flat_condition'].loc[res.index[0]]=='Без отделки')|(res['flat_condition'].loc[res.index[0]]=='без отделки'):
                                k_cond=-20100
                            else:
                                if (res['flat_condition'].loc[res.index[0]]=='Муниципальный ремонт')|(res['flat_condition'].loc[res.index[0]]=='муниципальный ремонт'):
                                    k_cond=-6700
                                else:
                                    k_cond=0

                    #расчет удаленность от станции метро
                    if row.metro_min<5:
                        if res['metro_min'].loc[res.index[0]]<5:
                            k_metro=0
                        else:
                            if res['metro_min'].loc[res.index[0]]<10:
                                k_metro=-7
                            else:
                                if res['metro_min'].loc[res.index[0]]<15:
                                    k_metro=-11
                                else:
                                    if res['metro_min'].loc[res.index[0]]<30:
                                        k_metro=-15
                                    else:
                                        if res['metro_min'].loc[res.index[0]]<60:
                                            k_metro=-19
                                        else:
                                            k_metro=-22
                    else:
                        if row.metro_min<10:
                            if res['metro_min'].loc[res.index[0]]<5:
                                k_metro=7
                            else:
                                if res['metro_min'].loc[res.index[0]]<10:
                                    k_metro=0
                                else:
                                    if res['metro_min'].loc[res.index[0]]<15:
                                        k_metro=-4
                                    else:
                                        if res['metro_min'].loc[res.index[0]]<30:
                                            k_metro=-8
                                        else:
                                            if res['metro_min'].loc[res.index[0]]<60:
                                                k_metro=-13
                                            else:
                                                k_metro=-17
                        else:
                            if row.metro_min<15:
                                if res['metro_min'].loc[res.index[0]]<5:
                                    k_metro=12
                                else:
                                    if res['metro_min'].loc[res.index[0]]<10:
                                        k_metro=4
                                    else:
                                        if res['metro_min'].loc[res.index[0]]<15:
                                            k_metro=0
                                        else:
                                            if res['metro_min'].loc[res.index[0]]<30:
                                                k_metro=-5
                                            else:
                                                if res['metro_min'].loc[res.index[0]]<60:
                                                    k_metro=-10
                                                else:
                                                    k_metro=-13
                            else:
                                if row.metro_min<30:
                                    if res['metro_min'].loc[res.index[0]]<5:
                                        k_metro=17
                                    else:
                                        if res['metro_min'].loc[res.index[0]]<10:
                                            k_metro=9
                                        else:
                                            if res['metro_min'].loc[res.index[0]]<15:
                                                k_metro=5
                                            else:
                                                if res['metro_min'].loc[res.index[0]]<30:
                                                    k_metro=0
                                                else:
                                                    if res['metro_min'].loc[res.index[0]]<60:
                                                        k_metro=-6
                                                    else:
                                                        k_metro=-9
                                else:
                                    if row.metro_min<60:
                                        if res['metro_min'].loc[res.index[0]]<5:
                                            k_metro=24
                                        else:
                                            if res['metro_min'].loc[res.index[0]]<10:
                                                k_metro=15
                                            else:
                                                if res['metro_min'].loc[res.index[0]]<15:
                                                    k_metro=11
                                                else:
                                                    if res['metro_min'].loc[res.index[0]]<30:
                                                        k_metro=6
                                                    else:
                                                        if res['metro_min'].loc[res.index[0]]<60:
                                                            k_metro=0
                                                        else:
                                                            k_metro=-4
                                    else:
                                        if res['metro_min'].loc[res.index[0]]<5:
                                            k_metro=29
                                        else:
                                            if res['metro_min'].loc[res.index[0]]<10:
                                                k_metro=20
                                            else:
                                                if res['metro_min'].loc[res.index[0]]<15:
                                                    k_metro=15
                                                else:
                                                    if res['metro_min'].loc[res.index[0]]<30:
                                                        k_metro=10
                                                    else:
                                                        if res['metro_min'].loc[res.index[0]]<60:
                                                            k_metro=4
                                                        else:
                                                            k_metro=0

                    #расчет корректировки на площадь квартиры
                    if row.square<30:
                        if res['square'].loc[res.index[0]]<30:
                            k_sq=0
                        else:
                            if res['square'].loc[res.index[0]]<50:
                                k_sq=-6
                            else:
                                if res['square'].loc[res.index[0]]<65:
                                    k_sq=-12
                                else:
                                    if res['square'].loc[res.index[0]]<90:
                                        k_sq=-17
                                    else:
                                        if res['square'].loc[res.index[0]]<120:
                                            k_sq=-22
                                        else:
                                            k_sq=-24
                    else:
                        if row.square<50:
                            if res['square'].loc[res.index[0]]<30:
                                k_sq=6
                            else:
                                if res['square'].loc[res.index[0]]<50:
                                    k_sq=0
                                else:
                                    if res['square'].loc[res.index[0]]<65:
                                        k_sq=-7
                                    else:
                                        if res['square'].loc[res.index[0]]<90:
                                            k_sq=-12
                                        else:
                                            if res['square'].loc[res.index[0]]<120:
                                                k_sq=-17
                                            else:
                                                k_sq=-19
                        else:
                            if row.square<65:
                                if res['square'].loc[res.index[0]]<30:
                                    k_sq=14
                                else:
                                    if res['square'].loc[res.index[0]]<50:
                                        k_sq=7
                                    else:
                                        if res['square'].loc[res.index[0]]<65:
                                            k_sq=0
                                        else:
                                            if res['square'].loc[res.index[0]]<90:
                                                k_sq=-6
                                            else:
                                                if res['square'].loc[res.index[0]]<120:
                                                    k_sq=-11
                                                else:
                                                    k_sq=-13
                            else:
                                if row.square<90:
                                    if res['square'].loc[res.index[0]]<30:
                                        k_sq=21
                                    else:
                                        if res['square'].loc[res.index[0]]<50:
                                            k_sq=14
                                        else:
                                            if res['square'].loc[res.index[0]]<65:
                                                k_sq=6
                                            else:
                                                if res['square'].loc[res.index[0]]<90:
                                                    k_sq=0
                                                else:
                                                    if res['square'].loc[res.index[0]]<120:
                                                        k_sq=-6
                                                    else:
                                                        k_sq=-8
                                else:
                                    if row.square<120:
                                        if res['square'].loc[res.index[0]]<30:
                                            k_sq=28
                                        else:
                                            if res['square'].loc[res.index[0]]<50:
                                                k_sq=21
                                            else:
                                                if res['square'].loc[res.index[0]]<65:
                                                    k_sq=13
                                                else:
                                                    if res['square'].loc[res.index[0]]<90:
                                                        k_sq=6
                                                    else:
                                                        if res['square'].loc[res.index[0]]<120:
                                                            k_sq=0
                                                        else:
                                                            k_sq=-3
                                    else:
                                        if res['square'].loc[res.index[0]]<30:
                                            k_sq=31
                                        else:
                                            if res['square'].loc[res.index[0]]<50:
                                                k_sq=24
                                            else:
                                                if res['square'].loc[res.index[0]]<65:
                                                    k_sq=16
                                                else:
                                                    if res['square'].loc[res.index[0]]<90:
                                                        k_sq=9
                                                    else:
                                                        if res['square'].loc[res.index[0]]<120:
                                                            k_sq=3
                                                        else:
                                                            k_sq=0

        
                c_sq=row.price/row.square #цена квадратного метра аналога
                final_price=c_sq*(1+k_torg/100) #цена с корректировкой на торг
                final_price=final_price*(1+k_sq/100) #цена с корректировкой на площадь
                final_price=final_price*(1+k_metro/100)#цена с коректировкой на удаленность от метро
                final_price=final_price*(1+k_fl/100)#цена с корректировкой на этаж
                final_price=final_price*(1+k_kit/100)#цена с корректировкой на площадь кухни
                final_price=final_price*(1+k_bal/100)#цена с корректировкой на наличие балкона
                k_remont=k_cond/final_price#корректировка на ремонт в %
                final_price=final_price*(1+k_remont/100)#цена с корректировкой на ремонт
                mas_rem.append(final_price)#массив корректировок на ремонт всех аналогов
                k_all_correction=abs(k_torg)+abs(k_sq)+abs(k_metro)+abs(k_fl)+abs(k_kit)+abs(k_bal)+abs(k_remont)
                mas.append(k_all_correction)
                if (k_all_correction!=0):
                    k_an=k_an+1/k_all_correction

            mas_pr=[mas_rem[i]/(mas[i]*k_an) for i in range(len(mas))]
            for el_mas_pr in mas_pr:
                sum=sum+el_mas_pr
            price_of_orig=sum*res['square'].loc[res.index[0]]
            print('Цена')
            print(price_of_orig)

            res['price'].loc[res.index[0]]=price_of_orig
            res.to_excel('C:\Project_flat\import.xlsx', index=False)
            res.to_csv(r'C:\Project_flat\import.csv',index=False)

        #file = 'import.xlsx'
        #file_open = xlrd.open_file_open(file)

        csv=convert_df(res)
        st.write('Данные успешно импортированы')
        st.download_button(label = "Получить файл", data=csv, file_name="import.csv")

    
    user = {
    "email": st.experimental_user,
    "name": st.experimental_name
    }


