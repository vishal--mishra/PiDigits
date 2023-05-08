#!/usr/bin/env python3

import json as js;
import sys;

def KeyPaths(d):
    if (type(d) != dict):
        return None;
    k = d.keys(); r = []; # r += k
    for i in k:
        if (type(d[i]) == dict):
            r += map(lambda k:i+'.'+k, KeyPaths(d[i]));
        else:
            r += [i];
    r.sort();
    return r;

def KeyPathValue(o,p):
    cmd = "o" + "".join(map(lambda k:'["'+k+'"]', p.split("."))); #print(cmd);
    return eval(cmd);

def KeyPathValueList(d):
    keys = KeyPaths(d);
    values = map(lambda k:KeyPathValue(d,k), keys);
    return (keys, values);

def KeyPathValueListToText(obj):
    kpvl = KeyPathValueList(obj);
    #return "\n".join(map(lambda (k,v):"%-40s | %s" % (k,v), zip(kpvl[0], kpvl[1])));
    return "\n".join(map(lambda kv:"%-40s | %s" % (kv[0],kv[1]), zip(kpvl[0], kpvl[1])));

def test(obj):
    print("obj =", obj);
    print("KeyPaths(obj) =", KeyPaths(obj));
    print('KeyPathValue(obj, "c.f.h.y") =', KeyPathValue(obj, "c.f.h.y"));
    print('KeyPathValueList(obj) =', KeyPathValueList(obj));
    print(KeyPathValueListToText(obj));

if 0:
    test({'a':'b', 'c':{'d':'e', 'f':{'h':{'y':'x'}}}});
    test({'a': 'b', 'm':[1,2], "n":[{"p":"q"}], 'c': {'d': 'e', 'f': {'h': {'y': 'x'}}}});

def dumpKeyPathValueList(objText):
    jsObjs = js.loads(objText);
    if type(jsObjs) != list:
        print(KeyPathValueListToText(jsObjs));
    else:
        for obj in jsObjs:
            print(KeyPathValueListToText(obj));

def dumpKeyPaths(objText):
    jsObjs = js.loads(objText);
    if type(jsObjs) != list:
        #print("obj =", jsObjs);
        #print("KeyPaths(obj) =", KeyPaths(jsObjs));
        print(" | ".join(KeyPaths(jsObjs)));
    else:
        for obj in jsObjs:
            #print("obj =", obj);
            #print("KeyPaths(obj) =", KeyPaths(obj));
            print(" | ".join(KeyPaths(obj)));

def Usage():
    print('''Usage: echo '{"a":"b"}' | %s [-k | -v]''' % sys.argv[0]);
     
def main():
    if len(sys.argv) < 2:
        Usage();
        return -1;
    if sys.argv[1] == '-k':
        dumpKeyPaths(sys.stdin.read());
    elif sys.argv[1] == '-v':
        dumpKeyPathValueList(sys.stdin.read());
    else:
        Usage();
    return 0;

main()
