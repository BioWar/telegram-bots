import telebot
import cherrypy
import config

WEBHOOK_HOST = 'YOUR_IP_HERE'
WEBHOOK_PORT = 80
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

WEBHOOK_URL_BASE = f'https://{WEBHOOK_HOST}:{WEBHOOK_PORT}'
WEBHOOK_URL_PATH = f'/{config.token}/'

bot = telebot.TeleBot(config.token)

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and 'content-type' in cherrypy.request.headers and cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)
        
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)
    
if __name__=='__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH,
                    certificate=open(WEBHOOK_SSL_CERT,'r'))
    cherrypy.config.update({
        'server.socket_host':WEBHOOK_LISTEN,
        'server.socket_port':WEBHOOK_PORT,
        'server.ssl_module':'builtin',
        'server.ssl_certificate':WEBHOOK_SSL_CERT,
        'server.private_key':WEBHOOK_SSL_PRIV,
        })
    
    cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/':{}})