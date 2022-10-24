# import numpy as np
# import face_recognition

# gbs_image = face_recognition.load_image_file("./faceimg/GBS_02.jpg")
# gbs_face_encoding = face_recognition.face_encodings(gbs_image)[0]

# known_face_names = [ ]
# known_face_encodings = [ ]

# # name_list에 있는 이름들을 읽어와서 known_face_names에 저장
# with open('name_list.txt', "r", encoding="UTF-8") as name_list:
# 		lst = name_list.readlines()
# 		for name in lst:
# 			name = name.strip()
# 			known_face_names.append(name)

# # with open('./facencod/encode.txt', 'w') as encode:
# #     lst = gbs_face_encoding.tolist()
# #     for code in lst:
# #         encode.write(str(code) +'\n')

# with open('./facencod/encode.txt', "r", encoding="UTF-8") as encode:
#     new_lst = []
#     lst = encode.readlines()
#     for code in lst:
#         new_lst.append(code.strip())
#     known_face_encodings.append(np.array(new_lst))


# print(known_face_names)
# print(known_face_encodings)


a = 0

a+=1

print(a)