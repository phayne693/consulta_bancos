from flask_restful import Resource
from flask import request
from robos_consulta_.c6_consulta import robo_c6_consulta
from robos_consulta_.facta_consulta import robo_facta_consulta
from robos_consulta_.ole_consulta import robo_ole_consulta
from robos_consulta_.master_consulta import robo_master_consulta
from robos_consulta_.pan_consulta import robo_pan_consulta
from robos_consulta_.mercantil_consulta import robo_mercantil_consulta
from send_rabbitmq import enviar_requisicao_fila

class c6_consulta(Resource):
    def post(self):
        #obtem as variaveis do payload
        cpf = request.json.get('cpf')
        #valida o tamanho das variaveis
        if len(cpf) > 11:
            return {'success': False, 'message': 'CPF deve conter no maximo 11 números', 'cpf': cpf}, 400
        elif not cpf.isnumeric():
            return {'success': False, 'message': 'CPF deve conter apenas numeros', 'cpf': cpf}, 400
        elif len(cpf) < 11:
            return {'success': False, 'message': 'CPF deve conter 11 números', 'cpf': cpf}, 400
        #obtem o retorno do robo
        # resultado = robo_c6_consulta(cpf)
        # if resultado is None:
        #     return {'success': False, 'message': resultado}, 400
        # else:
        #     return {'success': True, 'message': resultado}, 200
        return {'success': True, 'message':'CPF enviado para fila.'}
    
class ole_consulta(Resource):
    def post(self):
        #obtem as variaveis do payload
        cpf = request.json.get('cpf')
        #valida o tamanho das variaveis
        if len(cpf) > 11:
            return {'success': False, 'message': 'CPF deve conter no maximo 11 números'}, 400
        elif not cpf.isnumeric():
            return {'success': False, 'message': 'CPF deve conter apenas numeros'}, 400
        #obtem o retorno do robo
        resultado = robo_ole_consulta(cpf)
        if resultado is None:
            return {'success': False, 'message': resultado}, 400
        else:
            return {'success': True, 'message': resultado}, 200

class facta_consulta(Resource):
    def post(self):
        #obtem as variaveis do payload
        cpf = request.json.get('cpf')
        #valida o tamanho das variaveis
        if len(cpf) > 11:
            return {'success': False, 'message': 'CPF deve conter no maximo 11 números'}, 400
        elif not cpf.isnumeric():
            return {'success': False, 'message': 'CPF deve conter apenas numeros'}, 400
        #obtem o retorno do robo
        resultado = robo_facta_consulta(cpf)
        if resultado is None:
            return {'success': False, 'message': resultado}, 400
        else:
            return {'success': True, 'message': resultado}, 200
        
class master_consulta(Resource):
    def post(self):
        #obtem as variaveis do payload
        cpf = request.json.get('cpf')
        #valida o tamanho das variaveis
        if len(cpf) > 11:
            return {'success': False, 'message': 'CPF deve conter no maximo 11 números'}, 400
        elif not cpf.isnumeric():
            return {'success': False, 'message': 'CPF deve conter apenas numeros'}, 400
        #obtem o retorno do robo
        resultado = robo_master_consulta(cpf)
        if resultado is None:
            return {'success': False, 'message': resultado}, 400
        else:
            return {'success': True, 'message': resultado}, 200
        
class mercantil_consulta(Resource):
    def post(self):
        #obtem as variaveis do payload
        cpf = request.json.get('cpf')
        #valida o tamanho das variaveis
        if len(cpf) > 11:
            return {'success': False, 'message': 'CPF deve conter no maximo 11 números'}, 400
        elif not cpf.isnumeric():
            return {'success': False, 'message': 'CPF deve conter apenas numeros'}, 400
        #obtem o retorno do robo
        resultado = robo_mercantil_consulta(cpf)
        if resultado is None:
            return {'success': False, 'message': resultado}, 400
        else:
            return {'success': True, 'message': resultado}, 200

class pan_consulta(Resource):
    def post(self):
        #obtem as variaveis do payload
        cpf = request.json.get('cpf')
        #valida o tamanho das variaveis
        if len(cpf) > 11:
            return {'success': False, 'message': 'CPF deve conter no maximo 11 números'}, 400
        elif not cpf.isnumeric():
            return {'success': False, 'message': 'CPF deve conter apenas numeros'}, 400
        #obtem o retorno do robo
        resultado = robo_pan_consulta(cpf)
        if resultado is None:
            return {'success': False, 'message': resultado}, 400
        else:
            return {'success': True, 'message': resultado}, 200

class enviar_documento(Resource):
    def post(self):
        #obtem as variaveis do payload
        cpf = request.json.get('cpf')
        #valida o tamanho das variaveis
        if len(cpf) > 11:
            return {'success': False, 'message': 'CPF deve conter no maximo 11 números', 'cpf': cpf}, 400
        elif not cpf.isnumeric():
            return {'success': False, 'message': 'CPF deve conter apenas numeros', 'cpf': cpf}, 400
        elif len(cpf) < 11:
            return {'success': False, 'message': 'CPF deve conter 11 números', 'cpf': cpf}, 400
        #obtem o retorno do robo
        # resultado = robo_c6_consulta(cpf)
        # if resultado is None:
        #     return {'success': False, 'message': resultado}, 400
        # else:
        #     return {'success': True, 'message': resultado}, 200
                #envia o cpf para fila
        enviar_requisicao_fila(cpf)
        return {'success': True, 'message':'CPF enviado para fila.'}