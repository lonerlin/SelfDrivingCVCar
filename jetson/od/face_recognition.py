# _*_coding:utf-8 _*_
# @Time　　:2020/8/29 0029   下午 11:25
# @Author　 : Loner Lin
# @File　　  :face_recognition.py
# @Software  :PyCharm

import face_recognition
import os
import re
import threading
import time
import numpy as np
from queue import Queue
from multiprocessing import Process  # ,Queue
from queue import Queue


class FaceRecognition:

    def __init__(self, known_folder, callback):
        self._q_send = Queue(1)
        self._callback = callback
        self._known_folder = known_folder
        self.recognition_thread = MultiFaceRecognition(self._q_send, self._callback, self._known_folder)
        self.recognition_thread.start()

    def recognition(self, frame):

        if not self._q_send.full():
            self._q_send.put(frame)
        else:
            print("请减慢检测速度")

    def close(self):
        if not self._q_send.full():
            self._q_send.put("stop")


class MultiFaceRecognition(threading.Thread):

    def __init__(self, q_receive, callback, known_folder):
        super().__init__()
        self.q_receive = q_receive
        self.callback = callback
        self.known_people_folder = known_folder
        self.known_face_names, self.known_face_encodings = self._scan_known_people()
        print("init_finish.")

    def run(self):
        while True:
            if not self.q_receive.empty():
                brg_image = self.q_receive.get()

                if type(brg_image) == np.ndarray:
                    faces = self.multi_recognition(brg_image)
                    self.callback(faces)
                    pass
                else:
                    break
            # else:
                # print("empty")

    def _scan_known_people(self):
        known_names = []
        known_face_encodings = []

        for file in self._image_files_in_folder(self.known_people_folder):
            basename = os.path.splitext(os.path.basename(file))[0]
            # print(basename)
            img = face_recognition.load_image_file(file)
            encodings = face_recognition.face_encodings(img)

            if len(encodings) > 1:
                print("WARNING: More than one face found in {}. Only considering the first face.".format(file))

            if len(encodings) == 0:
                print("WARNING: No faces found in {}. Ignoring file.".format(file))
            else:
                known_names.append(basename)
                known_face_encodings.append(encodings[0])

        return known_names, known_face_encodings

    def _image_files_in_folder(self, folder):
        return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]

    def multi_recognition(self, image):

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = image[:, :, ::-1]

        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        face_list = []
        # print("recognition begin")
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]
                face_list.append([name, top, right, bottom, left])

            # face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            # best_match_index = np.argmin(face_distances)
            # if matches[best_match_index]:
            #     name = self.known_face_names[best_match_index]

            # if render_image:
            #     # Draw a box around the face
            #     cv2.rectangle(render_image, (left, top), (right, bottom), (0, 0, 255), 2)
            #
            #     # Draw a label with a name below the face
            #     cv2.rectangle(render_image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            #     font = cv2.FONT_HERSHEY_DUPLEX
            #     cv2.putText(render_image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        return face_list
