import cx_Oracle
import os
import time

def verifica_directorio():
    """
    Verifica si existe el directorio sino lo crea
    """
    if not os.path.isdir("C:\\respaldo_sql"):
        os.mkdir("C:\\respaldo_sql")
        print("El directorio no Existe y se creo y esta en: C:\\respaldo_sql")

def respaldopkg():
    """
    Realiza el respaldo de los procedimientos proporcionados
    """
    dsn = cx_Oracle.makedsn(host='127.0.0.1', port=1521, sid='mi_base')
    conexion = cx_Oracle.connect(user='user', password='root', dsn=dsn,encoding='UTF-8', nencoding='UTF-8')

    nombre_pkg = input("Ingresa nombre del package a respaldar: \n")
    lista = nombre_pkg.split(",")
    for i in range(0,int(len(lista))):
        cursor = conexion.cursor()
        cursor.execute(f"select dbms_metadata.get_ddl('PACKAGE_SPEC', '{lista[i].upper()}', 'user'),dbms_metadata.get_ddl('PACKAGE_BODY', '{lista[i].upper()}', 'user')  from dual")

        files = open(f"C:\\respaldo_sql\\{lista[i].upper()}-{str(time.strftime('%d-%m-%Y_%H%M%S'))}.sql","w")
        for j in cursor:
            files.write(str(j[0])+"\n\n")    
            files.write(str(j[1]))
    
        print("Se respaldo el package:",lista[i],"correctamente")
    input("Preciona cualquier tecla para cerrar")

    files.close()
    conexion.close()


if __name__ == "__main__":
    verifica_directorio()
    respaldopkg()