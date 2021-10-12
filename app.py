from flask import Flask, request, jsonify, render_template ,make_response
import numpy as np
import requests
from datetime import datetime
from datetime import date
import csv
import pandas as pd
import os
from bs4 import BeautifulSoup
from IPython.display import HTML
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/weather',methods =["GET", "POST"])
def weather():
    
    if request.method == "POST":
        city_name = request.form.get("cityname")
        today = date.today()
        starting_date= request.form.get("Startdate")
        Ending_date = request.form.get("Enddate")
        start_date=datetime.strptime(starting_date, '%d/%m/%Y').date()
        End_date=datetime.strptime(Ending_date, '%d/%m/%Y').date()
        del_diff=abs(today-start_date).days
        delta = (abs(start_date - End_date).days)
       
        URL="forecasts/latest"
        url="https://www.weather-forecast.com/locations/"
        
        req = requests.get(f'{url}{city_name}/{URL}')
        
        
        soup = BeautifulSoup(req.content, 'lxml')
        period_day = soup.findAll("div" , {"class":"b-forecast__table-days-name"})
        period_date= soup.findAll("div" , {"class":"b-forecast__table-days-date"})
        
        

        weather_max_temp = soup.find("tr" , {"class":"b-forecast__table-max-temperature js-temp"})
        weather_max_temp_value = weather_max_temp.findAll("span" , {"class":"temp b-forecast__table-value"})
        
        weather_min_temp = soup.find("tr" , {"class":"b-forecast__table-min-temperature js-min-temp"})
        weather_min_temp_val_ = weather_min_temp.findAll("span" , {"class":"b-forecast__table-value"})
        

        weather_wind = soup.find("tr" , {"class":"b-forecast__table-wind js-wind"})
        weather_wind_val = weather_wind.findAll("text" , {"class":"wind-icon-val"})
        

        rain=soup.find('tr',{'class':"b-forecast__table-rain js-rain"})
        rain_weather=rain.findAll('span',{"class":"rain b-forecast__table-value"})
        
     

        weather_chill = soup.find("tr" , {"class":"b-forecast__table-chill js-chill"})
        weather_chill_val = weather_chill.findAll("span" , {"class":"temp b-forecast__table-value"})
        
      

        weather_humidity = soup.find("tr" , {"class":"b-forecast__table-humidity js-humidity"})
        weather_humidity_val = weather_humidity.findAll("span" , {"class":"b-forecast__table-value"})
        '''
        weather_UV=soup.find('tr',{'class':"b-forecast__table-uv js-uv"})
        weather_UV_val=weather_UV.findAll('tr',{'class':"b-forecast__table-value"})'''
    
    df = pd.DataFrame()
    with open( city_name + '.csv',mode = 'w') as csv_file:
        attributes = ['Days_Name',
                  'Date_Name',
                  'Max_Temp\n[AM,PM,Night]',
                  'Min_Temp\n[AM,PM,Night]',
                  'Wind\n[AM,PM,Night]',
                  'Rain\n[AM,PM,Night]',
                  'Chill\n[AM,PM,Night]',
                  'Humidity\n[AM,PM,Night]',
                  'UV\n[AM,PM,Night]'
        ]
        writer = csv.DictWriter(csv_file, fieldnames = attributes)
        writer.writeheader()
        for (i,j) in zip(range(del_diff,(delta+del_diff)+1,1),range(0,36,3)):
            #print(j)
            a={
            'city':city_name,
            'Days_Name':str(period_day[i].text),
            'Date_Name':str(period_date[i].text),
            'Max_Temp\n[AM,PM,Night]':[str(weather_max_temp_value[j].text),str(weather_max_temp_value[j+1].text),str(weather_max_temp_value[j+2].text)],
            'Min_Temp\n[AM,PM,Night]':[str(weather_min_temp_val_[j].text),str(weather_min_temp_val_[j+1].text),str(weather_min_temp_val_[j+2].text)],
            'Wind\n[AM,PM,Night]':[str(weather_wind_val[j].text),str(weather_wind_val[j+1].text),str(weather_wind_val[j+2].text)],              
            'Rain\n[AM,PM,Night]':[str(rain_weather[j].text),str(rain_weather[j+1].text),str(rain_weather[j+2].text)],              
            'Chill\n[AM,PM,Night]':[str(weather_chill_val[j].text),str(weather_chill_val[j+1].text),str(weather_chill_val[j+2].text)],              
            'Humidity\n[AM,PM,Night]':[str(weather_humidity_val[j].text),str(weather_humidity_val[j+1].text),str(weather_humidity_val[j+2].text)],              
            #'UV\n[AM,PM,Night]':[str(weather_UV_val[j].text),str(weather_UV_val[j+1].text),str(weather_UV_val[j+2].text)],              
            
            }
            df = df.append(a, ignore_index = True)
        #print(df)
        response =make_response(df.to_csv())
        response.headers["Content-Disposition"] = "attachment; filename="+city_name + '.csv'
        return response
        
if __name__ == "__main__":
    app.run(debug=True)
