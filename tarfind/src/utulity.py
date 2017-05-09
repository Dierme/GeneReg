
class Utility(object):

    @staticmethod
    def cut_string(target_str, start_anchor, finish_anchor):
        start_idx = target_str.find(start_anchor)

        if start_idx == -1:
            return None

        start_idx += len(start_anchor)

        finish_idx = target_str.find(finish_anchor, start_idx)

        return target_str[start_idx:finish_idx]
