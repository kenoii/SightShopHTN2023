''' Demonstrates how to subscribe to and handle data from gaze and event streams '''

import time

import adhawkapi
import adhawkapi.frontend
import cv2
import numpy as np

import os # import google cloud vision
# from google.cloud import vision
# from google.cloud import vision_v1
# from google.cloud.vision_v1 import types

from web import *
# client = vision.ImageAnnotatorClient()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'mimetic-parity-399213-b0d6d77275d0'

latestCapFrame = None

class FrontendData:
    ''' BLE Frontend '''
    lastBlink  = 0

    def __init__(self):
        # Instantiate an API object
        # TODO: Update the device name to match your device
        self._api = adhawkapi.frontend.FrontendApi(ble_device_name='ADHAWK MINDLINK-290')

        # Tell the api that we wish to receive eye tracking data stream
        # with self._handle_et_data as the handler
        self._api.register_stream_handler(adhawkapi.PacketType.EYETRACKING_STREAM, self._handle_et_data)

        # Tell the api that we wish to tap into the EVENTS stream
        # with self._handle_events as the handler
        self._api.register_stream_handler(adhawkapi.PacketType.EVENTS, self._handle_events)

        # Start the api and set its connection callback to self._handle_tracker_connect/disconnect.
        # When the api detects a connection to a MindLink, this function will be run.
        self._api.start(tracker_connect_cb=self._handle_tracker_connect,
                        tracker_disconnect_cb=self._handle_tracker_disconnect)

    def shutdown(self):
        '''Shutdown the api and terminate the bluetooth connection'''
        self._api.shutdown()

    @staticmethod
    def _handle_et_data(et_data: adhawkapi.EyeTrackingStreamData):
        ''' Handles the latest et data '''
        # if et_data.gaze is not None:
        #     xvec, yvec, zvec, vergence = et_data.gaze
        #     print(f'Gaze={xvec:.2f},y={yvec:.2f},z={zvec:.2f},vergence={vergence:.2f}')

        # if et_data.eye_center is not None:
        #     if et_data.eye_mask == adhawkapi.EyeMask.BINOCULAR:
        #         rxvec, ryvec, rzvec, lxvec, lyvec, lzvec = et_data.eye_center
        #         print(f'Eye center: Left=(x={lxvec:.2f},y={lyvec:.2f},z={lzvec:.2f}) '
        #               f'Right=(x={rxvec:.2f},y={ryvec:.2f},z={rzvec:.2f})')

        # if et_data.pupil_diameter is not None:
        #     if et_data.eye_mask == adhawkapi.EyeMask.BINOCULAR:
        #         rdiameter, ldiameter = et_data.pupil_diameter
        #         print(f'Pupil diameter: Left={ldiameter:.2f} Right={rdiameter:.2f}')

        # if et_data.imu_quaternion is not None:
        #     if et_data.eye_mask == adhawkapi.EyeMask.BINOCULAR:
        #         x, y, z, w = et_data.imu_quaternion
        #         print(f'IMU: x={x:.2f},y={y:.2f},z={z:.2f},w={w:.2f}')

    @staticmethod
    def _handle_events(event_type, timestamp, *args):
        if event_type == adhawkapi.Events.BLINK:
            duration = args[0]
            if timestamp - FrontendData.lastBlink < 0.5:
                global latestCapFrame
                recImage(cv2, latestCapFrame)
            print(f'Got blink: {timestamp} {duration}')
            FrontendData.lastBlink = timestamp
        if event_type == adhawkapi.Events.EYE_CLOSED:
            eye_idx = args[0]
            print(f'Eye Close: {timestamp} {eye_idx}')
            # FrontendData.timeSinceClosed = timestamp
        if event_type == adhawkapi.Events.EYE_OPENED:
            # if timestamp-FrontendData.timeSinceClosed > 5:
            #     recImage()
            eye_idx = args[0]
            print(f'Eye Open: {timestamp} {eye_idx}')

    def _handle_tracker_connect(self):
        print("Tracker connected")
        self._api.set_et_stream_rate(60, callback=lambda *args: None)

        self._api.set_et_stream_control([
            adhawkapi.EyeTrackingStreamTypes.GAZE,
            adhawkapi.EyeTrackingStreamTypes.EYE_CENTER,
            adhawkapi.EyeTrackingStreamTypes.PUPIL_DIAMETER,
            adhawkapi.EyeTrackingStreamTypes.IMU_QUATERNION,
        ], True, callback=lambda *args: None)

        self._api.set_event_control(adhawkapi.EventControlBit.BLINK, 1, callback=lambda *args: None)
        self._api.set_event_control(adhawkapi.EventControlBit.EYE_CLOSE_OPEN, 1, callback=lambda *args: None)

    def _handle_tracker_disconnect(self):
        print("Tracker disconnected")

class WebcamCapture:
    def __init__(self, camera_index=1): # Index is selecting the device
        self.cap = cv2.VideoCapture(camera_index)
        global latestCapFrame
        latestCapFrame = self.cap
        if not self.cap.isOpened():
            raise Exception("Error: Could not open camera.")
        
        cv2.namedWindow("Webcam Feed", cv2.WINDOW_NORMAL)

    def start_capture(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                cv2.imshow("Webcam Feed", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def stop_capture(self):
        self.cap.release()
        cv2.destroyAllWindows()

#     def detect_text_uri(uri): # """Detects text in the file located in Google Cloud Storage or on the Web."""
        

#         image = vision.Image()
#         image.source.image_uri = uri

#         response = client.text_detection(image=image)
#         texts = response.text_annotations
#         print("Texts:")

#         for text in texts:
#             print(f'\n"{text.description}"')

#             vertices = [
#                 f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
#             ]

#             print("bounds: {}".format(",".join(vertices)))

#         if response.error.message:
#             raise Exception(
#                 "{}\nFor more info on error messages, check: "
#                 "https://cloud.google.com/apis/design/errors".format(response.error.message)
#             )
    
def main():
    ''' App entrypoint '''
    frontend = FrontendData()
    webcam = WebcamCapture(camera_index=0)
    webcam.start_capture()
    #detect_text_uri()
    try:
        while True:
            time.sleep(0)
    except (KeyboardInterrupt, SystemExit):
        frontend.shutdown()

if __name__ == '__main__':
    main()