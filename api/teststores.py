import math
import numpy as np
import pandas as pd
from scipy import stats
import gower
from scipy.stats import norm
from django.http import HttpResponse
from .serializers import *
from .models import *
import random, os
from . import json
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.core import serializers
from sklearn.preprocessing import StandardScaler
from rest_framework import generics
from django.views.generic import ListView,View
import random



def GetAllSavedData(request):

	import json as j 
	data = j.loads(request.body)
	data = data['data']
	gettestStore = TestMstr.objects.get(test_name=data,is_active=True,is_deleted=False)
	results  = gettestStoreSerializer(gettestStore)
	return json.Response(results.data,True)

def Get_StoresDetails(request):

	import json as j 
	data = j.loads(request.body)
	data = data['data']
	gettestStore = StoreMstr.objects.filter(store_sk__in=data)
	results  = MatchTestStoreSerializer(gettestStore,many=True)
	return json.Response(results.data,True)
	

class UploadTestStore(generics.ListCreateAPIView):

	def post(self,request):
			filename = request.FILES['store_mstr']
			if filename:
				filename_check = filename.name
				ext = [".xlsx", ".csv", ".xls"]
				if filename_check.endswith(tuple(ext)):
					extesnion = os.path.splitext(filename_check)[1]
					if (extesnion == '.csv'):
						data = pd.read_csv(filename)
					else:
						data = pd.read_excel(filename)
					# try:
					for i in data.index:
						if(data['Partner ID'][i]==None):
							break;
						else:
							Save_TestStore = StoreMstr(
								Freq_rating_2019                        = data['2019 Freq. rating'][i],
								Freq_rating_2020                        = data['2020 Freq. rating'][i],
								Banner                    				= data['Banner'][i],
								Business_Model                   		= data['Business Model'][i],
								CSV_of_outlet                			= data['CSV of outlet'][i],  
								CSV_of_outlet_Segment                   = data['CSV of outlet Segment'][i],
								Channel                     			= data['Channel'][i],
								# Chocolate_RSV                      		= data['Chocolate RSV'][i],
								City                  					= data['City'][i],
								City_Rural           					= data['City (Rural/Urban File)'][i],
								Classification 							= data['Classification'][i],
								Classification_RTM                    	= data['Classification RTM'][i],
								Department                   			= data['Department'][i],
								# Fulltime_total_duration             	= data['Fulltime_total_duration'][i],
								# Fulltime_visits           				= data['Fulltime_visits'][i],
								House_Number                   			= data['House Number'][i],
								House_Number_Rural             			= data['House Number (Rural/Urban File)'][i],
								Influence_Chocolate                    	= data['Influence Chocolate'][i],
								Influence_Overall                      	= data['Influence Overall'][i],
								Influence_Petcare                       = data['Influence Petcare'][i],
								Influence_Segment                  		= data['Influence Segment'][i],		
								Influence_on_activation                 = data['Influence on activation'][i], 
								Influence_on_checkout                   = data['Influence on checkout'][i],
								Influence_on_permanent_siting           = data['Influence on permanent siting'][i],
								Influence_on_shelf               		= data['Influence on shelf'][i],
								Outlet_Banner_Code                 		= data['Outlet Banner Code'][i],
								Outlet_surface                    		= data['Outlet surface'][i],								
								Partner_ID              				= data['Partner ID'][i],
								Partner_Name        					= data['Partner Name'][i],
								Partner_Name_Rural               		= data['Partner Name (Rural/Urban File)'][i],
								# Petcare_RSV            					= data['Petcare RSV'][i],
								Rural_vs_Urban   						= data['Rural vs Urban'][i],
								Sales_Throughout_Year              		= data['Sales Throughout Year'][i],
								Segment           						= data['Segment'][i], 
								Segment_Based                          	= data['Segment (Based on Outlet Surface Area)'][i],
								Shelf_meters_Cat                        = data['Shelf meters Cat'][i],
								Shelf_meters_Choc        				= data['Shelf meters Choc'][i],
								Shelf_meters_Dog        				= data['Shelf meters Dog'][i],
								Status        							= data['Status'][i],
								Street        							= data['Street'][i],
								Street_Rural               				= data['Street (Rural/Urban File)'][i], 
								Sub_Channel             				= data['Sub Channel'][i], 
								# Total_RSV     							= data['Total RSV'][i], 
								V4_invloed_op_activatie                	= data['V4+ invloed op activatie'][i], 
								V4_invloed_op_kassa               		= data['V4+ invloed op kassa'][i], 
								V4_invloed_op_permanente_siting         = data['V4+ invloed op permanente siting'][i], 
								V4_invloed_op_schap              		= data['V4+ invloed op schap'][i], 
								ZIP_code                 				= data['ZIP code'][i], 
								ZIP_code_Rural                			= data['ZIP code (Rural/Urban File)'][i], 
								ZIP_code_4_digitis_Rural            	= data['ZIP code 4 digitis (Rural/Urban File)'][i], 
								# thirdparty_total_duration           	= data['thirdparty_total_duration'][i], 
								# thirdparty_visits        				= data['thirdparty_visits'][i], 
								Territory        						= data['Territory'][i], 
								Chocolate_Annual_RSV_2018     			= data['Chocolate Annual RSV 2018'][i], 
								Chocolate_Annual_Volume_2018			= data['Chocolate Annual Volume 2018'][i], 
								Petcare_Annual_RSV_2018        			= data['Petcare Annual RSV 2018'][i], 
								Petcare_Annual_Volume_2018        		= data['Petcare Annual Volume 2018'][i], 
								Annual_RSV_2018        					= data['Annual RSV 2018'][i], 
								Annual_Volume_2018        				= data['Annual Volume 2018'][i], 
								Chocolate_Annual_RSV_2019        		= data['Chocolate Annual RSV 2019'][i], 
								Chocolate_Annual_Volume_2019        	= data['Chocolate Annual Volume 2019'][i], 
								Petcare_Annual_RSV_2019        			= data['Petcare Annual RSV 2019'][i], 
								Petcare_Annual_Volume_2019        		= data['Petcare Annual Volume 2019'][i], 
								Annual_RSV_2019        					= data['Annual RSV 2019'][i], 
								Annual_Volume_2019       				= data['Annual Volume 2019'][i], 
								Overall_Segment                   		= data['Overall Segment'][i],
								created_on								= int(time.time()),
								is_deleted 								= False,
								is_active								= True
								)
							Save_TestStore.save()

					return json.Response('Test Store Updated Successfully',True)	
					# except:
					# 	return json.Response('Can`t able to upload', False) 
				else:
					return json.Response("Invalid File Format! Please upload .csv or .xlsx",False)
			else:
				return json.Response("File Upload Failed",False)

class Parameter(ListView):

	def get(self,serializer):	
		import json as j
		gettestStore = StoreMstr.objects.filter(is_active=True,is_deleted=False)
		results  = TestStoreSerializer(gettestStore,many=True)
		arr= j.dumps(results.data)
		arr = j.loads(arr)
		banner = []
		segment = []
		territory = []
		store_grid =[] 
		for dat in arr:			
			banner.append(dat['Banner'])
			segment.append(dat['Segment'])	
			territory.append(dat['Territory'])	
			store_grid.append(dat['Overall_Segment'])
		finalbanner = []
		finalsegmet = []
		finalterritory = []
		finalstore =[]
		for i in banner:
			if i not in finalbanner:
				finalbanner.append(i)
		for j in segment:
			if j not in finalsegmet:
				finalsegmet.append(j)
		for k in territory:
			if k not in finalterritory:
				finalterritory.append(k)
		for l in store_grid:
			if l not in finalstore:
				finalstore.append(l)

		result = {
		"banner" : finalbanner,
		"segment" : finalsegmet,
		"territory" : finalterritory,
		"store_grid" :finalstore
		}
		return json.Response(result,True)

class Edit_TestStore(generics.ListCreateAPIView):

	def get(self,serializer,pk):	
		gettestStore = TestMstr.objects.get(test_id=pk)
		results  = gettestStoreSerializer(gettestStore)
		return json.Response(results.data,True)		

	def delete(self,serializer,pk):	
		try:
			deletetestStore = TestMstr.objects.filter(test_id=pk).update(deleted_at=int(time.time()),is_deleted=True,is_active=False)
			return json.Response('Test Deleted Successfully',True)
		except:
			return json.Response('Can`t able to delete data',False)

class SaveStage(generics.ListCreateAPIView):

	def post(self,request):
		import json as j 
		data = j.loads(request.body)
		datas = data['data']
		if 'desc' not in datas:
			desc = ""
		else:
			desc = datas['desc']

		if 'additional_det' not in datas:
			additional_det = ""
		else:
			additional_det = datas['additional_det']

		headers= request.META['HTTP_AUTHORIZATION']
		split_token = headers.split('Bearer ')		
		jwt_token = split_token[1]
		get_user = AuthTokenMstr.objects.get(jwt_token=jwt_token)
		if(get_user):
			user_data = AuthSeralizer(get_user)
			user = User.objects.get(id=user_data.data['user_id'])
			# try:		
			if(datas['stepindex']==1):
				StageSave = TestMstr(
					test_name   = datas['test_name'],
					user_id   	= user,
					test_desc   = desc,
					test_desc1  = additional_det,
					testtype	= datas['test_type'],
					target_var 	= datas['target_variable'],
					territory_name = datas['territory'],
					store_segment = datas['segment'],
					banners 	  = datas['banner'],
					category_name = datas['category'],
					store_grid 	  = datas['store_grid'],
					stepper_id   = datas['stepindex'],
					stage_id    = datas['stage_id'],
					created_on	= int(time.time()),
					is_deleted 	= False,
					is_active	= True
				)
				StageSave.save()
				return json.Response(StageSave.pk,True)
			elif (datas['stepindex']==2):

				if 'test_id' not in datas:
					StageSave = TestMstr(
					test_name   = datas['test_name'],
					user_id   	= user,
					test_desc   = desc,
					test_desc1  = additional_det,
					testtype	= datas['test_type'],
					target_var 	= datas['target_variable'],
					territory_name = datas['territory'],
					store_segment = datas['segment'],
					banners 	  = datas['banner'],
					category_name = datas['category'],
					store_grid 	  = datas['store_grid'],
					stepper_id   = datas['stepindex'],
					stage_id    = datas['stage_id'],
					confidence_lev = datas['confidence_lvl'],
					margin_oferror = datas['margin_error'],
					no_of_teststore = datas['no_of_teststores'],
					pre_start = datas['pretest_startdt'],
					pre_end = datas['pretest_enddt'],
					testwin_start = datas['testwin_startdt'],
					testwin_end = datas['testwin_enddt'],
					created_on	= int(time.time()),
					is_deleted 	= False,
					is_active	= True
					)
					StageSave.save()

					return json.Response(StageSave.pk,True)
				else:
					test_id = datas['test_id']
					confidence_lev = datas['confidence_lvl']
					margin_oferror = datas['margin_error']
					no_of_teststore = datas['no_of_teststores']
					pre_start = datas['pretest_startdt']
					pre_end = datas['pretest_enddt']
					testwin_start = datas['testwin_startdt']
					testwin_end = datas['testwin_enddt']
					stepper_id   = datas['stepindex'],

					StageSave = TestMstr.objects.filter(test_id=test_id).update(
						confidence_lev =confidence_lev,
						margin_oferror = margin_oferror,
						no_of_teststore = no_of_teststore,
						pre_start = pre_start,
						pre_end = pre_end,
						testwin_start = testwin_start,
						stepper_id   = str(2),
						testwin_end = testwin_end
						)	
					return json.Response("Updated Successfully",True)

			else:

				if 'test_id' not in datas:

					StageSave = TestMstr(
					test_name   = datas['test_name'],
					user_id   	= user,
					test_desc   = desc,
					test_desc1  = additional_det,
					testtype	= datas['test_type'],
					target_var 	= datas['target_variable'],
					territory_name = datas['territory'],
					store_segment = datas['segment'],
					banners 	  = datas['banner'],
					category_name = datas['category'],
					store_grid 	  = datas['store_grid'],
					stepper_id   = datas['stepindex'],
					stage_id    = datas['stage_id'],
					confidence_lev = datas['confidence_lvl'],
					margin_oferror = datas['margin_error'],
					no_of_teststore = datas['no_of_teststores'],
					pre_start = datas['pretest_startdt'],
					pre_end = datas['pretest_enddt'],
					testwin_start = datas['testwin_startdt'],
					testwin_end = datas['testwin_enddt'],
					created_on	= int(time.time()),
					is_deleted 	= False,
					is_active	= True
					)
					StageSave.save()
					
					for store in datas['selectedteststore']:
						storemap = StoreMstr.objects.get(Partner_ID = store['Partner_ID'])
						TStoreMap = TestStoreMap(
							test_id = StageSave,
							store_id = storemap,
							created_on	= int(time.time()),
							is_deleted 	= False,
							is_active	= True
						)
						TStoreMap.save()
					
					remove_record = RecordMstr.objects.filter(test_id = StageSave).delete()
					Record_save = RecordMstr(
						test_id   = StageSave,
						stage_id  = datas['stage_id'],
						record_value = datas['records'],
						stepper_id = str(3),
						created_on	= int(time.time()),
						is_deleted 	= False,
						is_active	= True
						)
					Record_save.save()

					return json.Response(StageSave.pk,True)
				else:

					test_id = datas['test_id']
					StageSave = TestMstr.objects.filter(test_id=test_id).update(
						stepper_id   = str(3),
					)

					for store in datas['selectedteststore']:
						storemap = StoreMstr.objects.get(Partner_ID = store['Partner_ID'])
						TStoreMap = TestStoreMap(
							test_id = StageSave,
							store_id = storemap,
							created_on	= int(time.time()),
							is_deleted 	= False,
							is_active	= True
						)
						TStoreMap.save()

					remove_record = RecordMstr.objects.filter(test_id = StageSave.test_id).delete()
					Record_save = RecordMstr(
						test_id   = StageSave.test_id,
						stage_id  = datas['stage_id'],
						record_value = datas['records'],
						stepper_id = str(3),
						created_on	= int(time.time()),
						is_deleted 	= False,
						is_active	= True
						)
					Record_save.save()
					return json.Response(test_id,True)

			# except:
			# 	return json.Response('Unable to Save',False)
		else:
			return json.Response('Unable to Save',False)


def UpdateStage(request):
	import json as j
	data = j.loads(request.body)
	datas = data['data']
	stringify = data['stringified_data']
	# Market_id = TestMstr.objects.filter(is_active=True, is_deleted=False, test_id=datas['trial']).update(stage_id=datas['stage_id'])
	# return json.Response('Stage saved Successfully', True)
	# try:
	removee_rec = RecordMstr.objects.filter(is_active=True, is_deleted=False, test_id=datas['trial'],stage_id=datas['stage_id']).count()
	if(removee_rec>0):
		removee_rec = RecordMstr.objects.filter(is_active=True, is_deleted=False, test_id=datas['trial'],
												stage_id=datas['stage_id']).delete()

	StageSave = RecordMstr(
		test_id=datas['trial'],
		stage_id=datas['stage_id'],
		record_value= stringify,
		created_on=int(time.time()),
		is_deleted = False,
		is_active	= True
	)
	StageSave.save()

	UpdateStage = TestMstr.objects.filter(is_active=True, is_deleted=False, test_id=datas['trial']).update(stage_id=datas['stage_id'])

	return json.Response(StageSave.pk ,True)

def LoadSaveData(request):	

	headers= request.META['HTTP_AUTHORIZATION']
	split_token = headers.split('Bearer ')		
	jwt_token = split_token[1]
	get_user = AuthTokenMstr.objects.get(jwt_token=jwt_token)
	if(get_user):
		user_data = AuthSeralizer(get_user)
		user_id = user_data.data['user_id']
		GetloadData = TestMstr.objects.filter(is_active=True,is_deleted=False,user_id=user_id).order_by('-created_on','-modified_on')
		results = LoadDataSeralizer(GetloadData,many=True)
		try:
			return json.Response(results.data,True)
		except:
			return json.Response('Can`t able to get data',False)


# Tiger Code
######################################################################

class DateRange(generics.ListCreateAPIView):

	def get(self,request):
		dataStore = pd.read_excel("datas/Weekly Target Variables Data.xlsx")
		dataStore['wkEndDate'] = dataStore['Year']
		dataStore = dataStore.sort_values(by=['wkEndDate'])
		results =  {
			"startdate": str(dataStore.wkEndDate.unique()[0]),
			"enddate"  : str(dataStore.wkEndDate.unique()[-1])
		}
		return json.Response(results,True)


def find_weeks(start,end):
	import datetime
	l = []
	for i in range((end-start).days + 1):
		d = (start+datetime.timedelta(days=i)).isocalendar()[:2] # e.g. (2011, 52)
		yearweek = '{}{:02}'.format(*d) # e.g. "201152"
		l.append(int(yearweek[-2:]))
	return sorted(set(l))

class GetTestParameter(generics.ListCreateAPIView):
	# def get_test_parameter(confidence_level=None,margin_of_error=None,num_test_stores=None,testwindow_start=None,testwindow_end=None,target_variable=None,banners=[]):
	
	def post(self,request):	

		import json as j 	
		from datetime import datetime
		data = j.loads(request.body)
		datas = data['data']
		testwindow_start 		= datas['testwindow_start']
		testwindow_end 			= datas['testwindow_end']
		if 'confidence_level' in datas:
			confidence_level 		= datas['confidence_level']
		else:
			confidence_level = None
		if 'margin_of_error' in datas:
			margin_of_error 		= datas['margin_of_error']
		else:
			margin_of_error = None
		if 'num_test_stores' in datas:
			num_test_stores			= datas['num_test_stores']
		else:
			num_test_stores = None

		if 'target_variable' in datas:
			target_variable			= datas['target_variable']
		else:
			target_variable = None

		if 'banners' in datas:
			banners			= datas['banners']
		else:
			banners = []

		if ((testwindow_start is not None) & (testwindow_end is not None) & (target_variable is not None) & (len(banners)!=0)):
		        
			# Reading the target varaibles file
			weekly_target_variables_file = pd.read_excel("datas/Weekly Target Variables Data.xlsx")

			# Getting the week numbers in window
			test_duration_week_numbers = find_weeks(datetime.strptime(testwindow_start, '%Y-%m-%d').date(),datetime.strptime(testwindow_end, '%Y-%m-%d').date())

			# Getting the no of weeks, year from window
			testwindow_start = pd.to_datetime(testwindow_start)
			testwindow_end = pd.to_datetime(testwindow_end)
			test_duration_weeks = len(test_duration_week_numbers)
			test_duration_year = testwindow_start.year

			# Filtering the Target variables file
			banner_filter = (weekly_target_variables_file["Banner"].isin(banners))
			year_filter = (weekly_target_variables_file["Year"]==test_duration_year)
			week_filter = (weekly_target_variables_file["Week"].isin(test_duration_week_numbers))
			weekly_target_variables_file = weekly_target_variables_file[banner_filter & year_filter & week_filter]

			standard_deviation = weekly_target_variables_file[target_variable].std()
			mean_value = weekly_target_variables_file[target_variable].mean()
        
			if sum([v is not None for v in [confidence_level,margin_of_error,num_test_stores]])==2:
				if confidence_level is None:
					value1 = num_test_stores*test_duration_weeks
					confidence_level = round(1 - 2*(1 - norm.cdf(np.sqrt(value1/2) * ( margin_of_error * mean_value )/standard_deviation)),2)
					test_parameter = confidence_level

				if margin_of_error is None:
					value1 = num_test_stores*test_duration_weeks
					margin_of_error = round(norm.ppf((1 - ( 1 - confidence_level ) / 2)) * standard_deviation / ( np.sqrt(value1/2) * mean_value ),2)
					test_parameter = margin_of_error

				if num_test_stores is None:
					value1 = 2 * np.power(norm.ppf((1 - ( 1 - confidence_level ) / 2)) * standard_deviation / ( margin_of_error * mean_value ),2)
					num_test_stores = math.ceil(value1/test_duration_weeks)
					test_parameter = num_test_stores

			else:
				return json.Response("Please enter approprite number of parameters", False)	
		else:
			return json.Response("Please check the inputs ", False)
		
		return json.Response(test_parameter, True) 




class IdentifyStores(generics.ListCreateAPIView):
		
	# def identify_test_stores(test_name="",type_of_test="",banners=[],segments=[],store_segments=[],segment_variables=[],num_of_teststores=40
	def post(self,request):	
		
		import json as j 	
		data = j.loads(request.body)
		datas = data['data']
		test_name 			= datas['test_name']
		type_of_test  		= datas['type_of_test']
		banners    			= datas['banners']	        					
		segments   			= datas['segments']
		store_segments   	= datas['store_segments']
		segment_variables   = datas['segment_variables']

		# predefined
		num_of_teststores = 40

		#Read the files
		# stores_master_df = pd.read_excel("datas/TL_StoreMstr.xlsx")
		Allstores = StoreMstr.objects.filter(is_active=True,is_deleted=False)
		Teststores  = TestStoreSerializer(Allstores,many=True)
		stores_master_df = pd.DataFrame(Teststores.data)

		# test_master_df = pd.read_excel("datas/TL_TestMstr.xlsx")
		# teststore_map_df = pd.read_excel("datas/TL_Teststore_map.xlsx")
		# controlstore_map_df = pd.read_excel("datas/TL_Controlstore_Mstr.xlsx")

		Alltest = TestMstr.objects.filter(is_active=True,is_deleted=False)
		Testmst  = TestSerializer(Alltest,many=True)
		test_master_df = pd.DataFrame(Testmst.data)

		# test_master_df = pd.read_excel("datas/TL_TestMstr.xlsx")
		if(test_master_df.empty):
			columns = ['test_id','test_name','test_desc','testtype','target_var','territory_name','store_segment','category_name','confidence_lev','margin_oferror','std_deviation','pre_start','pre_end','test_window','testwin_start','testwin_end','stage_id','created_on','modified_on','is_active','deleted_at','is_deleted']
			test_master_df = pd.DataFrame(columns=columns)

		Alltestmap = TestStoreMap.objects.filter(is_active=True,is_deleted=False)
		Teststop  = TestStoreMapSerializer(Alltestmap,many=True)
		teststore_map_df = pd.DataFrame(Teststop.data)
		# teststore_map_df = pd.read_excel("datas/TL_Teststore_map.xlsx")

		controlstore = ControlStoreMstr.objects.filter(is_active=True,is_deleted=False)
		controlstores  = ControlstoreSerializer(controlstore,many=True)
		controlstore_map_df = pd.DataFrame(Teststop.data)


		# Teststores list to store bannerwise teststores
		banner_teststores_list = list()
    
		# Teststores validate variables
		compare_variables = ["Outlet_surface","CSV_of_outlet"]
    
		# Validating Input Parameters (Ex: If banners are not provided, we consider all the banners from the population )
		if len(banners) == 0:
			banners = stores_master_df["Banner"].unique().tolist()
		if len(segments) == 0:
			segments = stores_master_df["Overall_Segment"].unique().tolist()
		if len(store_segments) == 0:
			store_segments = stores_master_df["Segment_Based"].unique().tolist()
		if len(segment_variables) == 0:
			segment_variables = ["Overall_Segment"] 


		# Create filters
		banner_filter = (stores_master_df["Banner"].isin(banners))
		segment_filter = (stores_master_df["Overall_Segment"].isin(segments))
		store_segment_filter = (stores_master_df["Segment_Based"].isin(store_segments))
		# Filter the stores only from the input filters
		stores_master_df = stores_master_df[banner_filter & segment_filter & store_segment_filter]

		# Get the proportion of stores to be sampled for each banner
		count_df = stores_master_df.groupby("Banner")["Partner_ID"].count().reset_index().rename(columns={"Partner_ID":"Count"})
		count_df["prop"] = count_df["Count"]/count_df["Count"].sum()
		count_df["stores_proportioned"] = count_df["prop"]*num_of_teststores
		count_df["stores_proportioned"] = count_df["stores_proportioned"].apply(lambda x:round(x))
		ah_num_of_teststores = count_df[count_df["Banner"]=="Albert Heijn"]["stores_proportioned"].values[0]
		jumbo_num_of_teststores = count_df[count_df["Banner"]=="Jumbo"]["stores_proportioned"].values[0]
	    
		# ELIMINATING ALL THE TEST AND CONTROL STORES WHICH ARE CURRENTLY ACTIVE
		# Get all the active tests(test ids)

		active_tests_df = test_master_df[test_master_df["is_active"]==True]

		# column_names = ["a", "b", "c"]
		# active_tests_df = pd.DataFrame(columns = column_names)


		if active_tests_df.shape[0] != 0:
			# THIS MEANS THERE ARE ACTIVE TESTS AND WE NEED TO ELIMINATE ACTIVE TEST AND CONTROL STORES

			#Get the active test stores using test ids
			active_test_stores = teststore_map_df[teststore_map_df["test_id"].isin(active_tests_df["test_id"])]
			
			#Get the active control stores using test ids
			active_control_stores = controlstore_map_df[controlstore_map_df["test_id"].isin(active_tests_df["test_id"])]

			#Remove active test and control stores from population
			filtered_stores_df = stores_master_df[~stores_master_df["store_id"].isin(active_test_stores["store_id"])]
			filtered_stores_df = filtered_stores_df[~filtered_stores_df["store_id"].isin(active_control_stores["store_id"])]
		else:
			# THIS MEANS THERE ARE NO ACTIVE TESTS AND WE NEED NOT ELIMINATE ANY TEST AND CONTROL STORES
			filtered_stores_df = stores_master_df
	    
		# Getting Bannerwise Teststores
		for banner in banners:
			intermediate_stores_list = list()
			banner_num_of_teststores = count_df[count_df["Banner"]==banner]["stores_proportioned"].values[0]
			banner_filter = (filtered_stores_df["Banner"]==banner)

			store_segments = filtered_stores_df[banner_filter].groupby(segment_variables)["Partner_ID"].count().reset_index()
			store_segments["proportion"] = (store_segments["Partner_ID"]/store_segments["Partner_ID"].sum())
			store_segments["stores_proportioned"] = store_segments["proportion"]*banner_num_of_teststores
			store_segments["stores_proportioned"] = store_segments["stores_proportioned"].apply(lambda x:round(x))
			segmentwise_stores_dict = store_segments.groupby(segment_variables)["stores_proportioned"].sum().to_dict()
			for i in list(range(0,10)):
				# Sampling the test stores
				banner_test_stores = filtered_stores_df[banner_filter].groupby(segment_variables).apply(lambda x: x.sample(segmentwise_stores_dict[x.name],replace=False)).reset_index(drop=True)
				threshold_count = validate_test_stores(banner_test_stores,compare_variables)
				if threshold_count == len(compare_variables):
					intermediate_stores_list.append(banner_test_stores)
			banner_teststores_list.append(intermediate_stores_list[random.randint(0,len(intermediate_stores_list)-1)])
	    
		# Teststores
		teststores = pd.concat(banner_teststores_list)
		teststores["is_teststore"] = 1
		stores_otherthan_teststores = filtered_stores_df[~filtered_stores_df["Partner_ID"].isin(teststores["Partner_ID"])]
		stores_otherthan_teststores["is_teststore"]=0
		teststores = pd.concat([teststores,stores_otherthan_teststores])
		
		finalstores_master_df = stores_master_df.reset_index().to_json(orient='records')

		return json.Response(finalstores_master_df, True)

		
class StoreSummary(generics.ListCreateAPIView):
	# def test_store_summary(test_stores=None,compare_variables=[],banners=[],segments=[],store_segments=[]):
	def post(self,request):
		# Get banner wise no of stores
		request = self.request.data
		stores = request['data']['test_stores']
		compare_variables = request['data']['compare_variables']
		banners = request['data']['banners']
		segments = request['data']['segments']
		store_segments = request['data']['store_segments']

		# stores = pd.DataFrame(eval(stores))
		# stores= stores.replace(np.nan, ' ', regex=True)
		test_stores = pd.DataFrame.from_dict(stores, orient='columns')

		if (test_stores is not None) & (len(compare_variables) != 0):
        
			# Converting list of jsons to Dataframe
			null=np.nan
			test_stores = pd.DataFrame(test_stores)

			# Create variables
			variables_metrics_dict = {}
			#Read the files
			# stores_master_df = pd.read_excel("datas/TL_StoreMstr.xlsx")
			
			Allstores = StoreMstr.objects.filter(is_active=True,is_deleted=False)
			Teststores  = TestStoreSerializer(Allstores,many=True)
			stores_master_df = pd.DataFrame(Teststores.data)

			stores_master_df = check_if_store_valid(storesfile=stores_master_df)

	        # Validating Input Parameters (Ex: If banners are not provided, we consider all the banners from the population )
			if len(banners) == 0:
				banners = test_stores["Banner"].unique().tolist()
			if len(segments) == 0:
				segments = test_stores["Overall_Segment"].unique().tolist()
			if len(store_segments) == 0:
				store_segments = test_stores["Segment_Based"].unique().tolist()

			# Create filters
			banner_filter = (stores_master_df["Banner"].isin(banners))
			segment_filter = (stores_master_df["Overall_Segment"].isin(segments))
			store_segment_filter = (stores_master_df["Segment_Based"].isin(store_segments))

			# Filter the stores only from the input filters
			stores_master_df = stores_master_df[banner_filter & segment_filter & store_segment_filter]
	        
			for col in compare_variables:
				variables_metrics_dict[col] = {}
				tStat, pVal = stats.ttest_ind(test_stores[col].astype(int),stores_master_df[col].astype(int),nan_policy='omit') 	            
				variables_metrics_dict[col]["Test Mean"] = round(test_stores[col].astype(int).mean(),2)
				variables_metrics_dict[col]["Population Mean"] = round(stores_master_df[col].astype(int).mean(),2)
				variables_metrics_dict[col]["Test Std Dev"] = round(test_stores[col].astype(int).std(),2)
				variables_metrics_dict[col]["Population Std Dev"] = round(stores_master_df[col].astype(int).std(),2)
				# Get banner wise no of stores
			variables_metrics_dict["Test stores split"] = test_stores.groupby("Banner")["Partner_ID"].count().to_dict()

		else:
		    return json.Response('Please pass appropriate parameters', False) 
		
		return json.Response(variables_metrics_dict, True) 


def validate_test_stores(test_stores=None,compare_variables=[],banners=[],segments=[],store_segments=[]):

	if (test_stores is not None) & (len(compare_variables) != 0):
        # Pvalue count
		count=0
		# Create variables threshold dict
		variables_thresholds_dict = {k:0.6 for k in compare_variables}
		#Read the files
		# stores_master_df = pd.read_excel("datas/TL_StoreMstr.xlsx")
		Allstores = StoreMstr.objects.filter(is_active=True,is_deleted=False)
		Teststores  = TestStoreSerializer(Allstores,many=True)
		stores_master_df = pd.DataFrame(Teststores.data)


		# Validating Input Parameters (Ex: If banners are not provided, we consider all the banners from the population )
		if len(banners) == 0:
			banners = test_stores["Banner"].unique().tolist()
		if len(segments) == 0:
			segments = test_stores["Overall_Segment"].unique().tolist()
		if len(store_segments) == 0:
			store_segments = test_stores["Segment_Based"].unique().tolist()

		# Create filters
		banner_filter = (stores_master_df["Banner"].isin(banners))
		segment_filter = (stores_master_df["Overall_Segment"].isin(segments))
		store_segment_filter = (stores_master_df["Segment_Based"].isin(store_segments))

		# Filter the stores only from the input filters
		stores_master_df = stores_master_df[banner_filter & segment_filter & store_segment_filter]

		for col in compare_variables:
			tStat, pVal = stats.ttest_ind(test_stores[col].astype(int),stores_master_df[col].astype(int),nan_policy='omit') 
			pVal = round(pVal,2)
			if pVal>=variables_thresholds_dict[col]:
				count+=1        
	else:
		return "Please pass appropriate parameters"
    
	return count


class IdentifyControlStore(generics.ListCreateAPIView):
	# def identify_control_stores(teststores=None,store_features=[]):
	def post(self,request):
		# request = self.request.data
		null=np.nan
		# stores = request['data']['teststores']

		# ########
		filename = request.FILES['store_mstr']
		if filename:
			filename_check = filename.name
			ext = [".xlsx", ".csv", ".xls"]
			if filename_check.endswith(tuple(ext)):
				extesnion = os.path.splitext(filename_check)[1]
				if (extesnion == '.csv'):
					data = pd.read_csv(filename)
				else:
					teststores = pd.read_excel(filename)
		
		
		store_features =request.POST['store_features']
		# stores  =request.POST['teststores']
		##############
		# stores = pd.DataFrame(eval(stores))
		# teststores = pd.DataFrame.from_dict(stores, orient='columns')
		# store_features =request['data']['store_features']
		
		if teststores is not None:

			mandatory_features = ['Banner', 'Outlet_surface', 'Shelf_meters_Choc','Shelf_meters_Dog', 'Shelf_meters_Cat', 
	                             'Influence_Overall','CSV_of_outlet']
			# store_features = mandatory_features + store_features

			# stores_master_df = pd.read_excel("datas/TL_StoreMstr.xlsx")
			# test_master_df = pd.read_excel("TL_TestMstr.xlsx")
			# teststore_map_df = pd.read_excel("TL_Teststore_map.xlsx")
			# controlstore_map_df = pd.read_excel("TL_Controlstore_Mstr.xlsx")
			
			Allstores = StoreMstr.objects.filter(is_active=True,is_deleted=False)
			Teststores  = TestStoreSerializer(Allstores,many=True)
			stores_master_df = pd.DataFrame(Teststores.data)

			Alltest = TestMstr.objects.filter(is_active=True,is_deleted=False)
			Testmst  = TestSerializer(Alltest,many=True)
			test_master_df = pd.DataFrame(Testmst.data)
			# test_master_df = pd.read_excel("datas/TL_TestMstr.xlsx")
			if(test_master_df.empty):
				columns = ['test_id','test_name','test_desc','testtype','target_var','territory_name','store_segment','category_name','confidence_lev','margin_oferror','std_deviation','pre_start','pre_end','test_window','testwin_start','testwin_end','stage_id','created_on','modified_on','is_active','deleted_at','is_deleted']
				test_master_df = pd.DataFrame(columns=columns)

			Alltestmap = TestStoreMap.objects.filter(is_active=True,is_deleted=False)
			Teststop  = TestStoreMapSerializer(Alltestmap,many=True)
			teststore_map_df = pd.DataFrame(Teststop.data)
			# teststore_map_df = pd.read_excel("datas/TL_Teststore_map.xlsx")

			controlstore = ControlStoreMstr.objects.filter(is_active=True,is_deleted=False)
			controlstores  = ControlstoreSerializer(controlstore,many=True)
			controlstore_map_df = pd.DataFrame(Teststop.data)


			# Eliminating the Invalid Stores From Population
			stores_master_df = check_if_store_valid(storesfile=stores_master_df)
			stores_master_df = stores_master_df[stores_master_df["Is Valid Store"]==1]

			# ELIMINATING ALL THE TEST AND CONTROL STORES WHICH ARE CURRENTLY ACTIVE
			# Get all the active tests(test ids)
			active_tests_df = test_master_df[test_master_df["is_active"]==True]

			

			if active_tests_df.shape[0] != 0:
				# THIS MEANS THERE ARE ACTIVE TESTS AND WE NEED TO ELIMINATE ACTIVE TEST AND CONTROL STORES

				#Get the active test stores using test ids
				active_test_stores = teststore_map_df[teststore_map_df["test_id"].isin(active_tests_df["test_id"])]

				#Get the active control stores using test ids
				active_control_stores = controlstore_map_df[controlstore_map_df["test_id"].isin(active_tests_df["test_id"])]

				#Remove active test and control stores from population
				stores_master_df = stores_master_df[~stores_master_df["store_id"].isin(active_test_stores["store_id"])]
				stores_master_df = stores_master_df[~stores_master_df["store_id"].isin(active_control_stores["store_id"])]

			else:
	            # THIS MEANS THERE ARE NO ACTIVE TESTS AND WE NEED NOT ELIMINATE ANY TEST AND CONTROL STORES
				pass

			# ELIMINATING THE TESTSTORES FROM POPULATION

			stores_master_df = stores_master_df[~(stores_master_df["Partner_ID"].isin(teststores["Partner_ID"]))]

			refA = teststores.copy(deep=True)
			refB = stores_master_df.copy(deep=True)

			useA = refA[store_features].copy(deep=True)
			useB = refB[store_features].copy(deep=True)

			scaler = StandardScaler()
			scale_cols = [item for item in store_features if item!="Banner"]
			useA[scale_cols] = scaler.fit_transform(useA[scale_cols])
			useB[scale_cols] = scaler.fit_transform(useB[scale_cols])

			gowermatrix = gower.gower_matrix(useA,useB)

			# Identifying similar stores
			df_list = list()
			for test_pid,row in zip(refA["Partner ID"],gowermatrix):
				df = refB.copy(deep=True)
				df["Gower_Distance"] = list(row)
				df = df.sort_values(by="Gower_Distance",ascending=True)
				df["Test store Partner ID"] = test_pid
				df["Gower_Distance"] = df["Gower_Distance"].apply(lambda x:round(x,2))
				df["Similarity Measure"] = df["Gower_Distance"].apply(lambda x: 1-x)
				df_list.append(df.head(1))
			control_stores = pd.concat(df_list)
			control_stores["Checked_Flag"] = 0
			finalcontrol_stores = control_stores.reset_index().to_json(orient='records')			
			return json.Response(finalcontrol_stores,True)
		else:
			return json.Response("Please pass Test stores",False)
	    

def check_if_store_valid(storesfile=None):
    stores_master_df = storesfile.copy(deep=True)
    
    stores_master_df["Is Valid Store"] = 1
    # Valid or Invalid Stores Flags
    stores_master_df.loc[(stores_master_df["Outlet_surface"].isin([0])),"Is Valid Store"] = 0
    stores_master_df.loc[(stores_master_df["Outlet_surface"].isna()),"Is Valid Store"] = 0    
    stores_master_df.loc[(stores_master_df["CSV_of_outlet"].isin([0])),"Is Valid Store"] = 0
    stores_master_df.loc[(stores_master_df["CSV_of_outlet"].isna()),"Is Valid Store"] =0    
    stores_master_df.loc[stores_master_df["Shelf_meters_Choc"].isin(["(NA)"]),"Is Valid Store"] = 0    
    stores_master_df.loc[stores_master_df["Shelf_meters_Dog"].isin(["(NA)"]),"Is Valid Store"] = 0    
    stores_master_df.loc[stores_master_df["Shelf_meters_Cat"].isin(["(NA)"]),"Is Valid Store"] = 0    
    stores_master_df.loc[stores_master_df["Influence_Chocolate"].isna(),"Is Valid Store"] = 0
    stores_master_df.loc[stores_master_df["Influence_Petcare"].isna(),"Is Valid Store"] = 0
    stores_master_df.loc[stores_master_df["Influence_Overall"].isna(),"Is Valid Store"] = 0    
    invalid_stores = stores_master_df[stores_master_df["Is Valid Store"]==0]
    stores_master_df = stores_master_df[stores_master_df["Is Valid Store"]==1]
    
    # Type conversions and Formatting
    stores_master_df["Outlet_surface"] = stores_master_df["Outlet_surface"].astype("float")    
    stores_master_df["CSV_of_outlet"] = stores_master_df["CSV_of_outlet"].astype("float")    
    stores_master_df["Shelf_meters_Choc"] = stores_master_df["Shelf_meters_Choc"].apply(lambda x:int(str(x)[:-1]))    
    stores_master_df["Shelf_meters_Dog"] = stores_master_df["Shelf_meters_Dog"].apply(lambda x: x.replace(",","."))
    stores_master_df["Shelf_meters_Dog"] = stores_master_df["Shelf_meters_Dog"].apply(lambda x:float(str(x)[:-1]))    
    stores_master_df["Shelf_meters_Cat"] = stores_master_df["Shelf_meters_Cat"].apply(lambda x: x.replace(",","."))
    stores_master_df["Shelf_meters_Cat"] = stores_master_df["Shelf_meters_Cat"].apply(lambda x:float(str(x)[:-1]))
    
    stores_master_df = pd.concat([stores_master_df,invalid_stores])
    
    return stores_master_df 


# class IdentifyControlStore(generics.ListCreateAPIView):
# 	# def control_store_summary(test_control_mapping_stores=None,compare_variables=[]):
# 	def post(self,request):
# 		request = self.request.data
# 		stores = request['data']['control_mapping']
# 		compare_variables = request['data']['compare_variables']

# 		test_control_mapping_stores = pd.DataFrame.from_dict(stores, orient='columns')

# 		if ((test_control_mapping_stores is not None) & (compare_variables is not None) & (len(compare_variables) != 0)):
	        
# 			# Converting list of jsons to Dataframe
# 			null=np.nan
# 			test_control_mapping_stores = pd.DataFrame(test_control_mapping_stores)

# 			# Create variables
# 			variables_metrics_dict = {}
# 			# Stores Master File
# 			stores_master_df = pd.read_excel("datas/TL_StoreMstr.xlsx")
# 			stores_master_df = check_if_store_valid(storesfile=stores_master_df)

# 			test_stores = stores_master_df[stores_master_df["Partner ID"].isin(test_control_mapping_stores["Test store Partner ID"])]
# 			control_stores = stores_master_df.merge(test_control_mapping_stores[["Partner ID","Banner"]],on=["Partner ID","Banner"])
	        
# 			for col in compare_variables:
# 				variables_metrics_dict[col] = {}
# 				tStat, pVal = stats.ttest_ind(test_stores[col],control_stores[col],nan_policy='omit') 	            
# 				variables_metrics_dict[col]["Test Mean"] = round(test_stores[col].mean(),2)
# 				variables_metrics_dict[col]["Control Mean"] = round(control_stores[col].mean(),2)
# 				variables_metrics_dict[col]["Test Std Dev"] = round(test_stores[col].std(),2)
# 				variables_metrics_dict[col]["Control Std Dev"] = round(control_stores[col].std(),2)

# 			return json.Response(variables_metrics_dict,True)
	    
# 		else:
# 			return json.Response("Please pass appropriate parameters",False)
