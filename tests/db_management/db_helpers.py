def GetDataDB(conn, command, params=''):
    cursor = conn.cursor()
    RETORNO = []
    if params=='': RETORNO = list(cursor.execute(command))
    else: RETORNO = list(cursor.execute(command, params))
    return RETORNO, cursor

def GetAllDataDB(conn, command, params=''):
    cursor = conn.cursor()
    RETORNO = []
    if params=='': RETORNO = list(cursor.execute(command))
    else: RETORNO = list(cursor.execute(command, params))
    return RETORNO, cursor
