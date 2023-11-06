from flask import Flask
from flask_restful import Api
from resources.consulta import c6_consulta, master_consulta, mercantil_consulta, facta_consulta, enviar_documento, enviar_cliente_crefaz, crefaz



app = Flask(__name__)
api = Api(app)


api.add_resource(c6_consulta, '/c6-consulta')
api.add_resource(facta_consulta, '/facta-consulta')
api.add_resource(master_consulta, '/master-consulta')
api.add_resource(mercantil_consulta, '/mercantil-consulta')
api.add_resource(enviar_documento, '/enviar_documento')
api.add_resource(enviar_cliente_crefaz, '/biro-webhook')
api.add_resource(crefaz, '/crefaz')

if __name__ == '__main__':
    app.run(debug=True, port=5500)