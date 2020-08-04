from collections import defaultdict

class Variables:
    def __init__():
        self.prevText = ""
        self.currBaseText = ""
        self.level = 0
        self.urlKnowledge = defaultdict(list) # key -> url, value -> list of highlighted text
        self.urlWindowNames = {}
        self.newWindowIndex = 0
        self.windowIndex = 0

    