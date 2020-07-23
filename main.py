from PIL import Image
from PIL.ExifTags import TAGS
import urllib.request
import json
from flask import Flask
import random
import string
from markupsafe import escape
def get_random_string():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(20))
    


def dl_img(url):
    full_path= get_random_string() + '.jpg'
    urllib.request.urlretrieve(url,full_path)
    return full_path




def getgeocoordinate(data ):
    geo_coordinate = '{0} {1} {2:.2f} {3}, {4} {5} {6:.2f} {7} '.format(
         data['GPSInfo'][2][0][0],data['GPSInfo'][2][1][0],int(data['GPSInfo'][2][2][0])/int(data['GPSInfo'][2][2][1]),
         data['GPSInfo'][1],
         data['GPSInfo'][4][0][0],data['GPSInfo'][4][1][0],int(data['GPSInfo'][4][2][0])/int(data['GPSInfo'][4][2][1]),
         data['GPSInfo'][3]
        )
    
    return geo_coordinate
    




def getmetadata(full_path:str):  
    path = full_path  #Path to the image or video
    image = Image.open(path) #Read The image data using PIL   
    exifdata = image.getexif() # Extract EXIF data , getexif return image metadata
    #Fiel names on exifdata are just IDs ! Prb : So , We need TAGS dictionary from PLI.ExifTags : maps each tag IDs into text
    data = {}
    for tags_id in exifdata:
        if (exifdata.get(tags_id) is not None ):
            info =exifdata.get(tags_id)
         
            if isinstance(info, bytes):
                info = info.decode()
            if (TAGS.get(tags_id,tags_id)=='GPSInfo'):
                data[TAGS.get(tags_id,tags_id)] = info
            if (isinstance(info,str) | isinstance(info,int)  ):
                if (isinstance(info,str)):
                    rep=['\u0000','\u0001','\u0002','\u0003']
                    for st in rep:
                        info = info.replace(st,'')
                    if (info != ""):
                        data[TAGS.get(tags_id,tags_id)] = info                                           
    if bool(data):
        if 'GPSInfo' in data:
            geo_coordinate = getgeocoordinate(data)      
            data['GPSInfo']=geo_coordinate          
        else:
            data['GPSInfo']="None"
   
    json_object = json.dumps(data,indent =4 ) 
  
    return json_object

 




app = Flask(__name__)

@app.route('/data/<path:data_url>')
def getjson(data_url):
    return getmetadata(escape(dl_img(data_url)))

if (__name__ == "__main__"):
    app.run()


