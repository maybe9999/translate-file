"""
Python 3.12.3
Encoding: UTF-8
"""
# Windows: Before running the script, run "chcp 65001" in the console
# chcp 65001
# Set InputEncoding and OutputEncoding to UTF8
# https://learn.microsoft.com/en-us/answers/questions/213769/what-are-the-differences-between-chcp-65001-and-(c

import datetime, re
try:
    import easygui
except:
    pass
from os import makedirs
from random import randint
from googletrans import Translator #pip install googletrans==4.0.0rc1
from pathlib import Path


input_lang = "en"
output_lang = "es"
output_lang2 = "ES"

makedirs("translated", exist_ok=True)



# https://proxyscrape.com/free-proxy-list
# To avoid bans for too many queries
list_of_proxies = {
	                "0":['http','138.68.60.8:8080'],
					"1":['http','4.157.219.21:80'],
					"2":['http','172.191.74.198:8080'],
					"3":['http','35.92.233.193:80'],
					"4":['http','198.49.68.80:80'],
					"5":['http','129.10.76.179:80'],
					"6":['http','23.237.145.36:31288'],
					"7":['http','138.68.60.8:3128'],
					"8":['http','172.191.74.198:8080'],
					"9":['http','172.212.97.167:80'],
					"10":['http','12.176.231.147:80'],
					"11":['http','132.145.134.243:31288'],
					"12":['http','162.223.90.130:80'],
					"13":['http','142.93.202.130:3128'],
					"14":['http','132.145.134.243:31288'],
					"15":['http','138.68.60.8:8080'],
					"16":['http','23.247.136.245:80'],
					"17":['http','63.143.57.116:80'],
					"18":['http','165.232.129.150:80'],
					"19":['http','162.223.90.130:80'],
					"20":['http','144.126.216.57:80'],
					"21":['http','12.176.231.147:80'],
					}

latests_proxys = [0,0,0,0,0]

def get_random_num_of_proxy():
	global latests_proxys
	while True:
		temp_num = randint(0, len(list_of_proxies)-1)
		if  temp_num not in latests_proxys[-4:]: 
			latests_proxys.append(temp_num)
			return temp_num

def get_time():
	return str(datetime.datetime.now().strftime("%H:%M:%S"))

def create_debug(open_file_path = "", err = "", other_content=None):
	with open('-Errores_debug.txt', 'a', encoding='utf-8') as f:
		content=f"{get_time()}: {open_file_path}{"\n" + other_content if other_content else ""} \n{err}\n"
		f.write(content)

def recharge_construct(): #Translator construct
	global translator
	num_random = get_random_num_of_proxy()
	translator = Translator(
				user_agent = "Mozilla/5.0 (Android; Android 5.1.1; SAMSUNG SM-G9350L Build/LMY47X) AppleWebKit/603.19 (KHTML, like Gecko)  Chrome/54.0.1522.302 Mobile Safari/601.0",
				proxies = {
					list_of_proxies[str(num_random)][0]:list_of_proxies[str(num_random)][1]
					}
			)
	print("\nProxy actual: ", translator.client.proxies)
	create_debug(translator.client.proxies)


def translate_simple_text(text):
    if not text:
        print("Texto vacío o None detectado en la traducción")
        return ""
    try:
        tradd = translator.translate(text, dest=output_lang, src=input_lang).text or text   #googletrans
        return tradd
    except Exception as err:
        print("error en traducion",err)
        return text

def get_paths():
	eleccion = easygui.buttonbox("¿Qué deseas seleccionar?",  
							  msg="""Si desea traducir un archivo en 
			  						particular seleccione 'Archivo'.\n
							  		Si desea traducir múltiples archivos, 
			  						seleccione 'Carpeta' y luego elija
									la carpeta que contiene los archivos""", 
							  choices=["Archivo", "Carpeta"])
	if eleccion == "Archivo": 
		return [easygui.fileopenbox(title="Selecciona un archivo")]
	elif eleccion == "Carpeta":
		carpeta = easygui.diropenbox(title="Selecciona una carpeta")
		return [archivo.as_posix() for archivo in Path(carpeta).rglob("*.txt")]
	else:
		return [archivo.as_posix() for archivo in Path(".").rglob("*.txt")]
	
def get_paths_android():
    return [archivo.as_posix() for archivo in Path(".").rglob("*.txt")]

def read_content(file):
	with open(file, "r",encoding="utf-8") as arch:
	    return arch.read()

def save_content(path, content):
	try:
		with open(path, "a", encoding="utf-8") as arch:
			return arch.write(str(content))
	except Exception as err:
		print("error en guardado",err)


def dividir_texto(texto, longitud_maxima=4000):
    if not texto:
        return [""]
    
    # Lista para almacenar los segmentos
    segmentos = []
    
    # Mientras queden partes de texto para procesar
    while len(texto) > longitud_maxima:
        # Buscar el último espacio dentro de la longitud máxima
        punto_corte = texto.rfind('.', 0, longitud_maxima)
        
        if punto_corte == -1:  # Si no hay espacio, cortamos en longitud_maxima
            punto_corte = longitud_maxima
        
        # Añadir el segmento y actualizar el texto
        segmentos.append(texto[:punto_corte])
        texto = texto[punto_corte:].lstrip()  # Eliminar el espacio al principio del siguiente segmento

    # Añadir el resto del texto (el último segmento)
    if texto:
        segmentos.append(texto.strip())

    return segmentos

def get_save_and_open_path(path: str) -> tuple[Path, Path]:
	full_file_path = Path(path)
	directory_path = full_file_path.parent
	file_name  = full_file_path.name
	print("Path:", full_file_path)

	return ( full_file_path, directory_path / "translated" / file_name )


try:
    files_paths = get_paths() #PC
except:
    files_paths = get_paths_android() #Android

for file_path in files_paths:
	if file_path == None and len(files_paths) <= 1: 
		print("Ningún archivo seleccionado")
		break
	
	recharge_construct()

	open_file_path, save_file_path = get_save_and_open_path(file_path)
	
	content_origin = str(read_content(open_file_path))
	content_origin = content_origin.replace("© Copyright NovelFull.Com. All Rights Reserved.", "")
	content_origin = content_origin.replace("\t", " ")  # Elimina tabulaciones
	content_origin = re.sub(r' {2,}', ' ', content_origin)

	partes = dividir_texto(content_origin)
	
	for index in range(len(partes)):
		if index % 50 == 0: recharge_construct()

		text = partes[index]
		print(index," \\ ",len(partes), "  -  ", len(text) )
		translate_content = translate_simple_text(f"{str(text)}")
		save_content(save_file_path, translate_content)
	
