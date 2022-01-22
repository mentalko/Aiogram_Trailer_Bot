from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  
WEBHOOK_URL = env.str("WEBHOOK_URL") 
TMDB_KEY = env.str("TMDB_KEY")  


