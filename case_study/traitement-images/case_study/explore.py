"""Check data loading and locate slots in representative scenes."""

from collections import Counter

from tools import RESULTS, available_images, load_image, save_preview, slots


def main():
    images = available_images()
    boxes = slots()
    print(f"{len(images)} images, {len(boxes)} monitored slots")
    print("Images by split:", dict(Counter(row["split"] for row in images)))
    for row in images:
        if row["image_id"] in ("R00", "C001", "C033", "C057", "V001", "E001"):
            image = load_image(row["filename"])
            output = RESULTS / f"preview-{row['image_id']}.png"
            save_preview(image, boxes, output)
            print(row["image_id"], row["day"], row["time"],
                  row["weather"], "->", output)


if __name__ == "__main__":
    main()
