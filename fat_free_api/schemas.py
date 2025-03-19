from pydantic import BaseModel, Field


class InitialMessage(BaseModel):
    message: str


class InputFatFree(BaseModel):
    project: str
    E: int = Field(..., alias='E[N/m^2]')
    alfa_t: float = Field(..., alias='alfa_t[celsius^-1]')
    v_steel: float = Field(..., alias='v_steel')
    p_water: int = Field(..., alias='p_water[kg/m^3]')
    p_steel: int = Field(..., alias='p_steel[kg/m^3]')
    p_concrete: int = Field(..., alias='p_concrete[kg/m^3]')
    p_coating: int = Field(..., alias='p_coating[kg/m^3]')
    p_content: int = Field(..., alias='p_content[kg/m^3]')
    Ds: float = Field(..., alias='Ds[m]')
    t_steel: float = Field(..., alias='t_steel[m]')
    t_concrete: float = Field(..., alias='t_concrete[m]')
    t_coating: float = Field(..., alias='t_coating[m]')
    Heff: float = Field(..., alias='Heff[N]')
    pression: float = Field(..., alias='p[bar]')
    delta_t: float = Field(..., alias='delta_t[celsius]')
    length: float = Field(..., alias='L[m]')
    e: float = Field(..., alias='e[m]')
    kc: float = Field(..., alias='kc')
    fcn: float = Field(..., alias='fcn[Mpa]')
    user_defined_soil: bool = Field(..., alias='user_defined_soil')
    kv: float = Field(..., alias='kv')
    kl: float = Field(..., alias='kl')
    kvs: float = Field(..., alias='kvs')


class OutputFatFree(InputFatFree):
    diameter_outer : float = Field(..., alias='D[m]')

    lenght_per_diameter: float = Field(..., alias='L/Ds')

    frequency_inline: float = Field(..., alias='f1 in-line[Hz]')
    frequency_crossflow: float = Field(..., alias='f1 cr-flow[Hz]')
    amplitude_inline: float = Field(..., alias='A1 in-line[Mpa]')
    amplitude_crflow: float = Field(..., alias='A1 cr-flow[Mpa]')
    deflection_per_diameter_outer: float = Field(..., alias='deflection/diameter_outer')
    seff_per_pe: float = Field(..., alias='Seff/Pe')

    kv_calculated: float = Field(..., alias='kv[Mpa]')
    kl_calculated: float = Field(..., alias='kl[Mpa]')
    kvs_calculated: float = Field(..., alias='kvs[Mpa]')

    EI_steel: float = Field(..., alias='EI_steel')
    me: float = Field(..., alias='me')
    q: float = Field(..., alias='q')
    CSF: float = Field(..., alias='CSF')
    seff: float = Field(..., alias='Seff')
    ds_per_d: float = Field(..., alias='ds/d')

    area_intern: float = Field(..., alias='Ai[m^2]')
    area_steel_pipe: float = Field(..., alias='A_steel[m^2]')
    area_coating_pipe: float = Field(..., alias='A_coating[m^2]')
    area_concrete_pipe: float = Field(..., alias='A_concrete[m^2]')
    area_extern: float = Field(..., alias='Ae[m^2]')
