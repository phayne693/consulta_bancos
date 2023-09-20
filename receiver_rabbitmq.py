import pika
import sys
import os
import threading
from robos_consulta_.c6_consulta import robo_c6_consulta
from robos_consulta_.facta_consulta import robo_facta_consulta
from robos_consulta_.ole_consulta import robo_ole_consulta
from robos_consulta_.master_consulta import robo_master_consulta
from robos_consulta_.pan_consulta import robo_pan_consulta
from robos_consulta_.mercantil_consulta import robo_mercantil_consulta

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='Fila TESTE')

    #receber mensagens
    def callback(ch, method, properties, body):
        #criar uma thread para processar cada mensagem
        threading_c6 = threading.Thread(target=c6, args=(body,))
        threading_ole = threading.Thread(target=ole, args=(body,))
        threading_facta = threading.Thread(target=facta, args=(body,))
        threading_mercantil = threading.Thread(target=mercantil, args=(body,))
        threading_master = threading.Thread(target=master, args=(body,))
        threading_pan = threading.Thread(target=pan, args=(body,))
        #inicia as threads
        threading_c6.start()
        threading_ole.start()
        threading_facta.start()
        threading_master.start()
        threading_mercantil.start()
        threading_pan.start()
        #aguarda as threads temrinarem
        threading_c6.join()
        threading_ole.join()
        threading_facta.join()
        threading_mercantil.join()
        threading_master.join()
        threading_pan.join()
        #confirmar a conclusão do processamento
        ch.basic_ack(delivery_tag=method.delivery_tag
                     )
    channel.basic_consume(queue='Fila TESTE', on_message_callback=callback, auto_ack=False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

#funcao para processar mensagem
def c6(body):
    mensagem = body.decode()
    resultado_c6 = robo_c6_consulta(mensagem)
    print(f"[x] Bank c6 Received Document:{mensagem}\n {resultado_c6}")

def ole(body):
    mensagem = body.decode()
    resultado_ole = robo_ole_consulta(mensagem)
    print(f"[x] Bank Ole Received Document:{mensagem}\n {resultado_ole}")

def facta(body):
    mensagem = body.decode()
    resultado_facta = robo_facta_consulta(mensagem)
    print(f"[x] Bank Facta Received Document:{mensagem}\n {resultado_facta}")

def master(body):
    mensagem = body.decode()
    resultado_master = robo_master_consulta(mensagem)
    print(f"[x] Bank Master Received Document:{mensagem}\n {resultado_master}")

def mercantil(body):
    mensagem = body.decode()
    resultado_mercantil = robo_mercantil_consulta(mensagem)
    print(f"[x] Bank Mercantil Received Document:{mensagem}\n {resultado_mercantil}")

def pan(body):
    mensagem = body.decode()
    resultado_pan = robo_pan_consulta(mensagem)
    print(f"[x] Bank Pan Received Document:{mensagem}\n {resultado_pan}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)