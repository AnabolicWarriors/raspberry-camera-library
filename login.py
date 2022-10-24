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

def time_count_plus():
	global time_count

	time_count += 1

window = Tk()
window.title("Face_Recogniser")

# 실행시 전체화면으로 실행
# F11을 통해 전체화면 제어
window.attributes('-fullscreen', True)
window.bind("<F11>", lambda event: window.attributes("-fullscreen", not window.attributes("-fullscreen")))
window.bind("<Escape>", lambda event: window.attributes("-fullscreen", False))

window.configure(background='white')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# 제목 라벨
message = Label(
	window, text="Face Recognition Login",
	bg="green", fg="white", width=50,
	height=3, font=('times', 30, 'bold'))
message.place(x=200, y=20)

# 웹캠
webcam_label = Label(window, width = 400, height=400)
webcam_label.place(x=500, y=200)


cap = cv2.VideoCapture(0)

def show_frame():
	detect_button = False
	sf_button = True

	cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
    
	img = Image.fromarray(cv2image)

	imgtk = ImageTk.PhotoImage(image = img)
	webcam_label.imgtk = imgtk
	webcam_label.configure(image=imgtk)

	if detect_button == False and sf_button == True:
		webcam_label.after(20, show_frame)
	else: return
	
def no_fnc():
	pass

time_count = 0

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
	if len(known_face_encodings) == 0:
		msg.showerror("에러","인식된 얼굴이 없습니다.")
		return

	global time_count

	detect_button = True
	sf_button = False

	# Grab a single frame of video
	ret, frame = cap.read()

	# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
	rgb_frame = frame[:, :, ::-1]

	# Find all the faces and face enqcodings in the frame of video
	face_locations = face_recognition.face_locations(rgb_frame)
	face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

	# Loop through each face in this frame of video
	for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
		# See if the face is a match for the known face(s)
		matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

		name = "Unknown"

		# If a match was found in known_face_encodings, just use the first one.
		# if True in matches:
		#     first_match_index = matches.index(True)
		#     name = known_face_names[first_match_index]

		# Or instead, use the known face with the smallest distance to the new face
		face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
		best_match_index = np.argmin(face_distances)
		if matches[best_match_index]:
			name = known_face_names[best_match_index]

		# Draw a box around the face
		cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

		# Draw a label with a name below the face
		cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
		font = cv2.FONT_HERSHEY_DUPLEX
		cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

	# Display the resulting image
	#cv2.imshow('Video', frame)

	
	# BGR to RGB -> 이거 해야 색이 똑바로 나옴
	frame = frame[:, :, ::-1]

	img = Image.fromarray(frame)
	imgtk = ImageTk.PhotoImage(image = img)
	webcam_label.imgtk = imgtk
	webcam_label.configure(image=imgtk)

	if detect_button == True and sf_button == False:
		webcam_label.after(20, detect)
		
		webcam_label.after(1000, time_count_plus)
	
	elif time_count >= 3:
		print(name + '이 인식되었습니다.')
		cap.release()
	
	else: return

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
name.place(x=200, y=350)

name = Label(window, text="name",
 			height=2, fg="green",
 			bg="white", font=('times', 15, ' bold '))
name.place(x=200, y=400)

name_Entry = Entry(window,
 			width=15, bg="white",
 			fg="green", font=('times', 15, ' bold '))
name_Entry.place(x=200, y=450)


name_Check = Button(window, text="check",
					fg="white", bg="green", command=check_name,
					width=5, activebackground="Red",
					font=('times', 15, ' bold '))
name_Check.place(x=360, y=450)

takePhoto = Button(window, text="Take photo",
				   fg="white", bg="green", command=take_Photo,
					width=20, height=3, activebackground="Red",
					font=('times', 15, ' bold '))
takePhoto.place(x=200, y=500)


takeImg = Button(window, text="Camera On",
				   fg="white", bg="green", command=show_frame,
					width=20, height=3, activebackground="Red",
					font=('times', 15, ' bold '))
takeImg.place(x=200, y=700)

trainImg = Button(window, text="No func",
				     fg="white", bg="green", command=no_fnc,
					width=20, height=3, activebackground="Red",
					font=('times', 15, ' bold '))
trainImg.place(x=500, y=700)

trackImg = Button(window, text="Login",
				 fg="white", bg="green", command=detect,
					width=20, height=3, activebackground="Red",
					font=('times', 15, ' bold '))
trackImg.place(x=800, y=700)

quitWindow = Button(window, text="Quit",
					command=window.destroy, fg="white", bg="green",
					width=20, height=3, activebackground="Red",
					font=('times', 15, ' bold '))
quitWindow.place(x=1100, y=700)


window.mainloop()
