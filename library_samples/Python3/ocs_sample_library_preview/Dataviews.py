# Dataviews.py
#
# Copyright 2019 OSIsoft, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# <http://www.apache.org/licenses/LICENSE-2.0>
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



from urllib.parse import urlparse
import urllib.request, urllib.parse, urllib.error
import http.client as http
import json

from .SdsError import SdsError
from .Dataview.Dataview import Dataview
from .Dataview.Datagroup import Datagroup 
from .BaseClient import BaseClient as BaseClient

import requests


class Dataviews(object):
    """Handles communication with Sds Service"""

    def __init__(self, client):
        self.__baseClient = client
        self.__setPathAndQueryTemplates()
   
    def postDataview(self, namespace_id, dataview):
        """Tells Sds Service to create a dataview based on local 'dataview' or get if existing dataview matches"""
        if namespace_id is None:
            raise TypeError
        if dataview is None or not isinstance(dataview, Dataview):
            raise TypeError		
		
        response = requests.post(
            self.__baseClient.uri_API + self.__dataviewPath.format(tenant_id=self.__baseClient.tenant, namespace_id=namespace_id, dataview_id=dataview.Id),
            data=dataview.toJson(), 
            headers= self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError(
                "Failed to create dataview, {dataview_id}. {status}:{reason}".format(dataview_id=dataview.Id, status=response.status_code, reason=response.text))
		
        dataview = Dataview.fromJson(json.loads(response.content))
        response.close()
        return dataview
		
    def putDataview(self, namespace_id, dataview):
        """Tells Sds Service to update a dataview based on local 'dataview'"""
        if namespace_id is None:
            raise TypeError
        if dataview is None or not isinstance(dataview, Dataview):
            raise TypeError
        response = requests.put(
            self.__baseClient.uri_API + self.__dataviewPath.format(tenant_id=self.__baseClient.tenant, namespace_id=namespace_id, dataview_id=dataview.Id),
            data=dataview.toJson(), 
            headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError(
                "Failed to update dataview, {dataview_id}. {status}:{reason}".format(dataview_id=dataview.Id, status=response.status_code, reason=response.text))
        
        dataview = Dataview.fromJson(json.loads(response.content))
        response.close()
        return dataview
		
				
    def deleteDataview(self, namespace_id, dataview_id):
        """Tells Sds Service to delete a dataview based on 'dataview_id'"""
        if namespace_id is None:
            raise TypeError
        if dataview_id is None:
            raise TypeError
	
        response = requests.delete(
            self.__baseClient.uri_API + self.__dataviewPath.format(tenant_id=self.__baseClient.tenant, namespace_id=namespace_id, dataview_id=dataview_id),
            headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError(
                "Failed to delete dataview, {dataview_id}. {status}:{reason}".format(dataview_id=dataview_id, status=response.status_code, reason=response.text))
        
        response.close()
        return
		
		
    def getDataview(self, namespace_id, dataview_id):
        """Retrieves the dataview specified by 'dataview_id' from Sds Service"""
        if namespace_id is None:
            raise TypeError
        if dataview_id is None:
            raise TypeError

        response = requests.get(
            self.__baseClient.uri_API + self.__dataviewPath.format(tenant_id=self.__baseClient.tenant, namespace_id=namespace_id, dataview_id=dataview_id),
            headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get dataview, {dataview_id}. {status}:{reason}".
                          format(dataview_id=dataview_id, status=response.status_code, reason=response.text))

        dataview = Dataview.fromJson(json.loads(response.content))
        response.close()
        return dataview
		
    def getDataviews(self, namespace_id, skip = 0, count =100):
        """Retrieves all of the dataviews from Sds Service"""
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__baseClient.uri_API + self.__getDataviews.format(tenant_id=self.__baseClient.tenant, namespace_id=namespace_id, skip=skip, count=count),
            headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get dataviews. {status}:{reason}".
                          format( status=response.status_code, reason=response.text))
        
        dataviews = json.loads(response.content)
        results = []
        for t in dataviews:
            results.append(Dataview.fromJson(t))
        response.close()
        return results
		
		
    def getDatagroups(self, namespace_id,dataview_id, skip = 0, count = 100):
        """Retrieves all of the datagroups from the specified dataview from Sds Service"""
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__baseClient.uri_API + self.__getDatagroups.format(tenant_id=self.__baseClient.tenant, namespace_id=namespace_id, dataview_id=dataview_id, skip=skip, count=count),
            headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get datagroups for dataview, . {status}:{reason}".
                          format(dataview_id=dataview_id, status=response.status_code, reason=response.text))
        
        datagroups = json.loads(response.content)   


        results = {}
        for key, value in datagroups.items():
            innerobj = {}
            for key2, value2 in value.items():
                innerobj[key2] = Datagroup.fromJson(value2)
            results[key] = innerobj
        response.close()

        return results
		
		
    def getDatagroup(self, namespace_id,dataview_id, datagroup_id):
        """Retrieves a datagroupby 'datagroup_id' from the specified dataview from Sds Service"""
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__baseClient.uri_API + self.__getDatagroup.format(tenant_id=self.__baseClient.tenant, namespace_id=namespace_id, dataview_id=dataview_id, datagroup_id=datagroup_id),
            headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get datagroup for dataview, . {status}:{reason}".
                          format(dataview_id=dataview_id, status=response.status_code, reason=response.text))
        

        datagroup = Datagroup.fromJson(json.loads(response.content))
        return datagroup
	
#needs other parameters with smart 
    def getDataviewPreview(self, namespace_id, dataview_id, startIndex = None, endIndex = None, interval = None, form = None, count = -1, value_class = None):
        """Retrieves the dataviewpreview of the 'dataview_id' from Sds Service"""
        if namespace_id is None:
            raise TypeError
        if dataview_id is None:
            raise TypeError

        urlAdd = []
        urlAddStr = ""
        
        if startIndex is not None:
            urlAdd.append("startIndex=" +startIndex)
        if endIndex is not None:
            urlAdd.append("endIndex=" +endIndex)
        if interval is not None:
            urlAdd.append("interval=" +interval)
        if form is not None:
            urlAdd.append("form=" +form)
        if count != -1:
            urlAdd.append("count=" + str(count))
        if len(urlAdd) != 0:
            urlAddStr = "?" + '&'.join(str(x) for x in urlAdd)
        
        
        response = requests.get(
            self.__baseClient.uri_API + self.__getDataviewPreview.format(tenant_id=self.__baseClient.tenant, namespace_id=namespace_id, dataview_id=dataview_id) + urlAddStr, 
            headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get dataview preview for dataview {dataview_id}. {status}:{reason}".
                          format(dataview_id=dataview_id, status=response.status_code, reason=response.text))

        content = json.loads(response.content)
        response.close()
		
        if value_class is None:
            return (content)
        return value_class.fromJson(content)
		
    def getDataInterpolated(self, namespace_id, dataview_id, skip = -1, count = -1, form = None, sessionId = -1,  value_class = None):
        """Retrieves the dataviewpreview of the 'dataview_id' from Sds Service"""
        if namespace_id is None:
            raise TypeError
        if dataview_id is None:
            raise TypeError

        urlAdd = []
        urlAddStr = ""
        if count != -1:
            urlAdd.append("count=" + str(count))
        if skip != -1:
            urlAdd.append("skip=" + str(count))        
        if form is not None:
            urlAdd.append("form=" +form)
        if sessionId != -1:
            urlAdd.append("sessionId=" + str(count))
        if len(urlAdd) != 0:
            urlAddStr = "?" + '&'.join(str(x) for x in urlAdd)
        
        
        response = requests.get(
            self.__baseClient.uri_API + self.__getDataInterpolated.format(tenant_id=self.__baseClient.tenant, namespace_id=namespace_id, dataview_id=dataview_id) + urlAddStr, 
            headers=self.__baseClient.sdsHeaders())
        if response.status_code < 200 or response.status_code >= 300:
            response.close()
            raise SdsError("Failed to get dataview data interpolated for dataview {dataview_id}. {status}:{reason}".
                          format(dataview_id=dataview_id, status=response.status_code, reason=response.text))
                          
        if(form is not None):
            return response.content.decode("utf-8") 

        content = json.loads(response.content)
        response.close()
		
        if value_class is None:
            return (content)
        return value_class.fromJson(content)
		

    def __setPathAndQueryTemplates(self):
        self.__basePath = "/Tenants/{tenant_id}/Namespaces/{namespace_id}"
              
        self.__dataviewsPath = self.__basePath + "/Dataviews"
        self.__getDataviews= self.__dataviewsPath + "?skip={skip}&count={count}"
        self.__dataviewPath = self.__dataviewsPath + "/{dataview_id}"
        self.__datagroupPath= self.__dataviewPath + "/Datagroups"
        self.__getDatagroup = self.__datagroupPath + "/{datagroup_id}"
        self.__getDatagroups = self.__datagroupPath + "?skip={skip}&count={count}"
        self.__getDataviewPreview = self.__dataviewPath + "/preview/interpolated"
        self.__getDataInterpolated= self.__dataviewPath + "/data/interpolated"