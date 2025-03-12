from components import FatFree

import os

import pandas as pd
import hvplot.pandas

import holoviews as hv
from holoviews import opts
hv.extension('bokeh')  # Ativa o backend para visualização

import json


input_list = []


file_path_v01 = 'jupyter_notebook\code\input\input_v01.json'
file_path_v02 = 'jupyter_notebook\code\input\input_v02.json'
file_path_v03 = 'jupyter_notebook\code\input\input_v03.json'

input_list.append(file_path_v01)
input_list.append(file_path_v02)
input_list.append(file_path_v03)

for file_path in input_list:

    with open(file_path, "r") as file:
        input_data = json.load(file)

    # Listas das variaveis
    t_concrete_list = []
    csf_list = []
    f_inline_list = []
    f_crossflow_list = []
    amplitude_inline_list = []
    amplitude_crossflow_list = []
    seff_per_pcr_list = []
    deflection_per_diameter_list = []

    # Dicionário das variáveis
    t_concrete_dic = {'kc_0': [] , 'kc': []}
    csf_dic = {'kc_0': [], 'kc': []}
    f_inline_dic = {'kc_0': [], 'kc': []}
    f_crossflow_dic = {'kc_0': [], 'kc': []}
    amplitude_inline_dic = {'kc_0': [], 'kc': []}
    amplitude_crossflow_dic = {'kc_0': [], 'kc': []}
    seff_per_pcr_dic = {'kc_0': [], 'kc': []}
    deflection_per_diameter_dic = {'kc_0': [], 'kc': []}
        
    for t in range(0,5):

        t_concrete = t/100
   
        input_data['t_concrete[m]'] = t_concrete
        
        kc_lim = input_data['kc']

        for kc in [0, kc_lim]:

            if kc == 0 :
                kc_str = 'kc_0'

            else:
                kc_str = 'kc'

            input_data['kc'] = kc

            fatfree = FatFree(input_data)

            (
                csf_result,
                f_inline_result,
                f_crossflow_result,
                amplitude,
                seff_per_pcr,
                deflection_per_diameter
            ) = fatfree.calculate()

            t_concrete_dic[kc_str].append(t_concrete)
            csf_dic[kc_str].append(csf_result)
            f_inline_dic[kc_str].append(f_inline_result)
            f_crossflow_dic[kc_str].append(f_crossflow_result)
            amplitude_inline_dic[kc_str].append(amplitude['inline'])
            amplitude_crossflow_dic[kc_str].append(amplitude['crossflow'])
            seff_per_pcr_dic[kc_str].append(seff_per_pcr)
            deflection_per_diameter_dic[kc_str].append(deflection_per_diameter)

    df = pd.DataFrame({
        't_concrete_kc0' : t_concrete_dic['kc_0'],
        't_concrete' : t_concrete_dic['kc'],
        
        'csf_kc0' : csf_dic['kc_0'],
        'csf' : csf_dic['kc'],
        
        'f_inline_kc0': f_inline_dic['kc_0'],
        'f_inline' : f_inline_dic['kc'],

        'f_crossflow_kc0' :f_crossflow_dic['kc_0'],
        'f_crossflow' :f_crossflow_dic['kc'],

        'amplitude_inline_kc0' : amplitude_inline_dic['kc_0'],
        'amplitude_inline' : amplitude_inline_dic['kc'],

        'amplitude_crossflow_kc0' : amplitude_crossflow_dic['kc_0'],
        'amplitude_crossflow' : amplitude_crossflow_dic['kc'],

        'seff/pcr_kc0' : seff_per_pcr_dic['kc_0'],
        'seff/pcr' : seff_per_pcr_dic['kc'],

        'deflection/diameter_kc0' : deflection_per_diameter_dic['kc_0'],
        'deflection/diameter' : deflection_per_diameter_dic['kc']
    })

    # Criar os gráficos
    plot_frequence = (
        hv.Curve(df, 't_concrete', 'f_inline_kc0', label='f_inline_kc0').opts(line_dash='dotted') * 
        hv.Curve(df, 't_concrete', 'f_crossflow_kc0', label='f_crossflow_kc0').opts(line_dash='dotted') * 
        hv.Curve(df, 't_concrete', 'f_inline', label='f_inline') * 
        hv.Curve(df, 't_concrete', 'f_crossflow', label='f_crossflow')
    ).opts(title="Frequência pela Espessura do Concreto", width=600, height=300)

    plot_csf = (
        hv.Curve(df, 't_concrete', 'csf_kc0', label='csf_kc0').opts(line_dash='dotted') * 
        hv.Curve(df, 't_concrete', 'csf', label='csf')
    ).opts(title="CSF pela Espessura do Concreto", width=600, height=300)

    plot_amplitude = (
        hv.Curve(df, 't_concrete', 'amplitude_inline_kc0', label='amplitude_inline_kc0').opts(line_dash='dotted') * 
        hv.Curve(df, 't_concrete', 'amplitude_crossflow_kc0', label='amplitude_crossflow_kc0').opts(line_dash='dotted') * 
        hv.Curve(df, 't_concrete', 'amplitude_inline', label='amplitude_inline') * 
        hv.Curve(df, 't_concrete', 'amplitude_crossflow', label='amplitude_crossflow')
    ).opts(title="Amplitude pela Espessura do Concreto", width=600, height=300)

    plot_seff_per_pcr = (
        hv.Curve(df, 't_concrete', 'seff/pcr_kc0', label='seff/pcr_kc0').opts(line_dash='dotted') * 
        hv.Curve(df, 't_concrete', 'seff/pcr', label='seff/pcr')
    ).opts(title="Carga Crítica de Flambagem pela Espessura do Concreto", width=600, height=300)

    plot_deflection_per_diameter = (
        hv.Curve(df, 't_concrete', 'deflection/diameter_kc0', label='deflection/diameter_kc0').opts(line_dash='dotted') * 
        hv.Curve(df, 't_concrete', 'deflection/diameter', label='deflection/diameter')
    ).opts(title="Deflexão/Diâmetro pela Espessura do Concreto", width=600, height=300)
    
    # Combinar os gráficos em um layout
    layout = hv.Layout([
    plot_csf, plot_frequence, plot_amplitude, plot_seff_per_pcr, plot_deflection_per_diameter
    ]).cols(1).opts(shared_axes=False)
    
    # Salvar como HTML e abrir no navegador
    name_html = input_data['Project'] + '_' + 'graficos.html'
    hv.save(layout, name_html)
    import webbrowser
    webbrowser.open(name_html)

    print('###################-END-##################')

                                                                                                              
