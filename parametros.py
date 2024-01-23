import numpy as np
import pandas as pd
import math as m
#PARÁMETROS DE SIMULACIÓN
##Funcion para definir el tiempo (base de minutos)
def conversor_tiempo(hora, minutos):
	tiempo = hora*60 + minutos
	return tiempo

def horario(tiempo):
	hour = tiempo/60
	minute = tiempo//60
	return	hour, minute

##Vehículos
total_autos= 1906209
# total_autos = 10000

##Distribución del parque vehicular
ve_pequenos = 0.43
ve_medianos = 0.32
ve_grandes = 0.25

#### Información del centro de carga rapida
potencia_CCR = 120
potencia_dom = 3
polos_CCR = 6
coef_red = 0.8

########################################################################################################################################
####Cantidad de tipos de viajeros
viajero_regular = 0.475
viajero_noregular = 1 - viajero_regular
viajero_regular_part = 0.3135
viajero_regular_full = 1 - viajero_regular_part

#############################################################################################
####distancias de viaje
#Viaje de ida: día de semana
dist_ida_sem_mu = 8.753
dist_ida_sem_sigma = 2.238
#Viaje de vuelta: dia de semana
dist_vuelta_sem_mu = 9.4
dist_vuelta_sem_sigma = 2.403
#Viaje de ida: fin de semana
dist_ida_fds_mu = 10.175
dist_ida_fds_sigma = 2.965
#Viaje de vuelta: fin de semana
dist_vuelta_fds_mu = 15.2
dist_vuelta_fds_sigma = 4.430

###############################################################################################
####velocidades promedio (distribucion normal)
v_mu = 19.827
v_sigma = 4.273

##########################################################################
####Capacidades de bateria de VE (distribucion normal)
#Vehiculos pequeños
c_peq_mu = 15
c_peq_sigma = 2.738
#Vehiculos medianos
c_med_mu = 25
c_med_sigma = 3.535
#Vehiculos grandes
c_grandes_mu = 35
c_grandes_sigma = 4.183
##RESUMEN
Cap_mu = np.array([c_peq_mu,c_peq_mu,c_peq_mu,c_peq_mu,c_peq_mu,c_peq_mu,
					c_med_mu,c_med_mu,c_med_mu,c_med_mu,c_med_mu,c_med_mu,
					c_grandes_mu,c_grandes_mu,c_grandes_mu,c_grandes_mu,c_grandes_mu,c_grandes_mu])
Cap_sigma = np.array([c_peq_sigma,c_peq_sigma,c_peq_sigma,c_peq_sigma,c_peq_sigma,c_peq_sigma,
					c_med_sigma,c_med_sigma,c_med_sigma,c_med_sigma,c_med_sigma,c_med_sigma,
					c_grandes_sigma,c_grandes_sigma,c_grandes_sigma,c_grandes_sigma,c_grandes_sigma,c_grandes_sigma])

#########################################################################
####Consumo de bateria de VE (distribución normal)
#Vehiculos pequeños
con_peq_mu = 0.1
con_peq_sigma = 0.03
#Vehiculos medianos
con_med_mu = 0.15
con_med_sigma = 0.03
#Vehiculos grandes
con_grandes_mu = 0.2
con_grandes_sigma = 0.03
##RESUMEN
consumo_mu = np.array([con_peq_mu,con_peq_mu,con_peq_mu,con_peq_mu,con_peq_mu,con_peq_mu,
					con_med_mu,con_med_mu,con_med_mu,con_med_mu,con_med_mu,con_med_mu,
					con_grandes_mu,con_grandes_mu,con_grandes_mu,con_grandes_mu,con_grandes_mu,con_grandes_mu])
consumo_sigma = np.array([con_peq_sigma,con_peq_sigma,con_peq_sigma,con_peq_sigma,con_peq_sigma,con_peq_sigma,
						con_med_sigma,con_med_sigma,con_med_sigma,con_med_sigma,con_med_sigma,con_med_sigma,
						con_grandes_sigma,con_grandes_sigma,con_grandes_sigma,con_grandes_sigma,con_grandes_sigma,con_grandes_sigma])

###################################################################################
####Tiempos de salida de vehiculos
##Viajero regular
#Dia dia de semana: promedio y desviación estandar
t_reg_semana_mu = conversor_tiempo(7,37)
t_reg_semana_sigma = conversor_tiempo(1,14)
#Fin de semana: promedio y desviación estandar:
t_reg_fds_mu = conversor_tiempo(7,45)
t_reg_fds_sigma = conversor_tiempo(1,24)
##Viajero no regular
#Dia de semana: promedio y desviación estandar
t_noreg_semana_mu = conversor_tiempo(14,12)
t_noreg_semana_sigma = conversor_tiempo(3,56)
 #Fin de semana: promedio y desviación estandar:
t_noreg_fds_mu = conversor_tiempo(14,35)
t_noreg_fds_sigma = conversor_tiempo(3,37)

#Matriz tiempos de salida SEMANA
salida_sem_mu = np.array([t_reg_semana_mu,t_reg_semana_mu,t_noreg_semana_mu,
							t_reg_semana_mu,t_reg_semana_mu,t_noreg_semana_mu,
							t_reg_semana_mu,t_reg_semana_mu,t_noreg_semana_mu,
							t_reg_semana_mu,t_reg_semana_mu,t_noreg_semana_mu,
							t_reg_semana_mu,t_reg_semana_mu,t_noreg_semana_mu,
							t_reg_semana_mu,t_reg_semana_mu,t_noreg_semana_mu])
salida_sem_sigma = np.array([t_reg_semana_sigma,t_reg_semana_sigma,t_noreg_semana_sigma,
							t_reg_semana_sigma,t_reg_semana_sigma,t_noreg_semana_sigma,
							t_reg_semana_sigma,t_reg_semana_sigma,t_noreg_semana_sigma,
							t_reg_semana_sigma,t_reg_semana_sigma,t_noreg_semana_sigma,
							t_reg_semana_sigma,t_reg_semana_sigma,t_noreg_semana_sigma,
							t_reg_semana_sigma,t_reg_semana_sigma,t_noreg_semana_sigma])
#Matriz tiempos de salida FIN DE SEMANA
salida_fds_mu = np.array([t_reg_fds_mu,t_reg_fds_mu,t_noreg_fds_mu,
						t_reg_fds_mu,t_reg_fds_mu,t_noreg_fds_mu,
						t_reg_fds_mu,t_reg_fds_mu,t_noreg_fds_mu,
						t_reg_fds_mu,t_reg_fds_mu,t_noreg_fds_mu,
						t_reg_fds_mu,t_reg_fds_mu,t_noreg_fds_mu,
						t_reg_fds_mu,t_reg_fds_mu,t_noreg_fds_mu])

salida_fds_sigma = np.array([t_reg_fds_sigma,t_reg_fds_sigma,t_noreg_fds_sigma,
							t_reg_fds_sigma,t_reg_fds_sigma,t_noreg_fds_sigma,
							t_reg_fds_sigma,t_reg_fds_sigma,t_noreg_fds_sigma,
							t_reg_fds_sigma,t_reg_fds_sigma,t_noreg_fds_sigma,
							t_reg_fds_sigma,t_reg_fds_sigma,t_noreg_fds_sigma,
							t_reg_fds_sigma,t_reg_fds_sigma,t_noreg_fds_sigma])

########################################################################################################################################
####Estados de carga de salida
##Limites de estado de carga (distribución uniforme)
SoC_recarga_down = 80
SoC_recarga_up = 100
##Limites de estado de carga (distribución uniforme)
SoC_sinrecarga_down = 30
SoC_sinrecarga_up = 80
##Estado de carga como array
SoC_inf = np.array([SoC_recarga_down,SoC_recarga_down,SoC_recarga_down,
					SoC_sinrecarga_down,SoC_sinrecarga_down,SoC_sinrecarga_down,
					SoC_recarga_down,SoC_recarga_down,SoC_recarga_down,
					SoC_sinrecarga_down,SoC_sinrecarga_down,SoC_sinrecarga_down
					,SoC_recarga_down,SoC_recarga_down,SoC_recarga_down,
					SoC_sinrecarga_down,SoC_sinrecarga_down,SoC_sinrecarga_down])
SoC_sup = np.array([SoC_recarga_up,SoC_recarga_up,SoC_recarga_up,
					SoC_sinrecarga_up,SoC_sinrecarga_up,SoC_sinrecarga_up,
					SoC_recarga_up,SoC_recarga_up,SoC_recarga_up,
					SoC_sinrecarga_up,SoC_sinrecarga_up,SoC_sinrecarga_up,
					SoC_recarga_up,SoC_recarga_up,SoC_recarga_up,
					SoC_sinrecarga_up,SoC_sinrecarga_up,SoC_sinrecarga_up])


########################################################################################################################################
##Estados de carga límite
#Estado de carga viaje de ida
SoC_salida_mu = 25
SoC_salida_sigma = 1.5

#Estado de carga viaje de vuelta
SoC_retorno_mu = 35
SoC_retorno_sigma = 2


########################################################################################################################################
####Tiempo de estacionamiento
##Día de semana
#Viajero regular full-time: promedio y desviación estandar
t_full_mu = conversor_tiempo(9,0)
t_full_sigma = conversor_tiempo(0,20)
#Viajero regular part-time: promedio y desviación estandar
t_part_mu = conversor_tiempo(5,0)
t_part_sigma = conversor_tiempo(0,15)
#Viajero no regular: límite inferior y superior distribución uniforme
t_noreg_down = conversor_tiempo(1,0)
t_noreg_up = conversor_tiempo(3,0)
##Fin de semana: limite inferiore y superior distribución uniforme
t_all_down = conversor_tiempo(1,0)
t_all_up = conversor_tiempo(5,0)

#Matriz tiempos de salida SEMANA
est_sem_1 = np.array([t_part_mu,t_full_mu,t_noreg_down,
					t_part_mu,t_full_mu,t_noreg_down,
					t_part_mu,t_full_mu,t_noreg_down,
					t_part_mu,t_full_mu,t_noreg_down,
					t_part_mu,t_full_mu,t_noreg_down,
					t_part_mu,t_full_mu,t_noreg_down])
est_sem_2 = np.array([t_part_sigma,t_full_sigma,t_noreg_up,
					t_part_sigma,t_full_sigma,t_noreg_up,
					t_part_sigma,t_full_sigma,t_noreg_up,
					t_part_sigma,t_full_sigma,t_noreg_up,
					t_part_sigma,t_full_sigma,t_noreg_up,
					t_part_sigma,t_full_sigma,t_noreg_up])
#Matriz tiempos de salida FIN DE SEMANA
est_fds_down = np.array([t_all_down,t_all_down,t_all_down,
						t_all_down,t_all_down,t_all_down,
						t_all_down,t_all_down,t_all_down,
						t_all_down,t_all_down,t_all_down,
						t_all_down,t_all_down,t_all_down,
						t_all_down,t_all_down,t_all_down])
est_fds_up = np.array([t_all_up,t_all_up,t_all_up,
						t_all_up,t_all_up,t_all_up,
						t_all_up,t_all_up,t_all_up,
						t_all_up,t_all_up,t_all_up,
						t_all_up,t_all_up,t_all_up,
						t_all_up,t_all_up,t_all_up])


##### DATOS DE ENTRADA AL MODELO LINEAL
### Estructura de datos comunales: 
cerrillos = np.array([35.7, 18.7/100, 20.2/100, 10633, #Socioeconomicas : edad promedio, % estudios universitarios, % trabajador independientes, ingreso promedio.
					48.188, 31.9/100, 3.3, #Hogar : Densidad poblacion, % casas pareadas, promedios residentes por hogar, 
					27/100, 33.1/100, 9.68, m.exp(0)]) #Transporte : % 1 auto x casa, % conductor para trabajo, HEV x 1000 autos, puntos de carga.
cerro_navia = np.array([36, 8.8/100, 20.2/100, 7225,
					119.5, 31.9/100, 3.4, 
					23/100, 33.1/100, 0.68, m.exp(0)]) 
conchali = np.array([37.3, 16.1/100, 20.2/100, 9617,
					114.28, 31.9/100, 3.3,
					23/100, 33.1/100, 0.68, m.exp(0)])
el_bosque = np.array([36, 13.6/100, 20.2/100, 9235,
					113.45, 31.9/100, 3.4,
					23/100, 33.1/100, 0.68, m.exp(0)])
estacion_central = np.array([36.6, 23.8/100, 20.2/100, 11693,
					102.44, 31.9/100, 3,
					25/100, 33.1/100, 0.68, m.exp(0)])
huechuraba = np.array([33.8, 30.8/100, 20.2/100, 12089,
					31.975, 31.9/100, 3.5,
					27/100, 33.1/100, 0.68, m.exp(3)])
independencia = np.array([35.5, 26.6/100, 20.2/100, 12443,
					136.27, 31.9/100, 2.8,
					26/100, 33.1/100, 0.68, m.exp(1)])
la_cisterna = np.array([37.7, 27.8/100, 20.2/100, 13772,
					90.307, 31.9/100, 3,
					25/100, 33.1/100, 0.68, m.exp(0)])
la_florida = np.array([37.1, 29.6/100, 20.2/100, 15227,
					51.807, 31.9/100, 3.2,
					27/100, 33.1/100, 0.68, m.exp(1)])
la_granja = np.array([36.6, 12.7/100, 20.2/100, 8557,
					115.54, 31.9/100, 3.4,
					24/100, 33.1/100, 0.68, m.exp(0)])
la_pintana = np.array([33.3, 7.3/100, 20.2/100, 6835,
					58.236, 31.9/100, 3.6,
					22/100, 33.1/100, 0.68, m.exp(0)])
la_reina = np.array([38.5, 52/100, 20.2/100, 28453,
					39.588, 31.9/100, 3.2,
					23/100, 33.1/100, 0.68, m.exp(1)])
las_condes = np.array([39.1, 62.4/100, 20.2/100, 32590,
					29.77, 31.9/100, 2.7,
					25/100, 33.1/100, 0.68, m.exp(7)])
lo_barnechea = np.array([33.4, 49/100, 20.2/100, 27861,
					1.034, 31.9/100, 3.8,
					21/100, 33.1/100, 0.68, m.exp(0)])
lo_espejo = np.array([36.3, 8.8/100, 20.2/100, 7432,
					119.87, 31.9/100, 3.6,
					24/100, 33.1/100, 0.68, m.exp(0)])
lo_prado = np.array([37.5, 14.3/100, 20.2/100, 9337,
					146.73, 31.9/100, 3.2,
					22/100, 33.1/100, 0.68, m.exp(0)])
macul = np.array([38.3, 33.4/100, 20.2/100, 15422,
				90.742, 31.9/100, 2.9,
				27/100, 33.1/100, 0.68, m.exp(1)])
maipu = np.array([35.5, 25.6/100, 20.2/100, 13896,
				37.887, 31.9/100, 3.3,
				27/100, 33.1/100, 0.68, m.exp(0)])
ñuñoa = np.array([39, 57.4/100, 20.2/100, 24257,
				123.53, 31.9/100, 2.5,
				28/100, 33.1/100, 0.68, m.exp(0)])
pedro_aguirre = np.array([38.3, 14.3/100, 20.2/100, 9408,
						115.54, 31.9/100, 3.4,
						25/100, 33.1/100, 0.68, m.exp(0)])
peñalolen = np.array([35.2, 25.2/100, 20.2/100, 13129,
					45.069, 31.9/100, 3.4,
					26/100, 33.1/100, 0.68, m.exp(0)])
providencia = np.array([39.7, 67.2/100, 20.2/100, 27946,
					98.731, 31.9/100, 2.2,
					27/100, 33.1/100, 0.68, m.exp(4)])
pudahuel = np.array([34.4, 19.9/100, 20.2/100, 9688,
					11.675, 31.9/100, 3.4,
					25/100, 33.1/100, 0.68, m.exp(2)])
puente_alto = np.array([33.7, 21.3/100, 20.2/100, 11329,
					64.395, 31.9/100, 3.4,
					25/100, 33.1/100, 0.68, m.exp(0)])
quilicura = np.array([32, 19.9/100, 20.2/100, 11438,
					36.707, 31.9/100, 3.5,
					26/100, 33.1/100, 0.68, m.exp(0)])
quinta_normal = np.array([37.1, 20.3/100, 20.2/100, 10160,
					93.119, 31.9/100, 3.1,
					24/100, 33.1/100, 0.68, m.exp(0)])
recoleta = np.array([36.6, 19.4/100, 20.2/100, 9841,
					100, 31.9/100, 3.1,
					26/100, 33.1/100, 0.68, m.exp(0)])
renca = np.array([34.3, 11.7/100, 20.2/100, 7921,
				61.944, 31.9/100, 3.4,
				25/100, 33.1/100, 0.68, m.exp(0)])
san_bernardo = np.array([33.4, 17/100, 20.2/100, 10201,
						19.709, 31.9/100, 3.5,
						24/100, 33.1/100, 0.68, m.exp(1)])
san_joaquin = np.array([38.2, 19/100, 20.2/100, 10108,
						95.042, 31.9/100, 3.1,
						25/100, 33.1/100, 0.68, m.exp(0)])
san_miguel = np.array([37.4, 42.7/100, 20.2/100, 17429,
					112.3, 31.9/100, 2.7,
					27/100, 33.1/100, 0.68, m.exp(0)])
san_ramon = np.array([37.2, 10.6/100, 20.2/100, 7747,
					132.08, 31.9/100, 3.4,
					23/100, 33.1/100, 0.68, m.exp(0)])
santiago = np.array([34.5, 46/100, 20.2/100, 15326,
					174.85, 31.9/100, 2.2,
					26/100, 33.1/100, 0.68, m.exp(4)])
vitacura = np.array([39.4, 64.7/100, 20.2/100, 36814,
					30.038, 31.9/100, 3,
					19/100, 33.1/100, 0.68, m.exp(4)])

#### COMUNAS VECINAS PARA CADA COMUNA DE SANTIAGO
vec_cerrillos = ['Estacion Central','Lo Espejo','Maipu','Pedro Aguirre Cerda']
vec_cerro_navia = ['Lo Prado','Pudahuel','Quinta Normal','Renca'] 
vec_conchali = ['Huechuraba','Independencia','Quilicura','Recoleta','Renca']
vec_el_bosque = ['La Cisterna','La Pintana','San Bernardo','San Ramon']
vec_estacion_central = ['Cerrillos','Lo Prado','Maipu','Pedro Aguirre Cerda','Pudahuel','Quinta Normal','Santiago']
vec_huechuraba = ['Conchali','Quilicura','Recoleta','Vitacura']
vec_independencia = ['Conchali','Recoleta','Renca','Santiago']
vec_la_cisterna = ['El Bosque','Lo Espejo','San Miguel','San Ramon']
vec_la_florida = ['La Granja','Macul','Peñalolen','Puente Alto','San Joaquin']
vec_la_granja = ['La Florida','La Pintana','San Joaquin','San Ramon']
vec_la_pintana = ['El Bosque','La Granja','Puente Alto','San Bernardo']
vec_la_reina = ['Las Condes','Ñuñoa','Peñalolen']
vec_las_condes = ['La Reina','Lo Barnechea','Peñalolen','Providencia','Vitacura']
vec_lo_barnechea = ['Las Condes','Vitacura']
vec_lo_espejo = ['Cerrillos','La Cisterna','Pedro Aguirre Cerda','San Bernardo']
vec_lo_prado = ['Cerro Navia','Estacion Central','Pudahuel','Quinta Normal']
vec_macul = ['La Florida','Ñuñoa','Peñalolen','San Joaquin']
vec_maipu = ['Cerrillos','Estacion Central','Pudahuel']
vec_ñuñoa = ['La Reina','Macul','Peñalolen','Providencia','San Joaquin','Santiago']
vec_pedro_aguirre = ['Cerrillos','Estacion Central','Lo Espejo','San Miguel','Santiago']
vec_peñalolen = ['La Florida','La Reina','Las Condes','Macul','Ñuñoa']
vec_providencia = ['Las Condes','Ñuñoa','Recoleta','Santiago','Vitacura']
vec_pudahuel = ['Cerro Navia','Estacion Central','Lo Prado','Maipu','Quilicura','Renca']
vec_puente_alto = ['La Florida','La Pintana']
vec_quilicura = ['Conchali','Huechuraba','Pudahuel','Renca']
vec_quinta_normal = ['Cerro Navia','Estacion Central','Lo Prado','Renca','Santiago']
vec_recoleta = ['Conchali','Huechuraba','Independencia','Providencia','Vitacura']
vec_renca = ['Cerro Navia','Conchali','Independencia','Pudahuel','Quilicura','Quinta Normal']
vec_san_bernardo = ['El Bosque','La Pintana','Lo Espejo']
vec_san_joaquin = ['La Florida','La Granja','Macul','Ñuñoa','San Miguel','Santiago']
vec_san_miguel = ['La Cisterna','Pedro Aguirre Cerda','San Joaquin','San Ramon','Santiago']
vec_san_ramon = ['El Bosque','La Cisterna','La Granja','San Miguel']
vec_santiago = ['Estacion Central','Independencia','Ñuñoa','Pedro Aguirre Cerda','Providencia','Quinta Normal','San Joaquin','San Miguel']
vec_vitacura = ['Huechuraba','Las Condes','Lo Barnechea','Providencia','Recoleta']

vecinos = np.array([vec_cerrillos, vec_cerro_navia, vec_conchali, vec_el_bosque, vec_estacion_central, vec_huechuraba, vec_independencia, vec_la_cisterna, vec_la_florida, vec_la_granja, vec_la_pintana, vec_la_reina, vec_las_condes, vec_lo_barnechea, vec_lo_espejo, vec_lo_prado, vec_macul, vec_maipu, vec_ñuñoa, vec_pedro_aguirre, vec_peñalolen, vec_providencia, vec_pudahuel, vec_puente_alto, vec_quilicura, vec_quinta_normal, vec_recoleta, vec_renca, vec_san_bernardo, vec_san_joaquin, vec_san_miguel, vec_san_ramon, vec_santiago, vec_vitacura])



###### PENETRACION DE VEHICULOS ELECTRICOS

año = np.array([2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035,2036,2037,2038,2039,2040,2041,2042,2043,2044,2045,2046])
penetracion = np.array([0.3,0.6,0.91,1.21,1.52,2.37,3.22,4.10,4.98,5.88,6.80,7.74,8.69,9.65,10.64,14.46,16.91,19.82,22.84,25.96,29.19,32.70,36.32,39.83,42.04,44.17,46.36,48.63,50.96,53.37,55.86])
