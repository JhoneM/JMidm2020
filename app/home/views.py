from flask import render_template, request, session, flash

from . import home
from ..conf.db import get_db, close_db
from ..auth.auth import login_required

from ..conf.functions import (
    get_ip_information1,
    get_ip_information2,
    get_AWS,
    distancia_puntos,
    get_now_format_date,
)

ARG_latlng = (-34.0, -64.0)


@home.route("/")
@login_required
def index():
    fecha = get_now_format_date()
    return render_template(
        "home/index.html", fecha=fecha, title="Bienvenido"
    )


@home.route("/busqueda", methods=["GET", "POST"])
@login_required
def busqueda():
    if request.method == "POST":
        values = {}
        ip = request.form["ip"]
        db, c = get_db()
        aws = get_AWS(ip)
        res = get_ip_information1(ip)
        error = None
        if res.status_code == 200:
            ctry = res.json()
            res_2 = get_ip_information2(ctry.get("countryCode3"))
            if res_2.status_code == 200:
                ctry_2 = res_2.json()
                coordenadas = ctry_2["latlng"]
                if coordenadas:
                    fech_act = get_now_format_date()
                    punto_2 = (coordenadas[0], coordenadas[1])
                    distancia_aprox = distancia_puntos(
                        ARG_latlng, punto_2
                    )
                    c.execute(
                        "SELECT count,id FROM historic where ip = %s",
                        (ip,),
                    )
                    value = c.fetchone()
                    if value is None:
                        c.execute(
                            "INSERT INTO historic (ip, country, distance, count) values (%s, %s, %s, %s)",
                            (
                                ip,
                                ctry.get("countryName"),
                                distancia_aprox,
                                1,
                            ),
                        )
                        db.commit()
                    else:
                        new_value = int(value["count"]) + 1
                        c.execute(
                            "UPDATE historic SET count = %s WHERE id = %s",
                            (
                                new_value,
                                value["id"],
                            ),
                        )
                        db.commit()

                    values = dict(
                        IP=ip,
                        Fecha=fech_act,
                        Pais=ctry.get("countryName"),
                        ISO=ctry.get("countryCode"),
                        Distancia=distancia_aprox,
                        AWS="Si" if aws else "No",
                    )

                    close_db()
                    return render_template(
                        "home/response_busqueda.html",
                        values=values,
                        title="Response",
                    )
        else:
            error = "Error en el request"
            flash(error)

    return render_template("home/busqueda.html", title="Busqueda")


@home.route("/historico")
@login_required
def historico():
    values = {}
    db, c = get_db()
    query = "SELECT * FROM historic"
    c.execute(query)
    values = c.fetchall()
    close_db()
    return render_template(
        "home/historico.html", values=values, title="Historico"
    )


@home.route("/consulta", methods=["GET", "POST"])
@login_required
def consulta():
    id_user = session["user_id"]
    flag = False
    invocaciones = 0
    max_d_values = False
    min_d_values = False
    query = "SELECT country FROM historic GROUP BY country"
    db, c = get_db()
    c.execute(query)
    values = c.fetchall()

    if request.method == "POST":
        max_d = True if request.form.get("max_distance") else False
        min_d = True if request.form.get("min_distance") else False
        prom_c = True if request.form.get("prom_country") else False
        country = (
            request.form["country"]
            if request.form.get("prom_country")
            else "None"
        )
        c.execute(
            "INSERT INTO log_tra (create_by, min_distance, max_distance, prom_country, country) values (%s, %s, %s, %s, %s)",
            (
                id_user,
                min_d,
                max_d,
                prom_c,
                country,
            ),
        )
        db.commit()

        if max_d:
            # La consulta se hace de esta manera por si hay dos o mas registros
            # con la misma distancia y la misma cantidad de consultas
            query_max_distance = """SELECT * FROM historic
            WHERE distance = (SELECT MAX(distance) FROM historic)
            AND count = (SELECT count from historic ORDER BY distance DESC, count DESC LIMIT 1) 
            ORDER BY distance DESC, count DESC"""
            c.execute(query_max_distance)
            max_d_values = c.fetchall()
            flag = True

        if min_d:
            # La consulta se hace de esta manera por si hay dos o mas registros
            # con la misma distancia y la misma cantidad de consultas
            query_min_distance = """SELECT * FROM historic
            WHERE distance = (SELECT MIN(distance) FROM historic)
            AND count = (SELECT count FROM historic ORDER BY distance ASC, count DESC LIMIT 1)
            ORDER BY distance ASC, count DESC"""
            c.execute(query_min_distance)
            min_d_values = c.fetchall()
            flag = True

        if prom_c:
            c.execute(
                (
                    "SELECT SUM(count) AS suma FROM historic WHERE country = %s"
                ),
                (country,),
            )
            sum_invo = c.fetchone()

            c.execute(
                (
                    "SELECT COUNT(id) as total FROM historic WHERE country = %s"
                ),
                (country,),
            )
            count_country = c.fetchone()

            if sum_invo and count_country:
                if count_country["total"] > 0:
                    invocaciones = (
                        sum_invo["suma"] / count_country["total"]
                    )
                    invocaciones = round(invocaciones, 2)
                    flag = True

        if flag:
            close_db()
            return render_template(
                "home/consulta_user.html",
                max_distance=max_d_values,
                min_distance=min_d_values,
                pais=country,
                invo=invocaciones,
            )

    return render_template(
        "home/consulta.html", values=values, title="Consultas"
    )


@home.route("/trazabilidad")
@login_required
def trazabilidad():
    values = {}
    db, c = get_db()
    query = "SELECT us.username, lg.* FROM log_tra lg JOIN user us ON lg.create_by = us.id"
    c.execute(query)
    values = c.fetchall()
    return render_template(
        "home/trazabilidad.html", values=values, title="Logs"
    )
