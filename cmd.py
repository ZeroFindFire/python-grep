#coding=utf-8


class Filter(object):
    def __init__(self, argv):
        self.argv = [s.strip() for s in argv]
    def gets(self, mark):
        rst = []
        for s in self.argv:
            if s.find(mark)== 0:
                rst.append(s[len(mark):])
        return rst 
    def lefts(self, mark = "-"):
        rst = []
        for s in self.argv:
            if s.find(mark)== -1:
                rst.append(s)
        return rst 
    def get(self, mark):
        rst = self.gets(mark)
        return None if len(rst)==0 else rst[-1]
    def contain(self, mark):
        return len(self.gets(mark))>0
def test():
    import sys 
    print("std:")
    print(sys.stdin)
    print(sys.stdout )
    argv = sys.argv[1:]
    ft = Filter(argv)
    print("-i:", ft.gets("-i"))
    print("-i:", ft.contain("-i"))
    print("not mark:", ft.lefts("-"))
    print("-v:", ft.gets("-v"))
if __name__=="__main__":
    test()
