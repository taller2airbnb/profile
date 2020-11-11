import json

VALID_PROFILE_ADMIN = json.dumps({'id': 0, 'description': 'admin'})

VALID_PROFILE_ANFITRION = json.dumps({'id': 1, 'description': 'anfitrion'})

VALID_ADMIN1_REGISTER = json.dumps({'first_name': 'Gonza', 'last_name': 'Paez', 'email': 'algo@algo.com',
                                   'password': '123456789', 'national_id': '12345678',
                                   'national_id_type': 'DNI',
                                   'alias': 'gonzalgo', 'profile': 0})

VALID_ADMIN1_LOGIN = json.dumps({'email': 'algo@algo.com', 'password': '123456789'})

VALID_USER2_REGISTER_WITH_ADMIN = json.dumps({'first_name': 'Admin', 'last_name': 'Istrador', 'email': 'admin@algo.com',
                                         'password': '123456789', 'national_id': '12345678', 'national_id_type': 'DNI',
                                         'alias': 'administrador', 'user_logged_id': 1})

VALID_ANFITRION1_REGISTER = json.dumps({'first_name': 'Anfi', 'last_name': 'trion', 'email': 'anfi@algo.com',
                                   'password': '123456789', 'national_id': '12345678',
                                   'national_id_type': 'DNI',
                                   'alias': 'anfitrion', 'profile': 1})

VALID_ANFITRION1_LOGIN = json.dumps({'email': 'anfi@algo.com', 'password': '123456789'})