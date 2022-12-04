from tkinter import *
import tkinter.messagebox as msg

import cv2
import numpy as np
from PIL import Image, ImageTk
import face_recognition

import os
import sys

import serial


port = "/dev/ttyUSB0"
baud = 19200
ser = serial.Serial(port, baud, timeout = 1)

def send_this(msg):
	ser.write(msg)


is_inf = False
msg_to_send = '$(failure)@(user_name)#'

def inf_false(event):
	global msg_to_send
	global is_inf
	
	is_inf = True
	msg_to_send = '$false@unknwon@0#'


def inf_true(event):
	global msg_to_send
	global is_inf
	
	is_inf = True

	msg_to_send = '$true@unknwon@1#'


def restart():
    os.execl(sys.executable, sys.executable, *sys.argv)

def check_name():
	
	if name_Entry.get() in known_face_names:
		msg.showerror("에러", "이미 있는 이름입니다.")
		name_Entry.delete(0, END)
	else:
		msg.showinfo("확인", name_Entry.get() + ' 이(는) 사용가능한 이름입니다.')

window = Tk()
window.title("Face_Recogniser")
window.geometry('800x480')

# 실행시 전체화면으로 실행
# F11을 통해 전체화면 제어
window.attributes('-fullscreen', True)
window.bind("<F11>", lambda event: window.attributes("-fullscreen", not window.attributes("-fullscreen")))
window.bind("<Escape>", lambda event: window.attributes("-fullscreen", False))

window.configure(background='white')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)


window.bind("<F8>", inf_true)
window.bind("<F9>", inf_false)


cap = cv2.VideoCapture(0)

def show_frame():

	cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
    
	cv2image = cv2.resize(cv2image, None, fx=0.6, fy=0.6)

	img = Image.fromarray(cv2image)

	imgtk = ImageTk.PhotoImage(image = img)
	webcam_label.imgtk = imgtk
	webcam_label.configure(image=imgtk)

	webcam_label.after(20, show_frame)

def restart_():
	restart()


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
	
	global msg_to_send

	# 캠 화면에서 하나의 프레임을 뽑아옴
	ret, frame = cap.read()

	# BGR color(OpenCV 에서 사용) 를 RGB color(face_recognition 에서 사용) 로 변경
	rgb_frame = frame[:, :, ::-1]
	rgb_frame = cv2.resize(rgb_frame, None, fx=0.4, fy=0.4)

	# 프레임에서 모든 얼굴과 얼굴 인코딩을 찾음
	face_locations = face_recognition.face_locations(rgb_frame)
	face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

	name = "Unknown"
	
	# 비디오 프레임에서 각 얼굴 반복
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


	
	# 얼굴 인식( 얼굴 위치 파악 )
	face_location = face_recognition.face_locations(frame)


	if not is_inf:

		# 위치 값이 없으면 => 얼굴이 인식되지 않으면
		if not face_location:
			msg_to_send = '$true@unkwon@1#'
			b_msg = bytes(msg_to_send, 'utf-8')
			detected_name.configure(text="반갑습니다.")
			send_this(b_msg)

		else:
			msg_to_send = '$false@'+ name + '@0#'
			b_msg = bytes(msg_to_send, 'utf-8')
			send_this(b_msg)

	elif is_inf:
		b_msg = bytes(msg_to_send, 'utf-8')
		send_this(b_msg)
	
	
	#print(msg_to_send)
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

# 제목 라벨
message = Label(
	window, text="Face Recognition Login",
	bg="green", fg="white", width=30,
	height=2, font=('times', 20, 'bold'))
message.place(x=170, y=20)


# 웹 캠
webcam_label = Label(window, width=400, height=300)
webcam_label.place(x=300, y=100)


# 등록부
name = Label(window, text="Regist",
 			height=2, fg="green",
 			bg="white", font=('times', 25, ' bold '))
name.place(x=20, y=110)


name = Label(window, text="name",
 			height=2, fg="green",
 			bg="white", font=('times', 15, ' bold '))
name.place(x=20, y=190)


name_Entry = Entry(window,
 			width=10, bg="white",
 			fg="green", font=('times', 15, ' bold '))
name_Entry.place(x=20, y=230)


name_Check = Button(window, text="check",
					fg="white", bg="green", command=check_name,
					width=5, activebackground="Red",
					font=('times', 10, ' bold '))
name_Check.place(x=120, y=230)



detected_name = Label(window, text="반갑습니다.",
 			height=3, fg="green",
 			bg="white", font=('times', 20, ' bold '))
detected_name.place(x=20, y=270)




takePhoto = Button(window, text="Take photo",
				   fg="white", bg="green", command=take_Photo,
					width=10, height=3, activebackground="Red",
					font=('times', 10, ' bold '))
takePhoto.place(x=140, y=400)


takeImg = Button(window, text="Camera On",
				   fg="white", bg="green", command=show_frame,
					width=10, height=3, activebackground="Red",
					font=('times', 10, ' bold '))
takeImg.place(x=240, y=400)

trainImg = Button(window, text="Restart",
				     fg="white", bg="green", command=restart_,
					width=10, height=3, activebackground="Red",
					font=('times', 10, ' bold '))
trainImg.place(x=340, y=400)

trackImg = Button(window, text="Login",
				 fg="white", bg="green", command=detect,
					width=10, height=3, activebackground="Red",
					font=('times', 10, ' bold '))
trackImg.place(x=440, y=400)

quitWindow = Button(window, text="Quit",
					command=window.destroy, fg="white", bg="green",
					width=10, height=3, activebackground="Red",
					font=('times', 10, ' bold '))
quitWindow.place(x=540, y=400)


window.mainloop()
