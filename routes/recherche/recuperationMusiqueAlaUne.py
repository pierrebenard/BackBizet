from flask import Blueprint, jsonify, request, current_app, Flask
import json

from bson import ObjectId
from dns.rdatatype import NULL
from pymongo import MongoClient
from pymongo.errors import PyMongoError

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/Bizeterie?retryWrites=true&w=majority')
app = Flask(__name__)

recuperationMusiqueRecherche = Blueprint('recuperationMusiqueRecherche', __name__)

def json_serial(obj):
    try:
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        raise TypeError("Type not serializable")
    except Exception as e:
        print("Error occurred during serialization:")
        print("Object:", obj)
        print("Error:", str(e))
        raise TypeError(f"Type not serializable: {obj}, Error: {str(e)}")

@recuperationMusiqueRecherche.route('/recuperationMusiqueRecherche', methods=['GET'])
def recuperationMusiqueAlaUne_def():

    db = client['Bizeterie']
    collection = db['musiqueRecherche']

    recherche = request.args.get('recherche', None)
    emotion = request.args.get('emotion', None)

    print(recherche)

    try:
        if recherche is not None and recherche != "":
            print('recherche')
            query = {'$and': []}

            regex_pattern = f".*{recherche}.*"
            query['$and'].append({'$or': [{'titre': {'$regex': regex_pattern}}]})

            data = list(collection.find(query))
        else:
            data = list(collection.find())

        if emotion is not None and emotion != "Aucune":
            print('emotion')
            query = {'$and': []}

            query['$and'].append({'tag': {'$in': [emotion]}})
            data = list(collection.find(query))

        if emotion == "Aucune":
            print("ererer")
            data = list(collection.find())

        # ==================== RECUPERATION TRADES TERMINEE ==================== # maxProfit
        
        data = json.loads(json.dumps(data, default=json_serial))
        return jsonify({'data': data})

    except Exception as e:
        current_app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Erreur lors du renvoie des données", "details": str(e)}), 500