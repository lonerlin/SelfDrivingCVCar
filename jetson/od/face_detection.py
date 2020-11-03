import cv2
class FaceDetection:
    def __init__(self, xml_file="", radio=1.0):
        if radio < 1.0:
            radio =1.0
        self.radio = radio

        if xml_file == "":
            self.xml_file = 'haarcascade_frontalface_default.xml'
        else:
            self.xml_file = xml_file
        self.detector = cv2.CascadeClassifier(self.xml_file)

    def detect(self, frame, render_image=None):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detectMultiScale(gray, 1.3, 5)
        if self.radio != 1.0 and faces:
            faces = self._radio(faces, frame)
        if render_image is not None:
            self._render(render_image, faces)
        return faces

    def _radio(self, faces, image):
        width = image.shape[0]
        height = image.shape[1]
        if faces:
            new_faces = []
            for(x, y, w, h) in faces:
                x_radio = (x + w) * (self.radio - 1.0) / 2
                x_temp = int(x - x_radio) if (x - x_radio) > 0 else 0
                w_temp = int(w + 2 * x_radio) if (x_temp + w + 2 * x_radio) < width else width
                y_radio = (y + h) * (self.radio - 1.0)/2
                y_temp = int(y-y_radio) if (y-y_radio) > 0 else 0
                h_temp = int(h + 2 * y_radio) if (y_temp + h + 2 * y_radio) < height else height
                new_faces.append(x_temp, y_temp, w_temp, h_temp)
        else:
            return []

    def _render(self, image, faces):
        if faces:
            for(x, y, w, h) in faces:
                for (x, y, w, h) in faces:
                    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
