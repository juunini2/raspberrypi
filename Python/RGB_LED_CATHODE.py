import RPi.GPIO as GPIO    # GPIO 제어 모듈
import time                # time 모듈

R1 = 17                    # wPi. 0(GPIO. 0), BCM. 17, Physical-Pin. 11(LED 4)
G1 = 18                    # wPi. 1(GPIO. 1), BCM. 18, Physical-Pin. 12(LED 2)
B1 = 27                    # wPi. 2(GPIO. 2), BCM. 27, Physical-Pin. 13(LED 1)

R2 = 22                    # wPi. 3(GPIO. 3), BCM. 22, Physical-Pin. 15(LED 4)
G2 = 23                    # wPi. 4(GPIO. 4), BCM. 23, Physical-Pin. 16(LED 2)
B2 = 24                    # wPi. 5(GPIO. 5), BCM. 24, Physical-Pin. 18(LED 1)

R3 = 5                     # wPi. 21(GPIO. 21), BCM. 5, Physical-Pin. 29(LED 4)
G3 = 6                     # wPi. 22(GPIO. 22), BCM. 6, Physical-Pin. 31(LED 2)
B3 = 13                    # wPi. 23(GPIO. 23), BCM. 13, Physical-Pin. 33(LED 1)
# 가장 긴 핀(LED 3)은 3.3V에 연결

GPIO.setmode(GPIO.BCM)     # BCM모드 설정

GPIO.setup(R1, GPIO.OUT)   # OUTPUT(출력) 설정
GPIO.setup(G1, GPIO.OUT)   # OUTPUT(출력) 설정
GPIO.setup(B1, GPIO.OUT)   # OUTPUT(출력) 설정

GPIO.setup(R2, GPIO.OUT)   # OUTPUT(출력) 설정
GPIO.setup(G2, GPIO.OUT)   # OUTPUT(출력) 설정
GPIO.setup(B2, GPIO.OUT)   # OUTPUT(출력) 설정

GPIO.setup(R3, GPIO.OUT)   # OUTPUT(출력) 설정
GPIO.setup(G3, GPIO.OUT)   # OUTPUT(출력) 설정
GPIO.setup(B3, GPIO.OUT)   # OUTPUT(출력) 설정

# pwm 2차원 배열 설정
pwm = [
    [GPIO.PWM(R1, 120), GPIO.PWM(G1, 120), GPIO.PWM(B1, 120)],
    [GPIO.PWM(R2, 120), GPIO.PWM(G2, 120), GPIO.PWM(B2, 120)],
    [GPIO.PWM(R3, 120), GPIO.PWM(G3, 120), GPIO.PWM(B3, 120)]
]

# pwm Duty Cycle 설정(Cathod는 값이 반대로 입력되어야 해서 Duty Cycle이 100이면 꺼짐)
for i in range(0, len(pwm)) :
    for j in range(0, len(pwm[i])) :
        pwm[i][j].start(100)

# LED 색 정의 함수(Cathode는 값이 반대로 입력되어야 해서 최대값(255)를 빼줌)
def LedColorSet1(r, g, b) :
    pwm[0][0].ChangeDutyCycle((255 - r) / 2.55)
    pwm[0][1].ChangeDutyCycle((255 - g) / 2.55)
    pwm[0][2].ChangeDutyCycle((255 - b) / 2.55)

def LedColorSet2(r, g, b) :
    pwm[1][0].ChangeDutyCycle((255 - r) / 2.55)
    pwm[1][1].ChangeDutyCycle((255 - g) / 2.55)
    pwm[1][2].ChangeDutyCycle((255 - b) / 2.55)

def LedColorSet3(r, g, b) :
    pwm[2][0].ChangeDutyCycle((255 - r) / 2.55)
    pwm[2][1].ChangeDutyCycle((255 - g) / 2.55)
    pwm[2][2].ChangeDutyCycle((255 - b) / 2.55)

# 각 LED의 초기값, 증가/감소값 3차원 배열 설정
freq = [
    [[0, 1], [100, 1], [200, -1]],
    [[200, -1], [100, 1], [0, 1]],
    [[100, 1], [200, -1], [0, 1]]
]

try :   # 정상 작동일 때
    print("Ctrl + C 를 눌러 종료합니다.")
    while True :    # 무한루프

        # 각 LED의 R, G, B 색상의 증감 설정
        for i in range(0, len(freq)) :
            for j in range(0, len(freq[i])) :
                freq[i][j][0] += freq[i][j][1]
                if freq[i][j][0] >= 256 :   # 255(최대값)을 넘었을 경우
                    freq[i][j][0] = 255
                    freq[i][j][1] = -1      # 증가 값을 감소로 돌림
                elif freq[i][j][0] <= -1 :  # 0(최소값)을 넘었을 경우
                    freq[i][j][0] = 0
                    freq[i][j][1] = 1       # 감소 값을 증가 값으로 돌림

        # 미리 선언한 함수를 이용하여 LED의 색 정의
        LedColorSet1(freq[0][0][0], freq[0][1][0], freq[0][2][0])
        LedColorSet2(freq[1][0][0], freq[1][1][0], freq[1][2][0])
        LedColorSet3(freq[2][0][0], freq[2][1][0], freq[2][2][0])
        time.sleep(0.005)   # 0.005초마다 증감이 발생하여 색이 변함

except :    # 종료 시

    # pwm 전부 중지
    for i in range(0, len(pwm)) :
        for j in range(0, len(pwm[i])) :
            pwm[i][j].stop()

    GPIO.cleanup()  # GPIO 초기화
    print("end")    # "end" 메시지 출력
