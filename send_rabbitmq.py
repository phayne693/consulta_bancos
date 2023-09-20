import pika

def enviar_requisicao_fila(cpf):
    #configura conexao
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    #cria uma fila
    channel.queue_declare(queue='Fila TESTE')

    #publica mensagem na fila
    channel.basic_publish(exchange='', routing_key='Fila TESTE', body=cpf)

    print('Mensagem publicada')

    #fecha a conexão
    connection.close()