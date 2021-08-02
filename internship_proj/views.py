from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
# from django.shortcuts import render_to_response
from django.urls import reverse_lazy, reverse
from django.contrib import messages
import glob
import pandas as pd
import json
from django.template import RequestContext

def homepage(request):
    try:
        xlsx_files = glob.glob("static/xlsx_files/*.xlsx")
        for single_file in xlsx_files:
            name = single_file.split('\\')[1].split('.xlsx')[0]
            df = pd.DataFrame(pd.read_excel(single_file))
            df.to_csv('static/csv_files/{}.csv'.format(name), index=False)
            lines = open('static/csv_files/{}.csv'.format(name)).readlines()
            open('static/csv_files/{}.csv'.format(name), 'w').writelines(lines[2:])
            
        df_april = pd.read_csv('static/csv_files/April-2021.csv', index_col=False)
        df_may = pd.read_csv('static/csv_files/May-2021.csv', index_col=False)
        df_june = pd.read_csv('static/csv_files/June-2021.csv', index_col=False)
        df_april.drop(['Serial No',], axis = 1, inplace = True)
        df_may.drop(['Serial No',], axis = 1, inplace = True)
        df_june.drop(['Serial No',], axis = 1, inplace = True)
        df_april.rename(columns = {'Total':'April'}, inplace = True)
        df_may.rename(columns = {'Total':'May'}, inplace = True)
        df_june.rename(columns = {'Total':'June'}, inplace = True)
        df_two = df_april.merge(df_may, how='outer', on='Vehicle Class')
        df_final = df_two.merge(df_june, how='outer', on='Vehicle Class')
        df_final.rename(columns = {'Vehicle Class':'Vehicle_Class'}, inplace = True)
        df_final.index = df_final.index + 1
        df_final.to_csv('static/downloadable_file/final_file.csv', index=False)
        json_records = df_final.reset_index().to_json(orient ='records')
        arr = []
        arr = json.loads(json_records)
        params = {
            'd': arr,
        }
    except Exception as e:
        print(e)
        params = {
            'd': e,
            'exception': True,
        }
    return render(request, 'internship_proj/index.html', params)



import csv
import os
from wsgiref.util import FileWrapper
def download(request, *args, **kwargs):
    filename = 'static/downloadable_file/final_file.csv'
    filewrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(filewrapper, content_type='text/csv')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=datafile.csv'
    # with open(csv_file, 'w') as csvfile: 
    #     # creating a csv writer object 
    #     csvwriter = csv.writer(csvfile) 
            
    #     # writing the fields 
    #     csvwriter.writerow(fields) 
            
    #     # writing the data rows 
    #     csvwriter.writerows(rows)
    # response = HttpResponse(csv_file, content_type='application/x-download')
    # content = "attachment; filename={}".format(csv_file)
    # response['Content-Disposition'] = content
    return response
