from flask import Flask, render_template, request, make_response
import pandas as pd
import json

app = Flask(__name__)


df = pd.read_csv("hack.csv")

@app.route("/",methods=['POST'])
def index():
    json_body = request.get_json()
    print(json_body)
    parameters = json_body['queryResult']['parameters']
    intent = json_body['queryResult']['intent']
    project_name = intent['name']

    global df
    dfi =df
    if 'geo-country' in parameters:
        geo = parameters.get('geo-country')
        print(parameters)
        parameters.pop('geo-country')

    if 'State' in parameters and parameters['State'] != '':
        State = parameters.get('State')
        print(State)
        dfi = dfi.loc[(dfi['State'] == State)]
        print(dfi.shape)

    if 'District' in parameters and parameters['District'] != '':
        District = parameters.get('District')
        print(District)
        dfi = dfi.loc[(dfi['District'] == District)]

    if 'Tier' not in parameters or parameters['Tier'] == '':
        parameters['Tier'] = 'Total'

    if 'Tier' in parameters:
        Tier = parameters.get('Tier')
        print(Tier)
        dfi = dfi.loc[(dfi['Tier'] == Tier)]
        print(dfi.shape)

    [parameters.pop(i,None) for i in ['State', 'District', 'Tier']]


    with open('mapping.json') as mapping:
        mappings = json.load(mapping)

    column_name = ""
    for i in mappings:
        if para_map(i, parameters):
            column_name = i['output']
            type_value = i['type']

    print(column_name)

    if column_name != "":
        result = 0
        number = 0
        # print (dfi[column_name].size)
        for i in dfi[column_name]:
            if type_value == 'int':
                # if all(map(lambda x: x != i, ['Not applicable', 'Not available',None, ""])):
                if type(i) == int or str(i).isdigit():
                    result+=int(i)

            if type_value == 'percent':
                if type(i) == int or str(i).isdigit():
                    number+=1
                    result+=float(i)

        if type_value == 'percent' and number !=0:
            result = result/number

        print(result)
        print(number)

        # response for the api ai

        where = " in india "
        if locals().get("District") or locals().get("State"):
            where = " in"
            if locals().get('District'):
                where += " {} , ".format(District)
            if locals().get('State'):
                where += " %s " % State
        message = column_name + where + "is {}".format(result)
    else:
        message = "Sorry, I couldn't understand."



    message = message.lower().capitalize()

    res = make_result(message, project_name)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r





def para_map(obj, parameters):
    parameters.pop('OutputType',None)
    parameters.pop('sys.date-period',None)
    parameters.pop('sys.duration',None)
    a = obj['parameters'] == parameters

    for item in parameters.keys():
        if item in obj['tmp'].keys() and parameters[item] == obj['tmp'][item]:
            parameters.pop(item,None)

    return obj['parameters'] == parameters
    obj['action'] == 'numberOf'





def make_result(message ,project_name ,options = {}):
    return {
    "fulfillmentText": message,
    "source": "example.com",
    "payload": {
        "google": {
        "expectUserResponse": "true",
        "richResponse": {
            "items": [
            {
                "simpleResponse": {
                "textToSpeech": message
                }
            }
            ]
        }
        }
    }
    }

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1234)
