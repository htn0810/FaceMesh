import mediapipe as mp
import cv2 as cv
from scipy.spatial import distance as dis
import threading
import pyttsx3

# Import date and time
import datetime
from time import strftime

# Import flask API
from flask import Flask, render_template, Response

# use SQL
from Database import Notification

# Import send message to telegram
from telegram_utils import send_telegram
import asyncio
import threading

# Import constant Facemesh
from ConstantFacemesh import *



def run_speech(speech ,speech_message):
    speech.say(speech_message)
    speech.runAndWait()




def draw_landmarks(image, outputs, land_mark, color):
    height, width = image.shape[:2]

    for face in land_mark:
        point = outputs.multi_face_landmarks[0].landmark[face]

        point_scale = ((int)(point.x * width), (int)(point.y * height))

        cv.circle(image, point_scale, 2, color, 1)


def euclidean_distance(image, top, bottom):
    height, width = image.shape[0:2]

    point1 = int(top.x * width), int(top.y * height)
    point2 = int(bottom.x * width), int(bottom.y * height)

    distance = dis.euclidean(point1, point2)
    return distance


def get_aspect_ratio(image, outputs, top_bottom, left_right):
    landmark = outputs.multi_face_landmarks[0]

    top = landmark.landmark[top_bottom[0]]
    bottom = landmark.landmark[top_bottom[1]]

    top_bottom_dis = euclidean_distance(image, top, bottom)

    left = landmark.landmark[left_right[0]]
    right = landmark.landmark[left_right[1]]

    left_right_dis = euclidean_distance(image, left, right)

    aspect_ratio = left_right_dis / top_bottom_dis

    # print(top_bottom_dis, left_right_dis, aspect_ratio)

    return aspect_ratio

def get_aspect_ratio_2(image, outputs, top_bottom_1, top_bottom_2, left_right):
    landmark = outputs.multi_face_landmarks[0]

    top_1 = landmark.landmark[top_bottom_1[0]]
    bottom_1 = landmark.landmark[top_bottom_1[1]]

    top_bottom_dis_1 = euclidean_distance(image, top_1, bottom_1)

    top_2 = landmark.landmark[top_bottom_2[0]]
    bottom_2 = landmark.landmark[top_bottom_2[1]]

    top_bottom_dis_2 = euclidean_distance(image, top_2, bottom_2)

    left = landmark.landmark[left_right[0]]
    right = landmark.landmark[left_right[1]]

    left_right_dis = euclidean_distance(image, left, right)

    aspect_ratio_2 = (top_bottom_dis_1 + top_bottom_dis_2)/(2 *left_right_dis)
    return aspect_ratio_2


# capture = cv.VideoCapture(0)

frame_count = 0
frame_count_focus = 0
min_frame = 10
min_tolerance = 3.0

# Declare main of Flask API
app = Flask(__name__)
msg_yawn = ""
msg_sleep = ""
message = ""
last_alert_sleep = None
last_alert_yawn = None
alert_each = 10


# speech = pyttsx3.init()

# t = threading.Thread(target=run_speech, args=(speech, 'Drowsy Warning: You looks tired.. please take rest'))

def generate_frames():
    global frame_count_focus, frame_count, msg_yawn, msg_sleep, message,last_alert_sleep, last_alert_yawn, alert_each
    capture = cv.VideoCapture(0)
    while True:
        result, image = capture.read()

        if result:
            image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            outputs = face_model.process(image_rgb)

            if outputs.multi_face_landmarks:
                frame_count_focus = 0
                # print(outputs.multi_face_landmarks)

                draw_landmarks(image, outputs, FACE, COLOR_GREEN)

                draw_landmarks(image, outputs, LEFT_EYE_TOP_BOTTOM, COLOR_RED)
                draw_landmarks(image, outputs, LEFT_EYE_LEFT_RIGHT, COLOR_RED)

                ratio_left = get_aspect_ratio(image, outputs, LEFT_EYE_TOP_BOTTOM, LEFT_EYE_LEFT_RIGHT)

                draw_landmarks(image, outputs, RIGHT_EYE_TOP_BOTTOM, COLOR_RED)
                draw_landmarks(image, outputs, RIGHT_EYE_LEFT_RIGHT, COLOR_RED)

                ratio_right = get_aspect_ratio(image, outputs, RIGHT_EYE_TOP_BOTTOM, RIGHT_EYE_LEFT_RIGHT)

                ratio = (ratio_left + ratio_right) / 2.0
                image = cv.putText(image, "Eye: " + str(ratio)[0:4], (50, 50), cv.FONT_HERSHEY_SIMPLEX,
                                   1, (255, 0, 0), 2, cv.LINE_AA)

                if ratio > min_tolerance:
                    frame_count += 1
                else:
                    frame_count = 0

                if frame_count > min_frame:
                    # Closing the eyes
                    # speech.say('Drowsy Alert: It Seems you are sleeping.. please wake up')
                    # speech.runAndWait()
                    message = 'Drowsy Alert: It Seems you are sleeping.. please wake up'
                    # t = threading.Thread(target=run_speech, args=(speech,message))  # create new instance if thread is dead
                    # t.start()

                    image = cv.putText(image, "Sleep!", (250, 50), cv.FONT_HERSHEY_SIMPLEX,
                                       1, (0, 0, 255), 2, cv.LINE_AA)
                    msg_sleep = "please wake up"
                    full_datetime = strftime("%d/%m/%y at %H:%M:%S %p")
                    if (last_alert_sleep is None) or (
                            (datetime.datetime.utcnow() - last_alert_sleep).total_seconds() > alert_each):
                        last_alert_sleep = datetime.datetime.utcnow()
                        Notification.saveNotify(None, full_datetime, msg_sleep)
                        thread = threading.Thread(target=send_telegram, args=("alert.png","It Seems you are sleeping.. please wake up"))
                        thread.start()
                        # send_telegram()

                draw_landmarks(image, outputs, UPPER_LOWER_LIPS, COLOR_BLUE)
                draw_landmarks(image, outputs, LEFT_RIGHT_LIPS, COLOR_BLUE)

                ratio_lips = get_aspect_ratio(image, outputs, UPPER_LOWER_LIPS, LEFT_RIGHT_LIPS)
                image = cv.putText(image, "Lips: " + str(ratio_lips)[0:4], (50, 100), cv.FONT_HERSHEY_SIMPLEX,
                                   1, (0, 255, 0), 2, cv.LINE_AA)
                if ratio_lips < 1.3:
                    # Open his mouth
                    # speech.say('Drowsy Warning: You looks tired.. please take rest')
                    # speech.runAndWait()
                    message = 'Drowsy Warning: You looks tired.. please take rest'
                    # p = threading.Thread(target=run_speech, args=(speech, message))  # create new instance if thread is dead
                    # p.start()
                    image = cv.putText(image, "Yawn!", (250, 100), cv.FONT_HERSHEY_SIMPLEX,
                                       1, (0, 255, 0), 2, cv.LINE_AA)
                    msg_yawn = "Có Dấu Hiệu Buồn Ngủ"
                    full_datetime = strftime("%d/%m/%y at %H:%M:%S %p")
                    if (last_alert_yawn is None) or (
                            (datetime.datetime.utcnow() - last_alert_yawn).total_seconds() > alert_each):
                        last_alert_yawn = datetime.datetime.utcnow()
                        Notification.saveNotify(None, full_datetime, msg_yawn)
                        cv.imwrite("alert.png", cv.resize(image, dsize=None, fx=1, fy=1))
                        # thread = threading.Thread(target=asyncio.run(send_telegram()))
                        thread = threading.Thread(target=send_telegram, args=("alert.png","You looks tired.. please take rest"))
                        thread.start()


            else:
                frame_count_focus += 1
                if frame_count_focus > min_frame * 2:
                    image = cv.putText(image, "Vui long nhin vao camera", (100, 100), cv.FONT_HERSHEY_SIMPLEX,
                                       1, (0, 0, 255), 2, cv.LINE_AA)
                    message = 'Please keep your eyes into the camera'
                    # p = threading.Thread(target=run_speech, args=(speech, message))  # create new instance if thread is dead
                    # p.start()
            cv.imshow("FACE MESH", image)

            # Flask Api
            ret, buffer = cv.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            # Flask Api

            if cv.waitKey(1) & 255 == 27:
                break

    capture.release()
    cv.destroyAllWindows()


# Flask API
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def videoTemplate():
    return render_template('video.html', msg_yawn=msg_yawn, msg_sleep=msg_sleep, message=message)


@app.route('/video/show')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')


@app.route('/statistics/worldwide')
def statistics_worldwide():
    return render_template('statistics_worldwide.html')


@app.route('/statistics/vietnam')
def statistics_vietnam():
    return render_template('statistics_vietnam.html')

@app.route('/notification')
def notification():
    results = Notification.getNotify(None)
    return render_template('notification.html', results=results)

@app.route('/notification/remove')
def remove_data():
    Notification.deleteAllRecords(None)
    return render_template('notification.html')



if __name__ == "__main__":
    app.run(debug=True)


