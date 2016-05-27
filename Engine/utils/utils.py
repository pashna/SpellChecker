import marshal
import sys
import cPickle

def print_error(line):
    print >> sys.stderr, line

def save_obj(obj, name ):
    with open('obj/' + name + '.pkl', 'wb') as f:
        cPickle.dump(obj, f)#,  marshal.version)#, marshal.HIGHEST_PROTOCOL)


def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return cPickle.load(f)
