import re
import sys
import codecs
import xml.etree.cElementTree as etree

arabic = re.compile(ur'[^\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff\.]+', re.UNICODE)


with open(sys.argv[1], 'r') as infile:
	with open(sys.argv[2], 'w') as outfile:

		context = etree.iterparse(infile, events = ('start','end'))
		context = iter(context)
		event, root = context.next()

		for event, elem in context:

			if event == 'end' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}text':

				text = elem.text
				
				if text:

					#text = text.encode('utf8')
					
					text = arabic.sub(' ', text)
					text = re.sub('\.', '\n', text)
					
					if text:
						outfile.write(text.encode('utf8'))
					# else:
						#print "none"

				root.clear()