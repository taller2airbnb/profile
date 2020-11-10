import json

VALID_PROFILE_ADMIN = json.dumps({'id': 0, 'description': 'admin'})

VALID_USER1_REGISTER = json.dumps({'first_name': 'Gonza', 'last_name': 'Paez', 'email': 'algo@algo.com',
                                   'password': '123456789', 'national_id': '12345678',
                                   'national_id_type': 'DNI',
                                   'alias': 'gonzalgo', 'profile': 0})

VALID_USER1_LOGIN = json.dumps({'email': 'algo@algo.com', 'password': '123456789'})

VALID_USER2_REGISTER_ADMIN = json.dumps({'first_name': 'Admin', 'last_name': 'Istrador', 'email': 'admin@algo.com',
                                         'password': '123456789', 'national_id': '12345678', 'national_id_type': 'DNI',
                                         'alias': 'administrador', 'user_logged_id': 1})
