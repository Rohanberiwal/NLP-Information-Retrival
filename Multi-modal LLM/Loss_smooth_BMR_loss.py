import numpy as np

def calculate_iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    intersection = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
    area_box1 = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    area_box2 = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)
    union = area_box1 + area_box2 - intersection
    return intersection / union if union > 0 else 0

def apply_bmr_smoothing(predictions, iou_threshold=0.5, weight_by_confidence=True):
    if len(predictions) == 0:
        return predictions
    predictions = predictions[np.argsort(-predictions[:, 4])]
    refined_boxes = []
    while len(predictions) > 0:
        current_box = predictions[0]
        remaining_boxes = predictions[1:]
        overlaps = [
            calculate_iou(current_box[:4], other_box[:4]) > iou_threshold
            for other_box in remaining_boxes
        ]
        overlapping_boxes = np.array([current_box] + remaining_boxes[np.array(overlaps)])
        if weight_by_confidence:
            weights = overlapping_boxes[:, 4]
            refined_box = np.average(overlapping_boxes[:, :4], axis=0, weights=weights)
            refined_confidence = np.mean(overlapping_boxes[:, 4])
        else:
            refined_box = np.mean(overlapping_boxes[:, :4], axis=0)
            refined_confidence = np.mean(overlapping_boxes[:, 4])
        refined_boxes.append(np.append(refined_box, refined_confidence))
        predictions = remaining_boxes[~np.array(overlaps)]
    return np.array(refined_boxes)

if __name__ == "__main__":
    predicted_boxes = np.array([
        [100, 150, 200, 250, 0.9],
        [105, 155, 205, 255, 0.85],
        [300, 400, 350, 450, 0.95],
        [320, 420, 370, 470, 0.88],
    ])
    refined_boxes = apply_bmr_smoothing(predicted_boxes, iou_threshold=0.5)
    print("Refined Bounding Boxes:")
    print(refined_boxes)
