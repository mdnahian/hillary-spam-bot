from bs4 import BeautifulSoup
import urllib2

base_url = 'https://wikileaks.org/clinton-emails/emailid/'
total_emails = 32795


def get_HTML(input_url):
        return urllib2.urlopen(input_url)


def match_class(target):
        def do_match(tag):
            classes = tag.get('class', [])
            return all(c in classes for c in target)
        return do_match


def execute():
	with open('hilary.txt', 'a') as hilary_file:
		for i in range(2, total_emails):
			raw_html = get_HTML(base_url+str(i))
			html = BeautifulSoup(raw_html, "html.parser")

			email = html.find(match_class(['email-content']))
			for element in email.find_all(['div', 'span']):
				element.decompose()

			raw_body = email.get_text()
			body = ""

			for line in raw_body.split('\n'):
				if 'Subject:' not in line and 'UNCLASSIFIED' not in line \
				and 'PR' not in line and 'Sent via' not in line \
				and 'B6' not in line and 'mm:' not in line \
				and 'QR' not in line and 'RE' not in line \
				and 'IN FULL' not in line and 'Headers' not in line \
				and 'Date:' not in line:
					body += line

			body = ' '.join(''.join(body.split('\n')).strip().split())

			if len(body) > 10 and len(body) < 2000:
				print('\n\n\n')
				print(i)
				print(body)
				hilary_file.write(body.encode('utf-8')+'\n\n')
			else:
				print('Too Large')
				print(len(body))
	



if __name__ == '__main__':
	execute()