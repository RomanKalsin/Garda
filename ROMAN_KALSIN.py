#Roman Kalsin
#Python 3.9.0
import datetime
import socket

def desired_look(string):# Принимает строку от сервера и выдает строку нужного вида
    call_date_time = datetime.datetime(int(string[121:125]), int(string[126:128]), int(string[129:131]), int(string[132:134]), int(string[135:137]), int(string[138:140])) #Записываем дату время в удобном формате при помощи модуля datetime
    id_s = string[0:5].lstrip("0") # Запиасываем ИД удаляя лишние нули в начале строки
    imei_s = string[29:44].strip() # Записваем EMAI (удаляя лишние пробелы на всякий случай) :)
    date_s = call_date_time.strftime("%d.%m.%Y") # Записываем дату в нужном нам формате из переменной call_date_time
    duration_s = string[141:151].lstrip("0") + " sec" # Записываем продолжительность звонка удаляя лишние нули в начале строки
    if duration_s == " sec":
        duration_s = "0 sec"
    name_from_s = string[45:65].strip() # Записываем ФИО вызывающего удаляя лишние пробелы в начале и конце строки
    name_to_s = string[95:115].strip() # Записываем ФИО вызываемого удаляя лишние пробелы в начале и конце строки
    numb_from_s = string[6:16].strip() # Записываем  Вызывающий номер удаляя лишние пробелы в начале и конце строки
    numb_to_s = string[84:94].strip() #  Записываем  Вызываемый номер удаляя лишние пробелы в начале и конце строки
    time_s = call_date_time.strftime("%H-%M-%S") # Записываем время в нужном нам формате из переменной call_date_time
    dict_call = '{{\n    "{}": {{\n        "{}": {{\n            "date": "{}",\n            "duration": "{}",\n            "name_from": "{}",\n            "name_to": "{}",\n            "numb_from": "{}",\n            "numb_to": "{}",\n            "time": "{}"\n        }}\n    }}\n}}'.format(id_s, imei_s, date_s, duration_s, name_from_s, name_to_s, numb_from_s, numb_to_s, time_s)
    return str(dict_call)
   
def con_serv(host, port, name): #Для наглядности оставил комманды PRINT
    sock = socket.socket()
    sock.connect((host, port))
    print(sock.recv(1024)) #Просьба ввести имя
    sock.send(bytes(name,"utf-8"))#Отправляем наше имя
    m = sock.recv(1024).decode("utf-8") #Сервер предлагает попытаться пройти тест
    if m == "{}, let's try to pass the test, good luck!\n\n".format(name):# Если сервер желает нам удачи входим в цикл
        while True:
            s = sock.recv(1024).decode("utf-8") # Ответ от сервера строка            
            if len(s) == 152: 
                print(s)
                sock.send(bytes(desired_look(s),"utf-8"))# Отправляем ответ серверу в нужном виде преобразуя в байты
            elif len(s) == 19:
                print(s)
            elif len(s) == 17: # Если сервер отвечает неправильно выводим сообщение и правильный ответ и закрываем соединение
                print(s)
                print(sock.recv(1024).decode("utf-8"))
                sock.close()
                break
            elif len(s) == 26: # Если сервер отвечает что тест успешно пройден 
                print(s)
                sock.close()
                break
            else: # Закрываем соединение если что то пошло не так
                print(s)
                sock.close()
                break
    else:
        sock.close()
        print(m)


HOST = "185.33.145.118"
PORT = 8000
name = "Roman Kalsin"
con_serv(HOST, PORT, name)
