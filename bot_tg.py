import telebot
from pytube import YouTube
import os
import time

#https://trello.com/b/GOvxCeC3/team-3

class BaseCommandHandler:
    def __init__(self, bot):
        self.bot = bot

    def send_welcome(self, message):
        self.bot.send_message(message.chat.id, '👋  Привіт! Ось список команд, які ти можеш використовувати:\n/start - короткий список доступних команд\n/help - як це працює\n/info - інформація про функціонал\n/donate - допомога авторам\n/support - служба підтримки\n/suggestions - ідеї та пропозиції\n/advertising - послуги реклами')
                
    def send_help(self, message):
        self.bot.send_message(message.chat.id, '📥  Для того, щоб завантажити відео, потрібно надіслати боту посилання на відео, яке бажаєте зберегти.')
                
    def send_info(self, message):
        self.bot.send_message(message.chat.id, 'Це - AstroMewBot 😼\nЗадача бота - зберігати відео за посиланням.\nНа даний момент ти можеш зберегти відео з YouTube Shorts.\nТи можеш зберегти відео тривалістю до 60 секунд.')

    def send_donate(self, message):
        self.bot.send_message(message.chat.id, '💰  Якщо вам сподобався цей бот та ви бажаєте підтримати авторів ось банка:\n"банка"')

    def send_support(self, message):
        self.bot.send_message(message.chat.id, '⚙️  Якщо у вас винекли проблеми звертайтесь до @Irrmmm')
        
    def send_suggestions(self, message):
        self.bot.send_message(message.chat.id, '✍️  За пропозиціями та ідеями звертайтеся до @maxpos')
        
    def send_advertising(self, message):
        self.bot.send_message(message.chat.id, '🗣  За рекламою звертайтесь до @zxcarseniyy')
    
class HandlerLink(BaseCommandHandler):
    def __init__(self, bot):
        super().__init__(bot)
        
    def is_video_duration_valid(self, youtube_link):
        try:
            youtube = YouTube(youtube_link)
            duration = youtube.length
            if duration > 60:
                return False, "Помилка 1: Відео перевищує максимальну тривалість YouTube Shorts."
            else:
                return True, None
        except Exception as e:
            error_message = "Помилка 2: Неправильний формат повідомлення."
            if "Network is unreachable" in str(e):
                error_message = "Помилка 3: Погана мережа. Перевірте з'єднання та спробуйте ще раз."
            elif "Timeout expired" in str(e):
                error_message = "Помилка 4: Час очікування вичерпано. Перевірте з'єднання та спробуйте ще раз."
                return False, error_message


    def handle_text(self, message):
        valid, error_message = self.is_video_duration_valid(message.text)
        if valid:
            self.bot.send_message(message.chat.id, '⚠️  Увага!\nЗавантаження відео може зайняти деякий час.\n⏱  Зачекайте кілька секунд.')
            try:
                youtube = YouTube(message.text)
                video = youtube.streams.get_highest_resolution()
                audio = youtube.streams.filter(only_audio=True).first()
                video_file_path = video.download(output_path='video')
                audio_file_path = audio.download(output_path='audio')
                self.bot.send_message(message.chat.id, 'Відео та аудіо доріжка завантажені успішно! Ось вони:')
                self.bot.send_video(message.chat.id, open(video_file_path, 'rb'))
                self.bot.send_audio(message.chat.id, open(audio_file_path, 'rb'))
                self.delete_file_after_delay(video_file_path, 20)
                self.delete_file_after_delay(audio_file_path, 20)
                self.bot.send_message(message.chat.id, 'РЕКЛАМА\nДякуємо за використання AstroMewBot!😸 Якщо вам сподобалося наш сервіс, не забудьте поділитися з друзями.\n😸🤝😸')
            except Exception as e:
                error_message = "Помилка 4: Неможливо обробити відео. Спробуйте ще раз."
                self.bot.send_message(message.chat.id, error_message)
        else:
            self.bot.send_message(message.chat.id, error_message)

    def delete_file_after_delay(self, filename, delay):
        time.sleep(delay)
        os.remove(filename)
        

bot = telebot.TeleBot('6793123533:AAEHDargwyBopL77CKtq37L-PAQLPOZoBus')
handler = HandlerLink(bot)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    handler.send_welcome(message)

@bot.message_handler(commands=['help'])
def send_help(message):
    handler.send_help(message)

@bot.message_handler(commands=['info'])
def send_info(message):
    handler.send_info(message)
    
@bot.message_handler(commands=['donate'])
def send_donate(message):
    handler.send_donate(message)

@bot.message_handler(commands=['support'])
def send_support(message):
    handler.send_support(message)
    
@bot.message_handler(commands=['suggestions'])
def send_suggestions(message):
    handler.send_suggestions(message)
    
@bot.message_handler(commands=['advertising'])
def send_advertising(message):
    handler.send_advertising(message)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    handler.handle_text(message)

bot.polling(none_stop=True)
