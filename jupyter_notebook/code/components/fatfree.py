import math

class FatFree:
    def __init__(self, data: dict):
        
        # Número pi
        self.pi_number = math.pi

        # Modulo de Elasticidade
        self.young_modulus_steel = data['E[N/m^2]']

        # Coeficiente de expansão térmica
        self.temperature_coefficient = data['alfa_t']

        # Coeficiente de Poisson
        self.poisson_coefficient_steel = data['v_steel:']

        # Constante Gravitacional
        self.gravity = 9.80665 # m/s²

        # Densidades
        self.specific_mass_water = data['p_water[kg/m^3]']
        self.specific_mass_steel = data['p_steel[kg/m^3]']
        self.specific_mass_concrete = data['p_concrete[kg/m^3]']
        self.specific_mass_coating = data['p_coating[kg/m^3]']
        self.specific_mass_content = data['p_content[kg/m^3]']

        # Espessura do aço
        self.steel_thickness = data['t_steel[m]'] # metros

        # Espessura do concreto
        self.concrete_thickness = data['t_concrete[m]'] # metros

        # Espessura do revestimento
        self.coating_thickness = data['t_coating[m]'] # metros

        # Diâmetro
        self.diameter = data['Ds[m]'] # metros

        # Diâmetro Interno
        self.diameter_intern = self.diameter - 2*self.steel_thickness
        self.area_intern = self.pi_number * ((self.diameter_intern/2) ** 2)

        # Diametro Externo
        self.diameter_outer = self.diameter  + 2*self.coating_thickness + 2*self.concrete_thickness
        self.area_outer = self.pi_number * ((self.diameter_outer/2) ** 2)

        # Carregamentos Funcionais
        self.heff = data['Heff[N]'] # Tensão Residual Efetiva

        # Pressão interna no duto
        self.pression_intern = data['p[bar]'] * (10 ** 5) # 1 bar = 10^5 Pa

        # Mudança de temperatura em relação à temperatura ambiente durante a instalação
        self.delta_t = data['delta_t'] # °C

        # Dados do Vão Livre
        self.length = data['L[m]']  # Comprimento da tubulação (em metros)
        self.e_gap = data['e[m]'] # Distância entre o duto e o leito marinho (gap)

        # Dados de Revestimento
        self.kc = data['kc']  # Fator de rigidez do concreto
        self.fcn = data['fcn']  # Resistência normalizada de compressão (MPa)

        # Escolha das propriedades do solo
        self.user_defined = data['user_defined_soil']
        self.kv = data['kv']
        self.kl = data['kl']
        self.kvs = data['kvs']

    def calculate(self):
        mass_effetive,coefficient_mass_added, area_steel_pipe, area_coating_pipe, area_concrete_pipe, diameter_outer_concrete, diameter_intern_concrete, mass_structure_pipe, mass_content, mass_water_displaced  = self.mass_effetive()

        ei_steel = self.stiffness_steel()

        csf = self.stiffness_concrete(ei_steel, diameter_outer_concrete,
                                            diameter_intern_concrete)

        seff = self.effective_axial_force()

        kv, kl, kvs, ds_per_d = self.stiffness_soil(self.user_defined, mass_structure_pipe,
                                                mass_content, mass_water_displaced)

        stiffness_soil = {'kv': kv, 'kl': kl, 'kvs': kvs}

        length_eff, pcr_dict, pcr = self.effetive_length(stiffness_soil, csf, ei_steel)

        length_eff_vertical_dynamic = length_eff['kv']
        length_eff_lateral_dynamic = length_eff['kl']
        length_eff_vertical_static = length_eff['kvs']
                                                                                                    
        deflection, q = self.deflection(mass_structure_pipe, mass_content, mass_water_displaced,
                                        seff, length_eff_vertical_static, ei_steel, csf, pcr)

        amplitude = self.amplitude(length_eff_vertical_dynamic, length_eff_lateral_dynamic, csf)
        amplitude_inline = max(amplitude['lateral'])
        amplitude_crossflow = max(amplitude['vertical'])
        amplitude_max = {'crossflow':amplitude_crossflow, 'inline' : amplitude_inline}

        f_inline, f_crossflow = self.frequency(mass_effetive, csf, ei_steel, length_eff_lateral_dynamic, length_eff_lateral_dynamic,
                pcr_dict['kl'], seff, deflection, length_eff_vertical_dynamic, pcr_dict['kv'])
        
        
        if self.kc != 0 :
            print('----------------MAIN----------------')
            print('STRUCTURAL MODELLING')
            print('coating data')
            print('kc : ' + str(self.kc))
            print('fcn : ' + str(self.fcn))
            #print('k[m] : ' + str())
            print('')

            print('Functional Loads')
            print('Heff: ' + str(self.heff))
            print('p[bar] : ' + str(self.pression_intern/(10 ** 5)))
            print('delta_T[ºC] : ' + str(self.delta_t))
            print('')

            print('Pipe Dimensions')
            print('Ds: ' + str(self.diameter))
            print('t_steel: ' + str(self.steel_thickness))
            print('t_concrete: ' + str(self.concrete_thickness))
            print('t_coating: ' + str(self.coating_thickness))
            print('')

            print('Constants')
            print('v: ' + str(self.poisson_coefficient_steel))
            print('alfa_exp_term: ' + str(self.temperature_coefficient))
            print('E(N/m²): ' + str(self.young_modulus_steel))
            print('')

            print('Densities: ')
            print('d_steel: ' + str(self.specific_mass_steel))
            print('d_concrete: ' + str(self.specific_mass_concrete))
            print('d_coating: ' + str(self.specific_mass_coating))
            print('d_cont: ' + str(self.specific_mass_content))
            print('')

            print('FREE SPAN SCENÁRIO')
            #print('h[m] : ' + str(Water_depth))
            print('L[m] : ' + str(self.length))
            print('e[m] : ' + str(self.e_gap))
            print('D[m] : ' + str(self.diameter_outer))
            print('L/Ds : ' + str(self.length/self.diameter))
            print('')

            print('RESPONSE DATA')
            print('f1 (in-line) : ' + str(f_inline))
            print('f1 (cr-flow) : ' + str(f_crossflow))
            print('A1 (in-line) : ' + str(max(amplitude['lateral'])))
            print('A1 (cr-flow) : ' + str(max(amplitude['vertical'])))
            print('delta/D : ' + str(deflection/self.diameter_outer))
            print('Seff/Pe : ' + str(seff / pcr))
            print('')

            print('SOIL PROPERTIES')
            print('Kv : ' + str(kv))
            print('Kl : ' + str(kl))
            print('Kv,s : ' + str(kvs))
            print('')

            print('------------------ABA------------------')
            print('STRUCTURAL MODELLING INTERMEDIATE RESULTS')
            print('Transfer Values')
            print('EI_steel : ' + str(ei_steel))
            print('me : ' + str(mass_effetive))
            print('q : ' + str(q))
            print('Seff : ' + str(seff))
            print('Ca : ' + str(coefficient_mass_added))
            print('CSF : ' + str(csf))
            print('ds/d : ' + str(ds_per_d))
            print('')

            print('Areas [m²]')
            print('Ai : ' + str(self.area_intern))
            print('A_steel : ' + str(area_steel_pipe))
            print('A_coating : ' + str(area_coating_pipe))
            print('A_concrete : ' + str(area_concrete_pipe))
            print('Ae : ' + str(self.area_outer))

        return csf, f_inline, f_crossflow, amplitude_max, seff/pcr, deflection/self.diameter_outer
            
    def mass_effetive(self):
        
        # Cálculo da massa da estrutura
        diameter_outer_steel = self.diameter
        diameter_intern_steel = self.diameter_intern
        area_steel_pipe = self.pi_number * (((diameter_outer_steel/2)**2) - ((diameter_intern_steel/2)**2))
        mass_steel_pipe =  self.specific_mass_steel * area_steel_pipe  # mass of the pipe

        diameter_outer_coating = diameter_outer_steel + 2*self.coating_thickness
        diameter_intern_coating = diameter_outer_steel 
        area_coating_pipe = self.pi_number * (((diameter_outer_coating/2)**2) - ((diameter_intern_coating/2)**2))
        mass_coating_pipe =  self.specific_mass_coating* area_coating_pipe  # mass of the pipe

        diameter_outer_concrete = self.diameter_outer
        diameter_intern_concrete = diameter_outer_coating
        area_concrete_pipe = self.pi_number * (((diameter_outer_concrete/2)**2) - ((diameter_intern_concrete/2)**2))
        mass_concrete_pipe =  self.specific_mass_concrete* area_concrete_pipe  # mass of the pipe

        mass_structure_pipe = mass_steel_pipe + mass_coating_pipe + mass_concrete_pipe

        area_water = self.pi_number * ((self.diameter_outer/2) ** 2)
        mass_water_displaced = self.specific_mass_water * area_water  #  mass of the displaced water

        area_content = self.pi_number * ((self.diameter_intern/2) ** 2)
        mass_content = self.specific_mass_content * area_content # mass of fluid

        # Cálculo do coeficiente
        if self.e_gap/self.diameter_outer < 0.8:
            coefficient_mass_added = 0.68 + (1.6/(1+5*(self.e_gap/self.diameter_outer)))

        else:
            coefficient_mass_added = 1

        # Calculo da massa adicionada
        mass_added = coefficient_mass_added * mass_water_displaced

        mass_effetive =  mass_structure_pipe + mass_added + mass_content

        return mass_effetive,coefficient_mass_added, area_steel_pipe, area_coating_pipe, area_concrete_pipe, diameter_outer_concrete, diameter_intern_concrete, mass_structure_pipe, mass_content, mass_water_displaced 
    
    def stiffness_steel(self):
        # Rigidez à flexão do aço (EI_steel), dada em N.m²
        moment_inertia_steel = (self.pi_number/4) * (((self.diameter/2) ** 4) - (((self.diameter/2) - self.steel_thickness)**4))
        ei_steel = moment_inertia_steel * self.young_modulus_steel

        return ei_steel
    
    def stiffness_concrete(self, stiffness_steel:float,
                                      diameter_outer_concrete:float, diameter_intern_concrete:float):
        
        # Módulo de Young do Concreto
        young_modulus_concrete = 10000 * (self.fcn ** 0.3) #N/mm²
        young_modulus_concrete = young_modulus_concrete * (10**6) #N/m²
        moment_inertia_concrete = (self.pi_number/4) * (((diameter_outer_concrete/2) ** 4) - ((diameter_intern_concrete/2)**4))
        ei_concrete =  moment_inertia_concrete * young_modulus_concrete

        # Contribuição da rigidez à flexão do concreto e revestimento expressa como porcentagem de EI aço
        csf = self.kc * ((ei_concrete/stiffness_steel) ** 0.75)

        return csf
    
    def effective_axial_force(self):
        # Tensão axial aplicada durante a instalação da tubulação (N)
        effective_lay_tension = self.heff

        # Diferença de pressão interna (assumida como zero neste caso)
        internal_pressure_diff = self.pression_intern

        # Diferença de temperatura entre a instalação e a operação (assumida como zero neste caso)
        temperature_diff = self.delta_t

        # **Cálculo da força axial efetiva**
        effective_axial_force = (effective_lay_tension -  # Tensão axial de instalação
                                internal_pressure_diff * self.area_intern *  # Termo da pressão interna
                                (1 - 2 * self.poisson_coefficient_steel) -  # Ajuste devido ao efeito de Poisson
                                self.area_outer * self.temperature_coefficient * temperature_diff)  # Termo da variação térmica

        return effective_axial_force

    def stiffness_soil(self, user, mass_structure_pipe, mass_content, mass_water_displaced):

        # Effetive Lenght
        ms = mass_structure_pipe + mass_content
        m = mass_water_displaced

        ds_per_d = ms/m

        if user == True:
            kvd = self.kv
            kld = self.kl
            kvs = self.kvs

        else:

            poisson_coefficient_soil = 0.45
            cv = 600000 # boundary condition coefficient (vertical dynamic stiffness)
            cl = 500000 # boundary condition coefficient (lateral dynamic stiffness)

            # Definição dos parâmetros de rigidez do solo para argila muito mole (Clay Very Soft)
            kvd = (cv/(1-poisson_coefficient_soil))*((2/3)*(ds_per_d) + 1/3)*math.sqrt(self.diameter_outer) # N/m/m - Rigidez dinâmica vertical do solo por unidade de comprimento
            kld = (cl*(1+poisson_coefficient_soil))*((2/3)*(ds_per_d) + 1/3)*math.sqrt(self.diameter_outer) # N/m/m - Rigidez dinâmica lateral do solo por unidade de comprimento
            kvs = 75000 # N/m/m - Rigidez estática vertical do solo por unidade de comprimento

        return kvd, kld, kvs, ds_per_d
    
    def effetive_length(self, k: dict, csf: int, stiffness: float):
        
        length_eff_dict = {}
        pcr_list = []
        pcr_dict = {}

        for key, k_value in k.items():

            # Cálculo do logaritmo do valor adimensional que influencia o comprimento efetivo
            value_log = k_value * (self.length ** 4) / ((1 + csf) * stiffness)

            beta = math.log10(value_log)  # Cálculo do logaritmo de base 10 do valor obtido

            # Cálculo da razão entre o comprimento efetivo e o comprimento total da tubulação
            ratio_length_eff = 4.73 / ((-0.066 * (beta ** 2)) + (1.02 * beta) + 0.63)

            # Cálculo do comprimento efetivo da tubulação
            length_eff = ratio_length_eff * self.length
            length_eff_dict[key] = length_eff

            # Coeficiente de condição de contorno
            c2 = 4

            # Cálculo da carga crítica de flambagem (Pcr)
            pcr = (1 + csf) * c2 * (self.pi_number ** 2) * stiffness / (length_eff ** 2)
            pcr_list.append(pcr)
            pcr_dict[key] = pcr 

        return length_eff_dict, pcr_dict, min(pcr_list)
    
    def deflection(self, mass_structure_pipe:float, mass_content: float,
                   mass_water_displaced: float, effective_axial_force: float,
                   length_eff_vertical_static: float, ei_steel:float, csf:float, pcr: float):

        # Coeficiente c6 de condição de contorno
        c6 = 1/384

        # Peso do tubo por unidade de comprimento
        pipe_structure_weight = (mass_structure_pipe + mass_content) * self.gravity

        # Cálculo do Empuxo
        empuxo = mass_water_displaced * self.gravity

        # Peso Submerso por Unidade de Comprimento
        q = pipe_structure_weight - empuxo

        # Solicitacao Axial Efetiva
        seff = effective_axial_force

        # Cálculo da Deflexão Estática
        deflection = c6 * ((q * (length_eff_vertical_static**4))/(ei_steel * (1 + csf))) * (1 / (1 + seff/pcr))

        return deflection, q
            
    def amplitude(self, length_eff_vertical_dynamic: float, length_eff_lateral_dynamic:float, csf:float):
        # Coeficiente C4 de condição de contorno

        length_eff_dic = {'vertical' : length_eff_vertical_dynamic, 'lateral' : length_eff_lateral_dynamic}

        amplitude_dic = {'vertical' : [], 'lateral': []}

        for key, length_eff in length_eff_dic.items():

            c4_midspan = 8.6
            c4_shouder = 14.1 * ((self.length/length_eff)**2)
            c4 = [c4_midspan, c4_shouder]

            if key == 'vertical':
                name_length_eff = 'Rigidez dinâmica vertical do solo'

            elif key == 'lateral':
                name_length_eff = 'Rigidez dinâmica lateral do solo'

            for c in c4:

                if c == c4_midspan:
                    name_c = 'midspan'

                else:
                    name_c = 'shouder'

                # Distância à linha neutra
                middle_line = (self.diameter_outer - 1*self.steel_thickness)/2

                # Cálculo seguindo a fórmulda do manual da fatfree
                amplitude_max = 2 * c * (1 + csf) * self.diameter * self.young_modulus_steel * middle_line / (length_eff ** 2)

                amplitude_dic[key].append(amplitude_max/1000000)

        return amplitude_dic

    def frequency(self, mass_effetive, csf, ei_steel, ength_eff_lateral_dynamic, length_eff_lateral_dynamic,
                   pcr_lateral_dynamic, seff, deflection, length_eff_vertical_dynamic, pcr_vertical_dynamic ):
        # Boundary condition coefficients
        c1_inline, c1_crossflow = 3.56, 3.56
        c3_inline, c3_crossflow = 0, 0.4

        # Massa efetiva
        me = mass_effetive

        # Cálculo das Frequências
        f_inline = c1_inline * math.sqrt(1 + csf) * math.sqrt(ei_steel/(me * (length_eff_lateral_dynamic ** 4)) * (1 + (seff/pcr_lateral_dynamic) + c3_inline * (deflection/self.diameter_outer) ** 2))
        f_crossflow = c1_crossflow * math.sqrt(1 + csf) * math.sqrt(ei_steel/(me * (length_eff_vertical_dynamic ** 4)) * (1 + (seff/pcr_vertical_dynamic) + c3_crossflow * (deflection/self.diameter_outer) ** 2))

        return f_inline, f_crossflow 