import cv2
import math
import win32api as win

from drawer import Drawer


def closest(faces, w, h):
    mid_w = w / 2
    mid_h = h / 2

    best = None
    best_dist = None
    for face in faces:
        face_x = mid_w - (face[0] + face[2] / 2)
        face_y = mid_h - (face[1] + face[3] / 2)

        dist = math.sqrt(face_x ** 2 + face_y ** 2)

        if best is None or best_dist > dist:
            best_dist = dist
            best = face

    return best


def calculate_move_vector(face, w, h):
    mid_w = w / 2
    mid_h = h / 2

    face_x = mid_w - (face[0] + face[2] / 2)
    face_y = mid_h - (face[1] + face[3] / 2)

    distance = math.sqrt(face_x ** 2 + face_y ** 2)
    x = face_x / max(MAX_DIST, distance)
    y = face_y / max(MAX_DIST, distance)

    return -x, -y


def move_mouse(vector):
    x, y = win.GetCursorPos()
    win.SetCursorPos((x + int(vector[0] * MAX_SPEED), y + int(vector[1] * MAX_SPEED)))


def frame_generator(video):
    while video.isOpened():
        ret, frame = video.read()
        yield frame


MAX_SPEED = 5
MAX_DIST = 300.0
MAX_LENGTH = 50


if __name__ == '__main__':
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    video = cv2.VideoCapture(0)

    for frame in frame_generator(video):
        drawer = Drawer(frame)
        drawer.draw_center_crosshair()

        height, width, three = frame.shape

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(40, 40))
        face = closest(faces, width, height)

        if face:
            move_vector = calculate_move_vector(face, width, height)

            move_mouse(move_vector)

            drawer.draw_line_from_center(*[x * MAX_LENGTH for x in move_vector])
            drawer.draw_head_rectangle(*face)

        cv2.imshow('img', drawer.get_image())

        if cv2.waitKey(1) and 0xFF == ord(' '):
            break

    video.release()
    cv2.destroyAllWindows()
