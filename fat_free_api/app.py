from http import HTTPStatus

from fastapi import FastAPI

from fat_free_api.schemas import (
    InitialMessage,
    ResultAxialForce,
    VariablesAxialForce,
)

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=InitialMessage)
def read_root():
    return {'message': 'Fat Free Simulation'}


@app.post(
    '/effective_axial_force',
    status_code=HTTPStatus.CREATED,
    response_model=ResultAxialForce,
)
def calculate_axial_force(user: VariablesAxialForce):
    # Extraindo os valores do usuário
    user_data = user.model_dump()

    # Pegando variáveis individuais
    effective_lag_tension = user_data['effective_lag_tension']
    internal_pressure = user_data['internal_pressure']
    cross_sectional_area = user_data['cross_sectional_area']
    temperature_difference = user_data['temperature_difference']
    temperature_coefficient = user_data['temperature_coefficient']
    young_modulus = user_data['young_modulus']
    poisson_coefficient = user_data['poisson_coefficent']

    # Implementação do cálculo do esforço axial efetivo (exemplo)
    effective_axial_force = (
        effective_lag_tension
        - (internal_pressure * cross_sectional_area)
        * (1 - 2 * poisson_coefficient)
        - (temperature_difference * temperature_coefficient * young_modulus)
    )

    # Criando o objeto de resposta
    result = ResultAxialForce(
        effective_axial_force=effective_axial_force, **user_data
    )

    return result
