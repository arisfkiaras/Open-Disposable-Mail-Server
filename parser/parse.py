import os.path
import time
import glob
import re
from elastic import Elastic
from postgres import Postgres

# https://gist.github.com/eranhirs/5c9ef5de8b8731948e6ed14486058842
def sanitize_string(text):
    
    # Escape special characters
    # http://lucene.apache.org/core/old_versioned_docs/versions/2_9_1/queryparsersyntax.html#Escaping Special Characters
    text = re.sub('([{}])'.format(re.escape('\\+\-&|!(){}\[\]^~*?:\/')), r"\\\1", text)

    # AND, OR and NOT are used by lucene as logical operators. We need
    # to escape them
    for word in ['AND', 'OR', 'NOT']:
        escaped_word = "".join(["\\" + letter for letter in word])
        text = re.sub(r'\s*\b({})\b\s*'.format(word), r" {} ".format(escaped_word), text)

    # Escape odd quotes
    quote_count = text.count('"')
    return re.sub(r'(.*)"(.*)', r'\1\"\2', text) if quote_count % 2 == 1 else text


def parse_mail_el(fromAddress, subject, content):
    fromAddress = sanitize_string(fromAddress.lower())
    subject = sanitize_string(subject)
    print(fromAddress)
    print(subject)
    print(content)
    if fromAddress[:7] != "from\: ":
        #throw exception
        # print ("throw exception fromAddress")
        return
    else:
        fromAddress = fromAddress[7:].replace('\r', '').replace('\n', '')
    
    if len(fromAddress) > 500:
        fromAddress = fromAddress[:500]
   
    if subject[:10].lower() != "subject\: ":
        print ("throw exception subject")
        #return
    else:
        subject = subject[10:].replace('\r', '').replace('\n', '')

    if len(subject) > 500:
        subject = subject[:500]

    if content is not None and len(content) > 0:
        content = sanitize_string(content)
    else:
        content = subject
    

    data = {}
    data["from"] = fromAddress
    data["subject"] = subject
    data["content"] = content
    # print(data)
    el = Elastic()
    el.postData(body=data)

def parse_mail_postgres(fromAddress, subject, content):
    fromAddress = sanitize_string(fromAddress.lower())
    subject = sanitize_string(subject)

    if fromAddress[:7] != "from\: ":
        return
    else:
        fromAddress = fromAddress[7:].replace('\r', '').replace('\n', '')
    
    if len(fromAddress) > 500:
        fromAddress = fromAddress[:500]
   
    if subject[:10].lower() != "subject\: ":
        print ("throw exception subject")
        #return
    else:
        subject = subject[10:].replace('\r', '').replace('\n', '')

    if len(subject) > 500:
        subject = subject[:500]

    if content is not None and len(content) > 0:
        content = content
    else:
        content = subject
    

    data = {}
    data["from"] = fromAddress
    data["subject"] = subject
    data["content"] = content
    user_domain =  fromAddress.split('@')

    postgres = Postgres()
    postgres.insert_email(user_domain[0], user_domain[1], subject, content)

def insert_to_postgres(data):
    postgres = Postgres()
    postgres.insert_email(
        data['from'], 
        '',
        data['to_user'],
        data['to_domain'], 
        data['subject'],
        data['content']
    )

def parse_mail(filee):
    data = {}

    with open(filee, 'r') as openfile:
        to_line = openfile.readline().lower()

        if len(to_line) < 4:
            to_line = openfile.readline().lower()

        if to_line[:15] != "x-original-to: ":

            print("to_line:" + to_line[:15])
            return
        to_address = to_line[15:].replace('\r', '').replace('\n', '')
        to_address = to_address.split('@')
        if len(to_address) != 2:
            print("to_address" + to_address)
            return
        data['to_user'] = to_address[0]
        data['to_domain'] = to_address[1]
        
        # NAME <user@domain.com>
        from_line = openfile.readline().lower()
        if from_line[:6] != "from: ":
            print("from_line" + from_line)
            return
        data['from'] = from_line[6:].replace('\r', '').replace('\n', '')
        
        content = ""

        subject_line = openfile.readline()
        if subject_line[:9].lower() != "subject: ":
            content = content + subject_line
            data['subject'] = ''
        else:
            data['subject'] = subject_line[10:].replace('\r', '').replace('\n', '')
    
        content = content + openfile.read()
        data['content'] = content

        return data

def main():    
    while True:
        time.sleep(2)
        for filee in glob.glob("/data/emails/*.mail"):
            try:
                data = parse_mail(filee)
                print(data)
                if data and data is not None:
                    insert_to_postgres(data)
                    os.remove(filee)
            except Exception as error:
                print('Caught this error: ' + repr(error))
            #os.remove(filee)

if __name__ == "__main__":
    # execute only if run as a script
    main()