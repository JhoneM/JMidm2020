import requests
from datetime import datetime
from math import acos, cos, sin, radians


def get_ip_information1(ip):
    """
    Consulta de geolocalización de IPs
    """
    url = "https://api.ip2country.info/ip?" + str(ip)
    res = requests.get(url)
    return res


def get_ip_information2(iso3):
    """
    Consultar unformación de paises
    """
    url = "https://restcountries.eu/rest/v2/alpha/" + str(iso3)
    res = requests.get(url)
    return res


def get_AWS(ip):
    """
    Consultar si una IP pertenece a AWS:
    """
    url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    res = requests.get(url)
    flag = False
    if res.status_code == 200:
        prefixes = res.json()
        prefixes = prefixes["prefixes"]
        for ips in prefixes:
            pi_aws = ips["ip_prefix"].split("/")
            if pi_aws[0] == ip:
                if ips["service"] != "AMAZON":
                    break
                flag = True
                break
            else:
                continue
    return flag


def distancia_puntos(punto_1, punto_2):
    """
    Calcular distancia segun latitud y long obtenido de get_ip_information2
    """
    if punto_1 != punto_2:
        punto_1 = (radians(punto_1[0]), radians(punto_1[1]))
        punto_2 = (radians(punto_2[0]), radians(punto_2[1]))

        distancia = acos(
            sin(punto_1[0]) * sin(punto_2[0])
            + cos(punto_1[0])
            * cos(punto_2[0])
            * cos(punto_1[1] - punto_2[1])
        )

        dis = round((distancia * 6371.01), 2)
        return dis
    else:
        return 0.0


def get_now_format_date():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string
