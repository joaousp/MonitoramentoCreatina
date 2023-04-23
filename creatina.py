import requests
from bs4 import BeautifulSoup
import re
import smtplib
from email.mime.text import MIMEText


url = 'https://www.soldiersnutrition.com.br/produto/creatina-monohidratada-1kg-100-pura-importada-soldiers-nutrition.html'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
script_tag = soup.find('script', string=re.compile('item_name:'))
price_match = re.search(r'price: (\d+\.\d+)', script_tag.string)
if price_match:
    price = price_match.group(1)
    print(price)


import psycopg2
from datetime import datetime

# Dados da conexão
host = "localhost"
port = 5432
database = "postgres"
user = "postgres"
password = "1234"

# Cria a conexão
conn = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)

# Cria o cursor
cur = conn.cursor()

# Insere um registro na tabela creatina
preco_atual = 244.90
preco_anterior = 240.50
diferenca = preco_atual - preco_anterior
data = datetime.now().strftime('%Y-%m-%d')
#INSERT INTO projeto1.creatina (entrada, preco_atual, preco_antigo, diferenca) VALUES(CURRENT_DATE, 0, 249.0, 0);

query_p_anterior=f"SELECT preco_atual FROM creatina c  ORDER BY c.id DESC LIMIT 1"
cur.execute(query_p_anterior)
preco = cur.fetchone()[0]
print(preco_anterior)

insert_query = f"INSERT INTO projeto1.creatina (entrada, preco_atual, preco_antigo, diferenca) VALUES ('{data}', {preco_atual}, {preco_anterior}, {diferenca})"
cur.execute(insert_query)

# Commita as alterações
conn.commit()

# Fecha a conexão
cur.close()
conn.close()


# Check the price
price = preco_atual
threshold = preco_anterior
if price < threshold:
    # Set up the email message
    msg = MIMEText(f'The price is {price:.2f}, below the threshold of {threshold:.2f}.')
    msg['Subject'] = 'Price Alert'
    msg['From'] = 'sender@example.com'
    msg['To'] = 'recipient@example.com'

    # Connect to the SMTP server and send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('sender@example.com', 'password')
    server.sendmail('sender@example.com', 'recipient@example.com', msg.as_string())
    server.quit()

