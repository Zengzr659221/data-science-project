def catgory_min(minutes):
   if int(minutes)>=0 and int(minutes)<15:
       return '00'
   elif int(minutes)>=15 and int(minutes)<30:
       return '15'
   elif int(minutes)>=30 and int(minutes)<45:
       return '30'
   else:
       return '45'
   
def catgory_min1(minutes):
   if int(minutes)>=0 and int(minutes)<5:
       return '00'
   elif int(minutes)>=5 and int(minutes)<10:
       return '05'
   elif int(minutes)>=10 and int(minutes)<15:
       return '10'
   elif int(minutes)>=15 and int(minutes)<20:
       return '15'
   elif int(minutes)>=20 and int(minutes)<25:
       return '20'
   elif int(minutes)>=25 and int(minutes)<30:
       return '25'
   elif int(minutes)>=30 and int(minutes)<35:
       return '30'
   elif int(minutes)>=35 and int(minutes)<40:
       return '35'
   elif int(minutes)>=40 and int(minutes)<45:
       return '40'
   elif int(minutes)>=45 and int(minutes)<50:
       return '45'
   elif int(minutes)>=50 and int(minutes)<55:
       return '50' 
   else:
       return '55'
   
def catgory_dis(distance):
   if distance>=0 and distance<4:
       return 'near'
   elif distance>=4 and distance<8:
       return 'middle'
   else:
       return 'far'