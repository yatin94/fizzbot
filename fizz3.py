# Interactive python client for fizzbot
import json
import urllib.request
import urllib.error
domain = 'https://api.noopschallenge.com'


def meetnoops(number,result):
    for i in number:
        if(int(i) % 7 == 0 and int(i)%5==0 and int(i) % 3 == 0):
            result = result+"MeetTheNoops "
        elif(int(i) % 3 == 0 and int(i)%5==0):
            result = result+"MeetThe "
        elif(int(i) % 5 == 0 and int(i)%7==0):
            result = result+"TheNoops "
        elif(int(i) % 3 == 0 and int(i)%7==0):
            result = result+"MeetNoops "
        elif((int(i)%5==0)):
            result = result+"The "
        elif (int(i) % 3 == 0):
            result = result + "Meet "
        elif(int(i) % 7 == 0):
            result = result+"Noops "
        else:
            result = result+str(i)+" "
    result = result[:-1]
    return(result)

def fizzbuzz(number,result):
    for i in number:
        if(int(i) % 3 == 0 and int(i)%5==0):
            result = result+"FizzBuzz "
        elif((int(i)%5==0)):
            result = result+"Buzz "
        elif (int(i) % 3 == 0):
            result = result + "Fizz "
        else:
            result = result+str(i)+" "
    result = result[:-1]
    return(result)

def BeepBoop(number,result):
    for i in number:
        if(int(i) % 2 == 0 and int(i)%5==0):
            result = result+"BeepBoop "
        elif((int(i)%5==0)):
            result = result+"Boop "
        elif (int(i) % 2 == 0):
            result = result + "Beep "
        else:
            result = result+str(i)+" "
    result = result[:-1]
    return(result)

def print_sep(): print('----------------------------------------------------------------------')
# print server response

def print_response(dict):
    print('')
    print('message:')
    print(dict.get('message'))
    print('')
    for key in dict:
        if key != 'message':
            print('%s: %s' % (key, json.dumps(dict.get(key))))
    print('')

# try an answer and see what fizzbot thinks of it

def try_answer(question_url, answer):
    print_sep()
    body = json.dumps({ 'answer': answer })
    print('*** POST %s %s' % (question_url, body))
    try:
        req = urllib.request.Request(domain + question_url, data=body.encode('utf8'), headers={'Content-Type': 'application/json'})
        res = urllib.request.urlopen(req)
        response = json.load(res)
        print_response(response)
        return response

    except urllib.error.HTTPError as e:
        response = json.load(e)
        print_response(response)
        return response

# keep trying answers until a correct one is given

def get_correct_answer(question_url,numbr,choice):
    while True:
        result = ""
        if(numbr is None):
            answer = "python"
        else:
            if(choice == "Fizz" or choice == "Buzz"):
                answer = fizzbuzz(numbr,result)
            elif(choice == "Beep" or choice == "Boop"):
                answer =  BeepBoop(numbr,result)
            elif(choice == "Meet" or choice == "The" or choice =="Noops"):
                answer =  meetnoops(numbr,result)
        response = try_answer(question_url, answer)
        if (response.get('result') == 'interview complete'):
            print('congratulations!')
            exit()
        if (response.get('result') == 'correct'):
            # input('press enter to continue')
            return response.get('nextQuestion')

# do the next question

def do_question(domain, question_url):
    print_sep()
    print('*** GET %s' % question_url)
    request = urllib.request.urlopen( ('%s%s' % (domain, question_url)) )
    question_data = json.load(request)
    rle = question_data.get('rules')
    try:
        choice = rle[0].get('response')
    except:
        choice = "None"
    print_response(question_data)
    print_sep()
    numbr = question_data.get('numbers')
    # print(numbr)
    next_question = question_data.get('nextQuestion')
    if next_question: return next_question
    return get_correct_answer(question_url,numbr,choice)

def main():
    question_url = '/fizzbot'
    while question_url:
        question_url = do_question(domain, question_url)


if __name__ == '__main__': 
    main()
