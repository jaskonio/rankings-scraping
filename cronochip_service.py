import re
from typing import List
import requests
from bs4 import BeautifulSoup
import pandas as pd

class CronoChipService():
    def getByDorsals(self, circuit_id:str, dorsals= List[str]):
        dts = []
        dorsal_not_found = []

        for dorsal in dorsals:
            data = self.getByDorsal(circuit_id, dorsal)
            if data is None:
                dorsal_not_found.append(dorsal)
                continue

            dts.append(data)
    
        result = []
        if len(dts) != 0:
            result = pd.concat(dts)
        else:
            result = None

        message_error = None
        if len(dorsal_not_found) != 0:
            message_error = f'No se ha encontrado datos para los dorsale: {str(dorsal_not_found)}'

        return result, message_error

    def getByDorsal(self, circuit_id:str, dorsal_id:str):
        print(f"getByDorsal. circuit_id: {circuit_id}. dorsal_id: {dorsal_id}")

        dorsal_id = dorsal_id.strip()
    
        url = "https://cronochip.com/inscripciones/clasificationsCircuits/findbydorsal"

        payload = f'data%5BDorsalFilter%5D%5Bdorsal%5D={dorsal_id}&data%5BDorsalFilter%5D%5Bcircuit_id%5D={circuit_id}&_method=POST'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        soup = BeautifulSoup(response.text, 'lxml')
        div_table = soup.find('div', {'id': 'result_table'})
        runner_name = div_table.find('h2', {'class': 'titulo_seccion'}).get_text().strip()
        regex = r'^(.*?)\s*\(dorsal:.*?\)$'
        runner_name = re.match(regex, runner_name)
        if runner_name:
            runner_name = runner_name.group(1)

        if runner_name == '':
            return None
    
        headers = []
        header_html = soup.find('thead')

        for th in header_html.find_all('th'):
            if 'class' in th.attrs and 'pruebas' in th['class']:
                pruebas_html = th.find_all('div', {'class': 'prueba'})
                for i in range(1, len(pruebas_html)+1):
                    headers.append(f'Prueba {i}')
            else:
                text = th.get_text()
                headers.append(text)

        rows = []
        tbody_html = soup.find('tbody')

        for tr in tbody_html.find_all('tr'):
            cells = tr.find_all(['td'])
            row = []
            for cell in cells:
                if 'class' in cell.attrs and 'pruebas' in cell['class']:
                    pruebas_html = cell.find_all('div', {'class': 'prueba'})
                    for prueba_html in pruebas_html:
                        row.append(prueba_html.get_text())
                else:
                    row.append(cell.get_text())
            rows.append(row)

        headers.append('Dorsal')
        [row.append(dorsal_id) for row in rows]

        headers.append('Nombre')
        [row.append(runner_name) for row in rows]

        df = pd.DataFrame(rows, columns=headers)
        return df