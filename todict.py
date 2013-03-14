#coding:utf-8

from xml.etree.ElementTree import *

def todict(xml):
    elem = fromstring(xml);
    return _todict(elem);

def _todict(elem):
    result = {};
    result[elem.tag] = None;

    if len(list(elem)) == 0:
        return elem.text
    else:
        result[elem.tag] = {};
        for child in list(elem):
            t = _todict(child)
            if child.tag in result[elem.tag]:
                result[elem.tag][child.tag].append(t);
            else:
                result[elem.tag][child.tag] = [t];

    return result;

if __name__ == '__main__':
    print todict("""
    <b>
        <y>a</y>
        <y>b</y>
        <x>b</x>
    </b>
    """)

