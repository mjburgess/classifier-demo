class Prediction(object):
    def __init__(self, label, description, probability):
        self.label = label
        self.description = description
        self.probability = probability
    
    def __str__(self):
        return '{label}: {description} @ {probability}'.format(**self.__dict__)
    
def predict_simple(image):
    """
        predicts using google 
    """
    import os
    
    result = None
    for line in open('input/urls.txt'):
        if os.path.basename(image) in line:
            result = _ask_google(line.strip())
            
    return [Prediction(result or "UNKNOWN", 'Simple Prediction', 0)]
    
def predict_neural(image, suggestions=3):
    """
        predicts using a pre-trained neural network
    """
    
    from keras.applications.resnet50 import ResNet50
    from keras.preprocessing import image
    from keras.applications.resnet50 import preprocess_input, decode_predictions
    import numpy as np
    
    model = ResNet50(weights='imagenet')
    
    img = image.load_img(image, target_size=(224, 224))

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    return [ Prediction(*result) 
        for result in decode_predictions(model.predict(x), top=suggestions)[0] 
    ]
    
    
def _ask_google(url):
    import urllib2
    import re 
    
    req = urllib2.Request(GGL + url, headers={ 'User-Agent': AGENT })
    html = urllib2.urlopen(req).read()

    result = re.search(r'Best guess for this image:\s*<a[^>]*>([^<]*)</a>', html)
    
    return result and result.group(1)
    

GGL = "http://www.google.com/searchbyimage?hl=en&image_url="
AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36"


    