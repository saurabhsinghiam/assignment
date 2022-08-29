from sys import platform
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile, File
from django.conf import settings
from django.http import HttpResponse

import os
import pandas as pd
import matplotlib.pyplot as plt
import pylab


def index(request):
    success = 0
    if success == 1:
        success = 2
    if request.POST and request.FILES:
        csvfile = request.FILES['csv_file']
        path = default_storage.save('tmp/csvfile',ContentFile(csvfile.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        df=pd.read_csv("tmp/csvfile")
        def f(df, col1,col2,col3,col4):
            df.insert(5,'TR','')
            df.insert(6,'+DM 1','')
            df.insert(7,'-DM 1','')
            for x in range(1,len(df)):
                val=max((df[col2].iloc[x]-df[col3].iloc[x]),abs(df[col2].iloc[x]-df[col4].iloc[x-1]),abs(df[col3].iloc[x]-df[col4].iloc[x-1]))
                df.loc[x,'TR'] = val
                #print(val)
                if ((df[col2].iloc[x]-df[col2].iloc[x-1])>(df[col3].iloc[x-1]-df[col3].iloc[x])):
                    val2=max((df[col2].iloc[x]-df[col2].iloc[x-1]),0)     
                else:
                    val2=0
                df.loc[x,'+DM 1'] = val2
                #print(val2)
                if ((df[col3].iloc[x-1]-df[col3].iloc[x])>(df[col2].iloc[x]-df[col2].iloc[x-1])):
                    val3=max((df[col3].iloc[x-1]-df[col3].iloc[x]),0)
                else:
                    val3=0
                df.loc[x,'-DM 1'] = val3
        def g(df, col1,col2,col3):
            df.insert(8,'TR14','')
            df.insert(9,'+DM14','')
            df.insert(10,'-DM14','')
            y=0
            z=0
            l=0
            for x in range(1,len(df)):
                if x<15:
                    y+=df[col1].iloc[x]
                    z+=df[col2].iloc[x]
                    l+=df[col3].iloc[x]
                    df.loc[14,'TR14']=y
                    df.loc[14,'+DM14']=z
                    df.loc[14,'-DM14']=l
                else:
                    y=(df['TR14'].iloc[x-1]-(df['TR14'].iloc[x-1])/14)+df['TR'].iloc[x]
                    z=(df['+DM14'].iloc[x-1]-(df['+DM14'].iloc[x-1])/14)+df['+DM 1'].iloc[x]
                    l=(df['-DM14'].iloc[x-1]-(df['-DM14'].iloc[x-1])/14)+df['-DM 1'].iloc[x]
                    df.loc[x,'TR14']=y
                    df.loc[x,'+DM14']=z
                    df.loc[x,'-DM14']=l
        def h(df, col1,col2,col3):
            df.insert(11,'+DI14','')
            df.insert(12,'-DI14','')
            df.insert(13,'DI 14 Diff','')
            df.insert(14,'DI 14 Sum','')
            df.insert(15,'DX','')
            df.insert(16,'ADX','')
            y=0
            z=0
            l=0
            k=0
            j=0
            h=0
            g=0
            for x in range(14,len(df)):
                #if x<15:
                    y=(100*(df[col2].iloc[x]/df[col1].iloc[x]))
                    z=(100*(df[col3].iloc[x]/df[col1].iloc[x]))
                    df.loc[x,'+DI14']=y
                    df.loc[x,'-DI14']=z
                    l=abs(df['+DI14'].iloc[x]-df['-DI14'].iloc[x])
                    k=df['+DI14'].iloc[x]+df['-DI14'].iloc[x]
                    df.loc[x,'DI 14 Diff']=l
                    df.loc[x,'DI 14 Sum']=k
                    j=(100*(df['DI 14 Diff'].iloc[x]/df['DI 14 Sum'].iloc[x]))
                    df.loc[x,'DX']=j
                    if x<28:
                        h+=df['DX'].iloc[x]
                        g+=1
                        df.loc[27,'ADX']=(h/g)
                    else:
                        h=((df['ADX'].iloc[x-1]*13+df['DX'].iloc[x]))/14
                        df.loc[x,'ADX']=h
        def graph1():
            df[['ADX','+DI14','-DI14']]= df[['ADX','+DI14','-DI14']].apply(pd.to_numeric)
            global fig
            fig=df.plot(y=['ADX','+DI14','-DI14'])
            plt.xlim([29,60])
            plt.plot([0,100], [20,20] ,linestyle='dashed',color='black')
            plt.tick_params(axis='y', which='both', labelleft=False, labelright=True)
            plt.grid(True)
            plt.save("tmp/fig")
        def excel():
            df.to_excel("tmp/Assignment1-solution.xlsx",index=False)
        
        
        f(df,'Open','High','Low','Close')
        g(df,'TR','+DM 1','-DM 1')
        h(df,'TR14','+DM14','-DM14')
        #graph1()
        excel()
        success=1
    return render(request, "index.html", locals())
def graph(request):
    path = "tmp/Assignment1-solution.xlsx"
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            df=pd.read_excel(fh.read())
            df[['ADX','+DI14','-DI14']]= df[['ADX','+DI14','-DI14']].apply(pd.to_numeric)
            df.plot(y=['ADX','+DI14','-DI14'])
            plt.xlim([29,60])
            plt.plot([0,100], [20,20] ,linestyle='dashed',color='black')
            plt.tick_params(axis='y', which='both', labelleft=False, labelright=True)
            plt.grid(True)
            response = HttpResponse(content_type="image/png")
            pylab.savefig(response, format="png")
            return response   
def download(request):
    path = "tmp/Assignment1-solution.xlsx"
    success = 2
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise "Http404"
    