###### CODIGO DE MONTECARLO FUNCIONANDO PARA MC CASOS
##Llamado de modulos
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
# import bottleneck as bn
import scipy.stats as st
import matplotlib as mpl 
import matplotlib.pyplot as plt
import os 
from scipy.stats import truncnorm

##Llamado de parámetros
import parametros as p
import calculo as c
# import probando as c
from calculo import estado_carga_sem as ecsem
from calculo import estado_carga_fds as ecfds
from calculo import escenario_ve
from calculo import multiple
from calculo import distribucion_comunal
from calculo import informacion_ssee
from calculo import distribucion_ssee

##### VARIABLES DE INGRESO AL MODELO
os.system('cls')
print()
print()
# print("MODELACIÓN PARA PREVISION DE DEMANDA DE VEHICULOS ELÉCTRICOS")
print("Electric demand forecasting for electric vehicle fleet")
print()
print()
print("Total electric vehicle: ",int(p.total_autos))
# print("El universo de vehículos es ",int(p.total_autos))
print()

# x = int(input('Ingrese la penetracion de vehículos electricos (en %):')) 
x = int(input('Electric vehicle penetration (in %):'))   
# y = int(input('Ingrese el porcentaje con opcion de carga domiciliaria (en %):'))
y = int(input('Slow fast home charging percentage (in %):'))
# w = int(input('Ingrese cantidad de Monte Carlo (aprox. 30 seg x MC):'))
w = int(input('Monte Carlo Samples: '))
print()

### AÑO ASOCIADO A LA PENETRACION ESTUDIADA
año = np.array([2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035,2036,2037,2038,2039,2040,2041,2042,2043,2044,2045,2046])
penetracion = np.array([0.3,0.6,0.91,1.21,1.52,2.37,3.22,4.10,4.98,5.88,6.80,7.74,8.69,9.65,10.64,14.46,16.91,19.82,22.84,25.96,29.19,32.70,36.32,39.83,42.04,44.17,46.36,48.63,50.96,53.37,55.86])
given_value = x
absolute_difference_function = lambda penetracion : abs(penetracion - given_value)
closest_value = min(penetracion, key=absolute_difference_function)
result_año = np.where(penetracion == closest_value)

### INFORMACION DE SUBESTACIONES EXISTENTES
informacion_ssee()
print('Power Station from the study')
print(c.data_ssee)
print()

####INFORMACION TOTAL POR COMUNA:
print('Installe capacity per zone')
print(c.info_comunas[['Nombre','Potencia_Instalada','Comunas_Vecinas','Pot_Inst_Com_Vecinas']])

##### CÁLCULO PARA LOS ESCENARIOS DE SIMULACIÓN
E_t = []
E_ssee = []
E_comuna = []
E_perfil = []
# Para cada MonteCarlo
for z in range(w):
	forgot = np.random.normal(10, 2)
	print()
	print("Simulation", z+1)
	print()
	escenario_ve(forgot/100,x/100,y/100)
	b = np.array([c.esc_0,c.esc_1,c.esc_2,c.esc_3,c.esc_4, c.esc_5, c.esc_6, c.esc_7, c.esc_8, c.esc_9, c.esc_10, c.esc_11, c.esc_12, c.esc_13, c.esc_14, c.esc_15, c.esc_16, c.esc_17])
	suma_ve = np.sum(b)
	print("Total EV simulated:",int(suma_ve))
	chrg = np.array([1,1,1,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0])
	aux = 0
	multiplo_3 = []
	E_esc = []
	E_h = []
	E_f = []
	aux_2 = 1
	perfil_esc = []
	for cell in b:
		if multiple(aux_2,3):  ##(Escenarios multiplos de 3 = Conductores no regulares: 3,6,9,12,15,18)
			print("Scenario:",aux_2)
			print('Total VE:',int(cell))
			multiplo_3.append(1)
			ecsem(int(aux_2),chrg[aux],int(cell),multiplo_3[aux],p.SoC_inf[aux],p.SoC_sup[aux],p.Cap_mu[aux],p.Cap_sigma[aux],p.consumo_mu[aux],p.consumo_sigma[aux],p.salida_sem_mu[aux],p.salida_sem_sigma[aux],p.est_sem_1[aux],p.est_sem_2[aux])
			perfil_sem = []
			for i in c.perfil_minuto_sem:
				perfil_sem.append(round(i * 5/7,2))
			# print('perfil semana escalado')
			# print(perfil_sem)
			ecfds(int(aux_2),chrg[aux],int(cell),p.SoC_inf[aux],p.SoC_sup[aux],p.Cap_mu[aux],p.Cap_sigma[aux],p.consumo_mu[aux],p.consumo_sigma[aux],p.salida_fds_mu[aux],p.salida_fds_sigma[aux],p.est_fds_down[aux],p.est_fds_up[aux])
			perfil_fds = []
			for i in c.perfil_minuto_fds:
				perfil_fds.append(round(i * 2/7,2))
			# print('perfil fds escalado')
			# print(perfil_fds)
			##Perfil total
			perfil = [perfil_sem, perfil_fds]
			perfil = sum(map(np.array, perfil))
			print(perfil)
			perfil_esc.append(perfil)
			###### CENTROS DE CARGA RAPIDA
			vector_sem = c.E_total_sem
			vector_fds = c.E_total_fds
			E_fcs = 5/7*vector_sem + 2/7*vector_fds
			E_f.append(E_fcs)
			## print("Semana:",vector_sem)
			## print("Fin de semana:",vector_fds)
			## print("Total FCS:",E_fcs)
			###### CARGA DOMICILIARIA
			home_sem = c.E_dom_sem
			home_fds = c.E_dom_fds
			E_home = 5/7*home_sem + 2/7*home_fds
			E_h.append(E_home)
			## print("Total carga domiciliaria:",E_home)
			##TOTAL
			vector_tot = E_fcs + E_home
			E_esc.append(vector_tot)
			## print("Energía total parque vehícular:",vector_tot)
			## print()

		else:   ## (Escenarios distintos a multiplos 3. Conductores regulares)
			print("Scenario:",aux_2)
			print('Total EV:',int(cell))
			multiplo_3.append(0)
			ecsem(int(aux_2),chrg[aux],int(cell),multiplo_3[aux],p.SoC_inf[aux],p.SoC_sup[aux],p.Cap_mu[aux],p.Cap_sigma[aux],p.consumo_mu[aux],p.consumo_sigma[aux],p.salida_sem_mu[aux],p.salida_sem_sigma[aux],p.est_sem_1[aux],p.est_sem_2[aux])
			perfil_sem = []
			for i in c.perfil_minuto_sem:
				perfil_sem.append(round(i * 5/7,2))
			# print('perfil semana escalado')
			# print(perfil_sem)
			ecfds(int(aux_2),chrg[aux],int(cell),p.SoC_inf[aux],p.SoC_sup[aux],p.Cap_mu[aux],p.Cap_sigma[aux],p.consumo_mu[aux],p.consumo_sigma[aux],p.salida_fds_mu[aux],p.salida_fds_sigma[aux],p.est_fds_down[aux],p.est_fds_up[aux])
			perfil_fds = []
			for i in c.perfil_minuto_fds:
				perfil_fds.append(round(i * 2/7,2))
			# print('perfil fds escalado')
			# print(perfil_fds)
			##Perfil total
			perfil = [perfil_sem, perfil_fds]
			perfil = sum(map(np.array, perfil))
			print(perfil)
			perfil_esc.append(perfil)
			####### CENTROS DE CARGA RAPIDA
			vector_sem = c.E_total_sem
			vector_fds = c.E_total_fds
			E_fcs = 5/7*vector_sem + 2/7*vector_fds
			E_f.append(E_fcs)
			## print("Semana:",vector_sem)
			## print("Fin de semana:",vector_fds)
			## print("Total FCS:",E_fcs)
			####### CARGA DOMICILIARIA
			home_sem = c.E_dom_sem
			home_fds = c.E_dom_fds
			E_home = 5/7*home_sem + 2/7*home_fds
			E_h.append(E_home)
			# print("Total carga domiciliaria:",E_home)
			##TOTAL
			vector_tot = E_fcs + E_home
			E_esc.append(vector_tot)
			# print("Energía total parque vehícular:",vector_tot)
			# print()
		aux_2 = aux_2 + 1
		aux = aux + 1
	perfil_esc = sum(map(np.array, perfil_esc))
	print(perfil_esc)
	E_t.append(np.sum(E_esc))
	distribucion_comunal(np.sum(E_esc))
	###Resultados para cada MonteCarlo	
	## print("Cantidad de vehículos eléctricos por escenario")
	### Resultados para cada escenario separado por FCS y carga domiciliaria
	## for i in range(len(b)):
	## 	print('Escenario',i,':',int(b[i]),'VE. Energía consumia:',round(E_esc[i],2),' kWh')
		## print('La energia consumida por FCS:',round(E_f[i],2),' kWh')
		## print('La energia consumida por este Carga Domiciliaria:',round(E_h[i],2),' kWh')
	# print("La energía total de centros de carga rápida:",round(np.sum(E_f)/1000,3)," MWh")
	print("Total energy from fast charging station:",round(np.sum(E_f)/1000,3)," MWh")
	# print("La energía total del carga domiciliaria:",round(np.sum(E_h)/1000,2)," MWh")
	print("Total energy from slow home charging:",round(np.sum(E_h)/1000,2)," MWh")
	# print("La energía total del parque automotriz es:",round(np.sum(E_esc)/1000,3)," MWh")
	print("Total energy consumed by electric vehicles:",round(np.sum(E_esc)/1000,3)," MWh")
	print()
	E_comuna.append(c.distribucion_final)
	distribucion_ssee(c.info_comunas,c.data_ssee, c.energia_comunal)
	E_ssee.append(c.total_ssee)
	E_perfil.append(perfil_esc)


print()
print('Results for ',w,' samples:')
#### PERFIL DE DEMANDA PARA CADA MINUTO
minutos = [*range(0, 1441, 1)]
resultados_perfil = pd.DataFrame({'Minuto':minutos})
contador = 0
for cell in E_perfil:
	resultados_perfil[contador] = cell
	contador = contador + 1
MC_perfil = resultados_perfil.set_index('Minuto')
MC_perfil['mean [kWh]'] = round(MC_perfil.mean(axis=1),2) #Crea una columna con promedios de cada fila
MC_perfil['mean [kWh]'] = MC_perfil['mean [kWh]'].astype(float)
MC_perfil['std [kWh]'] = round(MC_perfil.std(axis=1),2)
MC_perfil['std [kWh]'] = MC_perfil['std [kWh]'].astype(float)
MC_perfil.to_csv('resultados_perfil.csv', decimal=",")
print(MC_perfil)

#### RESULTADOS DEMANDA COMUNAL
print()
print('El año al cual ocurre la penetración de',x,'% es el año:', str(año[result_año]))
resultados_comunal = pd.DataFrame({'Comuna':c.nom_comunas})
contador = 0
for cell in E_comuna:
	resultados_comunal[contador] = cell
	contador = contador + 1
MC_comunal = resultados_comunal.set_index('Comuna')
print('Demanda para las Comunas')
MC_comunal['mean [MWh]'] = round(MC_comunal.mean(axis=1),2) #Crea una columna con promedios de cada fila
MC_comunal['mean [MWh]'] = MC_comunal['mean [MWh]'].astype(float)
MC_comunal['std [MWh]'] = round(MC_comunal.std(axis=1),2)
MC_comunal['std [MWh]'] = MC_comunal['std [MWh]'].astype(float)
MC_comunal.to_csv('resultados_comunal.csv', decimal=",")
print(MC_comunal)

#### RESULTADOS DEMANDA SSEE
print()
resultados_ssee = pd.DataFrame({'SSEE': c.arreglo_ssee})
cont = 0
for cell in E_ssee:
	resultados_ssee[cont] = cell
	cont = cont + 1
# print(MC_ssee)
print('Demanda para las SSEE')
resultados_ssee['mean [MWh]'] = round(resultados_ssee.mean(axis=1),2) #Crea una columna con promedios de cada fila
resultados_ssee['mean [MWh]'] = resultados_ssee['mean [MWh]'].astype(float)
resultados_ssee['std [MWh]'] = round(resultados_ssee.std(axis=1),2)
resultados_ssee['std [MWh]'] = resultados_ssee['std [MWh]'].astype(float)
resultados_ssee.to_csv('resultados_ssee.csv')
# prev_demanda = pd.read_csv('C://Users//juanj//OneDrive//Desktop//Modelo_VE//Prevision_Demanda_2019_2039.csv')
prev_demanda = pd.read_csv('C://Users//juanj//OneDrive//Escritorio//Modelo_VE//Prevision_Demanda_2019_2039.csv')
año_prev = prev_demanda.loc[:,prev_demanda.columns.str.startswith(str(año[result_año][0]))]
aux_dem_prev= año_prev.values.tolist()
demanda_año_prev = []
for sublist in aux_dem_prev:
    demanda_año_prev.extend(sublist)
# print(demanda_año_prev)
resultados_ssee['Demanda_Prevista'] = demanda_año_prev
resultados_ssee['Factor_carga'] = resultados_ssee['mean [MWh]'] / resultados_ssee.Demanda_Prevista * 100
resultados_ssee['Factor_carga'] = resultados_ssee['Factor_carga'].astype(float)
MC_ssee = resultados_ssee.set_index('SSEE')
MC_ssee.to_csv('resultados_ssee.csv', decimal=",")
print(MC_ssee)

### GRAFICO
promedio_perfil = MC_perfil['mean [kWh]'].tolist()
desv_perfil = MC_perfil['std [kWh]'].tolist()
plt.bar(range(len(promedio_perfil)), promedio_perfil)
plt.xlim([0, 1441])
plt.xlabel('Minuto')
plt.ylabel('Potencia')
plt.title('Perfil')
plt.show()






