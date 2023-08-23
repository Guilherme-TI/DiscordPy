from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import discord
from discord.ext import commands
from io import BytesIO

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
#Adicione o token do seu bot
token = ''
#Digite o caminho do seu banco de dados
df = pd.read_csv('Salario.csv')

# Evento para verificar quando o bot está pronto
@bot.event
async def on_ready():
    print(f'Bot está online como {bot.user}')

#Responde com pong quando digitam !ping
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

#Ataca um membro mencionado
@bot.command()
async def attack(ctx, membro: discord.Member):
    # Verificar se um membro foi mencionado
    if membro:
        # Criar uma mensagem embed
        embed = discord.Embed(
            title="Ataque!",
            description=f"{ctx.author.mention} atacou {membro.mention}!",
            color=discord.Color.red()
        )
        embed.set_image(url="https://media.tenor.com/0NnHtx0y0TYAAAAC/tapa-dessa.gif")

        # Obter a data e hora atuais
        current_time = datetime.now()

        # Formatando a data e hora para um formato legível
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        # Adicionar um footer com a data e hora formatada
        embed.set_footer(text=f"Enviado em {formatted_time}")

        # Enviar a embed no canal atual
        await ctx.send(embed=embed)
    else:
        await ctx.send("Você precisa mencionar um membro para atacar.")

# Comando para exibir um gráfico de barras do faturamento por gênero em uma embed
@bot.command()
async def data_gender(ctx):
    try:
        # Calcule o faturamento por gênero
        faturamento_total = df['Salary'].sum()
        faturamento_por_genero = df.groupby('Gender')['Salary'].sum().reset_index()

        # Crie um gráfico de barras
        plt.figure(figsize=(8, 6))
        plt.bar(faturamento_por_genero['Gender'], faturamento_por_genero['Salary'])
        plt.title('Faturamento por Gênero')

        # Salve o gráfico como uma imagem
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Crie uma mensagem embed
        embed = discord.Embed(
            title='Faturamento por Gênero',
            description='Aqui está o faturamento por gênero com base no banco de dados da Kaggle.com:',
            color=discord.Color.blue()
        )

        # Adicione o gráfico à embed como um anexo
        embed.set_image(url='attachment://grafico.png')

        # Calcule e adicione a soma dos valores como um campo na embed
        embed.add_field(name="Faturamento Total", value=f"```\n{faturamento_total}\n```", inline=False)
        embed.add_field(name="Faturamento Por Gênero", value=f"```\n{faturamento_por_genero}\n```", inline=False)

        #Adicione o link do banco de dados como rodapé
        embed.set_footer(text=f"Base de dados: https://www.kaggle.com/datasets/sudheerp2147234/salary-dataset-based-on-country-and-race")

        # Enviar a embed no canal atual com o gráfico como anexo
        await ctx.send(embed=embed, file=discord.File(buffer, 'grafico.png'))
    except Exception as e:
        await ctx.send(f"Ocorreu um erro: {str(e)}")

# Comando para exibir informações da raça com um gráfico em uma embed
@bot.command()
async def data_race(ctx):
    try:
        # Agrupe os dados por raça e calcule as estatísticas desejadas (por exemplo, contagem)
        race_stats = df.groupby('Race').size().reset_index(name='Count')

        # Crie um gráfico de barras com base nas estatísticas de raça
        plt.figure(figsize=(8, 6))
        plt.bar(race_stats['Race'], race_stats['Count'])
        plt.title('Contagem por Raça')

        # Salve o gráfico como uma imagem
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Crie uma mensagem embed
        embed = discord.Embed(
            title='Informações de Raça',
            description='Aqui estão as informações de raça com base no banco de dados da Kaggle.com',
            color=discord.Color.blue()
        )

        # Adicione o gráfico à embed como um anexo
        embed.set_image(url='attachment://grafico.png')

        #Adicione o link do banco de dados como rodapé
        embed.set_footer(text=f"Base de dados: https://www.kaggle.com/datasets/sudheerp2147234/salary-dataset-based-on-country-and-race")

        # Enviar a embed no canal atual com o gráfico como anexo
        await ctx.send(embed=embed, file=discord.File(buffer, 'grafico.png'))
    except Exception as e:
        await ctx.send(f"Ocorreu um erro: {str(e)}")

# Comando para exibir os 5 cargos com os maiores salários em uma mensagem embed com um gráfico de barras
@bot.command()
async def data_job(ctx):
    try:
        # Selecione os 5 cargos com os maiores salários
        top_cargos = df.head(5)

        # Crie um gráfico de barras dos 5 cargos com maiores salários
        plt.figure(figsize=(10, 6))
        plt.bar(top_cargos['Job Title'], top_cargos['Salary'])
        plt.title('Top 5 Cargos com os Maiores Salários')

        # Salve o gráfico como uma imagem
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Crie uma mensagem embed
        embed = discord.Embed(
            title='Top 5 Cargos com os Maiores Salários',
            description='Aqui estão os 5 cargos com os maiores salários com base no banco de dados da Kaggle.com:',
            color=discord.Color.blue()
        )

        # Adicione o gráfico à embed como um anexo
        embed.set_image(url='attachment://grafico.png')

        # Converta os dados dos cargos em uma tabela de texto formatada
        cargo_table = top_cargos[['Job Title', 'Salary']].to_string(index=False)

        # Adicione os cargos como um campo na embed
        embed.add_field(name='Cargos', value=f"```\n{cargo_table}\n```", inline=False)

        #Adicione o link do banco de dados como rodapé
        embed.set_footer(text=f"Base de dados: https://www.kaggle.com/datasets/sudheerp2147234/salary-dataset-based-on-country-and-race")

        # Enviar a embed no canal atual com o gráfico como anexo
        await ctx.send(embed=embed, file=discord.File(buffer, 'grafico.png'))
    except Exception as e:
        await ctx.send(f"Ocorreu um erro: {str(e)}")

bot.run(token)