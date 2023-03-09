import os
import sys
import yaml
from loguru import logger
from gusql import oneload_sql_db

CONFIG_FILE = f"{os.path.dirname(os.path.abspath(__file__))}/config.yml"

if os.path.exists(CONFIG_FILE) is False:
    try:
        data={
            "REFRESH_TOKEN":"",
            "RSS_URL":"",
            "BOT_TOKEN":"",
            "CHANNEL_ID":"",
            "BOT_ADMIN":[""],
            "RSS_SECOND":60,
            "PROXY":"socks5://127.0.0.1:8089",
            "PROXY_OPEN":False,
            "RSS_OPEN":True,
            "LOG_OPEN":True,
            "FILE_DELETE":True
        }
        with open(CONFIG_FILE, "w+") as c:
            c.write(yaml.dump(data=data,Dumper=yaml.CDumper))
        logger.success("配置文件创建成功，请填写配置信息后重启程序。")
        if oneload_sql_db() is False:
            logger.error("创建数据库失败，请检查权限。")
        else:
            logger.success("数据库创建成功。")
        sys.exit()
        
    except Exception as e:
        logger.error(f"创建配置文件失败，请检查权限。\n{e}")
        sys.exit()

def get_environment_variable(name):
    # Helper function to retrieve environment variables.
    value = os.environ.get(name)
    if not value:
        logger.warning(f"未找到系统环境变量 {name}，将从配置文件读取")
        with open(CONFIG_FILE, "r") as c:
            config = yaml.load(c.read(), Loader=yaml.CLoader)
        value = config.get(name)
    return value

def check_config():
    with open(CONFIG_FILE,"r") as c:
        config = yaml.load(c.read(),Loader=yaml.CLoader)
    
    # Retrieve variables from environment or config file
    config['REFRESH_TOKEN'] = get_environment_variable("REFRESH_TOKEN") or config['REFRESH_TOKEN']
    config['RSS_URL'] = get_environment_variable("RSS_URL") or config['RSS_URL']
    config['BOT_TOKEN'] = get_environment_variable("BOT_TOKEN") or config['BOT_TOKEN']
    config['CHANNEL_ID'] = get_environment_variable("CHANNEL_ID") or config['CHANNEL_ID']
    config['BOT_ADMIN'] = get_environment_variable("BOT_ADMIN") or config['BOT_ADMIN']
    config['PROXY_OPEN'] = bool(get_environment_variable("PROXY_OPEN") or config['PROXY_OPEN'])
    config['PROXY'] = get_environment_variable("PROXY") or config['PROXY']
    config['RSS_OPEN'] = bool(get_environment_variable("RSS_OPEN") or config['RSS_OPEN'])
    config['RSS_SECOND'] = int(get_environment_variable("RSS_SECOND") or config['RSS_SECOND'])
    config['LOG_OPEN'] = bool(get_environment_variable("LOG_OPEN") or config['LOG_OPEN'])
    config['FILE_DELETE'] = bool(get_environment_variable("FILE_DELETE") or config['FILE_DELETE'])

    if not config['REFRESH_TOKEN']:
        logger.error("REFRESH_TOKEN未配置，请填写配置信息或设置系统环境变量 'REFRESH_TOKEN' 后重启程序。")
        sys.exit()
    elif not config['BOT_TOKEN']:
        logger.error("BOT_TOKEN未配置，请填写配置信息或设置系统环境变量 'BOT_TOKEN' 后重启程序。")
        sys.exit()
    elif not config['CHANNEL_ID']:
        logger.error("BOT_CHANNEL未配置，请填写配置信息或设置系统环境变量 'CHANNEL_ID' 后重启程序。")
        sys.exit()
    elif not config['BOT_ADMIN']:
        logger.error("BOT_ADMIN未配置，请填写配置信息或设置系统环境变量 'BOT_ADMIN' 后重启程序。")
        sys.exit()
    elif not config['RSS_URL'] and config['RSS_OPEN']:
        logger.error("RSS_URL未配置，请填写配置信息或设置系统环境变量 'RSS_URL' 后重启程序。")
        sys.exit()
    elif not config['RSS_SECOND'] and config['RSS_OPEN']:
        logger.error("RSS_SECOND未配置，请填写配置信息或设置系统环境变量 'RSS_SECOND' 后重启程序。")
        sys.exit()
    elif config['PROXY_OPEN'] and not config['PROXY']:
        logger.error("PROXY未配置，请填写配置信息或设置系统环境变量 'PROXY' 后重启程序。")
        sys.exit()
    
    if config['LOG_OPEN']:
        logger.success("日志记录功能已开启")
        if not os.path.exists(f"{os.path.dirname(os.path.abspath(__file__))}/log"):
            os.mkdir(f"{os.path.dirname(os.path.abspath(__file__))}/log")
        logger.add(os.path.dirname(os.path.abspath(__file__))+"/log/bot_log_{time}.log", rotation="10MB", encoding="utf-8", enqueue=True, compression="zip", retention="10 days") #日志文件
    
    logger.success("配置检测通过!")
    return config

if __name__ == "__main__":
    print(check_config())
