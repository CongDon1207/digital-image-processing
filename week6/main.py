"""Chuong trinh phat hien khuon mat bang OpenCV Haar cascade."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Tuple, Union

import cv2


DEFAULT_CASCADE = "haarcascade_frontalface_alt2.xml"
WINDOW_TITLE = "Face Detection"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Chuong trinh phat hien khuon mat bang OpenCV Haar cascade"
    )
    parser.add_argument(
        "--source",
        default="0",
        help="Chi so webcam (vd: 0) hoac duong dan toi file video",
        metavar="PATH|INDEX",
    )
    parser.add_argument(
        "--cascade",
        default=DEFAULT_CASCADE,
        help="Ten file cascade nam trong cv2.data.haarcascades hoac duong dan tuy y.",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=1.05,
        help="He so phong to giua cac lan quet (nho hon -> nhay hon nhung cham hon).",
    )
    parser.add_argument(
        "--neighbors",
        type=int,
        default=7,
        help="So luong vung phat hien can xac nhan. Tang len de giam false positive.",
    )
    parser.add_argument(
        "--min-size",
        type=int,
        default=45,
        help="Chieu rong/cao toi thieu cua khuon mat (pixel).",
    )
    parser.add_argument(
        "--max-width",
        type=int,
        default=960,
        help="Gioi han do rong frame de giam nhieu va tang FPS.",
    )
    return parser.parse_args()


def resolve_source(raw_source: str) -> Union[int, str]:
    path_candidate = Path(raw_source)
    if raw_source.isdigit() and not path_candidate.exists():
        return int(raw_source)
    return raw_source


def load_cascade(cascade_arg: str) -> Tuple[cv2.CascadeClassifier, Path]:
    candidate = Path(cascade_arg)
    if not candidate.exists():
        candidate = Path(cv2.data.haarcascades) / cascade_arg
    cascade = cv2.CascadeClassifier(str(candidate))
    if cascade.empty():
        raise FileNotFoundError(f"Khong the mo cascade tai {candidate}")
    return cascade, candidate


def preprocess_frame(frame) -> cv2.Mat:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    return gray


def detect_faces(
    cascade: cv2.CascadeClassifier,
    gray_frame,
    scale_factor: float,
    min_neighbors: int,
    min_size_px: int,
) -> Iterable[Tuple[int, int, int, int]]:
    return cascade.detectMultiScale(
        gray_frame,
        scaleFactor=scale_factor,
        minNeighbors=min_neighbors,
        minSize=(min_size_px, min_size_px),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )


def resize_frame(frame, max_width: int):
    height, width = frame.shape[:2]
    if width <= max_width:
        return frame
    ratio = max_width / float(width)
    new_size = (int(width * ratio), int(height * ratio))
    return cv2.resize(frame, new_size, interpolation=cv2.INTER_AREA)


def annotate(frame, faces: Iterable[Tuple[int, int, int, int]]):
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            "Face",
            (x, max(0, y - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )


def main() -> int:
    args = parse_args()
    source = resolve_source(args.source)

    try:
        cascade, cascade_path = load_cascade(args.cascade)
    except FileNotFoundError as exc:
        print(f"Loi: {exc}")
        return 1

    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("Loi: Khong mo duoc nguon video/Webcam!")
        return 1

    print(
        "Dang chay phat hien khuon mat. Bam 'q' de thoat.\n"
        f"Cascade: {cascade_path}"
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Canh bao: Khong doc duoc frame moi, dung chuong trinh.")
            break

        frame = cv2.flip(frame, 1)  # Flip ngang de camera khong bi nguoc
        frame = resize_frame(frame, args.max_width)
        gray = preprocess_frame(frame)
        faces = detect_faces(cascade, gray, args.scale, args.neighbors, args.min_size)

        annotate(frame, faces)
        cv2.putText(
            frame,
            f"Faces: {len(faces)}",
            (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
        )
        cv2.imshow(WINDOW_TITLE, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

