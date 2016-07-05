import lxml.html

html = """
<html>
<head>
    <title>test</title>
</head>
<body>
    <div id="nothing">
        <table>
            <tr>
                <td>1</td><td>Game of Thrones</td>
            </tr>
        </table>
    </div>

    <p>hello</p>
    <div id="content">
        <table id="fruit">
            <tr>
                <td>1</td><td>apple</td>
            </tr>
            <tr>
                <td>2</td><td>pear</td>
            </tr>
        </table>

        <table id="os">
            <tr>
                <td>1</td><td>Linux</td>
            </tr>
            <tr>
                <td>2</td><td>OS X</td>
            </tr>
            <tr>
                <td>3</td><td>Windows</td>
            </tr>
        </table>

        <table id="car">
            <tr>
                <td>1</td><td>Golf R</td>
            </tr>
            <tr>
                <td>2</td><td>Focus RS</td>
            </tr>
            <tr>
                <td>3</td><td>A AMG</td>
            </tr>
            <tr>
                <td>4</td><td>Audi RS3</td>
        </tr>
    </table>
    </div>
</body>
</html>
"""


root = lxml.html.fromstring(html)

body = root.xpath('/html/body')
tables = body[0].xpath('//table')
print(len(tables))

# tables[0] is first table
trs1 = tables[0].xpath('.//tr')
trs2 = tables[0].xpath('//tr')
# same as line above
trs3 = root.xpath('//tr')

print(len(trs1))
print(len(trs2))
print(len(trs3))
