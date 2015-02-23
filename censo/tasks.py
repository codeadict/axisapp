import requests
import bs4
from celery import task


@task
def verificar_sri(cliente):
    """
    Verifica los datos del cliente en el SRi
    :param cliente:
    :return:
    """
    if cliente.tipo_id == cliente.RUC:
        params = {'accion': 'siguiente', 'ruc': cliente.identif, 'lineasPagina': ''}
        url = 'https://declaraciones.sri.gob.ec/facturacion-internet/consultas/publico/ruc-datos2.jspa'
        sri_page = requests.post(url, params)
        soup = bs4.BeautifulSoup(sri_page.text)

        data = soup.select('table.formulario tr td')

        if not data:
            return
        else:
            cliente.razon_social = data[0].text.strip(' \n\s')
            cliente.identif = data[2].text.strip(' \n\s')
            cliente.tipo_contribuyente = data[11].text.strip(' \n\s')
            cliente.lleva_contabilidad = True if data[13].text == 'SI' else False
            cliente.save()