from flask import Flask, request, jsonify
from pymongo import MongoClient
import time

app = Flask(__name__)
connection = MongoClient()
db = connection.inventory #database name.
collection = db['products'] # collection name.
collection1 = db['income']    # collection name

@app.route('/add',methods=['POST'])
def add():
      data=request.get_json()
      to_convert_given_data_to_key_valuepairs={}
      new_dictionary_from_data_to_store_dictionary={}
      for key, values in data.items():
          to_convert_given_data_to_key_valuepairs['pname'] = key
          for k, v in values.items():
              to_convert_given_data_to_key_valuepairs[k] = v

      for i,j in to_convert_given_data_to_key_valuepairs.items():
          if i=='qty':
              continue
          else:
              new_dictionary_from_data_to_store_dictionary[i]=j
      print new_dictionary_from_data_to_store_dictionary
      get_matched_records=list(collection.find(new_dictionary_from_data_to_store_dictionary))
      print get_matched_records
      if  get_matched_records:
        print "up "
        collection.update(new_dictionary_from_data_to_store_dictionary,{"$inc":{"qty":to_convert_given_data_to_key_valuepairs['qty']}})
        result = "it is updated"
        return jsonify(result)
      else:
        collection.insert(to_convert_given_data_to_key_valuepairs)
        result = "successfully inserted"
        return jsonify(result)

@app.route('/search',methods=['POST'])
def search():
     searchdata = request.get_json()
     print searchdata
     to_check_dictionary={}
     for j, k in searchdata.items():
         if(type(k) == type(to_check_dictionary)):
           to_store_in_key_value_pairs = {}
           for key,values in searchdata.items():
               to_store_in_key_value_pairs['pname'] = key
               for k, v in values.items():
                  to_store_in_key_value_pairs[k] = v
           result=list(collection.find(to_store_in_key_value_pairs,{"_id":0}))

         else:
           result = list(collection.find(searchdata, {"_id": 0}))
     return jsonify(result)
@app.route('/buy',methods=['POST'])
def buy():
    buydata = request.get_json()
    todaydate = time.strftime('%Y-%m-%d')
    print buydata
    dictionary_Without_quantity= {}
    dictionary_with_quantity={}
    for key, values in buydata.items():
        dictionary_Without_quantity['pname'] = key
        dictionary_with_quantity['pname']=key
        for k, v in values.items():
            if k=='qty':
             dictionary_Without_quantity[k] ={"$gte":v}
             dictionary_with_quantity[k]=v
            else:
             dictionary_Without_quantity[k]=v
             dictionary_with_quantity[k]=v
        print dictionary_Without_quantity

    s1 = list(collection.find(dictionary_Without_quantity))
    #print s1
    if s1:
        collection.update({'pname': dictionary_Without_quantity['pname']}, {'$inc': {'qty':-dictionary_with_quantity['qty']}})
        collection1.insert({'pname':dictionary_with_quantity['pname'], "qty": dictionary_with_quantity['qty'], "price": dictionary_with_quantity['price'] * dictionary_with_quantity['qty'],"date": todaydate})
        result="successfully"
        return jsonify(result)
    else:
        result = list(collection.find({"pname": dictionary_Without_quantity['pname']},{"_id": 0}))
        return jsonify(result)

@app.route('/money',methods=['POST'])
def money():
      moenydata=request.get_json()
      todaydate = time.strftime('%Y-%m-%d')

      get_date_dictionary=moenydata.values()[0]
      to_insert_date_into_dictionary={}
      if get_date_dictionary:
          to_check_date=get_date_dictionary
      else:
         to_insert_date_into_dictionary['date']=todaydate
         to_check_date=to_insert_date_into_dictionary

      get_matched_records_with_givenname=list(collection1.find(to_check_date,{"_id":0}))
      if get_matched_records_with_givenname:
          prices_sum = 0
          for i in range(0,len(get_matched_records_with_givenname)):
                prices_sum += get_matched_records_with_givenname[i]['price']
          return jsonify(prices_sum,get_matched_records_with_givenname)

      else:
          result="no transactions today"
          return jsonify(result)

if __name__ == '__main__':
   app.run(debug = True, host='0.0.0.0')

