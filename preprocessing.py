import os
from PIL import Image
import xml.dom.minidom as xmldom

rootdir =  os.getcwd().replace('\\', '/')

# files name
# xml_files = os.listdir('annotations')
# segmentation_files = os.listdir('segmentation')
# 
import numpy as np

def read_xml(xmlfilepath):
    #read xml
    
    domobj = xmldom.parse(xmlfilepath)
    elementobj = domobj.documentElement
    
    #w = elementobj.getElementsByTagName("width")[0].firstChild.data
    #h = elementobj.getElementsByTagName("width")[0].firstChild.data
    
    subElementObj1 = elementobj.getElementsByTagName("object")
    label_colors = {}
    for i in range(len(subElementObj1)):
    
        if subElementObj1[i].getElementsByTagName("name") is not [] and subElementObj1[i].getElementsByTagName("mask_color") is not []:
            label_name = subElementObj1[i].getElementsByTagName("name")[0].firstChild.data
            label_color = subElementObj1[i].getElementsByTagName("mask_color")[0].firstChild.data
            if label_name not in label_colors:
                label_colors[label_name] = [int(k) for k in label_color.split(',')]
    
    #print(label_colors)            
    return label_colors

def deal_mask(mask, label_map):
    
    mask_obj = Image.open(mask)
    h, w, _ = np.asarray(mask_obj).shape
    # print(np.asarray(mask_obj).reshape(-1))
    source_data = np.asarray(mask_obj).reshape((h*w, 3))
    #print(str(source_data[1].tolist()))
    #dest_data = np.asarray([label_map[str(j)] if j != [0,0,0] else 0 for j in source_data]).reshape((h, w, 1))
    dest_data = []
    for j in source_data:
        #print(str(j.tolist()))
        if str(j.tolist()) != '[0, 0, 0]':
            dest_data.append(label_map[str(j.tolist())])
        else:
            dest_data.append(0)
    print(dest_data)
    '''
    img = Image.fromarray(np.uint8(dest_data), 'L')
    img.save(mask)
    img.show()
    '''

if __name__ == "__main__":
    # labels 映射    
    labels_map = {'hat': 1,
              'hair': 2,
              'glove': 3,
              'sunglasses': 4,
              'upperclothes': 5,
              'dress': 6,
              'coat': 7,
              'socks': 8,
              'pants': 9,
              'jumpsuit': 10,
              'scarf': 11,
              'skirt': 12,
              'face': 13,
              'left-arm': 14,
              'right-arm': 15,
              'left-leg': 16,
              'right-leg': 17,
              'left-shoe': 18,
              'right-shoe': 19,
              'background': 0
              }
    # rootdir
     
    #xmlfilepath = '19e65cccec3ce21f1e2b6db585fa5b64'
    label2colors_map = read_xml('19e65cccec3ce21f1e2b6db585fa5b64.xml')
    color2label_map = {str(k): labels_map[j] for j, k in label2colors_map.items()}
    print(color2label_map)
    deal_mask('19e65cccec3ce21f1e2b6db585fa5b64.jpg', color2label_map)

