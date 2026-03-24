import sys
sys.path.append("D:/ai-parking-system/libs")

from flask import Flask, render_template, request
import cv2
import numpy as np
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def detect_parking(image_path):
    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 1)

    thresh = cv2.adaptiveThreshold(
        blur,255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        25,16
    )

    count = np.sum(thresh) / 255

    if count > 50000:
        return "Occupied"
    else:
        return "Free"


@app.route("/", methods=["GET","POST"])
def index():

    status = None
    image = None

    if request.method == "POST":

        file = request.files["image"]

        if file:
            path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(path)

            status = detect_parking(path)
            image = path

    return render_template("index.html", status=status, image=image)


if __name__ == "__main__":
    app.run(debug=True)