# Assuming files as (user_id, item_id, rating)
class FileStream:

    def __init__(self, path, sep=" "):
        self.stream = self._parse_file(path, sep)

    def _parse_file(self, path, sep):
        stream = []
        with open(path, "r") as f:
            line = f.readline()
            while line:
                stream_arr = line.split(sep)
                user_id = int(stream_arr[0])
                item_id = int(stream_arr[1])
                rating = float(stream_arr[2])
                stream.append((user_id, item_id, rating))
                line = f.readline()
            f.close()
        return stream

    def process_stream(self, model):
        # it = 0
        for rating in self.stream:
            # print(f"New rating entering: {rating} -> Iter: {it}")
            # it += 1
            model.new_rating(rating)
        return model

    def process_stream_eval_anim(self, evaluator, anim_class):
        animation = anim_class(self.stream, evaluator)
        animation.show()