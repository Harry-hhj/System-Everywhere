import os
import face_recognition
import scipy.io as scio
import pandas as pd

print("Tool for generating features of students")
print("Make sure every student's image is in this folder")
print()

inp = []

for img in os.listdir('./'):
    if os.path.splitext(img)[-1] in ['.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG']:
        image = face_recognition.load_image_file(img)
        face_encoding = face_recognition.face_encodings(image)[0]
        scio.savemat(f'{os.path.splitext(img)[0]}.mat', {'X': face_encoding})
        print(f"{img} finished.")
        inp.append({'学生姓名': os.path.splitext(img)[0]})

df = pd.DataFrame(inp)
df.to_excel(excel_writer='test.xlsx', header=True, index=False)
