import cv2
import serial
import time

# ====== Hubungkan ke Arduino ======
arduino = serial.Serial('COM6', 9600)
time.sleep(2)  # beri waktu koneksi stabil

# ====== Inisialisasi deteksi wajah ======
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kamera tidak dapat diakses.")
    exit()

print("Tekan 'q' untuk keluar dari program.\n")

last_send_time = 0  # waktu terakhir kirim data
status = '0'        # default: tidak ada wajah

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ubah ukuran frame agar efisien
    frame_resized = cv2.resize(frame, (800, 600))
    gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)

    # deteksi wajah
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(50, 50))

    # jika wajah terdeteksi
    if len(faces) > 0:
        status = '1'
        for (x, y, w, h) in faces:
            cv2.rectangle(frame_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame_resized, "Wajah Terdeteksi", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        status = '0'

    # ===== Kirim data ke Arduino setiap 1 detik =====
    current_time = time.time()
    if current_time - last_send_time >= 1:
        arduino.write(status.encode())
        print(f"Python -> {status} ({'Wajah' if status == '1' else 'Tidak ada wajah'})")
        last_send_time = current_time

    # tampilkan video
    cv2.imshow("Deteksi Wajah + Arduino", frame_resized)

    # tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()
