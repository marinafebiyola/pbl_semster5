import cv2
import time

# Load Haar Cascade wajah
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

last_face_time = time.time()     # waktu terakhir wajah terdeteksi
last_print_time = time.time()    # waktu terakhir print
last_printed_value = None        # mencegah print berulang status yang sama

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(40, 40)
        )

        current_time = time.time()

        # Update waktu terakhir wajah terdeteksi
        if len(faces) > 0:
            last_face_time = current_time
            current_value = 1
        else:
            # Jika tidak ada wajah >= 5 detik
            if current_time - last_face_time >= 5:
                current_value = 0
            else:
                current_value = None  # belum print apa-apa

        # Cetak setiap 1 detik
        if current_value is not None:
            if current_time - last_print_time >= 1:
                print(current_value)
                last_print_time = current_time
                last_printed_value = current_value

        # Gambar kotak wajah
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                          (0, 255, 0), 2)

        cv2.imshow("Face Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass

# Saat program dimatikan → cetak 0
print(0)

cap.release()
cv2.destroyAllWindows()
