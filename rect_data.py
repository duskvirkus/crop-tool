class RectData:

    def __init__(
        self,
        x: int,
        y: int,
        padding_percent: int = 40
    ):
        self.x1 = x
        self.y1 = y
        self.x2 = x
        self.y2 = y
        self.padding_percent = padding_percent

    def set1(self, x, y):
        self.x1 = x
        self.y1 = y
        self.swap_if_needed()

    def set2(self, x, y):
        self.x2 = x
        self.y2 = y
        self.swap_if_needed()

    def swap_if_needed(self):
        if self.x2 < self.x1:
            temp = self.x2
            self.x2 = self.x1
            self.x1 = temp

        if self.y2 < self.y1:
            temp = self.y2
            self.y2 = self.y1
            self.y1 = temp

    def get1(self):
        return (self.x1, self.y1)

    def get2(self):
        return (self.x2, self.y2)

    def get_square(self):
        x_dim = self.x2 - self.x1
        y_dim = self.y2 - self.y1

        if x_dim >= y_dim:
            y_mid = (y_dim / 2) + self.y1
            half_x = x_dim / 2

            return [
                (
                    self.x1,
                    int(y_mid - half_x)
                ),(
                    self.x2,
                    int(y_mid + half_x)
                )
            ]

        x_mid = (x_dim / 2) + self.x1
        half_y = y_dim / 2

        return [
            (
                int(x_mid - half_y),
                self.y1
            ),(
                int(x_mid + half_y),
                self.y2
            )
        ]

    def get_padded(self):
        square = self.get_square()
        
        dim = square[1][0] - square[0][0]

        padding = int(dim * (self.padding_percent / 100))

        return [
            (
                square[0][0] - padding,
                square[0][1] - padding
            ),
            (
                square[1][0] + padding,
                square[1][1] + padding
            )
        ]