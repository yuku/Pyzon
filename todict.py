#coding:utf-8

from xml.etree.ElementTree import *

def scraping_tag(tag):
    s = tag.find("{");
    e = tag.find("}");
    return tag

def todict(xml):
    elem = fromstring(xml);
    return _todict(elem);

def _todict(elem):
    result = {};
    result[scraping_tag(elem.tag)] = None;

    if len(list(elem)) == 0:
        return elem.text
    else:
        result[elem.tag] = {};
        for child in list(elem):
            t = _todict(child)
            if child.tag in result[elem.tag]:
                result[scraping_tag(elem.tag)][scraping_tag(child.tag)].append(t);
            else:
                result[scraping_tag(elem.tag)][scraping_tag(child.tag)] = [t];

    return result;

if __name__ == '__main__':
    print scraping_tag("nadeko{not}cute")
    print todict("""
    <b>
        <y>a</y>
        <y>b</y>
        <x>b</x>
    </b>
    """)

