#reference https://codehandbook.org/python-flask-jquery-ajax-post/
#reference http://containertutorials.com/docker-compose/flask-simple-app.html for Docker

#libraries
from flask import Flask
from flask import render_template
from flask import request
from time import sleep
import subprocess

app = Flask(__name__)

#default page to go to
@app.route('/')
def index():
    return render_template('index.html')

#run the python code inside docker
@app.route('/output',methods=['POST','GET'])
def output():
    #write the input code to another file called 'code.py'
    code = request.form['code']
    f = open("code.py", "w")
    f.write(code)
    f.close()
    sleep(1)
    #output = subprocess.Popen(["python" ,"code.py"],bufsize=100)
    #subprocess.Popen(["sudo", "usermod", "-aG", "docker", "${USER}"],bufsize=100)
    #output = subprocess.Popen(["docker","cp", "code.py","mydocker:code.py"], bufsize=100)
    #output = subprocess.Popen(["docker","build", "-t","mydocker","."], stdout=subprocess.PIPE).communicate()[0]
    #output = subprocess.Popen(["docker","run", "mydocker"], stdout=subprocess.PIPE).communicate()[0]
    #execute the python program
    proc = subprocess.Popen("python code.py", shell=True, stdout=subprocess.PIPE)
    script_response = proc.stdout.read()
    script_response = (script_response.decode('utf-8'))
    #return json.dumps({'status':str(script_response)})
    #return the response back to the UI
    return str(script_response)

#main function
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')