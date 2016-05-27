import marshal
import sys

def print_error(line):
    print >> sys.stderr, line

def save_obj(obj, name ):
    with open('obj/' + name + '.pkl', 'wb') as f:
        marshal.dump(obj, f)#, marshal.HIGHEST_PROTOCOL)


def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return marshal.load(f)
