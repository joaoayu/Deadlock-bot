import discord
from discord import app_commands
from discord.ui import Button, View

id_do_servidor = ID_DO_SEU_SERVIDOR

class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await self.tree.sync(guild=discord.Object(id=id_do_servidor))
            self.synced = True
            print(f"Entramos como {self.user}")

aclient = Client()

@aclient.tree.command(guild=discord.Object(id=id_do_servidor), name='painel', description='Painel de Tickets.')
async def painel(interaction: discord.Interaction):
    # Criação do embed do painel
    embed = discord.Embed(
        title="🎟️ Painel de Tickets 🎟️",
        description="Use o botão abaixo para abrir um ticket. Nossa equipe está pronta para ajudar você!",
        color=discord.Color.blue()
    )
    embed.add_field(name="🔍 Como Funciona", value="1. Clique no botão para abrir um ticket.\n2. Um canal será criado para sua conversa privada com a equipe.\n3. Para fechar o ticket, use o botão de fechar no canal.", inline=False)
    embed.add_field(name="🔔 Notas Importantes", value="🔹 Somente você e a equipe terão acesso ao ticket.\n🔹 Para questões gerais, utilize os canais apropriados.\n🔹 Se não precisar mais do ticket, feche-o para manter a organização.", inline=False)

    view = View()

    # Botão para abrir ticket
    open_ticket_button = Button(label="📩 Abrir Ticket", style=discord.ButtonStyle.green)

    async def open_ticket_callback(interaction):
        guild = interaction.guild
        ticket_channel_name = f"ticket-{interaction.user.name}"

        existing_channel = discord.utils.get(guild.text_channels, name=ticket_channel_name)

        if existing_channel:
            await interaction.response.send_message("Você já tem um ticket aberto!", ephemeral=True)
            return

        ticket_channel = await guild.create_text_channel(ticket_channel_name)

        await ticket_channel.set_permissions(guild.default_role, read_messages=False)
        await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await ticket_channel.set_permissions(guild.me, read_messages=True, send_messages=True)

        await ticket_channel.send(f"🎟️ {interaction.user.mention}, seu ticket foi aberto! Como podemos ajudar você?")
        await interaction.response.send_message(f"Seu ticket foi criado: {ticket_channel.mention}", ephemeral=True)

    open_ticket_button.callback = open_ticket_callback
    view.add_item(open_ticket_button)

    # Envia o embed do painel
    await interaction.response.send_message(embed=embed, view=view)

@aclient.tree.command(guild=discord.Object(id=id_do_servidor), name='regras', description='Exibe as regras do servidor.')
async def regras(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator:
        embed = discord.Embed(
            title="📝 Regras do Servidor 📝",
            description="**Por favor, siga as regras abaixo:**\n",
            color=discord.Color.green()
        )

        regras_text = "\n".join([
            "**1.** Respeite os Termos de Serviço do Discord e Deadlock.",
            "**2.** Respeite a equipe e os membros do servidor. Racismo, sexismo, homofobia, transfobia e qualquer outra forma de toxicidade não serão tolerados.",
            "**3.** NSFW (sexo, violência, etc...) não é permitido.",
            "**4.** Não divulgue informações de outras pessoas.",
            "**5.** Sem política ou religião.",
            "**6.** Não se faça passar por membros do servidor, membros da equipe, funcionários da Valve ou qualquer outra pessoa.",
            "**7.** Golpes não são permitidos.",
            "**8.** Não envie spam.",
            "**9.** Discussões sobre pirataria não são permitidas.",
            "**10.** Não discuta sobre quebrar as regras nem ajude outros usuários a quebrá-las.",
            "**11.** Use os canais adequados.",
            "**12.** Se alguém estiver infringindo as regras, entre em contato com a equipe fazendo ping na função @Moderação. Não faça ping nessa função para questões técnicas (ou similares) relacionadas ao Deadlock."
        ])

        embed.add_field(name="**Regras**", value=regras_text, inline=False)
        await interaction.channel.send(embed=embed)
    else:
        await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)

@aclient.tree.command(guild=discord.Object(id=id_do_servidor), name='deadlock', description='Atualmente estou em desenvolvimento para fornecer uma melhor experiencia para todos os membros')
async def slash2(interaction: discord.Interaction):
    embed = discord.Embed(
        title="⚠️ Em Desenvolvimento ⚠️",
        description="Ops, parece que ainda não estou pronto para uso. Fique atento para mais atualizações!",
        color=discord.Color.orange()
    )
    embed.set_footer(text="Obrigado pela sua paciência!")
    await interaction.response.send_message(embed=embed, ephemeral=True)

aclient.run("SEU_TOKEN_AQUI")  # Substitua pelo seu token


