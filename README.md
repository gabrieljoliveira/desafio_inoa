# desafio_inoa

Instruções para rodar o desafio e analisar os dados obtidos

1. Ter o docker-compose setado no ambiente.
2. Clonar o repositório.
3. Rodar o comando sudo docker-compose up --build para criar os containers e rodar os comandos
   iniciais (migrate, initsuperuser e runserver).
4. Abrir http://localhost:8000/admin e entrar com o email user@email.com e senha 123.
5. Entrar na aba Assets e criar um ativo (o campo name é a tag do ativo no yahoo finance), definir
   os valores mínimos e máximos do túnel, a periodicidade em que deseja que os dados sejam extraídos e se
   deseja que o ativo seja monitorado (enviar email alertando toda vez que seu valor estiver fora das margens)
6. Após esperar o tempo determinado, pode ver os dados na aba Asset datas sendo preenchidos com o ativo, seu valor e data de extração
7. Para checar o envio de email, basta abrir http://127.0.0.1:8025/, lá se encontram todos os emails enviados.

OBS: Ao alterar o nome do ativo, todos os dados coletados referente à esse ativo são deletados
OBS2: Ao deletar o ativo, a task referente à ele também é deletada
