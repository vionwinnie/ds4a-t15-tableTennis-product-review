import os
import yaml

def get_login_info():
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..'))
    CREDENTIAL_DIR = os.path.abspath(os.path.join(PROJECT_DIR,'credentials'))
    config_yaml_file_name = 'login.yaml'
    YAML_FILE_PATH = os.path.join(CREDENTIAL_DIR,config_yaml_file_name)
    with open(YAML_FILE_PATH) as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
        user_info = yaml.load(file, Loader=yaml.FullLoader)
    
    return user_info['mongo-db']

if __name__=="__main__":
    print(get_login_info())
