import re,json,requests
input1=raw_input("Enter url")
while True:

    string = raw_input('>')
    input = string.split()
    actions = ['add', 'search', 'buy', 'trans']
    def requesmethod(data,url):
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=jsondata, headers=headers)
        return  r
    def convertingregex():
        matches = re.search(r'(.*)of(.*)', string)
        group1 = matches.group(1)
        lastwords = re.findall('^\w+(.*)', group1)
        firstword = lastwords[0] #first word of last words
        rspace = firstword.strip() #removing spaces
        group2 = matches.group(2)
        formateddata = []
        result = group2.split()
        for i in result:
            num = re.search('[0-9]*', i)
            matching = num.group()
            if i == matching:  #converting string to integer
                i = int(i)
                formateddata.append(i)
            else:
                formateddata.append(i)

        convertdict = {}  #converting to dictionary
        convertdict[rspace] = dict(zip(formateddata[::2], formateddata[1::2]))
        jsondata = json.dumps(convertdict)
        return jsondata
    if input[0] == actions[0]:
        jsondata = convertingregex()

        url=input1+'/add'
        calling = requesmethod(jsondata, url)
        data = calling.json()
        print data

    elif input[0] == actions[1]:
        secword = input[1]  #to get the second word of string
        string1 = actions[1]
        rspace = secword.strip()
        result=string.split()
        length= len(result)
        if (length <= 2):

            convertdict = {}  #converting dictionary
            convertdict['pname'] = rspace
            jsondata = json.dumps(convertdict)
            url = input1 + '/search'
            calling=requesmethod(jsondata,url)
            data = calling.json()
            for i in data:
                for key, values in i.items():
                    print key, values
                print "\n"

        else:
            jsondata=convertingregex()
            url=input1+'/search'
            calling = requesmethod(jsondata, url)
            data = calling.json()
            for i in data:
                    for k, v in i.items():
                        print k, v
                    print "\n"

    elif input[0] == actions[2]:
        jsondata=convertingregex()
        url = input1 + '/buy'
        calling = requesmethod(jsondata, url)
        data = calling.json()
        list1=[]  #to know the type of list
        if type(data)==type(list1):
            for i in data:
                for key, values in i.items():
                    print key, values
                print "\n"
        else:
            print data
    elif input[0] == actions[3]:
        string1 = actions[3]
        lwords = re.findall('^\w+(.*)', string)
        rspace = input[0].strip()
        convertdict = {}
        onlydata = lwords[0]
        list2 = onlydata.split()
        convertdict[rspace] = dict(zip(list2[::2], list2[1::2]))
        jsondata = json.dumps(convertdict)
        url = input1 + '/money'
        calling = requesmethod(jsondata, url)
        data = calling.json()
        data1 = data[1]
        list2 = []  #to know type of list
        if type(data) == type(list2):
            for i in data1:
                for key, values in i.items():
                    print key, values
                print "\n"
            print "total net", data[0]
        else:
            print data

