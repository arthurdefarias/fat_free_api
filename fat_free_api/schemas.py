from pydantic import BaseModel


class InitialMessage(BaseModel):
    message: str


class VariablesAxialForce(BaseModel):
    effective_lag_tension: float
    internal_pressure: float
    cross_sectional_area: float
    temperature_difference: float

    # Constants
    temperature_coefficient: float
    young_modulus: float
    poisson_coefficent: float


class ResultAxialForce(VariablesAxialForce):
    effective_axial_force: float
