from ultralytics import YOLO
from ultralytics import settings
from pathlib import Path


def main():
    model = YOLO("./datasets/runs/detect/yolov8n_poker91/weights/best.pt")

    rel_path = "./data.yaml"

    # Update multiple settings
    settings.update({
        'runs_dir': '/Users/lukaflores/Code/object-tracking-opencv/Yolo-Poker/datasets/runs',
        'weights_dir': '/Users/lukaflores/Code/object-tracking-opencv/Yolo-Poker/datasets/weights'
    })

    # This file _does_ exist
    assert Path(rel_path).exists(), "File doesn't exist"

    try:
        model.train(
            data=rel_path,
            epochs=50,
            batch=8,
            imgsz=640,
            name='yolov8n_poker',
            device='mps'
        )
    except RuntimeError as e:
        print(
            f"Using a relative path to the YAML loads the YAML correctly, but "
            f"garbage gets prepended to the directories specified within the YAML,"
            f"leading to the following runtime error: \n {e}"
        )


if __name__ == '__main__':
    main()  # execute this only when run directly, not when imported!
