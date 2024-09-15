 from fastapi import FastAPI, Request

from fastapi.responses import HTMLResponse

from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates

from typing import List, Optional

from pydantic import BaseModel

import requests

from datetime import datetime

 

app = FastAPI()

 

# Montando a rota de arquivos estáticos

app.mount("/static", StaticFiles(directory="static"), name="static")

 

templates = Jinja2Templates(directory="templates")

 

# URLs da API

BASE_URL = http://127.0.0.1:8000

OPERADORES_URL = f"{BASE_URL}/operadores"

ATRACOES_PROGRAMADAS_URL = f"{BASE_URL}/atracoes_programadas"

NAVIOS_ATRACADOS_URL = f"{BASE_URL}/navios_atracados"

RESUMO_ATRACOES_URL = f"{BASE_URL}/resumo_atracoes"

NAVIOS_ESPERADOS_URL = f"{BASE_URL}/navios_esperados"

NAVIOS_FUNDEADOS_URL = f"{BASE_URL}/navios_fundeados"

 

def fetch_data(url):

    try:

        response = requests.get(url)

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:

        print(f"Erro ao buscar dados da URL {url}: {e}")

        return []

 

def formatar_tabela(navios):

    tabela = []

    for navio in navios:

        viagem = navio.get("viagem", "")

        codigo_imo = navio.get("imo", navio.get("codigo_imo", ""))

        nome_de_navio = navio.get("nomenavio", navio.get("navio", ""))

        data_chegada = (datetime.strptime(navio.get("data", ""), "%d/%m/%Y").strftime("%d%m%Y")

                        if navio.get("data") else "")

        hora_chegada = navio.get("hora", navio.get("periodo", "").split('/')[0].replace(":", "") + "00")

        tipo_de_escala = navio.get("manobra", navio.get("tipoviagem", ""))[:1].upper()

 

        linha = {

            "viagem": viagem,

            "navio": codigo_imo,

            "nome_de_navio": nome_de_navio,

            "data": data_chegada,

            "hora": hora_chegada,

            "tipo_de_escala": tipo_de_escala

        }

        tabela.append(linha)

    return tabela

 

@app.get("/", response_class=HTMLResponse)

async def read_root(request: Request):

    try:

        atracoes_programadas = fetch_data(ATRACOES_PROGRAMADAS_URL)

        navios_atracados = fetch_data(NAVIOS_ATRACADOS_URL)

        navios_esperados = fetch_data(NAVIOS_ESPERADOS_URL)

        navios_fundeados = fetch_data(NAVIOS_FUNDEADOS_URL)

 

        all_navios = atracoes_programadas + navios_atracados + navios_esperados + navios_fundeados

        tabela_formatada = formatar_tabela(all_navios)

 

        return templates.TemplateResponse("index.html", {"request": request, "tabela": tabela_formatada})

    except Exception as e:

        print(f"Erro ao processar a solicitação de navios: {e}")

        return HTMLResponse("Erro ao carregar navios", status_code=500)

 

class Operador(BaseModel):

    codigo: int

    nome: str

    data: str

    CNPJ: str

 

class AtracaoProgramada(BaseModel):

    data: str

    periodo: str

    eta: str

    local: str

    nomenavio: str

    imo: int

    mercadoria: str

    manobra: str

    viagem: str

    duv: int

    liberado: int

    pendente: int

 

class NavioAtracado(BaseModel):

    descricao_local: str

   nomenavio: str

    periodo1: Optional[str] = None

    periodo2: Optional[str] = None

    periodo3: Optional[str] = None

    periodo4: Optional[str] = None

    mercadoria: str

    descarga: int

    embarque: int

 

class ResumoAtracao(BaseModel):

    tipo: str

    quantidade: int

 

class NavioEsperado(BaseModel):

    navio: str

    nacionalidade: str

    comprimento_calado: str

    tipoviagem: str

    chegadaprevista: str

    numeroatracacao: Optional[str] = None

    agencia: str

    numeroviagem: str

    duv: int

    prioridade: str

    terminal: str

 

class NavioFundeado(BaseModel):

    navio: str

    nacionalidade: str

    compr_e_calado: str

    tipoviagem: str

    entrada: str

    numeroatracacao: str

    agencia: str

    oper_emb_desc: str

    mer_emb_desc: str

    ton_emm_desc: str

    numero_viagem: str

    prioridade: str

    terminal: str

   

class Jup(BaseModel):

    jup: str

    navio: str

    viagem: str

    tipo_viagem: str

    operador: str

   dt_hr_aviso_chegada: str

    dt_hr_autoriza: Optional[str] = None

    dt_hr_previsao_atraca: Optional[str] = None

    dt_hr_atraca_efetiva: Optional[str] = None

    possui_dt: str

 

class PainelMonitoramento(BaseModel):

    local: str

    viagem: str

    navio: str

    agente: str

    carga: str

    atracacao: str

    inicio_operacao: str

    operador: str

    manifestacao: int

    movimento: str

    status: str

    estimativa_fim_operacao: Optional[str] = None

 

operadores = [

    {"codigo": 1, "nome": "AUTORIDADE PORTUÁRIA DE SANTOS - APS", "data": "01/01/1900", "CNPJ": "44837524000107"},

    {"codigo": 50, "nome": "TERMARES - TERMINAIS MARÍTIMOS ESPECIALIZADOS LTDA", "data": "07/12/2028", "CNPJ": "53730495000170"},

    {"codigo": 54, "nome": "STOLTHAVEN SANTOS LTDA.", "data": "24/01/2029", "CNPJ": "51979359000193"},

    {"codigo": 104, "nome": "DEICMAR ARMAZENAGEM E DISTRIBUIÇÃO LTDA", "data": "04/03/2025", "CNPJ": "58188756000196"},

    {"codigo": 112, "nome": "COMPORTCE OPERADOR PORTUÁRIO CESARI LTDA.", "data": "20/03/2029", "CNPJ": "00288078000153"},

    {"codigo": 118, "nome": "MARIMEX DESPACHOS, TRANSPORTES E SERVIÇOS LTDA.", "data": "05/08/2029", "CNPJ": "45050663000159"},

    {"codigo": 133, "nome": "TRANSBRASA TRANSITÁRIA BRASILEIRA LTDA", "data": "15/08/2029", "CNPJ": "45557022000195"},

    {"codigo": 157, "nome": "SM - OPERADOR PORTUÁRIO LTDA.", "data": "06/03/2029", "CNPJ": "01505291000132"},

    {"codigo": 159, "nome": "CIA AUXILIAR DE ARMAZÉNS GERAIS", "data": "04/09/2028", "CNPJ": "61145488000300"},

    {"codigo": 178, "nome": "ULTRACARGO LOGÍSTICA S.A.", "data": "19/06/2029", "CNPJ": "14688220001136"},

    {"codigo": 194, "nome": "ECOPORTO SANTOS S.A.", "data": "21/12/2028", "CNPJ": "02390435000115"},

    {"codigo": 215, "nome": "RELIANCE AGENCIAMENTO E SERV. PORT. LTDA.", "data": "01/08/2028", "CNPJ": "03574813000183"},

    {"codigo": 239, "nome": "TERMINAL XXXIX DE SANTOS S/A.", "data": "15/11/2028", "CNPJ": "04244527000112"}

]

 

atracoes_programadas = [

    {"data": "13/09/2024", "periodo": "13:00/19:00", "eta": "06/09/2024", "local": "AL 4", "nomenavio": "CHEM SILICON", "imo": 9829681, "mercadoria": "OLEO VEGETAL", "manobra": "ATRACACAO", "viagem": "3994/2024", "duv": 394902024, "liberado": 1, "pendente": 0},

    {"data": "13/09/2024", "periodo": "13:00/19:00", "eta": "10/09/2024", "local": "19", "nomenavio": "CORINNA", "imo": 9593842, "mercadoria": "MILHO A GRANEL", "manobra": "ATRACACAO", "viagem": "4111/2024", "duv": 403682024, "liberado": 1, "pendente": 0},

    {"data": "13/09/2024", "periodo": "13:00/19:00", "eta": "10/08/2024", "local": "TIPLAN", "nomenavio": "MARIA S", "imo": 9642368, "mercadoria": "ACUCAR A GRANEL", "manobra": "ATRACACAO", "viagem": "3547/2024", "duv": 350242024, "liberado": 1, "pendente": 0}

]

 

navios_atracados = [

    {"descricao_local": "AGEO I", "nomenavio": "RAINBOW", "periodo1": None, "periodo2": None, "periodo3": None, "periodo4": None, "mercadoria": "GRAN.LIQUIDO NAO ESPECIF", "descarga": 33446, "embarque": 0},

    {"descricao_local": "ALAMOA I", "nomenavio": "PACIFIC ZIRCON", "periodo1": None, "periodo2": None, "periodo3": None, "periodo4": None, "mercadoria": "OLEO DIESEL", "descarga": 0, "embarque": 25000},

    {"descricao_local": "ALAMOA II", "nomenavio": "LUIGI LAGRANGE", "periodo1": None, "periodo2": None, "periodo3": None, "periodo4": None, "mercadoria": "GAS LIQUEFEITO", "descarga": 25000, "embarque": 0}

]

 

resumo_atracoes = [

    {"tipo": "CARGUEIRO COMUM", "quantidade": 7},

    {"tipo": "EMBARCACAO DE APOIO", "quantidade": 1},

    {"tipo": "GRANELEIRO", "quantidade": 24},

    {"tipo": "OCEANOGRAFICO", "quantidade": 2},

    {"tipo": "OUTROS", "quantidade": 1},

    {"tipo": "PESQUEIRO", "quantidade": 1},

    {"tipo": "PETROLEIRO", "quantidade": 8},

    {"tipo": "PORTA-CONTAINERS", "quantidade": 8},

    {"tipo": "TANQUE", "quantidade": 1}

]

 

navios_esperados = [

    {"navio": "DEFENSORA", "nacionalidade": "BRASILEIRA", "comprimento_calado": "129<br>6", "tipoviagem": "Cab", "chegadaprevista": "14/09/2024", "numeroatracacao": None, "agencia": "CODESP", "numeroviagem": "9010-0<br>2022", "duv": 0, "prioridade": "A", "terminal": "MORTONA-M.G.B."},

    {"navio": "GUAPORE", "nacionalidade": "BRASILEIRA", "comprimento_calado": "47<br>5", "tipoviagem": "Cab", "chegadaprevista": "14/09/2024", "numeroatracacao": None, "agencia": "CODESP", "numeroviagem": "9004-6<br>2024", "duv": 0, "prioridade": "A", "terminal": "27"}

]

 

navios_fundeados = [

    {"navio": "MSC LOS ANGELES", "nacionalidade": "LIBERIANA", "compr_e_calado": "276<br>10.1", "tipoviagem": "Long", "entrada": "13/06/2024 10:00:00", "numeroatracacao": "2555", "agencia": "MSC MEDITERRANEAN SHIPPING DO BRASIL LTDA.", "oper_emb_desc": "EMB<br>DESC", "mer_emb_desc": "CONTEINERES CHEIOS<br>CONTEINERES CHEIOS", "ton_emm_desc": "1800<br>18000", "numero_viagem": "2453-0<br>2024", "prioridade": "B", "terminal": "B.T.P. 1"},

    {"navio": "RIGI VENTURE<br><span style=\"color:green;font-weight:bold;\">PROGRAMADO</span>", "nacionalidade": "HONG KONG", "compr_e_calado": "200<br>13", "tipoviagem": "Long", "entrada": "03/08/2024 07:00:00", "numeroatracacao": "3336", "agencia": "WILLIAMS SERVICOS MARITIMOS LTDA.", "oper_emb_desc": "EMB<br>    ", "mer_emb_desc": "ACUCAR A GRANEL<br>", "ton_emm_desc": "59000<br>", "numero_viagem": "3549--<br>2024", "prioridade": "B", "terminal": "16/17"}

]

 

jup_data = [

    {"jup": "9400083", "navio": "MAIPO", "viagem": "3675 2024", "tipo_viagem": "", "operador": "EMBRAPORT - OPERADOR", "dt_hr_aviso_chegada": "11/09/2024 00:00", "possui_dt": "Nao"},

    # ... outros dados

]

 

painel_monitoramento_data = [

    {"local": "ALAMOA I", "viagem": "3337/2024", "navio": "LUIGI LAGRANGE", "agente": "CONE SUL AGENCIA DE NAVEGACAO S/C LTDA.", "carga": "G L P / B U N K E R", "atracacao": "10/08/24 14:45:00", "inicio_operacao": "10/08/24 22:54:00", "operador": "PETROBRAS TRANSPORTE S/A TRANSPETRO", "manifestacao": 25000, "movimento": "49,61%", "status": "AG DESATRACACAO", "estimativa_fim_operacao": "2024-08-11 19:54:00"},

    # ... outros dados

]

 

@app.get("/operadores", response_model=List[Operador])

def get_operadores():

    return operadores

 

@app.get("/atracoes_programadas", response_model=List[AtracaoProgramada])

def get_atracoes_programadas():

    return atracoes_programadas

 

@app.get("/navios_atracados", response_model=List[NavioAtracado])

def get_navios_atracados():

    return navios_atracados

 

@app.get("/resumo_atracoes", response_model=List[ResumoAtracao])

def get_resumo_atracoes():

    return resumo_atracoes

 

@app.get("/navios_esperados", response_model=List[NavioEsperado])

def get_navios_esperados():

    return navios_esperados

 

@app.get("/navios_fundeados", response_model=List[NavioFundeado])

def get_navios_fundeados():

    return navios_fundeados

 

@app.get("/jup", response_model=List[Jup])

def get_jup():

    return jup_data

 

@app.get("/painel_monitoramento", response_model=List[PainelMonitoramento])

def get_painel_monitoramento():

    return painel_monitoramento_data

 

if __name__ == '__main__':

    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8002)
