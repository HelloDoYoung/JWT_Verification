import os
import cv2
from pyzbar.pyzbar import decode
import jwt

# JWT secret key (PHP 코드와 동일해야 함)
key = "V2RXZ-u4yQm2Wk4rwNvn"

# 환경 변수 설정 (Homebrew 설치 경로를 포함)
os.environ["DYLD_LIBRARY_PATH"] = "/opt/homebrew/Cellar/zbar/0.23.93/lib:/usr/local/lib"

def decode_qr_code(frame):
    decoded_objects = decode(frame)
    for obj in decoded_objects:
        jwt_token = obj.data.decode('utf-8')
        try:
            decoded_payload = jwt.decode(jwt_token, key, algorithms=['HS256'])
            student_info = decoded_payload['data']
            print(f"Student ID: {student_info['student_id']}")
            print(f"Name: {student_info['name']}")
            print(f"Grade: {student_info['grade']}")
            print(f"Class: {student_info['class']}")
        except jwt.ExpiredSignatureError:
            print("The token has expired")
        except jwt.InvalidTokenError:
            print("Invalid token")

def main():
    cap = cv2.VideoCapture(0)  # 0번 카메라를 엽니다

    if not cap.isOpened():
        print("Cannot open camera")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Cannot receive frame (stream end?). Exiting ...")
            break

        decode_qr_code(frame)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):  # 'q' 키를 눌러서 종료합니다
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
