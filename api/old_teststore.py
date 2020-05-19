import math
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import norm
from django.http import HttpResponse
from .serializers import *
from .models import *
from . import json
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.core import serializers
from rest_framework import generics
from django.views.generic import ListView,View


class GetTestParameter(generics.ListCreateAPIView):
	# def get_test_parameter(confidence_level=None,margin_of_error=None,test_duration_weeks=None,num_test_stores=None):
	def post(self,request):	

		import json as j 	
		data = j.loads(request.body)
		datas = data['data']
		if 'confidence_level' in datas:
			confidence_level 		= datas['confidence_level']
		else:
			confidence_level = None

		if 'margin_of_error' in datas:
			margin_of_error  		= datas['margin_of_error']
		else:
			margin_of_error = None

		if 'test_duration_weeks' in datas:
			test_duration_weeks     = datas['test_duration_weeks']	        					
		else:
			test_duration_weeks = None
			
		if 'num_test_stores' in datas:
			num_test_stores   	= datas['num_test_stores']
		else:
			num_test_stores =None

		standard_deviation = 521.2839825
		mean_value = 1224.386856

		if sum([v is not None for v in [confidence_level,margin_of_error,test_duration_weeks,num_test_stores]])>=3:
			if confidence_level is None:
				value1 = num_test_stores*test_duration_weeks
				confidence_level = round(1 - 2*(1 - norm.cdf(np.sqrt(value1/2) * ( margin_of_error * mean_value )/standard_deviation)),2)
				test_parameter = confidence_level

			if margin_of_error is None:
				value1 = num_test_stores*test_duration_weeks
				margin_of_error = round(norm.ppf((1 - ( 1 - confidence_level ) / 2)) * standard_deviation / ( np.sqrt(value1/2) * mean_value ),2)
				test_parameter = margin_of_error

			if test_duration_weeks is None:
				value1 = 2 * np.power(norm.ppf((1 - ( 1 - confidence_level ) / 2)) * standard_deviation / ( margin_of_error * mean_value ),2)
				test_duration_weeks = math.ceil(value1/num_test_stores)
				test_parameter = test_duration_weeks

			if num_test_stores is None:
				value1 = 2 * np.power(norm.ppf((1 - ( 1 - confidence_level ) / 2)) * standard_deviation / ( margin_of_error * mean_value ),2)
				num_test_stores = math.ceil(value1/test_duration_weeks)
				test_parameter = num_test_stores
		else:
        	# test_parameter = "Enter atleast three parameters"
			return json.Response("Enter atleast three parameters", False)
    
		return json.Response(test_parameter, True) 




class IdentifyStores(generics.ListCreateAPIView):
		# def identify_test_stores(test_name="",type_of_test="",banners=[],segments=[],store_segments=[],segment_variables=[]):
		
		# Sample Inputs
		
		# # Schema of parameters to be passed into the function
		# test_name = "Test 1"
		# type_of_test = "Duration Test"
		# banners = ["Albert Heijn","Jumbo"]
		# segments = ["High-High"]
		# store_segments = ["Supermarket Large"]
		# segment_variables = ["Banner"]

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

		#Read the files
		stores_master_df = pd.read_excel("TL_StoreMstr.xlsx")
		test_master_df = pd.read_excel("TL_TestMstr.xlsx")
		teststore_map_df = pd.read_excel("TL_Teststore_map.xlsx")
		controlstore_map_df = pd.read_excel("TL_Controlstore_Mstr.xlsx")

		# Validating Input Parameters (Ex: If banners are not provided, we consider all the banners from the population )
		if len(banners) == 0:
			banners = stores_master_df["Banner"].unique().tolist()
		if len(segments) == 0:
			segments = stores_master_df["Overall Segment"].unique().tolist()
		if len(store_segments) == 0:
			store_segments = stores_master_df["Overall Segment"].unique().tolist()
		if len(segment_variables) == 0:
			segment_variables = ["Banner"] 

		# Create filters
		banner_filter = (stores_master_df["Banner"].isin(banners))
		segment_filter = (stores_master_df["Overall Segment"].isin(segments))
		store_segment_filter = (stores_master_df["Segment (Based on Outlet Surface Area)"].isin(store_segments))
		# Filter the stores only from the input filters
		stores_master_df = stores_master_df[banner_filter & segment_filter & store_segment_filter]
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
			return json.Response('No active Test', False)
		
		return json.Response(stores_master_df, True)

		
class StoreSummary(generics.ListCreateAPIView):
	
	def get(self,serializer):
		# Get banner wise no of stores
		test_stores_summary = test_stores.groupby("Banner")["Partner ID"].count().to_dict()
		return json.Response(test_stores_summary, True) 


class ValidateTeststore(generics.ListCreateAPIView):
	# def validate_test_stores(test_stores=None,compare_variables=[]):

	def post(self,request):			
		import json as j 	
		data = j.loads(request.body)
		datas = data['data']
		test_stores = datas['test_stores']
		compare_variables = datas['compare_variables']
    
		variables_pvalue_dict = {}
		#Read the files
		stores_master_df = pd.read_excel("TL_StoreMstr.xlsx")
		if (test_stores is not None) & (len(compare_variables) != 0):
			for col in compare_variables:
				tStat, pVal = stats.ttest_ind(stores_master_df[col],test_stores[col],nan_policy='omit') 
				variables_pvalue_dict[col] = round(pVal,2)
		else:
			return json.Response('Please pass appropriate parameters', False)
	    
		return json.Response(variables_pvalue_dict, True) 
