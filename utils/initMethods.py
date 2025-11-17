import configparser
import yaml

def readYaml(filePath: str) -> dict:
    with open(filePath, "r") as f:
        content = yaml.safe_load(f)
    return content 

def getConfig(path: str) -> dict:
    config = configparser.ConfigParser()
    config.read(path)
    return config