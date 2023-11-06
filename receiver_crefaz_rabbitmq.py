import pika
import sys
import os
import threading
from robos_consulta_.crefaz import crefaz_consulta

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='Fila_CREFAZ')

    #receber mensagens
    def callback(ch, method, properties, body):
        #criar uma thread para processar cada mensagem
        threading_crefaz = threading.Thread(target=crefaz, args=(body,))
        #inicia as threads
        threading_crefaz.start()
        #aguarda as threads temrinarem
        threading_crefaz.join()
        #confirmar a conclusão do processamento
        ch.basic_ack(delivery_tag=method.delivery_tag)
    channel.basic_consume(queue='Fila_CREFAZ', on_message_callback=callback, auto_ack=False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

#funcao para processar mensagem
def crefaz(body):
    mensagem = body.decode()
    print(mensagem)
    #separar a mensagem e obeter os dados
    cpf, nome, nascimento, telefone, cep = mensagem.split(',')
    resultado_crefaz = crefaz_consulta(cpf, nome, nascimento, telefone, cep)
    print(f"[x] Bank crefaz Received Client:{mensagem}\n {resultado_crefaz}")




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)