import json

VALID_PROFILE_ADMIN = json.dumps({'id': 0, 'description': 'admin'})

VALID_PROFILE_ANFITRION = json.dumps({'id': 1, 'description': 'anfitrion'})

VALID_ADMIN1_REGISTER = json.dumps(
    {'user_type': 'bookbnb', 'first_name': 'Gonza', 'last_name': 'Paez', 'email': 'algo@algo.com',
     'password': '123456789', 'national_id': '12345678',
     'national_id_type': 'DNI',
     'alias': 'gonzalgo', 'profile': 0})

VALID_ADMIN1_LOGIN = json.dumps({'user_type': 'admin', 'email': 'algo@algo.com', 'password': '123456789'})

VALID_USER2_REGISTER_WITH_ADMIN = json.dumps(
    {'user_type': 'admin', 'first_name': 'Admin', 'last_name': 'Istrador', 'email': 'admin@algo.com',
     'password': '123456789', 'national_id': '12345678', 'national_id_type': 'DNI',
     'alias': 'administrador', 'user_logged_id': 1, 'profile': 0})

VALID_ANFITRION1_REGISTER = json.dumps(
    {'user_type': 'bookbnb', 'first_name': 'Anfi', 'last_name': 'trion', 'email': 'anfi@algo.com',
     'password': '123456789', 'national_id': '12345678',
     'national_id_type': 'DNI',
     'alias': 'anfitrion', 'profile': 1})

VALID_ANFITRION1_LOGIN = json.dumps({'email': 'anfi@algo.com', 'password': '123456789'})

VALID_MODIFY_ANFITRION = json.dumps(
    {'user_type': 'bookbnb', 'first_name': 'Norbert', 'last_name': 'DeGoas', 'national_id': '334455',
     'national_id_type': 'CedulaVerde', 'id': 1})

VALID_MODIFY_ANFITRION_JUST_NAME = json.dumps({'user_type': 'bookbnb', 'first_name': 'Norbert', 'id': 1})

INVALID_MODIFY_USER_EMPTY = json.dumps({'id': 1})

INVALID_MODIFY_USER_BLANK = json.dumps(
    {'user_type': 'bookbnb', 'first_name': '', 'last_name': '', 'national_id': '', 'national_id_type': '',
     'id': 1})
VALID_USER_INFO = json.dumps({'id': 1})

VALID_PEPE_CHATRUC_BOOKBNB_REGISTER = json.dumps(
    {'user_type': 'bookbnb', 'first_name': 'El Pepe', 'last_name': 'Chatruc', 'email': 'elpepechatruc@gmail.com',
     'password': '123456789', 'national_id': '12345678',
     'national_id_type': 'DNI',
     'alias': 'El Pepe Chatruc', 'profile': 1})
