#coding=utf-8

import re 
import os 
def output(*argv):
    s = " ".join(str(t) for t in argv)
    import sys 
    sys.stdout.write(s+"\n")
def readfile(filepath):
    try:
        f = open(filepath,'r')
        s = f.read()
        f.close()
        return s 
    except:
        return ''
def compare(string, pattern):
    rst = pattern.findall(string)
    return rst 

# list filename, match_pattern, filepath 
# 
def link_path(path, filename):
    try:
        import platform
        is_windows = platform.system().lower() == 'windows'
    except:
        is_windows = False
    spt = "\\" if is_windows else "/"
    if path[-1] not in ['/','\\']:
        path = path + spt 
    return path + filename 
def __search_filename(path, pattern, max_depth = -1):
    check_quit()
    rst = []
    name = os.path.basename(path)
    path_type = "f" if os.path.isfile(path) else "d"
    match = compare(name,pattern)
    if len(match)>0:
        #s = "%s %s %s %s"%(path, name, path_type, str(match))
        s = "%s    %s"%(path, path_type)
        rst.append(s)
    if os.path.isfile(path):
        return rst
    if max_depth == 0:
        return rst 
    elif max_depth > 0:
        max_depth -= 1
    try:
        lst = os.listdir(path)
        for it in lst:
            tpath = link_path(path, it )
            rst += __search_filename(tpath, pattern, max_depth)
    except:
        output("error: can't visit ", path)
    finally:
        return rst 
def compare_contents(string, pattern, line_mark = True):
    rst = pattern.findall(string)
    outs = []
    base = 0
    lines = string.split("\n")
    if len(rst)>0:
        for it in rst:
            if type(it) in [list, tuple]:
                s = it[0]
                show = str(it)
            else:
                s = it 
                show = s 
            index = string.find(s, base)
            ts = string[:index+len(s)]
            line = len(ts.split("\n"))
            base = index + 1
            show = lines[line-1] #+" match:"+ show 
            if line_mark:
                show = str(line)+": "+show
            outs.append(show)
    return outs 

def __search_filecontents(path, pattern, name_pattern, max_depth = -1):
    check_quit()
    rst = []
    name = os.path.basename(path)
    if os.path.isfile(path):
        if name_pattern is not None and len(name_pattern.findall(name)) == 0:
            return rst 
        contents = readfile(path)
        match = compare_contents(contents,pattern)
        if len(match)>0:
            match = '\n    '.join(match)
            s = "%s:\n\n    %s\n\n"%(path, match)
            rst.append(s)
        return rst
    if max_depth == 0:
        return rst 
    elif max_depth > 0:
        max_depth -= 1
    try:
        lst = os.listdir(path)
        for it in lst:
            tpath = link_path(path, it )
            rst += __search_filecontents(tpath, pattern, name_pattern, max_depth)
    except:
        output("error: can't visit ", path)
    finally:
        return rst 
def search_contents_input(pattern):
    pattern = re.compile(pattern)
    contents = ""
    try:
        while True:
            contents+=raw_input()+"\n"
    except:
        pass 
    match = compare_contents(contents,pattern,False)
    output("result:")
    output('\n'.join(match))
    
def search_name(path, pattern, max_depth = -1):
    pattern = re.compile(pattern)
    rst = __search_filename(path, pattern, max_depth)
    output("result:")
    output('\n'.join(rst))

def search_contents(path, pattern, name_pattern = None, max_depth = -1):
    pattern = re.compile(pattern)
    if name_pattern is not None:
        name_pattern = re.compile(name_pattern)
    rst = __search_filecontents(path, pattern, name_pattern, max_depth)
    output("result:")
    output('\n'.join(rst))
quit_mark = False
def check_quit():
    global quit_mark
    if not quit_mark:
        return 
    import sys 
    sys.exit()
def check_input():
    global quit_mark
    global quit_thd_mark
    try:
        while not quit_thd_mark:
            raw_input()
    except:
        quit_mark = True
helps = """
Find in path:
python pre.py pattern [path] [-dn :depth = n]

Find in contents:
python pre.py -c pattern [path] [-dn :depth = n] [-nexp :use expression exp to filter path]

Find in input:
order|python pre.py -i pattern

pattern should be regular expression
"""

def main():
    import threading
    import cmd 
    import sys 
    thd = threading.Thread(target = check_input)
    ft = cmd.Filter(sys.argv[1:])
    if ft.contain("-h") or ft.contain("--help"):
        output(helps)
        return 
    lefts = ft.lefts("-")
    path = "."
    if len(lefts)==0:
        raise Exception("no pattern found")
    else:
        pattern = lefts[0]
        if len(lefts)>1:
            path = lefts[1]
    depth = -1
    sdepth = ft.get('-d')
    if sdepth is not None:
        depth = int(sdepth)
    name_pattern = ft.get("-n")
    global quit_thd_mark 
    quit_thd_mark = False
    if ft.contain("-i"):
        search_contents_input(pattern)
    elif ft.contain('-c'):
        thd.setDaemon(True)
        thd.start()
        search_contents(path, pattern, name_pattern, depth)
        quit_thd_mark = True
        #thd.join()
    else:
        thd.setDaemon(True)
        thd.start()
        search_name(path, pattern, depth)
        quit_thd_mark = True
        #thd.join()
    sys.exit()
if __name__=='__main__':
    main()