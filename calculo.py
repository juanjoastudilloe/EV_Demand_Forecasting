##Funcion para calcular si el numero es multiplo utilizando el modulo de la division
def multiple(valor, multiple):
	resto = valor % multiple
	if resto == 0:
		return True
	else:
		return False


##Funcion para truncar la distribución normal
from scipy.stats import truncnorm
def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

##DEFICINION DE ESCENARIO CONSIDERANCO PROBABILIDAD DE OLVIDO
def escenario_ve(forgot,penetracion_ve,carga_dom):
	import parametros1 as p
	import numpy as np
	global esc_0, esc_1, esc_2, esc_3, esc_4, esc_5, esc_6, esc_7, esc_8, esc_9, esc_10, esc_11, esc_12, esc_13, esc_14, esc_15, esc_16, esc_17
	global ve_c, ve_s, ve_con, ve_sin
	# print("La penetración de vehículos eléctricos corresponde a ",float(penetracion_ve)*100," %")
	
	# print("El porcentaje de usuarios con opción de carga domiciliaria es de ",float(carga_dom)*100," %")
	total_ve = round(penetracion_ve*p.total_autos,0)
	
	#Con opción de carga (con) o sin opcion de carga domiciliaria (sin). Además incluir prob. de personas que olvidan cargar en la casa
	forg = round(forgot,4)
	ve_c = total_ve*carga_dom
	ve_s = total_ve*(1-carga_dom)
	ve_con = round(ve_c*(1-forg),0)
	ve_sin = round(total_ve - ve_con,0)
	
	##Segun tipo de vehículo
	ve_peq_con = round(p.ve_pequenos*ve_con,0)
	ve_peq_sin = round(p.ve_pequenos*ve_sin,0)
	ve_med_con = round(p.ve_medianos*ve_con,0)
	ve_med_sin = round(p.ve_medianos*ve_sin,0)
	ve_gra_con = round(p.ve_grandes*ve_con,0)
	ve_gra_sin = round(p.ve_grandes*ve_sin,0)

	#Según categorización de viajero: Regular o no regular
	ve_peq_con_reg = round(ve_peq_con*p.viajero_regular,0)
	ve_peq_con_noreg = round(ve_peq_con*p.viajero_noregular,0)
	ve_peq_sin_reg = round(ve_peq_sin*p.viajero_regular,0)
	ve_peq_sin_noreg = round(ve_peq_sin*p.viajero_noregular,0)
	ve_med_con_reg = round(ve_med_con*p.viajero_regular,0)
	ve_med_con_noreg = round(ve_med_con*p.viajero_noregular,0)
	ve_med_sin_reg = round(ve_med_sin*p.viajero_regular,0)
	ve_med_sin_noreg = round(ve_med_sin*p.viajero_noregular,0)
	ve_gra_con_reg = round(ve_gra_con*p.viajero_regular,0)
	ve_gra_con_noreg = round(ve_gra_con*p.viajero_noregular,0)
	ve_gra_sin_reg = round(ve_gra_sin*p.viajero_regular,0)
	ve_gra_sin_noreg = round(ve_gra_sin*p.viajero_noregular,0)

	#Segun tipo de trabajador
	esc_0 = round(ve_peq_con_reg*p.viajero_regular_part,0)
	esc_1 = round(ve_peq_con_reg*p.viajero_regular_full,0)
	esc_2 = round(ve_peq_con_noreg,0)
	esc_3 = round(ve_peq_sin_reg*p.viajero_regular_part,0)
	esc_4 = round(ve_peq_sin_reg*p.viajero_regular_full,0)
	esc_5 = round(ve_peq_sin_noreg,0)
	esc_6 = round(ve_med_con_reg*p.viajero_regular_part,0)
	esc_7 = round(ve_med_con_reg*p.viajero_regular_full,0)
	esc_8 = round(ve_med_con_noreg,0)
	esc_9 = round(ve_med_sin_reg*p.viajero_regular_part,0)
	esc_10 = round(ve_med_sin_reg*p.viajero_regular_full,0)
	esc_11 = round(ve_med_sin_noreg,0)
	esc_12 = round(ve_gra_con_reg*p.viajero_regular_part,0)
	esc_13 = round(ve_gra_con_reg*p.viajero_regular_full,0)
	esc_14 = round(ve_gra_con_noreg,0)
	esc_15 = round(ve_gra_sin_reg*p.viajero_regular_part,0)
	esc_16 = round(ve_gra_sin_reg*p.viajero_regular_full,0)
	esc_17 = round(ve_gra_sin_noreg,0)
	
	print("Porcentaje de usuarios que olvidan cargar en su casa:",round(forg*100,2),"%")
	# print("VE_con:",ve_c,"VE_sin:",ve_s,"VE_con_forg:",ve_con,"VE_sin_forg:", ve_sin)

	return esc_0, esc_1, esc_2, esc_3, esc_4, esc_5, esc_6, esc_7, esc_8, esc_9, esc_10, esc_11, esc_12, esc_13, esc_14, esc_15, esc_16, esc_17   


#############################################
##FUNCION DE ESTADO DE CARGA DIA DE SEMANA

def estado_carga_sem(escenario,esc_dom,num_ve,multiplo_3,SoC_inf,SoC_sup,Cap_mu,Cap_sigma,consumo_mu,consumo_sigma,salida_mu,salida_sigma,est_1,est_2):
	import numpy as np
	import pandas as pd
	import parametros1 as p
	from scipy.stats import truncnorm
	global E_total_sem, E_dom_sem, ida_sem, vuelta_sem, viaje_sem, perfil_minuto_sem

	aux_escenario = escenario
	aux_dom = esc_dom
	num_veh = num_ve
	pot_charge = p.potencia_CCR
	pot_dom = p.potencia_dom
	### Variables
	#IDA
	SoC_inicial = [] #
	cap_bateria = [] #
	dist_rec_i = [] #
	cons_bat = [] #
	vel_ida = [] #
	t_out_home = [] #
	SoC_limite_ida = [] #
	SoC_work = []
	SoC_fcs = []
	E_fcs = []
	dist_fcs = []
	t_fcs = []
	t_recarga = []
	t_llegada_work = []
	SoC_salida_work = []
	carga_ida = []
	#Vuelta
	t_parking = [] #
	t_out_work = [] #
	dist_rec_v = [] #
	vel_vuelta = [] #
	SoC_limite_vuelta = [] #
	SoC_casa = []
	SoC_fcs2 = []
	dist_fcs2 = []
	t_fcs2 = []
	E_fcs2 = []
	t_recarga2 = []
	t_llegada_casa = []
	E_dom = []
	SoC_final = []
	E_home = []  
	carga_vuelta = []  
	carga_home = []  
	delta_home = []
	if (aux_escenario == 1 or aux_escenario == 2 or aux_escenario == 3 or aux_escenario == 4 or aux_escenario == 5 or aux_escenario == 6):
		Capacidad_bat = get_truncated_normal(mean=Cap_mu, sd=Cap_sigma, low=10, upp=20)   
	elif (aux_escenario == 7 or aux_escenario == 8 or aux_escenario == 9 or aux_escenario == 10 or aux_escenario == 11 or aux_escenario == 12):
		Capacidad_bat = get_truncated_normal(mean=Cap_mu, sd=Cap_sigma, low=20, upp=30)
	elif (aux_escenario == 13 or aux_escenario == 14 or aux_escenario == 15 or aux_escenario == 16 or aux_escenario == 17 or aux_escenario == 18):
		Capacidad_bat = get_truncated_normal(mean=Cap_mu, sd=Cap_sigma, low=30, upp=40)
	Consumo_bat = get_truncated_normal(mean=consumo_mu, sd=consumo_sigma, low=consumo_mu-consumo_sigma, upp=consumo_mu+consumo_sigma)
	tiempo_salida_casa = get_truncated_normal(mean=salida_mu, sd=salida_sigma, low=0, upp=1440)
	Distancia_ida = get_truncated_normal(mean=p.dist_ida_sem_mu, sd=p.dist_ida_sem_sigma, low=0, upp=p.dist_ida_sem_mu+4*p.dist_ida_sem_sigma)
	Distancia_vuelta = get_truncated_normal(mean=p.dist_vuelta_sem_mu, sd=p.dist_vuelta_sem_sigma, low=0, upp=p.dist_vuelta_sem_mu+4*p.dist_vuelta_sem_sigma)
	# Capacidad_bat = get_truncated_normal(mean=Cap_mu, sd=Cap_sigma, low=Cap_mu-2*Cap_sigma, upp=Cap_mu+2*Cap_sigma)   #*******
	velocidad = get_truncated_normal(mean=p.v_mu, sd=p.v_sigma, low=p.v_mu-4*p.v_sigma, upp=p.v_mu+4*p.v_sigma)   #*******
	# print("DIA DE SEMANA:") 
	## Iteración para cantidad de vehículos
	for i in range(num_veh):
		### Viaje de IDA
		SoC_i = np.random.uniform(SoC_inf,SoC_sup)
		SoC_inicial.append(SoC_i)
		Battery_cap = Capacidad_bat.rvs()
		cap_bateria.append(Battery_cap)
		D_rec_ida = Distancia_ida.rvs()
		dist_rec_i.append(D_rec_ida)
		C_bat = Consumo_bat.rvs()   #*******
		cons_bat.append(C_bat)
		vel_rec = velocidad.rvs()  #*******   ####SE PUEDE MEJORAR ESTA VARIABLE, MAYOR PRECISION
		vel_ida.append(vel_rec)
		t_salida_casa = tiempo_salida_casa.rvs()
		t_out_home.append(round(t_salida_casa,0))
		# Calculo estado de carga término de viaje
		SoC_lim_ida = np.random.normal(p.SoC_salida_mu,p.SoC_salida_sigma)
		SoC_limite_ida.append(SoC_lim_ida)
		SoC_work.append(SoC_i -D_rec_ida*C_bat*100/Battery_cap)
		aux = SoC_lim_ida > SoC_work[i]
		### Condicion en caso que estado carga inicial sea inferior al limite
		if SoC_i > SoC_lim_ida:
			if aux == True:  ### Viaje normal en caso de que SI necesite carga rapida
				fcs_aux = SoC_lim_ida*p.coef_red
				SoC_fcs.append(fcs_aux)
				dist_aux = (SoC_i - fcs_aux)*Battery_cap/(100*C_bat)
				dist_fcs.append(dist_aux)
				t_aux = t_salida_casa + 60*dist_aux/vel_rec
				t_fcs.append(round(t_aux,0))
				E_aux = (80 - fcs_aux)*Battery_cap/100
				E_fcs.append(E_aux)
				recarga_aux = 60*E_aux/pot_charge
				t_recarga.append(round(recarga_aux,0))
				llegada_aux = t_salida_casa + 60*(D_rec_ida+dist_aux)/vel_rec
				t_llegada_work.append(round(llegada_aux,0))
				carga_ida.append(pot_charge)
				SoC_salida_work.append(80)
			else:   ### Viaje normal en caso de que NO necesite carga rapida
				SoC_fcs.append(0)
				dist_fcs.append(0)
				t_fcs.append(0)
				E_fcs.append(0)
				t_recarga.append(0)
				llegada_aux = t_salida_casa + 60*D_rec_ida/vel_rec
				carga_ida.append(0)
				t_llegada_work.append(round(llegada_aux,0))
				SoC_salida_work.append(SoC_work[i])
		else:   ### En caso de que el estado de carga inicial sea menor que punto limite
			fcs_aux = SoC_i*p.coef_red
			SoC_fcs.append(fcs_aux)
			dist_aux = (SoC_i - fcs_aux)*Battery_cap/(100*C_bat)
			dist_fcs.append(dist_aux)
			t_aux = t_salida_casa + 60*(dist_aux/vel_rec)
			t_fcs.append(round(t_aux,0))
			E_aux = (80 - fcs_aux)*Battery_cap/100
			E_fcs.append(E_aux)
			recarga_aux = 60*E_aux/pot_charge
			t_recarga.append(recarga_aux)
			llegada_aux = t_salida_casa + 60*(D_rec_ida+dist_aux)/vel_rec
			carga_ida.append(pot_charge)
			t_llegada_work.append(round(llegada_aux,0))
			SoC_salida_work.append(80)
		### Tiempo de estacionado según escenario (varia para usuarios en la semana)
		if multiplo_3 == 0: ##Usuarios regulares
			t_estacionado = np.random.normal(est_1, est_2)
			t_parking.append(round(t_estacionado,0))
		else:
			t_estacionado = np.random.uniform(est_1, est_2)
			t_parking.append(round(t_estacionado,0))
		### Viaje de VUELTA
		t_salida = t_llegada_work[i] + t_estacionado
		t_out_work.append(round(t_salida,0))
		D_rec_vuelta = Distancia_vuelta.rvs()
		dist_rec_v.append(D_rec_vuelta)
		vel_rec_vuelta = velocidad.rvs()
		vel_vuelta.append(vel_rec_vuelta)
		SoC_lim_vuelta = np.random.normal(p.SoC_retorno_mu,p.SoC_retorno_sigma)
		SoC_limite_vuelta.append(SoC_lim_vuelta)
		SoC_casa.append(SoC_salida_work[i] - D_rec_vuelta*C_bat*100/Battery_cap)
		aux2 = SoC_lim_vuelta > SoC_casa[i]   ##Compara el estado de carga final con el limite
		aux3 = SoC_salida_work[i] > SoC_lim_vuelta
		if aux3 == True:   ### En caso de que el estado de carga a la salida del trabajo sea mayor que punto limite
			if aux2 == True:  ### en caso de que se necesite carga rapida en el viaje de retorno
				fcs_aux2 = SoC_lim_vuelta*p.coef_red
				SoC_fcs2.append(fcs_aux2)
				dist_aux2 = (SoC_salida_work[i] - fcs_aux2)*Battery_cap/(100*C_bat)
				dist_fcs2.append(dist_aux2)
				t_aux2 = t_salida + 60*dist_aux2/vel_rec_vuelta
				t_fcs2.append(round(t_aux2,0))
				E_aux2 = (80 - fcs_aux2)*Battery_cap/100
				E_fcs2.append(E_aux2)
				recarga_aux2 = E_aux2/pot_charge
				t_recarga2.append(recarga_aux2)
				llegada_aux2 = t_salida + 60*(D_rec_vuelta+dist_aux2)/vel_rec_vuelta
				t_llegada_casa.append(round(llegada_aux2,0))
				SoC_final.append(80)
				carga_vuelta.append(pot_charge)
				carga_home.append(0)
				delta_home.append(0)
				E_home.append(0)
			else:		## estado de carga con que llega al hogar sin la necesidad de carga rapida
				SoC_fcs2.append(0)
				dist_fcs2.append(0)
				t_fcs2.append(0)
				E_fcs2.append(0)
				t_recarga2.append(0)
				llegada_aux2 = t_salida + 60*D_rec_vuelta/vel_rec_vuelta 
				carga_vuelta.append(0)
				t_llegada_casa.append(round(llegada_aux2,0))
				SoC_final.append(SoC_casa[i])
				if aux_dom == 1:    ### Si es escenario CON opcion de carga domiliciaria
					if SoC_fcs[i] == 0:  ## Si no se cargo en ningun momento de su viaje, se carga en su hogar
						E_aux_dom = (100 - SoC_casa[i])*Battery_cap/100
						delta_home_aux = 60*E_aux_dom/pot_dom
						delta_home.append(round(delta_home_aux,0))
						carga_home.append(pot_dom)
						E_home.append(E_aux_dom)
					else:
						E_home.append(0)
						delta_home.append(0)
						carga_home.append(0)
				else:   ### SI es escenario SIN opcion de carga domiciliaria
					E_home.append(0)
					delta_home.append(0)
					carga_home.append(0)
		else:		### En caso de que el estado de carga a la salida del trabajo sea menor que punto limite	
			fcs_aux2 = SoC_salida_work[i]*p.coef_red
			SoC_fcs2.append(fcs_aux2)
			dist_aux2 = (SoC_salida_work[i] - fcs_aux2)*Battery_cap/(100*C_bat)
			dist_fcs2.append(dist_aux2)
			t_aux2 = t_salida + 60*dist_aux2/vel_rec_vuelta
			t_fcs2.append(round(t_aux2,0))
			E_aux2 = (80 - fcs_aux2)*Battery_cap/100
			E_fcs2.append(E_aux2)
			recarga_aux2 = 60*E_aux2/pot_charge
			t_recarga2.append(round(recarga_aux2,0))
			llegada_aux2 = t_salida + 60*(D_rec_vuelta+dist_aux2)/vel_rec_vuelta
			t_llegada_casa.append(round(llegada_aux2,0))
			SoC_final.append(80)
			carga_vuelta.append(pot_charge)
			delta_home.append(0)
			carga_home.append(0)
			E_home.append(0)

	E_total_ida = np.sum(E_fcs)
	E_total_vuelta = np.sum(E_fcs2)
	E_total_sem = E_total_ida + E_total_vuelta
	E_dom_sem = np.sum(E_home)
	# IDA
	ida_sem = pd.DataFrame({'SoC.i':SoC_inicial,'Bat.cap':cap_bateria,'Dist.rec': dist_rec_i,'Consum.Bat':cons_bat,'Vel':vel_ida,'T.salida.casa': t_out_home,'SoC.lim.ida': SoC_limite_ida,'SoC.wrk':SoC_work,'SoC.fcs':SoC_fcs,'E.fcs':E_fcs,'dist.fcs':dist_fcs,'t.fcs':t_fcs,'t.lleg.work':t_llegada_work,'SoC.salida.wrk':SoC_salida_work})
	# print("Viaje de ida")
	# print(fds_ida_sem)
	# VUELTA
	vuelta_sem = pd.DataFrame({'SoC.salida.wrk':SoC_salida_work,'Bat.cap':cap_bateria,'Dist.rec': dist_rec_v,'Consum.Bat':cons_bat,'Vel':vel_vuelta,'T.estacionado':t_parking,'T.salida.wrk': t_out_work,'SoC.lim.vuelta': SoC_limite_vuelta,'SoC.casa':SoC_casa,'SoC.fcs':SoC_fcs2,'E.fcs':E_fcs2,'dist.fcs':dist_fcs2,'t.fcs':t_fcs2,'t.lleg.casa':t_llegada_casa})
	# print("Viaje de vuelta")
	# print(fds_vuelta_sem)
	# TOTAL
	viaje_sem = pd.DataFrame({'t_fcs_ida':t_fcs,'E_fcs_ida':E_fcs,'delta_rec_ida':t_recarga,'carga_ida':carga_ida,'t_fcs_vuelta':t_fcs2,'E_fcs_vuelta':E_fcs2,'delta_rec_vuelta':t_recarga2,'carga_vuelta':carga_vuelta,'t_llegada_casa':t_llegada_casa,'E_casa':E_home,'delta_home':delta_home,'Pot_dom':carga_home})
	#  print("Viaje de ida y vuelta")
	# print(viaje_sem)
	# ida_sem.to_csv('viaje_ida.csv')
	# vuelta_sem.to_csv('viaje_vuelta.csv')
	viaje_sem.to_csv('viaje_sem.csv')	

	# Generación de perfil
	perfil = [[] for i in range(1441)] 

	for index,row in viaje_sem.iterrows():
		### FCS
		# IDA
		fcs_ida = viaje_sem.at[index,'E_fcs_ida']
		aux_ida = viaje_sem.at[index,'t_fcs_ida']
		aux_ida2 = viaje_sem.at[index,'delta_rec_ida']
		potencia_ida = viaje_sem.at[index,'carga_ida']
		min_inicio_ida = round(int(aux_ida),0)
		min_delta_ida = round(int(aux_ida2),0)
		min_termino_ida = int(min_inicio_ida + min_delta_ida)
		if (fcs_ida > 0 and min_termino_ida <= 1440 and min_inicio_ida <= 1440):
			for x in range(min_inicio_ida, min_termino_ida):
				y = potencia_ida
				perfil[x].append(y)
		elif (fcs_ida > 0 and min_termino_ida > 1440 and min_inicio_ida <= 1440):
			ciclo_ida = min_termino_ida - 1440
			y2 = potencia_ida
			for z in range(min_inicio_ida, 1440):
				perfil[z].append(y2)
			for z in range(0,ciclo_ida):
				perfil[z].append(y2)
		elif (fcs_ida > 0 and min_termino_ida > 1440 and min_inicio_ida > 1440):
			ciclo_ida_inicio = min_inicio_ida - 1440
			ciclo_ida_termino = min_termino_ida - 1440
			y3 = potencia_ida
			for z in range(ciclo_ida_inicio,ciclo_ida_termino):
				perfil[z].append(y3)
		# VUELTA
		fcs_vuelta = viaje_sem.at[index,'E_fcs_vuelta']
		aux_vuelta = viaje_sem.at[index,'t_fcs_vuelta']
		aux_vuelta2 = viaje_sem.at[index,'delta_rec_vuelta']
		potencia_vuelta = viaje_sem.at[index,'carga_vuelta']
		min_inicio_vuelta = round(int(aux_vuelta),0)
		min_delta_vuelta = round(int(aux_vuelta2),0)
		min_termino_vuelta = int(min_inicio_vuelta + min_delta_vuelta)
		if (fcs_vuelta > 0 and min_termino_vuelta <= 1440 and min_inicio_vuelta <= 1440):
			for z in range(min_inicio_vuelta, min_termino_vuelta):
				y4 = potencia_vuelta
				perfil[z].append(y4)
		elif (fcs_vuelta > 0 and min_termino_vuelta > 1440 and min_inicio_vuelta <= 1440):
			ciclo_vuelta = min_termino_vuelta - 1440
			y5 = potencia_vuelta
			for z in range(min_inicio_vuelta, 1440):
				perfil[z].append(y5)
			for z in range(0,ciclo_vuelta):
				perfil[z].append(y5)  
		elif (fcs_ida > 0 and min_termino_vuelta > 1440 and min_inicio_vuelta > 1440):
			ciclo_ida_inicio = min_inicio_vuelta - 1440
			ciclo_ida_termino = min_termino_vuelta - 1440
			y6 = potencia_ida
			for z in range(ciclo_ida_inicio,ciclo_ida_termino):
				perfil[z].append(y6)		
		### DOMICILIARIO
		if aux_dom == 1:
			carga_home = viaje_sem.at[index,'E_casa']
			aux_home = viaje_sem.at[index,'t_llegada_casa']
			aux_home2 = viaje_sem.at[index,'delta_home']
			potencia_home = viaje_sem.at[index,'Pot_dom']
			min_inicio_home = round(int(aux_home),0)
			min_delta_home = round(int(aux_home2),0)
			min_termino_home = round(int(min_inicio_home + min_delta_home),0)
			# prueba_max.append(min_termino_home)
			if (carga_home > 0 and min_termino_home <= 1440 and min_inicio_home <= 1440):
				for w in range(min_inicio_home, min_termino_home):
					y7 = potencia_home
					perfil[w].append(y7)
			elif (carga_home > 0 and min_termino_home > 1440 and min_inicio_home <= 1440):
				ciclo = min_termino_home - 1440
				y8 = potencia_home
				for z in range(min_inicio_home, 1440):
					perfil[z].append(y8)
				for z in range(0,ciclo):
					perfil[z].append(y8)   #######
			elif (carga_home > 0 and min_termino_home > 1440 and min_inicio_home > 1440):
				ciclo_home_inicio = min_inicio_home - 1440
				ciclo_home_termino = min_termino_home - 1440
				y9 = potencia_home
				for z in range(ciclo_home_inicio,ciclo_home_termino):
					perfil[z].append(y9)

	perfil_minuto_sem = list(map(sum, perfil))
	# print('perfil demanda dia semana')
	# print(perfil_minuto_sem)

	# panda_perfil = pd.DataFrame({'Demanda':perfil_minuto_sem})

	# return E_total_sem, E_dom_sem, ida_sem, vuelta_sem, viaje_sem
	return E_total_sem, E_dom_sem, ida_sem, vuelta_sem, viaje_sem, perfil_minuto_sem


#############################################
##FUNCION DE ESTADO DE CARGA LOS FINES DE SEMANA
def estado_carga_fds(escenario,esc_dom,num_ve,SoC_inf,SoC_sup,Cap_mu,Cap_sigma,consumo_mu,consumo_sigma,salida_mu,salida_sigma,est_down,est_up):
	import numpy as np
	import parametros1 as p
	import pandas as pd
	from scipy.stats import truncnorm
	global E_total_fds, E_dom_fds, ida_fds, vuelta_fds, perfil_minuto_fds
	
	aux_escenario_1 = escenario
	num_veh_1 = num_ve
	aux_dom_1 = esc_dom
	pot_charge_1 = p.potencia_CCR
	pot_dom_1 = p.potencia_dom
	### Variables
	#IDA
	SoC_inicial_1 = [] #
	cap_bateria_1 = [] #
	dist_rec_i_1 = [] #
	cons_bat_1 = [] #
	vel_ida_1 = [] #
	t_out_home_1 = [] #
	SoC_limite_ida_1 = [] #
	SoC_work_1 = []
	SoC_fcs_1 = []
	E_fcs_1 = []
	dist_fcs_1 = []
	t_fcs_1 = []
	t_recarga_1 = []
	t_llegada_work_1 = []
	SoC_salida_work_1 = []
	carga_ida_1 = []
	#Vuelta
	t_parking_1 = [] #
	t_out_work_1 = [] #
	dist_rec_v_1 = [] #
	vel_vuelta_1 = [] #
	SoC_limite_vuelta_1 = [] #
	SoC_casa_1 = []
	SoC_fcs2_1 = []
	dist_fcs2_1 = []
	t_fcs2_1 = []
	E_fcs2_1 = []
	t_recarga2_1 = []
	t_llegada_casa_1 = []
	E_dom_1 = []
	SoC_final_1 = []
	E_home_1 = []  
	carga_vuelta_1 = []  
	carga_home_1 = []  
	delta_home_1 = []
	if (aux_escenario_1 == 1 or aux_escenario_1 == 2 or aux_escenario_1 == 3 or aux_escenario_1 == 4 or aux_escenario_1 == 5 or aux_escenario_1 == 6):
		Capacidad_bat_1 = get_truncated_normal(mean=Cap_mu, sd=Cap_sigma, low=10, upp=20)   
	elif (aux_escenario_1 == 7 or aux_escenario_1 == 8 or aux_escenario_1 == 9 or aux_escenario_1 == 10 or aux_escenario_1 == 11 or aux_escenario_1 == 12):
		Capacidad_bat_1 = get_truncated_normal(mean=Cap_mu, sd=Cap_sigma, low=20, upp=30)
	elif (aux_escenario_1 == 13 or aux_escenario_1 == 14 or aux_escenario_1 == 15 or aux_escenario_1 == 16 or aux_escenario_1 == 17 or aux_escenario_1 == 18):
		Capacidad_bat_1 = get_truncated_normal(mean=Cap_mu, sd=Cap_sigma, low=30, upp=40)
	Consumo_bat_1 = get_truncated_normal(mean=consumo_mu, sd=consumo_sigma, low=consumo_mu-consumo_sigma, upp=consumo_mu+consumo_sigma)
	tiempo_salida_casa_1 = get_truncated_normal(mean=salida_mu, sd=salida_sigma, low=0, upp=1440)
	# Capacidad_bat_1 = get_truncated_normal(mean=Cap_mu, sd=Cap_sigma, low=Cap_mu-2*Cap_sigma, upp=Cap_mu+2*Cap_sigma)   #*******
	Distancia_ida_1 = get_truncated_normal(mean=p.dist_ida_fds_mu, sd=p.dist_ida_fds_sigma, low=0, upp=p.dist_ida_fds_mu+4*p.dist_ida_fds_sigma)
	Distancia_vuelta_1 = get_truncated_normal(mean=p.dist_vuelta_sem_mu, sd=p.dist_vuelta_sem_sigma, low=0, upp=p.dist_vuelta_sem_mu+4*p.dist_vuelta_sem_sigma)
	velocidad_1 = get_truncated_normal(mean=p.v_mu, sd=p.v_sigma, low=p.v_mu-4*p.v_sigma, upp=p.v_mu+4*p.v_sigma)   #*******
	# print("FIN DE SEMANA:")
	## Iteración para cantidad de vehículos
	for i in range(num_veh_1):
		### Viaje de IDA
		SoC_i_1 = np.random.uniform(SoC_inf,SoC_sup)
		SoC_inicial_1.append(SoC_i_1)
		Battery_cap_1 = Capacidad_bat_1.rvs()
		cap_bateria_1.append(Battery_cap_1)
		D_rec_ida_1 = Distancia_ida_1.rvs()
		dist_rec_i_1.append(D_rec_ida_1)
		C_bat_1 = Consumo_bat_1.rvs()
		cons_bat_1.append(C_bat_1)
		vel_rec_1 = velocidad_1.rvs()
		vel_ida_1.append(vel_rec_1)
		t_salida_casa_1 = tiempo_salida_casa_1.rvs()
		t_out_home_1.append(round(t_salida_casa_1,0))
		SoC_lim_ida_1 = np.random.normal(p.SoC_salida_mu,p.SoC_salida_sigma)
		SoC_limite_ida_1.append(SoC_lim_ida_1)
		SoC_work_1.append(SoC_i_1 -D_rec_ida_1*C_bat_1*100/Battery_cap_1)
		aux_1 = SoC_lim_ida_1 > SoC_work_1[i]
		if SoC_i_1 > SoC_lim_ida_1:
			if aux_1 == True:
				fcs_aux_1 = SoC_lim_ida_1*p.coef_red
				SoC_fcs_1.append(fcs_aux_1)
				dist_aux_1 = (SoC_i_1 - fcs_aux_1)*Battery_cap_1/(100*C_bat_1)
				dist_fcs_1.append(dist_aux_1)
				t_aux_1 = t_salida_casa_1 + 60*dist_aux_1/vel_rec_1
				t_fcs_1.append(round(t_aux_1,0))
				E_aux_1 = (80 - fcs_aux_1)*Battery_cap_1/100
				E_fcs_1.append(E_aux_1)
				recarga_aux_1 = E_aux_1/pot_charge_1
				t_recarga_1.append(round(recarga_aux_1,0))
				llegada_aux_1 = t_salida_casa_1 + 60*(D_rec_ida_1+dist_aux_1)/vel_rec_1
				t_llegada_work_1.append(round(llegada_aux_1,0))
				carga_ida_1.append(pot_charge_1)
				SoC_salida_work_1.append(80)
			else:
				SoC_fcs_1.append(0)
				dist_fcs_1.append(0)
				t_fcs_1.append(0)
				E_fcs_1.append(0)
				t_recarga_1.append(0)
				carga_ida_1.append(0)
				llegada_aux_1 = t_salida_casa_1 + D_rec_ida_1/vel_rec_1
				t_llegada_work_1.append(round(llegada_aux_1,0))
				SoC_salida_work_1.append(SoC_work_1[i])
		else:
			fcs_aux_1 = SoC_i_1*p.coef_red
			SoC_fcs_1.append(fcs_aux_1)
			dist_aux_1 = (SoC_i_1 - fcs_aux_1)*Battery_cap_1/(100*C_bat_1)
			dist_fcs_1.append(dist_aux_1)
			t_aux_1 = t_salida_casa_1 + 60*(dist_aux_1/vel_rec_1)
			t_fcs_1.append(round(t_aux_1,0))
			E_aux_1 = (80 - fcs_aux_1)*Battery_cap_1/100
			E_fcs_1.append(E_aux_1)
			recarga_aux_1 = 60*E_aux_1/pot_charge_1
			t_recarga_1.append(round(recarga_aux_1,0))
			carga_ida_1.append(pot_charge_1)
			llegada_aux_1 = t_salida_casa_1 + 60*(D_rec_ida_1+dist_aux_1)/vel_rec_1
			t_llegada_work_1.append(round(llegada_aux_1,0))
			SoC_salida_work_1.append(80)

		t_estacionado_1 = np.random.uniform(est_down, est_up)
		t_parking_1.append(round(t_estacionado_1,0))
		### Viaje de VUELTA
		t_salida_1 = t_llegada_work_1[i] + t_estacionado_1
		t_out_work_1.append(round(t_salida_1,0))
		D_rec_vuelta_1 = Distancia_vuelta_1.rvs()
		dist_rec_v_1.append(D_rec_vuelta_1)
		vel_rec_vuelta_1 = velocidad_1.rvs()
		vel_vuelta_1.append(vel_rec_vuelta_1)
		SoC_lim_vuelta_1 = np.random.normal(p.SoC_retorno_mu,p.SoC_retorno_sigma)
		SoC_limite_vuelta_1.append(SoC_lim_vuelta_1)
		SoC_casa_1.append(SoC_salida_work_1[i] - D_rec_vuelta_1*C_bat_1*100/Battery_cap_1)
		aux2_1 = SoC_lim_vuelta_1 > SoC_casa_1[i]
		aux3_1 = SoC_salida_work_1[i] > SoC_lim_vuelta_1
		if aux3_1 == True:
			if aux2_1 == True:
				fcs_aux2_1 = SoC_lim_vuelta_1*p.coef_red
				SoC_fcs2_1.append(fcs_aux2_1)
				dist_aux2_1 = (SoC_salida_work_1[i] - fcs_aux2_1)*Battery_cap_1/(100*C_bat_1)
				dist_fcs2_1.append(dist_aux2_1)
				t_aux2_1 = t_salida_1 + 60*dist_aux2_1/vel_rec_vuelta_1
				t_fcs2_1.append(round(t_aux2_1,0))
				E_aux2_1 = (80 - fcs_aux2_1)*Battery_cap_1/100
				E_fcs2_1.append(E_aux2_1)
				recarga_aux2_1 = E_aux2_1/pot_charge_1
				t_recarga2_1.append(round(recarga_aux2_1,0))
				llegada_aux2_1 = t_salida_1 + 60*(D_rec_vuelta_1+dist_aux2_1)/vel_rec_vuelta_1
				t_llegada_casa_1.append(round(llegada_aux2_1,0))
				SoC_final_1.append(80)
				carga_vuelta_1.append(pot_charge_1)
				carga_home_1.append(0)
				delta_home_1.append(0)
				E_home_1.append(0)
			else:
				SoC_fcs2_1.append(0)
				dist_fcs2_1.append(0)
				t_fcs2_1.append(0)
				E_fcs2_1.append(0)
				t_recarga2_1.append(0)
				llegada_aux2_1 = t_salida_1 + 60*D_rec_vuelta_1/vel_rec_vuelta_1 
				carga_vuelta_1.append(0)
				t_llegada_casa_1.append(round(llegada_aux2_1,0))
				SoC_final_1.append(SoC_casa_1[i])
				if aux_dom_1 == 1:
					if SoC_fcs_1[i] == 0:
						E_aux_dom_1 = (100 - SoC_casa_1[i])*Battery_cap_1/100
						delta_home_aux_1 = 60*E_aux_dom_1/pot_dom_1
						delta_home_1.append(round(delta_home_aux_1,0))
						carga_home_1.append(pot_dom_1)
						E_home_1.append(E_aux_dom_1)
					else:
						E_home_1.append(0)
						delta_home_1.append(0)
						carga_home_1.append(0)
				else:
					E_home_1.append(0)
					delta_home_1.append(0)
					carga_home_1.append(0)
		else:	
			fcs_aux2_1 = SoC_salida_work_1[i]*p.coef_red
			SoC_fcs2_1.append(fcs_aux2_1)
			dist_aux2_1 = (SoC_salida_work_1[i] - fcs_aux2_1)*Battery_cap_1/(100*C_bat_1)
			dist_fcs2_1.append(dist_aux2_1)
			t_aux2_1 = t_salida_1 + 60*dist_aux2_1/vel_rec_vuelta_1
			t_fcs2_1.append(round(t_aux2_1,0))
			E_aux2_1 = (80 - fcs_aux2_1)*Battery_cap_1/100
			E_fcs2_1.append(E_aux2_1)
			recarga_aux2_1 = 60*E_aux2_1/pot_charge_1
			t_recarga2_1.append(round(recarga_aux2_1,0))
			llegada_aux2_1 = t_salida_1 + 60*(D_rec_vuelta_1+dist_aux2_1)/vel_rec_vuelta_1
			t_llegada_casa_1.append(round(llegada_aux2_1,0))
			SoC_final_1.append(80)
			carga_vuelta_1.append(pot_charge_1)
			delta_home_1.append(0)
			carga_home_1.append(0)
			E_home_1.append(0)

	E_total_ida_1 = np.sum(E_fcs_1)
	E_total_vuelta_1 = np.sum(E_fcs2_1)
	E_total_fds = E_total_ida_1 + E_total_vuelta_1
	E_dom_fds = np.sum(E_home_1)
	
	#IDA
	ida_fds = pd.DataFrame({'SoC.i':SoC_inicial_1,'Bat.cap':cap_bateria_1,'Dist.rec': dist_rec_i_1,'Consum.Bat':cons_bat_1,'Vel':vel_ida_1,'T.salida.casa': t_out_home_1,'SoC.lim.ida': SoC_limite_ida_1,'SoC.wrk':SoC_work_1,'SoC.fcs':SoC_fcs_1,'E.fcs':E_fcs_1,'dist.fcs':dist_fcs_1,'t.fcs':t_fcs_1,'t.lleg.work':t_llegada_work_1,'SoC.salida.wrk':SoC_salida_work_1})
	# print("Viaje de ida")
	# print(fds_ida_fds)
	# VUELTA
	vuelta_fds = pd.DataFrame({'SoC.salida.wrk':SoC_salida_work_1,'Bat.cap':cap_bateria_1,'Dist.rec': dist_rec_v_1,'Consum.Bat':cons_bat_1,'Vel':vel_vuelta_1,'T.estacionado':t_parking_1,'T.salida.wrk': t_out_work_1,'SoC.lim.vuelta': SoC_limite_vuelta_1,'SoC.casa':SoC_casa_1,'SoC.fcs':SoC_fcs2_1,'E.fcs':E_fcs2_1,'dist.fcs':dist_fcs2_1,'t.fcs':t_fcs2_1,'t.lleg.casa':t_llegada_casa_1})
	# print("Viaje de ida")
	# print(fds_ida_fds)
	# Viaje ida y vuelta
	viaje_fds = pd.DataFrame({'t_fcs_ida':t_fcs_1,'E_fcs_ida':E_fcs_1,'delta_rec_ida':t_recarga_1,'carga_ida':carga_ida_1,'t_fcs_vuelta':t_fcs2_1,'E_fcs_vuelta':E_fcs2_1,'delta_rec_vuelta':t_recarga2_1,'carga_vuelta':carga_vuelta_1,'t_llegada_casa':t_llegada_casa_1,'E_casa':E_home_1,'delta_home':delta_home_1,'Pot_dom':carga_home_1})
	# print("Viaje de ida y vuelta")
	# print(viaje_fds)
	# ida_fds.to_csv('viaje_ida.csv')
	# vuelta_fds.to_csv('viaje_vuelta.csv')
	viaje_fds.to_csv('viaje_fds.csv')


	### PERFIL DE DEMANDA, RESOLUCION DE MINUTOS
	perfil = [[] for i in range(1441)] 

	for index,row in viaje_sem.iterrows():
		### FCS
		# IDA
		fcs_ida = viaje_sem.at[index,'E_fcs_ida']
		aux_ida = viaje_sem.at[index,'t_fcs_ida']
		aux_ida2 = viaje_sem.at[index,'delta_rec_ida']
		potencia_ida = viaje_sem.at[index,'carga_ida']
		min_inicio_ida = round(int(aux_ida),0)
		min_delta_ida = round(int(aux_ida2),0)
		min_termino_ida = int(min_inicio_ida + min_delta_ida)
		if (fcs_ida > 0 and min_termino_ida <= 1440 and min_inicio_ida <= 1440):
			for x in range(min_inicio_ida, min_termino_ida):
				y = potencia_ida
				perfil[x].append(y)
		elif (fcs_ida > 0 and min_termino_ida > 1440 and min_inicio_ida <= 1440):
			ciclo_ida = min_termino_ida - 1440
			y2 = potencia_ida
			for z in range(min_inicio_ida, 1440):
				perfil[z].append(y2)
			for z in range(0,ciclo_ida):
				perfil[z].append(y2)
		elif (fcs_ida > 0 and min_termino_ida > 1440 and min_inicio_ida > 1440):
			ciclo_ida_inicio = min_inicio_ida - 1440
			ciclo_ida_termino = min_termino_ida - 1440
			y3 = potencia_ida
			for z in range(ciclo_ida_inicio,ciclo_ida_termino):
				perfil[z].append(y3)
		# VUELTA
		fcs_vuelta = viaje_sem.at[index,'E_fcs_vuelta']
		aux_vuelta = viaje_sem.at[index,'t_fcs_vuelta']
		aux_vuelta2 = viaje_sem.at[index,'delta_rec_vuelta']
		potencia_vuelta = viaje_sem.at[index,'carga_vuelta']
		min_inicio_vuelta = round(int(aux_vuelta),0)
		min_delta_vuelta = round(int(aux_vuelta2),0)
		min_termino_vuelta = int(min_inicio_vuelta + min_delta_vuelta)
		if (fcs_vuelta > 0 and min_termino_vuelta <= 1440 and min_inicio_vuelta <= 1440):
			for z in range(min_inicio_vuelta, min_termino_vuelta):
				y4 = potencia_vuelta
				perfil[z].append(y4)
		elif (fcs_vuelta > 0 and min_termino_vuelta > 1440 and min_inicio_vuelta <= 1440):
			ciclo_vuelta = min_termino_vuelta - 1440
			y5 = potencia_vuelta
			for z in range(min_inicio_vuelta, 1440):
				perfil[z].append(y5)
			for z in range(0,ciclo_vuelta):
				perfil[z].append(y5)  
		elif (fcs_ida > 0 and min_termino_vuelta > 1440 and min_inicio_vuelta > 1440):
			ciclo_ida_inicio = min_inicio_vuelta - 1440
			ciclo_ida_termino = min_termino_vuelta - 1440
			y6 = potencia_ida
			for z in range(ciclo_ida_inicio,ciclo_ida_termino):
				perfil[z].append(y6)		
		### DOMICILIARIO
		if aux_dom_1 == 1:
			carga_home = viaje_sem.at[index,'E_casa']
			aux_home = viaje_sem.at[index,'t_llegada_casa']
			aux_home2 = viaje_sem.at[index,'delta_home']
			potencia_home = viaje_sem.at[index,'Pot_dom']
			min_inicio_home = round(int(aux_home),0)
			min_delta_home = round(int(aux_home2),0)
			min_termino_home = round(int(min_inicio_home + min_delta_home),0)
			# prueba_max.append(min_termino_home)
			if (carga_home > 0 and min_termino_home <= 1440 and min_inicio_home <= 1440):
				for w in range(min_inicio_home, min_termino_home):
					y7 = potencia_home
					perfil[w].append(y7)
			elif (carga_home > 0 and min_termino_home > 1440 and min_inicio_home <= 1440):
				ciclo = min_termino_home - 1440
				y8 = potencia_home
				for z in range(min_inicio_home, 1440):
					perfil[z].append(y8)
				for z in range(0,ciclo):
					perfil[z].append(y8)   #######
			elif (carga_home > 0 and min_termino_home > 1440 and min_inicio_home > 1440):
				ciclo_home_inicio = min_inicio_home - 1440
				ciclo_home_termino = min_termino_home - 1440
				y9 = potencia_home
				for z in range(ciclo_home_inicio,ciclo_home_termino):
					perfil[z].append(y9)
	# # print(perfil)
	# # print(prueba_max)
	# # print(max(prueba_max))
	perfil_minuto_fds = list(map(sum, perfil))
	# print('perfil demanda fin de semana')
	# print(perfil_minuto_fds)

	panda_perfil_fds = pd.DataFrame({'Demanda':perfil_minuto_fds})

	return E_total_fds, E_dom_fds, ida_fds, vuelta_fds, perfil_minuto_fds


def distribucion_comunal(energia_equivalente):
	import numpy as np
	import parametros1 as p
	import pandas as pd
	import math
	global modelo_lineal, ln_tasa, tasa, nom_comunas, energia_comunal, distribucion_final

	energia_total = energia_equivalente
	ln_tasa = []
	tasa = []

	# edad_com = np.array([35.7,36,37.3,36,36.6,33.8,35.5,37.7,37.1,36.6,33.3,38.5,39.1,33.4,36.3,37.5,38.3,35.5,39,38.3,35.2,39.7,34.4,33.7,32,37.1,36.6,34.3,33.4,38.2,37.4,37.2,34.5,39.4])
	# estudis_univ = np.array([18.7,8.8,16.1,13.6,23.8,30.8,26.6,27.8,29.6,12.7,7.3,52,62.4,49,8.8,14.3,33.4,25.6,57.4,14.3,25.2,67.2,19.9,21.3,19.9,20.3,19.4,11.7,17,19,42.7,10.6,46,64.7])
	coef_beta = np.array([0.488,
					0.426,
					0.353,
					0.74,
					0.003,
					0.193,
					-1.878,
					-1.44,
					-0.085,
					0.274,
					0.03])
	coef_alpha = -5.101



	nom_comunas = np.array(['Cerrillos','Cerro Navia','Conchalí','El Bosque','Estación Central','Huechuraba','Independencia','La Cisterna','La Florida','La Granja','La Pintana','La Reina','Las Condes','Lo Barnechea','Lo Espejo','Lo Prado','Macul','Maipú','Ñuñoa','Pedro Aguirre Cerda','Peñalolen','Providencia','Pudahuel','Puente Alto','Quilicura','Quinta Normal','Recoleta','Renca','San Bernardo','San Joaquín','San Miguel','San Ramón','Santiago','Vitacura'])
	array_comunas = np.array([p.cerrillos, p.cerro_navia, p.conchali, p.el_bosque, p.estacion_central, p.huechuraba, p.independencia, p.la_cisterna, p.la_florida, p.la_granja, p.la_pintana, p.la_reina, p.las_condes, p.lo_barnechea, p.lo_espejo, p.lo_prado, p.macul, p.maipu, p.ñuñoa, p.pedro_aguirre, p.peñalolen, p.providencia, p.pudahuel, p.puente_alto, p.quilicura, p.quinta_normal, p.recoleta, p.renca, p.san_bernardo, p.san_joaquin, p.san_miguel, p.san_ramon, p.santiago, p.vitacura])
	ln_comunas = np.log(array_comunas)

	aux = 0
	for cell in ln_comunas:
		# print(nom_comunas[aux])
		comuna = cell
		tasa_ve_ln = np.dot(comuna,coef_beta) + coef_alpha
		ln_tasa.append(tasa_ve_ln)
		# print('tasa ve en ln:', tasa_ve_ln)
		tasa_ve = math.exp(tasa_ve_ln)
		tasa.append(tasa_ve)
		# print('tasa total x 1000 vehiculos:', tasa_ve)
		aux = aux + 1


	modelo_lineal = pd.DataFrame({'Comuna':nom_comunas,'tasa_ln':ln_tasa,'tasa':tasa})
	# print(modelo_lineal)
	prop = int(np.sum(tasa))
	distribucion_final = [round((i * energia_total)/(1000*prop),3) for i in tasa]
	energia_comunal = pd.DataFrame({'Comuna':nom_comunas,'Energia_comunal':distribucion_final})
	# print(energia_comunal)

	return modelo_lineal, ln_tasa, tasa, nom_comunas, energia_comunal, distribucion_final


def informacion_ssee():
	import numpy as np
	import pandas as pd
	import parametros1 as p
	global info_comunas, data_ssee, nom_comunas

	#### Nombre de Comunas de Santiago
	nom_comunas = np.array(['Cerrillos','Cerro Navia','Conchali','El Bosque','Estacion Central','Huechuraba','Independencia','La Cisterna','La Florida','La Granja','La Pintana','La Reina','Las Condes','Lo Barnechea','Lo Espejo','Lo Prado','Macul','Maipu','Ñuñoa','Pedro Aguirre Cerda','Peñalolen','Providencia','Pudahuel','Puente Alto','Quilicura','Quinta Normal','Recoleta','Renca','San Bernardo','San Joaquin','San Miguel','San Ramon','Santiago','Vitacura'])
	info_comunas = pd.DataFrame({'Nombre': nom_comunas})

	##### Subestaciones del area de estudio:
	# subestaciones = np.array(['Alonso de Cordova','Altamirano','Andes','Apoquindo','Bicentenario','Brasil','Carrascal','Chacabuco','La Cisterna',
	# 						'Club Hipico','La Dehesa','La Reina','Las Acacias','Pudahuel','Lo Boza','Lo Prado','Lo Valledor','Lord Cochrane',
	# 						'Los Dominicos','Macul','Maipu','Mariscal','Ochagavia','Pajaritos','Panamericana','Quilicura','Recoleta','San Bernardo',
	# 						'San Cristobal','San Joaquin','San Jose','San Pablo','Santa Elena','Santa Marta','Santa Raquel','Santa Rosa','Vitacura'])  ## se incluye LO BOZA
	subestaciones = np.array(['Alonso de Cordova','Altamirano','Andes','Apoquindo','Bicentenario','Brasil','Carrascal','Chacabuco','La Cisterna',
							'Club Hipico','La Dehesa','La Reina','Las Acacias','Pudahuel','Lo Prado','Lo Valledor','Lord Cochrane',
							'Los Dominicos','Macul','Maipu','Mariscal','Ochagavia','Pajaritos','Panamericana','Quilicura','Recoleta','San Bernardo',
							'San Cristobal','San Joaquin','San Jose','San Pablo','Santa Elena','Santa Marta','Santa Raquel','Santa Rosa','Vitacura'])
	# print(np.count_nonzero(subestaciones))
	# potencia_ssee = np.array([130,125,97.4,146,50,150,67.2,284.9,160,147.4,145,170,125,64.8,172.4,31.5,200,139.4,97.4,170,69.8,88,103.33,172.4,72.4,97.4,
	# 						147.4,117.2,233.33,147.4,97.4,100,172.4,126,163.4,97.4,200])  ## se incluye LO BOZA
	potencia_ssee = np.array([130,125,97.4,146,50,150,67.2,284.9,160,147.4,145,170,125,64.8,31.5,200,139.4,97.4,170,69.8,88,103.33,172.4,72.4,97.4,
							147.4,117.2,233.33,147.4,97.4,100,172.4,126,163.4,97.4,200])
	# print(np.count_nonzero(potencia_ssee))
	# comuna_ssee = np.array(['Las Condes','Renca','La Reina','Las Condes','Maipu','Santiago','Quinta Normal','Quilicura','La Cisterna','Santiago',
	# 						'Lo Barnechea','Peñalolen','San Bernardo','Cerro Navia','Renca','Pudahuel','Estacion Central','Santiago','Las Condes',
	# 						'Peñalolen','Maipu','La Pintana','Pedro Aguirre Cerda','Maipu','San Bernardo','Quilicura','Huechuraba','San Bernardo',
	# 						'Recoleta','San Joaquin','Lo Prado','Pudahuel','Macul','Maipu','La Florida','Puente Alto','Las Condes'])  ## se incluye LO BOZA
	comuna_ssee = np.array(['Las Condes','Renca','La Reina','Las Condes','Maipu','Santiago','Quinta Normal','Quilicura','La Cisterna','Santiago',
							'Lo Barnechea','Peñalolen','San Bernardo','Cerro Navia','Pudahuel','Estacion Central','Santiago','Las Condes',
							'Peñalolen','Maipu','La Pintana','Pedro Aguirre Cerda','Maipu','San Bernardo','Quilicura','Huechuraba','San Bernardo',
							'Recoleta','San Joaquin','Lo Prado','Pudahuel','Macul','Maipu','La Florida','Puente Alto','Las Condes'])
	# print(np.count_nonzero(comuna_ssee))
	data_ssee = pd.DataFrame({'Nombre':subestaciones,'Capacidad_Instalada':potencia_ssee,'Comuna_Localizada':comuna_ssee})
	# print('SUBESTACIONES EXISTENTES')
	# print(data_ssee)
	# print()

	### Agrupa las subestaciones por comuna
	aux_pot_com = data_ssee.groupby(by='Comuna_Localizada').sum()
	pot_comuna = aux_pot_com.copy()
	pot_instalada_com = pot_comuna.reset_index()
	# print('Potencia instalada por comuna')
	# print(pot_instalada_com)
	# print(type(pot_instalada_com))

	#### DATAFRAME CON INFORMACION TOTAL POR COMUNA:
	info_comunas['Con_SSEE'] = info_comunas['Nombre'].isin(pot_instalada_com['Comuna_Localizada'])
	# info_comunas['Capacidad_Instalada'] = ['red' if x == True else 0 for x in info_comunas['Con_SSEE']]
	potencia_instalada = []
	for index,row in info_comunas.iterrows():
		if info_comunas.loc[index,'Con_SSEE'] == True:
			com = info_comunas.at[index,'Nombre']
			# print(com)
			for ind,row in pot_instalada_com.iterrows():
				com_aux = row['Comuna_Localizada']
				pot_aux = row['Capacidad_Instalada']
				if com == com_aux:
					potencia_instalada.append(pot_aux)
		else:
			potencia_instalada.append(0)

	# print(potencia_instalada)
	info_comunas['Potencia_Instalada'] = potencia_instalada
	info_comunas['Comunas_Vecinas'] = p.vecinos
	# print(info_comunas)

	##Potencia total de SSEE aledañas a comunas sin SSEE
	potencia_com_vecinas = []
	for label, row in info_comunas.iterrows():
		aux = info_comunas.loc[label,'Potencia_Instalada'] 
		a2 = info_comunas.loc[label,'Comunas_Vecinas'] 
		# print(aux)
		if aux == 0:
			pot_com_vec = 0
			for cell in a2:
				comuna = cell
				for ind,row in pot_instalada_com.iterrows():
					com_aux = row['Comuna_Localizada']
					pot_aux = row['Capacidad_Instalada']
					if comuna == com_aux:
						pot_com_vec = pot_com_vec + pot_aux
			potencia_com_vecinas.append(pot_com_vec)
		else:
			potencia_com_vecinas.append(0)
	# print(potencia_com_vecinas)
	info_comunas['Pot_Inst_Com_Vecinas'] = potencia_com_vecinas
	# print(info_comunas[['Nombre','Potencia_Instalada','Comunas_Vecinas','Pot_Inst_Com_Vecinas']])

	return info_comunas, data_ssee, nom_comunas



def distribucion_ssee(comunas, subestaciones, demanda_com):
	import numpy as np
	import pandas as pd
	import calculo1 as c
	import parametros1 as p
	global ssee_resultados, total_ssee, datos_comuna, arreglo_ssee, nom_comunas
	
	nom_comunas = ['Cerrillos','Cerro Navia','Conchali','El Bosque','Estacion Central','Huechuraba','Independencia','La Cisterna','La Florida','La Granja','La Pintana','La Reina','Las Condes','Lo Barnechea','Lo Espejo','Lo Prado','Macul','Maipu','Ñuñoa','Pedro Aguirre Cerda','Peñalolen','Providencia','Pudahuel','Puente Alto','Quilicura','Quinta Normal','Recoleta','Renca','San Bernardo','San Joaquin','San Miguel','San Ramon','Santiago','Vitacura']
	# arreglo_ssee = np.array(['Alonso de Cordova','Altamirano','Andes','Apoquindo','Bicentenario','Brasil','Carrascal','Chacabuco','La Cisterna',
	# 						'Club Hipico','La Dehesa','La Reina','Las Acacias','Pudahuel','Lo Boza','Lo Prado','Lo Valledor','Lord Cochrane',
	# 						'Los Dominicos','Macul','Maipu','Mariscal','Ochagavia','Pajaritos','Panamericana','Quilicura','Recoleta','San Bernardo',
	# 						'San Cristobal','San Joaquin','San Jose','San Pablo','Santa Elena','Santa Marta','Santa Raquel','Santa Rosa','Vitacura'])   ## se incluye LO BOZA
	arreglo_ssee = np.array(['Alonso de Cordova','Altamirano','Andes','Apoquindo','Bicentenario','Brasil','Carrascal','Chacabuco','La Cisterna',
							'Club Hipico','La Dehesa','La Reina','Las Acacias','Pudahuel','Lo Prado','Lo Valledor','Lord Cochrane',
							'Los Dominicos','Macul','Maipu','Mariscal','Ochagavia','Pajaritos','Panamericana','Quilicura','Recoleta','San Bernardo',
							'San Cristobal','San Joaquin','San Jose','San Pablo','Santa Elena','Santa Marta','Santa Raquel','Santa Rosa','Vitacura'])
	
	ssee = []
	potencia_ssee = []
	for ind, row in comunas.iterrows():
		aux_nombre = []
		aux_potencia = []
		comuna = comunas.at[ind,'Nombre']
		# print(comuna)
		for index, row in subestaciones.iterrows():
			nombre_ssee = subestaciones.at[index,'Nombre']
			potencia = subestaciones.at[index,'Capacidad_Instalada']
			comuna_loc = subestaciones.at[index,'Comuna_Localizada']
			# print(nombre_ssee, potencia, comuna_loc)
			if comuna_loc == comuna:
				aux_nombre.append(nombre_ssee)
				aux_potencia.append(potencia)
		ssee.append(aux_nombre)
		potencia_ssee.append(aux_potencia)	
	datos_comuna = pd.DataFrame({'Comuna':nom_comunas,'SSEE':ssee,'Potencia_SSEE':potencia_ssee})
	# print(datos_comuna)

	total_ssee = []
	for index, row in subestaciones.iterrows():
		comunas_abastecidas = []
		demanda_abastecida = []
		subestacion = subestaciones.at[index,'Nombre']
		potencia_ssee = subestaciones.at[index,'Capacidad_Instalada']
		comuna_ssee = subestaciones.at[index,'Comuna_Localizada']
		# print('Subetacion ',subestacion,'de Pot. Instalada ', potencia_ssee,'ubicada en ',comuna_ssee)
		for ind, row in comunas.iterrows():
			comuna = comunas.at[ind,'Nombre']
			pot_inst_com = comunas.at[ind,'Potencia_Instalada']
			demanda = demanda_com.at[ind,'Energia_comunal']
			if comuna == comuna_ssee:
				vecinos = comunas.at[ind,'Comunas_Vecinas']
				# print(comuna, pot_inst_com, demanda)
				comunas_abastecidas.append(comuna)
				aux = round(demanda * potencia_ssee / pot_inst_com,2)
				demanda_abastecida.append(aux)
				# print(vecinos)
				for cell in vecinos:
					comuna_vecina = cell
					for index2, row in datos_comuna.iterrows():
						comuna_aux = comunas.at[index2,'Nombre']
						potencia_aux = comunas.at[index2,'Pot_Inst_Com_Vecinas']
						demanda_vec = demanda_com.at[index2,'Energia_comunal']
						if ((comuna_aux == comuna_vecina) and (potencia_aux > 0)):
							comunas_abastecidas.append(comuna_aux)
							aux2 = round(demanda_vec * potencia_ssee / potencia_aux,2)
							demanda_abastecida.append(aux2)
				aux_df = pd.DataFrame({'Comunas_abastecidas':comunas_abastecidas,'Demanda de cada comuna':demanda_abastecida})
				# print('Comunas abastecidas:',comunas_abastecidas,'.Demanda de cada comuna:', demanda_abastecida)
				# print(aux_df)
				# print()
		resultado = sum(demanda_abastecida)
		total_ssee.append(resultado)
	# print(total_ssee)
	# print(len(total_ssee))
	
	# ## RESULTADO
	ssee_resultados = pd.DataFrame({'Nombre': arreglo_ssee,'Demanda':total_ssee})

	return ssee_resultados, total_ssee, datos_comuna, arreglo_ssee, nom_comunas