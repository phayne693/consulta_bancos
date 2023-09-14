from flask import Flask
from flask_restful import Api
from resources.consulta import c6_consulta, pan_consulta, master_consulta, mercantil_consulta, ole_consulta, facta_consulta



app = Flask(__name__)
api = Api(app)


api.add_resource(c6_consulta, '/c6-consulta')
api.add_resource(facta_consulta, '/facta-consulta')
api.add_resource(master_consulta, '/master-consulta')
api.add_resource(mercantil_consulta, '/mercantil-consulta')
api.add_resource(ole_consulta, '/ole-consulta')
api.add_resource(pan_consulta, '/pan-consulta')

if __name__ == '__main__':
    app.run(debug=True)