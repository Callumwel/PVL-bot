from header import *
async def setlp(message, args):
  c = message.channel
  if c.id != '481721487569453076':
    await client.send_message(c, 'Please only use !setlp in the <#481721487569453076> channel')
    return
  await client.send_message(c,'Time to set up your league pass!\nYou start with 6 main pokemon, and will unlock 4 sideboard slots as you continue.\nAs a reminder, legendary pokemon are not allowed in our format.\nAs well as this please ensure pokemon are spelt correctly with a capital letter, also specify the form, for example Alolan Ninetales would be: Ninetales (Alola).\nWhen entering a Mega Pokemon, please only enter the base form.\nThe full details can be found on the subreddit wiki.')
  retry = False
  while not retry:
    await client.send_message(c, 'Type "cancel" to cancel')
    await client.send_message(c, 'Now, enter the names of your first 6 pokemon, one at a time:')
    mons = []
    while len(mons) < 6:
      resp = await client.wait_for_message(timeout=60, author=message.author, channel=c)
      if resp == None or resp.content.lower() == 'cancel':
        await client.send_message(c, 'Bye')
        return
      if resp.content in pokemon_list[0]:
        mons.append(resp.content)
        await client.send_message(c, 'Added ' + resp.content)
      else:
        await client.send_message(c, resp.content + ' is not a Pokemon I know. Double check spelling and capitalization, and you may need to specfiy form')
    await client.send_message(c, 'Alright, your pokemon are: ' + ', '.join(mons))
    await client.send_message(c, 'Is this correct? (y/n)')
    resp = await client.wait_for_message(timeout=60, author=message.author, channel=c)
    if resp == None:
      await client.send_message(c, 'Bye')
      return
    retry = resp.content.lower()[0] == 'y'
  cursor.execute('SELECT * FROM betalp WHERE id=?', (message.author.id,))
  result = cursor.fetchone()
  if result != None:
    cursor.execute('DELETE FROM betalp WHERE id=?', (message.author.id,))
  cursor.execute('INSERT INTO betalp (id, mon1, mon2, mon3, mon4, mon5, mon6) VALUES (?,?,?,?,?,?,?)', (message.author.id, *mons))
  connection.commit()
  sprites = [pokemon_list[1][pokemon_list[0].index(mon)] for mon in mons]
  finalimg = Image.new('RGBA', (130, 65), (0,0,0,0))
  for i,mon in enumerate(sprites):
    url = 'https://raw.githubusercontent.com/msikma/pokesprite/master/icons/pokemon/regular/{}.png'.format(mon)
    monimg = Image.open(requests.get(url, stream=True).raw)
    finalimg.paste(monimg, box=((i%3)*45, (i//3)*35))
  finalimg.save('/root/badgebot/rosters/{}.png'.format(message.author.id))
  subprocess.call('/root/badgebot/git.sh')
  await client.send_message(c, 'All Done!')
