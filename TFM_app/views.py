from django.shortcuts import render
from django.http import HttpResponse, Http404

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import os
# Create your views here.


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