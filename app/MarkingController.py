

class MarkingController:
    def __init__(self, *args, **kwargs):
        self.markings = {}

    def get_markings(self):
        return self.markings

    def get_image_markings(self, image_number):
        try:
            return self.markings[image_number]
        except KeyError:
            return []

    def add_marking(self, marking):
        # just add to dict without checking, performance issues
        if marking['image'] in self.markings.keys():
            self.markings[marking['image']].append(marking)
        else:
            self.markings[marking['image']] = [marking]

    def remove_marking_by_id(self, marking_id):
        if marking_id in self.markings.keys():
            del self.markings[marking_id]

    def remove_marking_by_coordinates(self, image_number, x, y):
        try:
            image_markings = self.markings[image_number]
            for marking in image_markings:
                cx1, cy1, cx2, cy2 = marking['coordinates']
                marking_id = marking['marking_id']
                return marking_id
        except KeyError:
            pass

    def delete_all_markings(self):
        self.markings = {}

    def delete_image_markings(self, image_number):
        self.markings[image_number] = []
