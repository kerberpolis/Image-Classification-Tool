



class MarkingController:
    def __init__(self, *args, **kwargs):
        self.markings = {}

    def add_marking(self, new_marking):
        if self.markings:
            for marking_id, marking in self.markings.copy().items():
                if new_marking['coordinates'] == marking['coordinates']:
                    print('marking already in markings, will not add')
                    return
                print(new_marking)
                self.markings[new_marking['marking_id']] = new_marking
                print(self.markings)
        else:
            self.markings[new_marking['marking_id']] = new_marking

    def remove_marking(self, marking_id):
        if marking_id in self.markings.keys():
            del self.markings[marking_id]

    def get_markings(self):
        return self.markings

    def delete_all_markings(self):
        self.markings = {}