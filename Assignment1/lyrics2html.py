import sys


def main():
    content = {}
    song = ''
    with open(in_file, 'r+') as text:
        name_line = text.readline()
        for line in text:
            if 'metadata:' in line:
                line = text.next()
                content['url'] = line.replace('source url: ', '')
                line = text.next()
                content['Composer'] = line.replace('Composer: ', '')
                line = text.next()
                content['Lyrics'] = line.replace('Lyrics: ', '')
                line = text.next()
                content['Performer'] = line.replace('Performer: ', '')
                line = text.next()
                content['Year'] = line.replace('Year: ', '')
            elif line != name_line:
                song += line + '<br>'
    if in_hebrew(name_line):
        opening_tags = '<!DOCTYPE html>\n<html dir="rtl">\n<body>\n'
    else:
        opening_tags = '<!DOCTYPE html>\n<html>\n<body>\n'
    closing_tags = '\n</body>\n</html>\n'
    with open(out_file, 'w+') as html:
        html.write(opening_tags)
        html.write('<h1><u>{}</u></h1>'.format(name_line))
        html.write('<p>{}</p>'.format(song.strip('<br>')))
        html.write('<h3><u>Metadata:</u></h3>')
        for key, val in content.iteritems():
            if key == 'url':
                html.write('<h4><u>URL</u>: <a href={val}>click here</a></h4>'.format(val=val))
            else:
                html.write('<h4><u>{key}</u>: {val}</h4>'.format(key=key, val=val))
        html.write(closing_tags)


def in_hebrew(line):
    line = line.decode('UTF-8')
    return any(u"\u0590" <= c <= u"\u05EA" for c in line)


if len(sys.argv) > 2:
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    main()
