import os
from sets import Set
import csv
from parallel_framework import ParallelRunner
from collections import OrderedDict
#number of parallel threads
dist_count = 16

folders = [[] for i in range(dist_count)]

#distributing folders
def folderDistributor(filepath):
   for directory,sublist,flist in os.walk(filepath):
     count = 0
     for item in sublist:
        if 'data_' in item:
           index = count % dist_count
           folder_list = folders[index]
           folder_list.append('%s/%s'%(directory,item))
           count += 1

#function to be executed parallely
h=['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
mi=['00','15','30','45']
def execute(directories,pid):
   final_map=OrderedDict(list())
   for directory in directories:
      try:
         samplefile=open(directory+'/sample_data_submeter.csv','w')

         for d,s,f in os.walk(directory):
            mydict=OrderedDict(list())
            no_of_submeters=OrderedDict()
            date=0
            if d=="*.py" or d=="*.pyc" or d=="*.csv":
               pass
            else:
            #print "Processing [%s] : %s"%(pid,d)
               for f1 in f:
    #print "Processing [%s] : %s"%(pid,f1)
                  if f1=="sample_dataKW.csv" or f1=="sample_dataKWH.csv" or f1=="sample_data_submeter.csv" or f1=="sample_data15.csv":
                     pass
                  else:
                     mfile = open('%s/%s'%(d,f1),'rU')
                     reader = csv.reader(mfile,delimiter=',')
                 
                     headers = None
                     for line in reader:
                        interval=line[3]
                        date_value = str(line[6])
                        ch_value   = line[5]
                        store_name=line[2]
                        submeter=line[1]
                        date,time = date_value.split(" ")
                        p,q,r=time.split(":")
                        hour=p
                        minu=q
                        
                         if submeter not in no_of_submeters:
                            no_of_submeters[submeter]=[]
                         if store_name not in mydict:
                            mydict[store_name]=[]
                         mydict.get(store_name).append((submeter,ch_value,hour,interval,minu))
         headerlist=['store']
         headerlist.append('date')
       
         e=0
         for k1,v1 in mydict.items():
            store=str(k1)
            for item2 in h:
               for item3 in mi:
                  data_list = [store]
                  f=str(item2+":"+item3)
                  data_list.append(str(t)+" "+f)
                  for item in no_of_submeters:
                     min_list00=[]
                     min_list15=[]
                     min_list30=[]
                     min_list45=[]
                     a0=0
                     a15=0
                     a30=0
                     a45=0
                     x=0.0
                     for item in v1:
                        t1,t2,t3,t4,t5=item
                            if item==t1:
                               if item2==t3:
                                
                               if t4=='15':
                                  if t5==item3:
                                     x=float(t2)
                            
                               if t4=='1':
                                  if float(t5)>=0 and float(t5)<15:
                                     min_list00.append(float(t2))
                                     a0+=1
                                    
                                  if float(t5)>=15 and float(5)< 30:
                                     min_list15.append(float(t2))
                                     a15+=1
                                    
                                  if float(t5)>=30 and float(t5)< 45:
                                     min_list30.append(float(t2))
                                     a30+=1
                                    
                                  if float(t5)>=45 and float(t5)< 60:
                                     min_list45.append(float(t2))
                                        a45+=1
                                            
                     if item3=='00' and a0>0:
                        a0=float(sum(min_list00)/a0)
                        x=a0
                     if item3=='15' and a15>0:
                        a15=float(sum(min_list15)/a15)
                        x=a15
                     if item3=='30' and a30>0:
                        a30=float(sum(min_list30)/a30)
                        x=a30
                     if item3=='45' and a45>0:
                        a45=float(sum(min_list45)/a45)
                        x=a45
                                                                                            
                     data_list.append(str(x))
                  if e==0:
                     samplefile.write('%s\n'%','.join(headerlist))
                     e+=1
                              
                  samplefile.write('%s\n'%','.join(data_list))
         samplefile.close()
      #print(".......sample3 written........."+directory)
         for d,s,f in os.walk(directory):
            for f1 in f:
               if f1=="sample_data_submeter.csv":
                  mfile = open('%s/%s'%(d,f1),'rU')
                  reader = csv.reader(mfile,delimiter=',')
                  y=OrderedDict()
                  i=0
                  for line in reader:
                     if i==0:
                        for a in range (len(line)):
                           if a==0:
                              pass
                           if a==1:
                              pass
                           if a>1:
                              if line[a] not in y:
                                 y[line[a]]=[]		
                        i+=1
                        pass
                     else:
                        if line[1] not in final_map:
                           final_map[line[1]]=[]
                        a=2
                        for item in y:
                           final_map.get(line[1]).append((line[0],item,line[a]))
                           a+=1
                        
               else:
	              pass
 #   os.remove(directory+'/sample_data2.csv')
      except Exception as ex:
         print(ex)
         print("............."+directory+"..................")
	 pass
   return final_map
final_map3 = OrderedDict(list())
def reducer(result):
   for k,v in result.items():
      if k not in final_map3:
         final_map3[k]=[]
         for item in v:
            t1,t2,t3=item
            final_map3.get(k).append((t1,t2,t3))

def writeFile():
   final_map5 = OrderedDict(list())
   my_list=sorted(final_map3.keys())
  
   for k1 in my_list:
      for k,v in final_map3.items():
         if k1==k:
            for item in v:
               t1,t2,t3=item
               f=(k,t1)
               if f not in final_map3:
                  final_map3[f]=[]
               final_map5.get(f).append((t2,t3))

   s1= OrderedDict()
   for k,v in final_map5.items():
      for item in v:
         t1,t2=item
         if t1 not in s1:
            s1[t1]=[]
   for item2 in s1:
      for k,v in final_map5.items():
         x=0
         for item in v:
            t1,t2=item
            if t1==item2:
	           x+=1
         if x==0:
            final_map5.get(k).append((item2,0))

   f1 = open('/home/sbat/external_drive/mainload/final_output_submeter.csv','w')
   headerlist=['store']
   headerlist.append("date")
   for k,v in s1.items():
      #print("writing store names")
      if k == '':
         pass
      else:
         headerlist.append(str(k))

   f1.write('%s\n'%','.join(headerlist))
   print("wrote headers")

   for k,v in final_map5.items():
      store=k[1]
      date=k[0]
      data_list =[store]
      data_list.append(str(date))
      for item1 in s1:
         for item in v:
            t1,t2=item
            if item1==t1:
               data_list.append(str(t2))
	       

      f1.write('%s\n'%','.join(data_list))
   print("done writing............................................")
   f1.close()


folderDistributor('/home/sbat/external_drive/mainload')
pp = ParallelRunner(execute,reducer,folders,dist_count)
pp.runThreads()
pp.reducer()
writeFile()
