class MyModel:
    """Models the input sensors.
    
    These are just touch sensitive panels.
    Broken out so that this can be changed from either the simulator panel or the real sensors.
    """

    def __init__(self):
        self.sensors = [False, False]

    def toggle(self, i: int) -> None:
        self.sensors[i] = not self.sensors[i]

    def update(self, new: list[int]) -> None:
        for i in range(len(self.sensors)):
            if self.sensors[i] != new[i]:
                self.sensors[i] = new[i]


class MyController:
    def __init__(self, model):
        self.model = model
        pass

    def destroy(self) -> None:
        pass

    def draw(self, lights, locator) -> None:
        pass

    def process_inputs(self) -> None:
        pass
    
    def read_key(self):
        pass
