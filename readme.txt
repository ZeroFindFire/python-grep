Find in path:
python pre.py pattern [path] [-dn :depth = n]

Find in contents:
python pre.py -c pattern [path] [-dn :depth = n] [-nexp :use expression exp to filter path]

Find in input:
order|python pre.py -i pattern

pattern should be regular expression

example:
a) Find in path:
python pre.py (.*?)\.py . -d1
result:
.\cmd.py    f
.\cmd.pyc    f
.\pre.py    f

python pre.py (.*?)\.py$ . -d1
result:
.\cmd.py    f
.\pre.py    f

b) Find in contents:
python pre.py -c cmd -n(.*?)\.py$
result:
.\pre.py:

    129:     import cmd
    131:     ft = cmd.Filter(sys.argv[1:])

c) Find in input:
dir|python pre.py -i "<DIR>"
result:
2018/10/12  09:59    <DIR>          .
2018/10/12  09:59    <DIR>          ..