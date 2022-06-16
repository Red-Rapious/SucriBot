# Développé par 
# - Ajay "pa1n" Probst (2020-2021)
# - Antoine "Red Rapious" Groudiev (2021-2022)

import discord
from os import path
from discord import NotFound
import asyncio
import emoji
from webserver import keep_alive
import datetime
from exo_aleatoire import exo_aleatoire


intents = discord.Intents.all()
client = discord.Client(intents=intents)

admin_id=313264206621179906 # id de l'admin, RedRapious
serveur_id=882700982218268773 #id du serveur
tdgrp1_id = 882700982235062325 # TD grp 1
eleve_id  = 882700982247641172 # rôle élève
general_sans_profs = 882700982574792758 # id du channel general_sans_profs
tag_eleves = "<@"+eleve_id+">"

tokennn='ODk3NTAzMTUxNTQ3MDk3MTI4.YWWm8g.DO_7_7ey-U4kmTMvW43lRTPchYU'  # https://discord.com/developers/applications/

pause_vacances = True # si pause_vacances est activé, il n'y aura pas de rappel de livres

async def log(message, notify_admin=False): # écrit un message dans le fichier texte log
  today = datetime.datetime.now()
  user = await client.fetch_user(admin_id)
  log_file = open("fichiers/logs.txt", "a")
  log_file.write("\n" + str(today) + " : " + str(message))
  if notify_admin:
    await user.send(message)
  log_file.close()


def surnom(g,idd) -> str: # retourne le surnom discord plutôt que le pseudo (eg Ajay Probst au lieu de pa1n)
    for m in g.members:
        if m.id == idd:
            if m.nick is None:
                return m.name
            else:
                return m.nick
    return "Problème"

def pluriel(m) -> str: # trivial
    if m>1:
        return "s"
    else:
        return ""
        
def pluriel2(m) -> str: # trivial
    if m>1:
        return "élèves sont présents"
    else:
        return "élèves est présent"
            
def voyelle(m): # pour éviter d'avoir "Le mail de Isabelle Séguret..." au lieu de "Le mail d'Isabelle Séguret..."
    if (m.lower())[0] in ["a","e","y","u","i","o","h"]:
        return " d'"
    else:
        return " de "

def colleur(m): # Renvoie la phrase "Le mail d'Ottavio Khalifa est ..."
    code = m.upper()
    if path.exists("fichiers/mails.txt"):
        f = open("fichiers/mails.txt", "r", encoding='utf8')
        Lines = f.readlines()
        for line in Lines:
            ligne = line.split(",")
            if code in ligne[0].split(" "):
                if ligne[1] == "":
                    return "Désolé, je n'ai pas encore l'adresse mail" + voyelle(ligne[2]) + ligne[2] + ", si tu l'as n'hésite pas à contacter pa1n pour qu'il l'ajoute au bot"
                elif ligne[3] == "\n":
                    return "Le mail" + voyelle(ligne[2]) + ligne[2].replace('\n', '') + " est **" + ligne[1] + "**"
                elif ligne[3] == "1\n":
                    return ligne[1]
                else:
                    return "Le mail de " + ligne[2] + " est **" + ligne[1] + "** et j'ai même son numéro : **" + ligne[3].replace('\n', '') + "**"
        return "Ce colleur n'est pas répertorié, assure-toi d'avoir pris les codes du colloscope. Il est également possible que je ne connaisse pas son adresse email."
            
    else:
        return "Erreur, contactez Ajay Probst/Antoine Groudiev, il m'a mal conçu"


def prof(ctxid): #check si quelqu'un est prof, si oui on retourne son id
    if path.exists("fichiers/profs.txt"):
        f = open("fichiers/profs.txt", "r", encoding='utf8')
        Lines = f.readlines()
        for line in Lines:
            ligne = line.split(",")
            if int(ligne[0])==ctxid:
                return True, int(ligne[1]), ligne[2], int(ligne[3])
        return False, "", ctxid
    else:
        return False, "", "Erreur"
        
async def reaction(idd,emos): #fonction pour mettre un emote avec l'id d'un message suivi de l'emote
    for channel in client.get_all_channels():
        if str(channel.type) == 'text':
            try:
                msgg = await channel.fetch_message(idd)
                await client.wait_until_ready()
            except NotFound:
                continue
    #emojis=["\U0001F44D"]
    for emo in emos:
        await msgg.add_reaction(emoji.emojize(emo))

async def appel(msg): #
    admin_user = await client.fetch_user(admin_id)
    await client.wait_until_ready()
    ctx = msg.author
    s = prof(ctx.id)
    if s[0]:
        if "g1" in msg.content:
            p = [s[0],s[1],s[2],747755284612644882] # TD groupe 1
        elif "g2" in msg.content:
            p = [s[0],s[1],s[2],747755284612644881] # TD groupe 2
        else:
            p = [s[0],s[1],s[2],s[3]]
        absents = []
        #guild = msg.guild # à changer 829394918790529105
        guild = client.get_guild(serveur_id) 
        role = guild.get_role(p[3])
        chan = client.get_channel(p[1])
        presents = [p.id for p in chan.members]
        eleves = [e.id for e in role.members]       
        presents_nbre = 0
        for k in range(len(presents)):
            if presents[k] in eleves:
                presents_nbre += 1
        for e in eleves:
            if e not in presents:
                absents.append(surnom(guild,e))
        #today = date.today()
        #message = "Bonjour " + p[2] + "\n" + "\n" + "      Nous sommes le " + today.strftime("%d/%m/%Y") + "\n" + "      **" + str(len(presents)) + "/" + str(len(eleves)) + "** elèves sont présents" + "\n" + "      Il manque aujourd'hui " + str(len(absents)) + " élèves : " + "\n" + "\n"
        message = "Bonjour " + p[2] + "\n" + "\n" + "      **" + str(presents_nbre) + "/" + str(len(eleves)) + "**" + " " + pluriel2(presents_nbre) + "\n"
        if len(absents)>0:
            message = message + "      Il manque **" + str(len(absents)) + "** élève" + pluriel(len(absents)) + " : " + "\n" + "\n"
        else:
            message = message + "      Il ne manque **personne**" + "\n"
        liste = ""
        k = 1
        for a in absents:
            liste = liste + "           " + "• :x:  **" + a + "** \n"
            k+=1
        message = message + liste + "\n" + "Bien à vous," + "\n" + "En cas d'erreur, contacter Ajay Probst/Antoine Groudiev"
        print(len(message))
        await ctx.send(message)
        if ctx != admin_user:
            #await admin_user.send(ctx.name + " demande l'appel")
            await log(ctx.name + " demande l'appel", True)
    else:
        await ctx.send("Accès refusé, contactez Ajay Probst/Antoine Groudiev en cas d'erreur, désolé " + ctx.name)
        await log(ctx.name + " demande l'appel")

async def rappel_livres(): # tag les élèves vers 19h tous les lundi et mardi pour leur rappeler de prendre leurs livres
  decalage = 2
  if not pause_vacances:
    message_send = datetime.datetime.now().hour == 19+1
    while True:
      today = datetime.datetime.now()
      if not message_send and (today.hour+decalage) == 19 and today.strftime("%A") == "Monday":
        channel = client.get_channel(general_sans_profs)
        await channel.send(":books: " + tag_eleves + ", n\'oubliez pas vos livres de français ! :books:")
        await log("rappel à tous des livres de français")
        message_send = True

      """if not message_send and (today.hour+decalage) == 19 and today.strftime("%A") == "Tuesday":
        channel = client.get_channel(general_sans_profs)
        await channel.send(":books: " + tag_eleves + ", n\'oubliez pas vos livres de français si vous avez TD ! :books:")
        await log("rappel au groupe de TD des livres de français")
        message_send = True"""

      if today.hour == 18:
        message_send = False
      await asyncio.sleep(10*60) # 10 minutes


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await log("le bot a démarré")
    #activity = discord.Game(name="skribbl.io", type=3)
    activity = discord.Activity(type=discord.ActivityType.watching, name="$sucri help")
    await client.change_presence(status=discord.Status.online, activity=activity)
    await rappel_livres()
    
@client.event
async def on_message(message):
    v = msg=message.content
    admin_user = await client.fetch_user(admin_id)
    await client.wait_until_ready()
    if message.author == client.user:
        return

    
      #if not message.channel.type is discord.ChannelType.private:
      #  await message.delete()

    if message.channel.type is discord.ChannelType.private: # en mp
        if msg.startswith('$sucri td') or msg.startswith("$sucri tp") or msg.startswith("td"):
          guild = client.get_guild(serveur_id)
          role_td1 = guild.get_role(tdgrp1_id)
          listepersrole_td1 = [e.id for e in role_td1.members]
          role_eleve = guild.get_role(eleve_id)
          listepersrole_eleve = [e.id for e in role_eleve.members]
        
          now = datetime.datetime.now()
          day = now.strftime("%A")
          week_message = "**cette semaine**, tu as"
          if day=="Saturday" or day=="Sunday":
            week_message = "la **semaine prochaine**, tu auras"
            week = now.isocalendar()[1] + 1
          else:
            week = now.isocalendar()[1]

          if message.author.id not in listepersrole_eleve: # pas un élève
            choquet_le_boss = await client.fetch_user(915352497894354974)
            if message.author == choquet_le_boss:
              await message.channel.send(f"{message.author.mention}, vous avez l'incroyable chance d'avoir TD de maths avec toute la MPSI2, pendant toute la matinée de lundi !")
            else:
              await message.channel.send(f"{message.author.mention}, vous n'êtes pas un élève, vous avez la chance de ne pas avoir TD !")
          else : # est un élève
            if (message.author.id in listepersrole_td1 and week%2==0) or (message.author.id not in listepersrole_td1 and week%2==1):
              await message.author.send(f"{message.author.mention}, " + week_message + " :"
              + "\n  - :test_tube: TP de Physique/Chimie lundi à **8h30**"
              + "\n  - :triangular_ruler: TD de Mathématiques lundi à **10h30**"
              + "\n  - :page_facing_up: TD de Physique/Chimie vendredi à **8h30**")
            else:
              await message.author.send(f"{message.author.mention}, " + week_message + " :"
              + "\n  - :triangular_ruler: TD de Mathématiques lundi à **8h30**"
              + "\n  - :test_tube: TP de Physique/Chimie lundi à **10h30**"
              + "\n  - :page_facing_up: TD de Physique/Chimie vendredi à **9h30**")
            await log(str(message.author) + " demande ses horaires de td en MP")

        elif msg.startswith('mail'):
            await message.author.send(colleur(v.split("mail ",1)[1]))
            await log(str(message.author) + " demande **" + v.split("mail ",1)[1] + "**")
          
        elif msg.startswith('appel'):
            await appel(message)
            await log(str(message.author) + " demande l'appel")
        
        """elif message.author != admin_user:
            await message.author.send("Désolé, je ne sais pas faire :cry: \nPour avoir le mail d'un colleur, écris dans le chat **mail CODE_DU_COLLEUR** \nExemple : 'mail OK2'")
            await log(str(message.author) + " dit **" + msg + "**")"""
      
        if message.author == admin_user:
            if msg.startswith('publie'): #envoie un message sur un channel du serv
                cmd = msg.split(' ',2)
                chan = client.get_channel(int(cmd[1]))
                await client.wait_until_ready()
                await chan.send(cmd[2])
            
            elif msg.startswith('mp'): #envoie un message pv à qqun
                cmd = msg.split(' ',2)
                cible = await client.fetch_user(int(cmd[1]))
                await client.wait_until_ready()
                await cible.send(cmd[2])
                #await message.author.send(cmd[2])
            
            elif msg.startswith('emoji'): #ajoute un emote sur un msg
                cmd = msg.split(' ',2)
                emos = cmd[2].split(',')
                await reaction(int(cmd[1]),emos)

    elif msg.startswith("$sucri"): # hors mp
      if msg.startswith('$sucri td') or msg.startswith("$sucri tp"):
        role_eleve = discord.utils.find(lambda r: r.name == 'Elèves', message.guild.roles)
        role_td1 = discord.utils.find(lambda r: r.name == 'TD grp 1', message.guild.roles)
      
        now = datetime.datetime.now()
        day = now.strftime("%A")
        week_message = "**cette semaine**, tu as"
        if day=="Friday" or day=="Saturday" or day=="Sunday":
          week_message = "la **semaine prochaine**, tu auras"
          week = now.isocalendar()[1] + 1
        else:
          week = now.isocalendar()[1]

        if not role_eleve in message.author.roles: # pas un élève
          choquet_le_boss = await client.fetch_user(915352497894354974)
          if message.author == choquet_le_boss:
            await message.channel.send(f"{message.author.mention}, vous avez l'incroyable chance d'avoir TD de maths avec toute la MPSI2, pendant toute la matinée de lundi !")
          else:
            await message.channel.send(f"{message.author.mention}, vous n'êtes pas un élève, vous avez la chance de ne pas avoir TD !")
        else : # est un élève
          if (role_td1 in message.author.roles and week%2==0) or (role_td1 not in message.author.roles and week%2==1):
            await message.channel.send(f"{message.author.mention}, " + week_message + " :"
            + "\n  - :test_tube: TP de Physique/Chimie lundi à **8h30**"
            + "\n  - :triangular_ruler: TD de Mathématiques lundi à **10h30**"
            + "\n  - :page_facing_up: TD de Physique/Chimie vendredi à **8h30**")
          else:
            await message.channel.send(f"{message.author.mention}, " + week_message + " :"
            + "\n  - :triangular_ruler: TD de Mathématiques lundi à **8h30**"
            + "\n  - :test_tube: TP de Physique/Chimie lundi à **10h30**"
            + "\n  - :page_facing_up: TD de Physique/Chimie vendredi à **9h30**")
          await log(str(message.author) + " demande ses horaires de td")

      elif msg.startswith('$sucri mail'):
        await message.author.send(colleur(v.split("$sucri mail ",1)[1]))
        await message.delete()
            
      elif msg.startswith("$sucri help"):
        await message.author.send("Liste des fonctions de Sucri Bot :\n- $sucri mail [mail] : te donne l'adresse mail d'un professeur ou colleur\n- $sucri td : te donne tes horaires de TD et TP en fonction de ton groupe\n- Plus à venir !")    
      
      elif msg.startswith('$sucri appel'):
          await appel(message)
          await message.delete()

      elif msg.startswith('$sucri exo'):
          await message.channel.send("Voici un exo pour " +  surnom(client.get_guild(serveur_id) , message.author) + " : " + exo_aleatoire())
          """
          image_name = "images/exo.png"
          sympy.preview(exo_aleatoire(), viewer='file', filename=image_name, euler=False)
          with open(image_name, "rb") as fh:
            f = discord.File(fh, filename=image_name)
          await message.channel.send(file=f)
          #await message.channel.send(",tex " + exo_aleatoire())
          """
          

      else:
          await message.author.send("Désolé, je ne sais pas faire :cry: \nPour avoir le mail d'un colleur, écris dans le chat **mail CODE_DU_COLLEUR** \nExemple : 'mail OK2'")
            
          await log(str(message.author) + " dit **" + msg + "**")
          await message.delete()
    
    

keep_alive()
client.run(tokennn)