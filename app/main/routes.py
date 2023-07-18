import logging
import os
from urllib.parse import urlparse

import httpx
from app import pages
from flask import current_app
from flask import make_response
from flask import render_template
from flask import request
from flask import Response
from flask import send_from_directory

from . import main

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@main.get("/")
def home_page():
    page_title = "Acceuil"
    return render_template("index.html", page_title=page_title)


@main.get("/contact/")
def contact_page():
    page_title = "Contatez-nous"
    return render_template("page/contact.html", page_title=page_title)


@main.get("/proprietes-disponibles/")
def houses_page():
    page_title = "Nos propriétés disponible"
    return render_template("page/house_list.html", page_title=page_title)


@main.route("/api/houses/")
def api():
    app = current_app._get_current_object()
    req_url = app.config.get("API_URL")

    try:
        with httpx.Client() as client:
            houses_response = client.get(req_url)
            print(houses_response)
            return houses_response.text
    except (httpx.RequestError, ValueError) as error:
        logger.debug(f"Error fetching houses data {error}")
        return "Error fetching houses data"


@main.get("/<path:path>/")
def page(path):
    page = pages.get_or_404(path)
    template = page.meta.get("template", "page/page.html")
    return render_template(template, page=page)


@main.get("/sitemap/")
@main.get("/sitemap.xml/")
def sitemap():
    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc

    static_urls = list()
    for rule in current_app.url_map.iter_rules():
        if (
            not str(rule).startswith("/contact/")
            and not str(rule).startswith("/favicon.png")
            and not str(rule).startswith("/sitemap/")
            and not str(rule).startswith("/sitemap.xml")
        ):
            if "GET" in rule.methods and len(rule.arguments) == 0:
                url = {
                    "loc": f"{host_base}{str(rule)}",
                    "changefreq": "weekly",
                    "priority": "0.9",
                }
                static_urls.append(url)

    xml_sitemap = render_template(
        "sitemap.xml", static_urls=static_urls, host_base=host_base
    )
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response


@main.get("/robots.txt/")
def noindex():
    def Disallow(string):
        return f"Disallow: {string}"

    r = Response(
        "User-Agent: *\n{0}\n".format("\n".join([Disallow("/contact/")])),
        status=200,
        mimetype="text/plain",
    )
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r


@main.get("/favicon.png")
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, "static"), "img/logo/favicon.png"
    )
