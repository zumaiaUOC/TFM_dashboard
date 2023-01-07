from django.shortcuts import render
from django.http import HttpResponse, Http404

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import os
import pandas as pd
# Create your views here.
from .models import PredResults
from django.http import JsonResponse
import numpy as np


def import_data_file(request):
    if "GET" == request.method:
        return render(request, 'import_data_file.html')
    else:
        users_file = request.FILES["users_file"]
        print('data_file')
        path = 'media/data/'
    
        
        #path = 'media/users/'

        print('data_file_1')
        fs = FileSystemStorage(location=path)
        print('data_file_2')
        # save the file to the path

        fs.save(users_file.name, users_file)

        print('data_file_3')

        print(os.getcwd())

        #etl_agente_clientes_facturacion()
        
        return render(request, 'import_data_file_resp.html')
    
def predict(request):
    return render(request, 'predict.html', context=None)


def predict_chances(request):

    if request.method == "POST":

        # Receive data from client
        sensor_02 = str(request.POST.get('sensor_02'))
        sensor_04 = str(request.POST.get('sensor_04'))
        sensor_06 = str(request.POST.get('sensor_06'))
        sensor_10 = str(request.POST.get('sensor_10'))
        sensor_11 = str(request.POST.get('sensor_11'))
        sensor_12 = str(request.POST.get('sensor_12'))
        
        global result_final
        result_final = ''

        try:

            model = pd.read_pickle(r"media/model.pickle")

            print(float(sensor_02), float(sensor_04), float(sensor_06), float(sensor_10), float(
                sensor_11), float(sensor_12))

            x = np.array([float(sensor_02), float(sensor_04), float(sensor_06), float(sensor_10), float(
                sensor_11), float(sensor_12)])

            x = x.reshape(1, -1)

            print(x)
            
            
            
            result_final = model.predict([[sensor_02, sensor_04, sensor_06, sensor_10, sensor_11, sensor_12]])
            print("El resultado es")
            
        except Exception as e:
            print(e)
            print("something went wrong")

        global res
        res = ''
        if int(float(result_final)) == 0:
            res = 'No Disease'
        elif int(float(result_final))  == 1:
            res = 'You Have Disease'
        else:
            res = 'resto'

        print(res)
        context = {
            'data': result_final,
            'q': res,
        }
        return render(request, 'results.html', context)

    return render(request, 'predict.html')



def view_results(request):
    # Submit prediction and show all
    data = {"dataset": PredResults.objects.all()}
    return render(request, "results.html", data)