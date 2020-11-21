class LayeredArray:
    def __init__(self):
        self.data = []
        self.start_indices = [0]

    def append(self, thing):
        self.data.append(thing)

    def close_layer(self):
        start_index = len(self.data)
        assert start_index >= self.start_indices[-1]
        self.start_indices.append(start_index)

    def get_layer_slice(self, layer_index):
        assert layer_index < len(self.start_indices)
        start = self.start_indices[layer_index]
        end = self.start_indices[layer_index + 1]
        return slice(start, end)

    def get_layer_size(self, layer_index):
        layer_slice = self.get_layer_slice(layer_index)
        return layer_slice.stop - layer_slice.start

    def get_layer(self, layer_index):
        layer_slice = self.get_layer_slice(layer_index)
        return self.data[layer_slice]
