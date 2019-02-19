#encoding=utf-8
import platform as pf
import cv2
# import numpy as np

python_version = pf.python_version()
pf_sys = pf.uname()[0]
print (pf_sys,'Python',python_version)

sourse = 0
if	 (pf_sys == "Windows"):
	cas = cv2.CascadeClassifier("D:\Program Files\haarcascades\haarcascade_smile.xml")	  #载入级联分类器，即人脸数据库
elif (pf_sys == "Linux"):
	cas = cv2.CascadeClassifier("/home/wanl/Desktop/disk/part_d/Program Files/haarcascades/haarcascade_frontalface_alt2.xml")
elif (pf_sys == "Darwin"):
	cas = cv2.CascadeClassifier("/Volumes/ntfs_d/Program Files/haarcascades/haarcascade_frontalface_alt2.xml")
	sourse = "/Volumes/SHARE/videoplayback.mp4"
else :
	print("Hello World!")

cap = cv2.VideoCapture(sourse)
fps = 24.0
h = int(cap.get(3))  #获取当前摄像头支持的高
w = int(cap.get(4))  #获取当前摄像头支持的宽
print (h," x ",w,'\n')

# # FourCC全称Four-Character Codes，代表四字符代码 (four character code), 它是一个32位的标示符，其实就是typedef unsigned int FOURCC;是一种独立标示视频数据流格式的四字符代码。
# # 因此cv2.VideoWriter_fourcc()函数的作用是输入四个字符代码即可得到对应的视频编码器。
# fourcc = cv2.VideoWriter_fourcc(*'XVID')	#使用XVID编码器

# # 创建视频文件，用于保存
# # 文件名、选择编码方式、每秒钟播放fps、视频尺寸
# videosave = cv2.VideoWriter("F:\项目\无人机项目\Debug\摄像头\TV_CAM_设备_Detected_4.avi", fourcc, fps, (h,w))	#出分别是：保存文件名、编码器、帧率、视频宽高

firstFrame = 1	#None
cmp = 27
gauss = 5 
full = 0
face_num = 0
rate = 0.8
try:
	while(1):
		(ret, img) = cap.read()
		if not ret:  
			print ("open video failed")  
			break
		else:
			# print ("open video success")
			img = cv2.flip(img, 1)
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图，以便运算

			rects = cas.detectMultiScale(gray)	#检测人脸：跟数据库进行比较
			face_num = 0
			line = 0
			for x, y, width, height in rects:
				cv2.rectangle(img, (x, y), (x+width, y+height), (255, 0, 0), 2)	#结果：人脸的坐标x, y, 长度, 宽度
				face_num += 1
				# print ('**','落水',face_num,':',x, y, end='\t')
				line = 1
			if (line):
				line = 0
				print('->')
			# # blur = cv2.GaussianBlur(gray, (gauss, gauss), 0)	#进行高斯平滑处理，图像矩阵、滤波窗口大小、标准差，取该像素周围窗口大小内像素的平均值
			# # # if firstFrame is None:
				# # # firstFrame = gray	#初始背景图
			# # frameData = cv2.absdiff(firstFrame, gray)	#计算当前帧与背景图的不同
			# # motion = cv2.threshold(frameData, cmp, 255, cv2.THRESH_BINARY)[1]	#进行二值化处理，如果像素小于阈值25，就变成0，大于阈值变成255
			# # motion = cv2.dilate(motion, None, iterations=full)		#膨胀：扩展阈值图像 填充孔洞
			# (cnts, ret) = cv2.findContours(motion.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)	#		在阈值图像上寻找轮廓
			
			# for c in cnts:	#遍历轮廓
				# if cv2.contourArea(c) < 100:	#计算轮廓大小，忽略掉小于500的
					# continue
				# (x, y, w, h) = cv2.boundingRect(c)	#计算轮廓的边界框，在当前帧中绘制
				# cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
			
			# videosave.write(img)
			cv2.imshow("Org", cv2.resize(img, (int(h*rate), int(w*rate))))
			# cv2.imshow("Gray", gray)
			# cv2.imshow("Blur", blur)
			# cv2.imshow("Abs", frameData)
			# cv2.imshow("Threshold", motion)
		Key = cv2.waitKey(1) & 0xFF
		if Key == ord('q'):
			break
		elif Key == ord('+'):	#修改二值化比较阈值
			cmp += 1
			print ("			cmp =",cmp)
		elif Key == ord('_'):
			cmp -= 1
			print ("			cmp =",cmp)
		elif Key == ord('z'):	#修改高斯模糊深度
			if gauss >= 3:
				gauss -= 2
				print ("			gauss =",gauss)
			else : print ("			Stop Adjusting Gauss Value !")
		elif Key == ord('x'):
			gauss += 2
			print ("			gauss =",gauss)
		elif Key == ord('i'):	#修改膨胀填充面积
			full += 1
			print ("			full = ",full)
		elif Key == ord('d'):
			if full > 0:
				full -= 1
				print ("			full = ",full)
			else : print ("			full has been full !")
		elif Key == ord(' '):	#Press blank to pause;
			cv2.waitKey(0)
	print("* " *13)

finally:
	cap.release()
	# videosave.release() #释放保存句柄
	cv2.destroyAllWindows()
	print("Exit!")
