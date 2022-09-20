import cv2 as cv

video_cap = cv.VideoCapture("videos/video3.avi")

WIDTH = int(video_cap.get(cv.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(video_cap.get(cv.CAP_PROP_FRAME_HEIGHT))

comms = []  # komutlar listesi
is_arrived = False


def give_command(widthF, heightF, xF, yF):
    hDiff = 30  # merkez ve kapı arasındaki yükseklik farkının alabileceği değer
    wDiff = 5
    whDiff = 10  # yükseklik ve genişlik arası alabilecek değer farkı değişkeni
    initTurn = False  # belirli bir yakınlığa gelindiğinde dönme işlemi başlatılması için değişken
    global is_arrived
    global comms

    if(not is_arrived):
        if(heightF != 720):
            if "ILERLE" not in comms:
                comms.append("ILERLE")
            # DÖNME KOMUTLARI
            if(heightF > 300 and heightF - widthF > whDiff):
                initTurn = True
            if(initTurn):
                if "ILERLE" in comms:
                    comms.remove("ILERLE")
                if "SOLA DON" not in comms:
                    comms.append("SOLA DON")

                if(heightF - widthF < whDiff):
                    initTurn = False
                    if "SOLA DON" in comms:
                        comms.remove("SOLA DON")
                    if "ILERLE" not in comms:
                        comms.append("ILERLE")
            else:
                if "SOLA DON" in comms:
                    comms.remove("SOLA DON")
        else:
            is_arrived = True
            comms = []
        #
        if(heightF < 400 and (2*yF + heightF - HEIGHT)/2 > hDiff):
            if "ALCAL" not in comms:
                comms.append("ALCAL")
        elif(heightF >= 400 and (2*yF + heightF - HEIGHT)/2 > hDiff * 2):
            if "ALCAL" not in comms:
                comms.append("ALCAL")
        else:
            if "ALCAL" in comms:
                comms.remove("ALCAL")
        #
        if(heightF < 400 and (2*xF + widthF - WIDTH)/2 - wDiff > 0):
            if "SAGA YONEL" not in comms:
                comms.append("SAGA YONEL")
            if "SOLA YONEL" in comms:
                comms.remove("SOLA YONEL")
        elif(heightF < 400 and (2*xF + widthF - WIDTH)/2 + wDiff < 0):
            if "SOLA YONEL" not in comms:
                comms.append("SOLA YONEL")
            if "SAGA YONEL" in comms:
                comms.remove("SAGA YONEL")
        else:
            if "SAGA YONEL" in comms:
                comms.remove("SAGA YONEL")
            if "SOLA YONEL" in comms:
                comms.remove("SOLA YONEL")


while True:
    ret, frame = video_cap.read()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (7, 7), 0)
    canny = cv.Canny(blur, 100, 100)

    contours, _ = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        cntArea = cv.contourArea(cnt)
        maxCntArea = max(contours, key=cv.contourArea)
        cv.drawContours(frame, [cnt], -1, (0, 0, 255), 2)
        x, y, w, h = cv.boundingRect(maxCntArea)
        give_command(widthF=w, heightF=h, xF=x, yF=y)

        if(not is_arrived):
            # width text
            cv.putText(frame, f"Genislik: {str(w)}", (50, 50),
                       cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2, cv.LINE_AA)
            # height text
            cv.putText(frame, f"Yukseklik: {str(h)}", (50, 100),
                       cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2, cv.LINE_AA)
            # komut text
            cv.putText(frame, f"Komutlar: {str(comms)}", (250, 50),
                       cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2, cv.LINE_AA)

        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv.circle(frame, ((x * 2 + w) // 2, (y * 2 + h) // 2), radius=0,
                  color=(0, 255, 0), thickness=10)

    cv.circle(frame, (WIDTH//2, HEIGHT//2), radius=0,
              color=(0, 0, 255), thickness=10)

    cv.imshow("Canny", canny)
    cv.imshow("Frame", frame)

    if cv.waitKey(20) & 0xFF == ord("d"):
        break

video_cap.release()
cv.destroyAllWindows()
