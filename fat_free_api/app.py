from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fat_free_api.fatfree import FatFree
from fat_free_api.schemas import InitialMessage, InputFatFree, OutputFatFree

app = FastAPI()

'''
@app.get('/', status_code=HTTPStatus.OK, response_model=InitialMessage)
def read_root():
    return {'message': 'Fat Free Simulation'}
'''

@app.get('/', status_code=HTTPStatus.OK)
def read_root(name: str = 'Guest'):
    return {'message': f'Hello, {name} ! Welcome to FastAPi'}


@app.post(
    '/calculate',
    status_code=HTTPStatus.CREATED,
    response_model=OutputFatFree,
)
def calculate_fatfree(user: InputFatFree):
    # Extraindo os valores do usuário
    user_data = user.model_dump(by_alias=True)

    # Instanciando a classe FatFree e calculando os resultados
    fatfree = FatFree(user_data)
    fatfree_output_dic = fatfree.calculate()

    # Criando o objeto de resposta
    
    result = OutputFatFree(
        **{'D[m]' : fatfree_output_dic['D'],
           'L/Ds' : fatfree_output_dic['L/Ds'],

           'f1 in-line[Hz]' : fatfree_output_dic['f1_inline'],
           'f1 cr-flow[Hz]' : fatfree_output_dic['f1_crflow'],
           'A1 in-line[Mpa]': fatfree_output_dic['A1_inline'],
           'A1 cr-flow[Mpa]': fatfree_output_dic['A1_crflow'],
           'deflection/diameter_outer' : fatfree_output_dic['delta/D'],
           'Seff/Pe' : fatfree_output_dic['Seff/Pe'],

           'kv[Mpa]' : fatfree_output_dic['Kv'],
           'kl[Mpa]' : fatfree_output_dic['Kl'],
           'kvs[Mpa]': fatfree_output_dic['Kvs'],
           
           'EI_steel[N.m^2]' : fatfree_output_dic['EI_steel'],
           'me[kg/m]' : fatfree_output_dic['me'],
           'q[N/m]' : fatfree_output_dic['q'],
           'CSF' : fatfree_output_dic['CSF'],
           'Seff[N]' : fatfree_output_dic['Seff'],
           'ds/d' : fatfree_output_dic['ds/d'],

           'Ai[m^2]' : fatfree_output_dic['Ai'],
           'A_steel[m^2]' : fatfree_output_dic['A_steel'],
           'A_coating[m^2]' : fatfree_output_dic['A_coating'],
           'A_concrete[m^2]' : fatfree_output_dic['A_concrete'],
           'Ae[m^2]' : fatfree_output_dic['Ae']
           },
        **user_data  # Passando os dados de entrada para o modelo
        )

    return result
