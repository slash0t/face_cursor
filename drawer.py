import cv2


class Drawer:
    crosshair_color = (255, 0, 0)
    line_color = (0, 255, 0)
    rectangle_color = (255, 255, 0)

    def __init__(self, image):
        self._img = image
        self.height, self.width, three = self._img.shape

    def get_image(self):
        return self._img

    def draw_center_crosshair(self):
        mid_x = self.width // 2
        mid_y = self.height // 2

        cv2.rectangle(self._img, (mid_x, 0), (mid_x, self.height), self.crosshair_color, 1)
        cv2.rectangle(self._img, (0, mid_y), (self.width, mid_y), self.crosshair_color, 1)

    def draw_line_from_center(self, x, y):
        mid_x = self.width // 2
        mid_y = self.height // 2

        cv2.arrowedLine(
            self._img,
            (mid_x, mid_y),
            (mid_x + int(x), mid_y + int(y)),
            self.line_color,
            2
        )

    def draw_head_rectangle(self, x, y, w, h):
        cv2.rectangle(self._img, (x, y), (x + w, y + h), self.rectangle_color, 2)
