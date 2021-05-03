def ocr(FOLDER_PATH, FILE_NAME):
    import os,io
    from google.cloud import vision
    from google.cloud.vision import types
    import pandas as pd
    import cv2
    from matplotlib import pyplot as plt
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'google-api.json'
    client=vision.ImageAnnotatorClient()
    with io.open(os.path.join(FOLDER_PATH,FILE_NAME),'rb') as image_file:
        content=image_file.read()
    image=vision.types.Image(content=content)
    response=client.document_text_detection(image=image)
    texts=response.text_annotations
    df=pd.DataFrame(columns=['locale','description'])
    for texts in texts:
        df=df.append(dict(locale=texts.locale,description=texts.description),ignore_index=True)
    entities = []
    res = ""
    for i in df['description'][0]:
        if i == '\n':
            entities.append(res)
            res = ""
            continue
        res+=i
    return entities
