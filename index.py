import cx_Oracle
import os
from datetime import datetime
import csv


class SavePackages:
    def __init__(self):
        self.path = 'C:\\respaldo_sql\\'
        self.user = 'root'
        self.pwd = 'your_psw'
        self.host = '127.0.0.1'
        self.sid = 'mi_base'
        self.port = 1521
        self.dns = cx_Oracle.makedsn(host=self.host, port=self.port, sid=self.sid)        
        self.menu()

    def verify_directory(self):
        try:
            if not os.path.isdir(self.path):
                os.mkdir(self.path)
                print(f'El directorio no existe se creo en: {self.path}')
        except Exception as ex:
            print(ex)

    def save_backup(self,item=None):
        try:
            if item is None:
                name_pkg = input('Ingresa nombre del package a respaldar puede ser mas de uno separado por (,): \n').split(',')
            else:
                name_pkg = item            
            connection = cx_Oracle.connect(user=self.user, password=self.pwd, dsn=self.dns, encoding='utf-8', nencoding='utf-8')
            with connection as conexion:
                for pkg in name_pkg:
                    date = datetime.strftime(datetime.now(), '%d-%m-%Y_%H_%M_%S')
                    if pkg.strip() is not '':
                        with conexion.cursor() as cursor:
                            for row in cursor.execute(f"select dbms_metadata.get_ddl('PACKAGE_SPEC', '{pkg.strip().upper()}', '{self.user}'),dbms_metadata.get_ddl('PACKAGE_BODY', '{pkg.strip().upper()}', '{self.user}')  from dual"):                                
                                with open(f'{self.path}{pkg.strip().upper()}{date}.sql', 'w', encoding='utf-8') as file:
                                    file.write(str(row[0]).replace('"', '').strip()+'\n/\n')
                                    file.write(str(row[1]).replace('"', '').strip()+'\n/\n')
                                    print(f'Se realizo el respaldo del package: {pkg.strip().upper()}{date}')
        except Exception as ex:
            print(ex)

    def read_csv(self):
        try:
            path_file = input('Ingresa la ruta del archivo csv:\n\t')
            if os.path.isfile(path_file) and os.path.splitext(path_file)[1].upper()  == '.CSV':
                with open(path_file, 'r',encoding='utf-8',) as file_csv:
                    reader = csv.reader(file_csv.readlines())
                    for ls in reader:
                        self.save_backup(ls)
            else:
                print('Verifique que el archivo exista o sea en formato .CSV')
        except Exception as ex:
            print(ex)
            
    def menu(self):
        try:            
            while True:
                opcion = int(input('Script para realizar respaldos de packages en BD ORACLE ingresa:\n\n1.- ingresar nombre de packages\n2.- Cargar CSV, se debe dar la ruta del archivo\n\t'))
                if opcion > 0 and opcion < 3:
                    if opcion == 1:
                        self.save_backup()
                    elif opcion == 2:
                        self.read_csv()
                    break
                print('Opcion no valida\n')
        except Exception as ex:
            print(ex)

if __name__ == '__main__':
    SavePackages()