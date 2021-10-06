
import unicodedata as UNI


html_template = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8"/>
    <title>U</title>
    <style>
        td      {{ padding: 1px 10px 2px 10px; }}
        .header {{ cursor: pointer; font-size: 20px; margin-top: 50px; margin-bottm: 10px; }}
        .hidden {{ display: none; }}
    </style>
    <script>
        window.toggle_hidden = function (id)
        {{
            //console.log(id);
            table = document.getElementById(id);
            if (table)
            {{
                table.classList.toggle("hidden");
            }}
        }}
    </script>
  </head>
  <body style="font-size: 14px;">
    <div id="content">
      {CONTENT}
    </div>
  </body>
</html>
"""

block_template = """
<div>
  <div><span class="header" onclick="toggle_hidden('{TID}')">&#62; {BNAME}</span></div>
  <table class="hidden" id="{TID}">
    {BCNT}
  </table>
</div>
"""


def unipoint(intpoint) :
    hexstr = hex(intpoint)[2:].upper()
    while (len(hexstr) < 4) :
        hexstr = '0' + hexstr
    return 'U+' + hexstr

def binarystr(bytearr) :
    ret = ''
    for b in bytearr :
        act = bin(b)[2:]
        while len(act) < 8 :
            act = '0' + act
        ret += ' ' + act
    return ret




#############   MAIN   #############


blocks = []
content = ''

with open('unicode_blocks.txt','r') as bf :
    for line in bf :
        linestr = line.strip()
        if (len(linestr) == 0) or (linestr[0] == '#') :
            continue
        block = linestr.split('\t')
        blocks.append(block)
        #i+=1
        #if i > 318 :
        #    break


for block in blocks :
    r = block[1].split('..')
    r1 = int(r[0][2:], 16)
    r2 = int(r[1][2:], 16)
    blockcnt = ''
    for i in range(r1, r2+1) :
        
        try :
            actname = UNI.name(chr(i)).lower()
        except ValueError:
            actname = 'noname'
        
        try :
            bin8name = binarystr(chr(i).encode('utf_8'))
        except UnicodeEncodeError:
            bin8name = '--'
        
        try :
            bin32name = binarystr(chr(i).encode('utf_32_be'))
        except UnicodeEncodeError:
            bin32name = '--'
        
        blockcnt += ('          <tr><td>' + unipoint(i) + '</td>' +
                                   '<td>' + str(i) + '</td>' +
                                   '<td>U8:' + bin8name + '</td>' +
                                   #'<td>U32:' + bin32name + '</td>' +
                                   '<td style="font-size: 40px;"> &#' + str(i) + '; </td>' +
                                   '<td>' + actname + '</td>' +
                                '</tr>\n')
    content += block_template.format(BNAME = block[1] + ' // ' + block[2] + ' // ' + block[5], BCNT = blockcnt, TID='T' + str(i))
        
    
f = open('unicode.html', 'w')
htmlstr = html_template.format(CONTENT=content)
f.write(htmlstr)
f.close()
