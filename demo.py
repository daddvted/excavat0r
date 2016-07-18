from lxml import etree

xml_doc = """
<books>
<book>
  <title lang="eng">Harry Potter</title>
  <price>29.99</price>
</book>
<book>
  <title lang="eng">Learning XML</title>
  <price>39.95</price>
</book>
</books>
"""


root = etree.fromstring(xml_doc)

books = root.xpath('book')
print(books)
bks = root.xpath('//book')
print(bks)

