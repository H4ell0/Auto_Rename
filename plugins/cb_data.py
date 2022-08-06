from helper.utils import progress_for_pyrogram, convert
from pyrogram import Client, filters
from pyrogram.types import ( Message, InlineKeyboardButton, InlineKeyboardMarkup,ForceReply)
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.database import find
import os 
import humanize
from PIL import Image
import time

@Client.on_callback_query(filters.regex('cancel'))
async def cancel(bot,update):
	try:
           await update.message.delete()
	except:
           return


#@Client.on_callback_query(filters.regex('rename'))
#async def rename(bot,update):
	#user_id = update.message.chat.id
	#date = update.message.date
	#await update.message.delete()
	#await update.message.reply_text("__𝙿𝚕𝚎𝚊𝚜𝚎 𝙴𝚗𝚝𝚎𝚛 𝙽𝚎𝚠 𝙵𝚒𝚕𝚎𝙽𝚊𝚖𝚎...__",	
	#reply_to_message_id=update.message.reply_to_message.id,  
	#reply_markup=ForceReply(True))

	
#@Client.on_callback_query(filters.regex("upload"))

@Client.on_message(filters.private &( filters.document | filters.audio | filters.video ))
async def doc(bot, update):
     file = getattr(update, update.media.value)
     filename = file.file_name     
     if not "." in filename:
         new_filename = filename + ".mkv"
     else:
         new_filename = filename + ".mkv"

     file_path = f"downloads/{new_filename}"
     file = getattr(update, update.media.value)     
     ms = await bot.send_message(update.chat.id, text="𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳...")     
     c_time = time.time()
     try:
     	path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳....", ms, c_time   ))        
     except Exception as e:
     	await ms.edit(e)
     	return 
     splitpath = path.split("/downloads/")
     dow_file_name = splitpath[1]
     old_file_name =f"downloads/{dow_file_name}"
     os.rename(old_file_name,file_path)
     duration = 0
     try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
           duration = metadata.get('duration').seconds
     except:
        pass
     user_id = int(update.chat.id) 
     ph_path = None
     data = find(user_id) 
     #media = getattr(file, file.media.value)
     c_caption = data[1] 
     c_thumb = data[0]
     if c_caption:
         caption = c_caption.format(filename=new_filename)
     else:
         caption = f"**{filename}**"
     if c_thumb:
         ph_path = await bot.download_media(c_thumb) 
     else:
         ph_path = await bot.download_media(c_thumb)  
         Image.open(ph_path).convert("RGB").save(ph_path)
         img = Image.open(ph_path)
         img.resize((320, 320))
         img.save(ph_path, "JPEG")
     await ms.edit("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....")
     c_time = time.time() 
     try:       
         await bot.send_document(
	     update.chat.id,
             document=file_path,
             thumb=ph_path, 
             caption=caption, 
             progress=progress_for_pyrogram,
             progress_args=( "𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....",  ms, c_time  )) 
            
     except Exception as e: 
         await ms.edit(e) 
         os.remove(file_path)
         if ph_path:
           os.remove(ph_path)
     await ms.delete() 
     os.remove(file_path) 
     if ph_path:
        os.remove(ph_path) 
