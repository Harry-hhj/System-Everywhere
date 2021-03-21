import face_recognition
import cv2
import threading
import time
import ctypes
import inspect


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


class FaceRecognition:
    def __init__(self, names: list, features: list, callback):
        self.names = names
        self.features = features
        self.thread = None
        self.start(callback)

    def detect(self, callback):
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        # print(self.features)

        while True:
            # 读取摄像头画面
            ret, frame = self.video_capture.read()
            if not ret:
                continue
            # out.write(cv2.resize(frame, (1920, 1080)))

            # 改变摄像头图像的大小，图像小，所做的计算就少
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # opencv的图像是BGR格式的，而我们需要是的RGB格式的，因此需要进行一个转换。
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # 根据encoding来判断是不是同一个人，是就输出true，不是为false
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # 默认为unknown
                    matches = face_recognition.compare_faces(face_encoding, self.features, tolerance=0.39)
                    name = "Unknown"
                    # print(self.names)
                    # print(matches)

                    if True in matches:
                        first_match_index = matches.index(True)
                        # print(first_match_index)
                        name = self.names[first_match_index]
                    face_names.append(name)

            process_this_frame = not process_this_frame

            # 将捕捉到的人脸显示出来
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # 矩形框
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # 加上标签
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                # print(name)

            callback.emit(frame, face_names)
            time.sleep(1)

    def start(self, callback):
        self.video_capture = cv2.VideoCapture(0)
        if self.thread is not None:
            self.stop()
        self.thread = threading.Thread(target=self.detect, args=(callback,))
        self.thread.setDaemon(True)
        self.thread.start()

    def stop(self):
        stop_thread(self.thread)
        self.thread = None
        self.video_capture.release()
        self.video_capture = None

    def __del__(self):
        try:
            self.video_capture.release()
            stop_thread(self.thread)
        except Exception as e:
            print(e)
