#libraries
from flask import Flask
from flask import render_template
from flask import request
import random
import string
import json

app = Flask(__name__)

#global queue
queue = []
queue_testing = []

#hashmap to store which publisher publishes to which topic
'''pub_topic_map = {
    "pub1" : ["topic1"],
    "pub2" : ["topic2"]
}'''
pub_topic_map = {}
sub_topic_map = {}
topic_data_map = {}

#number of pub,sub and topics for random
pub_num = 0
sub_num = 0
topics_num = 0

#list of generated publishers,subscribers and topics based on user input
pubs_test = []
subs_test = []
topics_test = []

#map to store publisher,subscriber and topic connections for randomly generating and testing
pub_topic_map_test = dict()
sub_topic_map_test = dict()
topic_data_map_test = dict()

#default page to go to
@app.route('/')
def index():
    return render_template('P2.html')

#match publisher and topics
@app.route('/pubTopic',methods=['POST','GET'])
def matchPubTopic():
    topic = request.form['topic']
    pub = request.form['pub']
    if pub in pub_topic_map.keys():
        pub_topic_map[pub].append(topic)
    else:
        pub_topic_map[pub] = [topic]
    return "success!!!"

#match subscribers and topics
@app.route('/subTopic',methods=['POST','GET'])
def subscribe():
    topic = request.form['topic']
    sub = request.form['sub']
    if topic in sub_topic_map.keys():
        sub_topic_map[topic].append(sub)
    else:
        sub_topic_map[topic] = [sub]
    return "success!!!"

#function to publish data
@app.route('/publish',methods=['POST','GET'])
def publish():
    msg = request.form['msg']
    pub = request.form['pub']
    data = msg + "," + pub
    queue.append(data)
    return "success"

#function to notify
@app.route('/notify',methods=['POST','GET'])
def notify():
    data = ""
    print("matchSubTopic", sub_topic_map)
    print("matchPubTopic", pub_topic_map)
    for info in queue:
        print(info,len(info))
        msg,pub = info.split(",")
        print(msg,pub)
        for x in pub_topic_map[pub]:
            for y in sub_topic_map[x]:
                data += (str(y))
                data += " received the message:"
                data += msg
                data += "\n"
    print(data)
    del queue[:]
    return data

#function to match random publishers and topics and post messages randomly
def eventGenerator():

    #randomly generate a possile set of pub,sub and topic connections
    print(sub_topic_map_test)
    count = 0
    for i in range(pub_num):
        pub = pubs_test[count]
        count += 1
        lst = list(sub_topic_map_test.keys())
        print(lst)
        topic = random.choice(lst)
        if bool(pub_topic_map_test) and pub in pub_topic_map_test.keys():
            pub_topic_map_test[pub].append(topic)
        else:
            pub_topic_map_test[pub] = [topic]
    print(pub_topic_map_test)
    print(sub_topic_map_test)

    data = "Publisher Topic Matching is: " + json.dumps(pub_topic_map_test) +"\n" + "Subscriber Topic Matching is: " + json.dumps(sub_topic_map_test) + "\n"

    #randomly generate data for the publisher to publish
    for x in pub_topic_map_test.keys():
        digits = "".join([random.choice(string.digits) for i in range(8)])
        queue_testing.append(digits + "," + x)
        data += x + " is publishing the message : " + digits + "\n"

    #iterate through the messaes in the queue
    for info in queue_testing:
        print(info,len(info))
        msg,pub = info.split(",")
        print(msg,pub)
        for x in pub_topic_map_test[pub]:
            for y in sub_topic_map_test[x]:
                data += (str(y))
                data += " received the message:"
                data += msg
                data += " from the topic " + x
                data += "\n"
    print(data)
    del queue_testing[:]
    return data

#function to match random topics and subscribers
@app.route('/randomGenerator',methods=['POST','GET'])
def subscriberGenerator():

    global pub_topic_map_test
    pub_topic_map_test = {}
    global sub_topic_map_test
    sub_topic_map_test = {}
    global topic_data_map_test
    topic_data_map_test= {}

    global pub_num
    pub_num = 0
    global sub_num
    sub_num = 0
    global topics_num
    topics_num = 0

    global pubs_test
    pubs_test = []
    global subs_test
    subs_test = []
    global topics_test
    topics_test = []

    pub_num = int(request.form['pubsNum'])
    sub_num = int(request.form['subsNum'])
    topics_num = int(request.form['topicsNum'])

    for i in range(pub_num):
        pubs_test.append("pub" + str(i+1))

    for i in range(sub_num):
        subs_test.append("sub" + str(i+1))

    for i in range(topics_num):
        topics_test.append("topic" + str(i+1))

    for i in range((sub_num)):
        sub = random.choice(subs_test)
        topic = random.choice(topics_test)
        if bool(sub_topic_map_test) and topic in sub_topic_map_test.keys():
            sub_topic_map_test[topic].append(sub)
        else:
            sub_topic_map_test[topic] = [sub]
    return eventGenerator()

#main function
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=5001)
