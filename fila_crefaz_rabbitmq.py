import pika

def enviar_cliente_fila(cpf, nome, nascimento, telefone, cep):
    # Configura conexão
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Cria uma fila
    channel.queue_declare(queue='Fila_CREFAZ')

    # Monta os atributos em uma única mensagem (pode usar um formato de sua escolha, como JSON)
    mensagem = f"CPF: {cpf}, Nome: {nome}, Nascimento: {nascimento}, Telefone: {telefone}, CEP: {cep}"

    # Publica a mensagem na fila
    channel.basic_publish(exchange='', routing_key='Fila_CREFAZ', body=mensagem)

    print('Mensagem publicada:', mensagem)

    # Fecha a conexão
    connection.close()