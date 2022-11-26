from tkinter import *
import numpy as np
import tkinter.messagebox as msg

import cv2
from PIL import Image, ImageTk
import face_recognition

import os

def check_name():
	
	if name_Entry.get() in known_face_names:
		msg.showerror("에러", "이미 있는 이름입니다.")
		name_Entry.delete(0, END)
	else:
		msg.showinfo("확인", name_Entry.get() + ' 이(는) 사용가능한 이름입니다.')

window = Tk()
window.title("Face_Recogniser")
window.geometry('600x400')

# 실행시 전체화면으로 실행
# F11을 통해 전체화면 제어
#window.attributes('-fullscreen', True)
#window.bind("<F11>", lambda event: window.attributes("-fullscreen", not window.attributes("-fullscreen")))
#window.bind("<Escape>", lambda event: window.attributes("-fullscreen", False))

window.configure(background='white')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# 제목 라벨
message = Label(
	window, text="Face Recognition Login",
	bg="green", fg="white", width=30,
	height=2, font=('times', 20, 'bold'))
message.place(x=100, y=20)

# 웹캠
webcam_label = Label(window, width=300, height=200)
webcam_label.place(x=200, y=100)


cap = cv2.VideoCapture(0)

def show_frame():

	cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
    
	cv2image = cv2.resize(cv2image, None, fx=0.4, fy=0.4)

	img = Image.fromarray(cv2image)

	imgtk = ImageTk.PhotoImage(image = img)
	webcam_label.imgtk = imgtk
	webcam_label.configure(image=imgtk)

	webcam_label.after(20, show_frame)

def no_fnc():
	pass

# 샘플
#gbs_image = face_recognition.load_image_file("./faceimg/GBS_02.jpg")
#gbs_face_encoding = face_recognition.face_encodings(gbs_image)[0]

known_face_encodings = [ ]
known_face_names = [ ]

# name_list에 있는 이름들을 읽어와서 known_face_names에 저장
with open('name_list.txt', "r", encoding="UTF-8") as name_list:
		lst = name_list.readlines()
		for name in lst:
			name = name.strip()
			known_face_names.append(name)
known_face_names.sort()

# facencoding 디렉터리의 파일들을 읽어서 리스트로 저장
encoding_file_list = os.listdir('./facencoding')
encoding_file_list.sort()
for file in encoding_file_list:
	# 인코딩 정보 known_face_encodings에 저장
	with open('./facencoding/' + file, "r", encoding="UTF-8") as encode:
		new_lst = []
		lst = encode.readlines()
		for code in lst:
			new_lst.append(float(code.strip()))
		known_face_encodings.append(np.array(new_lst))


def detect():
	
	# Grab a single frame of video
	ret, frame = cap.read()

	# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
	rgb_frame = frame[:, :, ::-1]
	rgb_frame = cv2.resize(rgb_frame, None, fx=0.4, fy=0.4)

	# Find all the faces and face enqcodings in the frame of video
	face_locations = face_recognition.face_locations(rgb_frame)
	face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

	name = "Unknown"
	
	# Loop through each face in this frame of video
	for face_encoding in face_encodings:
		matches = face_recognition.compare_faces(known_face_encodings, face_encoding)


		# If a match was found in known_face_encodings, just use the first one.
		#if True in matches:
		#	first_match_index = matches.index(True)
		#	name = known_face_names[first_match_index]

		# Or instead, use the known face with the smallest distance to the new face
		face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
		best_match_index = np.argmin(face_distances)
		if matches[best_match_index]:
			name = known_face_names[best_match_index]
			detected_name.configure(text=name+"님 반갑습니다.")

	# BGR to RGB -> 이거 해야 색이 똑바로 나옴
	frame = frame[:, :, ::-1]

	img = cv2.resize(frame, None, fx=0.4, fy=0.4)
	img = Image.fromarray(img)
	imgtk = ImageTk.PhotoImage(image = img)
	webcam_label.imgtk = imgtk
	webcam_label.configure(image=imgtk)
	
	
	webcam_label.after(1000, detect)

	

def take_Photo():
	# 사진 촬영
	ret, frame = cap.read()
	# 좌우 대칭
	frame = cv2.flip(frame, 1)

	# 얼굴 인식( 얼굴 위치 파악 )
	face_location = face_recognition.face_locations(frame)

	# 위치 값이 없으면 => 얼굴이 인식되지 않으면
	if len(face_location) == 0:
		msg.showerror("다시 시도해주세요", "얼굴이 인식되지 않았습니다")

	# 위치값이 하나면 => 얼굴이 하나 인식되면
	elif len(face_location) == 1:
 		# 사진 저장
		cv2.imwrite('./faceimg/' + name_Entry.get() + '.jpg', frame)
		msg.showinfo("완료", "사진이 저장되었습니다.")

		# 이름 리스트에 이름 저장
		with open('name_list.txt', "a", encoding="UTF-8") as name_list:
			name_list.write(name_Entry.get()+'\n')
		known_face_names.append(name_Entry.get())

		# 찍은 이미지 불러오기
		image = face_recognition.load_image_file('./faceimg/' + name_Entry.get() + '.jpg')
		face_encoding = face_recognition.face_encodings(image)[0]

		# 인코딩 정보 저장
		with open('./facencoding/' + name_Entry.get() + '_encoding.txt', "w") as encode:
			lst = face_encoding.tolist()
			for code in lst:
				encode.write(str(code) +'\n')


	else:
		msg.showerror("다시 시도해주세요", "얼굴이 2개 이상 인식되거나 에러입니다.")


name = Label(window, text="Regist",
 			height=2, fg="green",
 			bg="white", font=('times', 20, ' bold '))
name.place(x=20, y=60)

name = Label(window, text="name",
 			height=2, fg="green",
 			bg="white", font=('times', 15, ' bold '))
name.place(x=20, y=110)

name_Entry = Entry(window,
 			width=10, bg="white",
 			fg="green", font=('times', 15, ' bold '))
name_Entry.place(x=20, y=160)


name_Check = Button(window, text="check",
					fg="white", bg="green", command=check_name,
					width=5, activebackground="Red",
					font=('times', 10, ' bold '))
name_Check.place(x=100, y=160)



detected_name = Label(window, text="반갑습니다.",
 			height=3, fg="green",
 			bg="white", font=('times', 15, ' bold '))
detected_name.place(x=20, y=200)




takePhoto = Button(window, text="Take photo",
				   fg="white", bg="green", command=take_Photo,
					width=10, height=3, activebackground="Red",
					font=('times', 10, ' bold '))
takePhoto.place(x=20, y=300)


takeImg = Button(window, text="Camera On",
				   fg="white", bg="green", command=show_frame,
					width=10, height=3, activebackground="Red",
					font=('times', 10, ' bold '))
takeImg.place(x=120, y=300)

trainImg = Button(window, text="No func",
				     fg="white", bg="green", command=no_fnc,
					width=10, height=3, activebackground="Red",
					font=('times', 10, ' bold '))
trainImg.place(x=220, y=300)

trackImg = Button(window, text="Login",
				 fg="white", bg="green", command=detect,
					width=10, height=3, activebackground="Red",
					font=('times', 10, ' bold '))
trackImg.place(x=320, y=300)

quitWindow = Button(window, text="Quit",
					command=window.destroy, fg="white", bg="green",
					width=10, height=3, activebackground="Red",
					font=('times', 10, ' bold '))
quitWindow.place(x=420, y=300)


window.mainloop()
