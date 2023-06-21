from django.shortcuts import render

# Create your views here.
import os
import numpy as np
import pandas as pd
import pickle
from pickle import load
from tensorflow import keras
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler 
from .models import MyData
from django.http import HttpResponse
from matplotlib import pyplot as plt
import seaborn as sns
from django.contrib import messages
# from background_task import background

# Create your views here.
def home(request):
    data = MyData.objects.all()
    # Persiapkan data yang diperlukan untuk visualisasi
    gre_scores = [item.GRE for item in data]
    university_data = [item.UNI_rating for item in data]
    
    # Kirim data sebagai konteks ke template
    context = {
        'gre_scores': gre_scores,
        'university_data': university_data
        }
    
    return render(request, 'index.html', context)

def display(request):
    return render(request,'input.html')

def save(request):
    if request.method=="POST":
        s=MyData()
        s.TOFEL=request.POST.get('ht_tofel')
        s.GRE=request.POST.get('ht_gre')
        s.UNI_rating=request.POST.get('ht_Uni_rating')
        s.SOP=request.POST.get('ht_sop')
        s.LOR=request.POST.get('ht_lor')
        s.CGPA=request.POST.get('ht_cgpa')
        s.Research_Ex=request.POST.get('ht_research')

        # Membaca data dalam data frame
        data=[[s.GRE,s.TOFEL,s.UNI_rating,s.SOP,s.LOR,s.CGPA,s.Research_Ex]]
        newx=pd.DataFrame(data,columns=["GRE","TOFEL","UNI_rating","SOP","LOR","CGPA","Research_Ex"])

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Mendefinisikan direktori model dan scaler
        filename = BASE_DIR + '/myapp/data/model_cnn_lstm.h5'
        filename1 = BASE_DIR + '/myapp/data/scaler_ds.pkl'

        # Memuat model
        model = load_model(filename)
        x = pickle.load(open(filename1,"rb"))

        # Menerapkan scaler untuk menskalakan data
        newx[newx.columns] = x.transform(newx[newx.columns])

        # Memprediksi skor pada data baru
        y_predict = model.predict(newx)
        
        # Melakukan training ulang pada model untuk mempelajari data baru 
        opt = keras.optimizers.Adam(lr=0.0001)
        model.compile(optimizer=opt, loss='mean_squared_error')
        model.fit(newx, y_predict, epochs=60, batch_size=32, verbose=0)
        model.save(filename)
        y_predict = round(float(y_predict[0][0]), 2)
        
        # Menyimpan pada database
        s.Chance_of_Admit = y_predict
        s.save()
        
        #return HttpResponse
        return render(request,'output.html', {'score':int(y_predict*100)})



