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

    if request.POST.get('action') == 'post':

        # Receive data from client
        sensor_02 = int(request.POST.get('sensor_02'))
        sensor_04 = int(request.POST.get('sensor_04'))
        sensor_06 = int(request.POST.get('sensor_06'))
        sensor_10 = int(request.POST.get('sensor_10'))
        sensor_11 = int(request.POST.get('sensor_11'))
        sensor_12 = int(request.POST.get('sensor_12'))

        # Unpickle model
        model = pd.read_pickle(r"media/model.pickle")
        # Make prediction
        result_final = model.predict([[sensor_02, sensor_04, sensor_06, sensor_10, sensor_11, sensor_12]])

        stat = result_final[0]
        print("stat", stat)
        print("sensor_02", sensor_02)
        print("sensor_04", sensor_04)
        print("sensor_06", sensor_06)
        print("sensor_10", sensor_10)
        print("sensor_11", sensor_11)
        print("sensor_12", sensor_12)
        

        PredResults.objects.create(sensor_02=sensor_02, sensor_04=sensor_04, sensor_06=sensor_06,
                                   sensor_10=sensor_10, sensor_11=sensor_11, sensor_12=sensor_12, stat=stat)

        return render ({'result_final': stat, 
                             'sensor_02': sensor_02,
                             'sensor_04': sensor_04, 
                             'sensor_06': sensor_06, 
                             'sensor_10': sensor_10, 
                             'sensor_11': sensor_11, 
                             'sensor_12': sensor_12},
                            safe=False)
    else:
        return JsonResponse({'result_final': 'Error'})


def view_results(request):
    # Submit prediction and show all
    data = {"dataset": PredResults.objects.all()}
    return render(request, "results.html", data)