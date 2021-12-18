from .models import Model


class Method:
    def __init__(self, model: Model, xvec: tuple, yvec: tuple):
        self.model = model
        self.xvec = xvec
        self.yvec = yvec


class MinSquared(Method):
    def __init__(self, model: Model, xvec: tuple, yvec: tuple):
        super().__init__(model, xvec, yvec)

    def __str__(self):
        func = ""
        for x, y in zip(self.xvec, self.yvec):
            func += f"({str(self.model)}-{y})**2 + ".replace('x', str(x))
        func = func[:-2]
        result = f"(1/{len(self.xvec)-1})*({func})"

        return result

Calcs = [MinSquared]
