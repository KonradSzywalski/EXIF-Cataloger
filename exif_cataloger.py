try:    
    from geolocation.main import GoogleMaps
    from geolocation.exceptions import ApiClientException
    import exifread
    import glob
    import os
    import shutil
    import random
    import sys
    import string
    import requests
    from multiprocessing import Queue
except:
    print('No required libraries!')
    os.system("PAUSE")
    
def location_inf(exif_parametrs, api_attribute):
    if api_attribute in exif_parametrs:
        return exif_parametrs[api_attribute]
    return
    print('No data available')
    os.system("PAUSE")

def google_format(exif_parametrs):
    first_data = float(exif_parametrs.values[0].num) / float(exif_parametrs.values[0].den)
    second_data = float(exif_parametrs.values[1].num) / float(exif_parametrs.values[1].den)
    third_data = float(exif_parametrs.values[2].num) / float(exif_parametrs.values[2].den)

    return first_data + (second_data / 60.00) + (third_data / 3600.00)

def copyDirectory(src, dest):
        shutil.copytree(src, dest)
        
def generate_key(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

input_path=input('Podaj sciezke do katalogu, w ktorym znajduja sie zdjecia\nNp. C:/Users/Konrad/Desktop/program_python/img/\n -> ')
print('')
input_path_copy=input('Podaj sciezke do stworzenia kopii wyżej podanego katalogu, w którym nazwy zdjec beda zawieraly geolokacje  \nNp. C:/Users/Konrad/Desktop/program_python/img_geolocation/\n -> ')
if not os.path.exists(input_path_copy):
    copyDirectory(input_path,input_path_copy)
else:
    print('Taka sciezka juz istnieje. Uruchom program jeszcze raz z prawidlowymi wartosciami')
    os.system("PAUSE")   
    
i=-1;
path_prim_info = input_path
path_prim = input_path_copy
pattern = path_prim+'*.jpg'
file_list = glob.glob(pattern)
dlugosc_path = len(path_prim)
new_list = list(file_list)
print('------------------------------------------------------\n')
print('Used path:',path_prim_info,'\n')
print('------------------------------------------------------\n')

for sprawdz in file_list:
    print(file_list.length())
    i=i+1
    name_file=new_list[i].split('\\')

    print(name_file)
    
    path = file_list[i]
    print('File name:',name_file[1],'\n')
    print('Google Maps Coordinates:')
    plik = open(path, 'rb')

    inf = exifread.process_file(plik)
    width = location_inf(inf, 'GPS GPSLatitude')
    width_direction = location_inf(inf, 'GPS GPSLatitudeRef')
    length = location_inf(inf, 'GPS GPSLongitude')
    length_direction = location_inf(inf, 'GPS GPSLongitudeRef')

    plik.close()
    
    if width and width_direction and length and length_direction:
        x = google_format(width)
        if width_direction.values != 'N':
            x = -x
            
        y = google_format(length)
        if length_direction.values != 'E':
            y = -y
    
    print('x =',x,'-',width_direction)
    print('y =',y,'-',length_direction,'\n')

    gps = 0
    while gps == 0:  
        try:
            google_maps = GoogleMaps(api_key='Your api key')
            gps = google_maps.search(lat=x, lng=y)
        except ApiClientException:
            key = generate_key(40)
            
    localization = gps.first()
    country = localization.country.decode('utf-8')
    city = localization.city.decode('utf-8')
    print('Country:',country)
    print('City:',city+'\n')
    print('------------------------------------------------------\n')
    os.rename(path_prim+name_file[1],path_prim+country+"-"+city+"-"+name_file[1])
    
print('Gotowe!')    
os.system("PAUSE")    
