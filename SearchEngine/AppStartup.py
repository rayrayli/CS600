#!/usr/local/bin/python3
from flask import Flask, jsonify, request, Response
from SearchEngine import SearchEngine
from flask import render_template
import re

app = Flask(__name__)

@app.route('/getRecommendKey', methods=['GET'])
def getRecommendKey():
    keylist = se.getRecomendKey(request.args.get('key'))
    html = render_template("recommend.html", keylist=keylist)
    return jsonify({'result': html})

@app.route('/', methods=['GET'])
def search():
#    print (request.args.get('key'))
    if request.args.get('key')==None:
        html = render_template("search.html", ol=False, key=False)
    else:
        rank = None
        regex = re.compile('\s+')
        keywords = request.args.get('key')
        keylist = []
        odict = {}
        for key in regex.split(keywords):
            result = se.search(key)
            #print(result)
            if result:
                result.pop('key', None)
                keylist.append(result.keys())
                for r in result:
                    if r in odict:
                        odict[r] = odict[r] + result[r]
                    else:
                        odict[r] = result[r]
            else:
                keylist.append(result.keys())

        intersetion = None
        for kl in keylist:
            if intersetion == None:
                intersetion = set(kl)
            else:
                intersetion = set(intersetion) & set(kl)

        output = {}

        for sub_intersetion in intersetion:
            sub = sub_intersetion
            output[sub] = odict[sub]
        print(odict)
        if output:
            rank = sort_by_value(output)
            html = render_template("search.html", ol=output, rank=rank, key=keywords)
        else:
            html = render_template("search.html", ol=None, key=False)
    return html

def sort_by_value(d):
    items=d.items()
    backitems=[[v[1],v[0]] for v in items]
    backitems.sort(reverse=True)
    return [ backitems[i][1] for i in range(0,len(backitems))]


if __name__ == '__main__':
    se = SearchEngine()
    se.buildTries()
    app.run(debug=True, port=8886)

