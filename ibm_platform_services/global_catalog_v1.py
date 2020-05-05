# coding: utf-8

# (C) Copyright IBM Corp. 2020.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
The catalog service manages offerings across geographies as the system of record. The
catalog supports a RESTful API where users can retrieve information about existing
offerings and create, manage, and delete their offerings. Start with the base URL and use
the endpoints to retrieve metadata about services in the catalog and manage service
visbility. Depending on the kind of object, the metadata can include information about
pricing, provisioning, regions, and more. For more information, see the [catalog
documentation](https://cloud.ibm.com/docs/overview/catalog.html#global-catalog-overview).
"""

from datetime import datetime
from enum import Enum
from typing import BinaryIO, Dict, List
import json

from ibm_cloud_sdk_core import BaseService, DetailedResponse
from ibm_cloud_sdk_core.authenticators.authenticator import Authenticator
from ibm_cloud_sdk_core.get_authenticator import get_authenticator_from_environment
from ibm_cloud_sdk_core.utils import convert_model, datetime_to_string, string_to_datetime

from .common import get_sdk_headers

##############################################################################
# Service
##############################################################################

class GlobalCatalogV1(BaseService):
    """The Global Catalog V1 service."""

    DEFAULT_SERVICE_URL = 'https://globalcatalog.cloud.ibm.com/api/v1'
    DEFAULT_SERVICE_NAME = 'global_catalog'

    @classmethod
    def new_instance(cls,
                     service_name: str = DEFAULT_SERVICE_NAME,
                    ) -> 'GlobalCatalogV1':
        """
        Return a new client for the Global Catalog service using the specified
               parameters and external configuration.
        """
        authenticator = get_authenticator_from_environment(service_name)
        service = cls(
            authenticator
            )
        service.configure_service(service_name)
        return service

    def __init__(self,
                 authenticator: Authenticator = None,
                ) -> None:
        """
        Construct a new client for the Global Catalog service.

        :param Authenticator authenticator: The authenticator specifies the authentication mechanism.
               Get up to date information from https://github.com/IBM/python-sdk-core/blob/master/README.md
               about initializing the authenticator of your choice.
        """
        BaseService.__init__(self,
                             service_url=self.DEFAULT_SERVICE_URL,
                             authenticator=authenticator)


    #########################
    # Object
    #########################


    def list_catalog_entries(self,
        *,
        account: str = None,
        include: str = None,
        q: str = None,
        sort_by: str = None,
        descending: str = None,
        languages: str = None,
        complete: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Returns parent catalog entries.

        Includes key information, such as ID, name, kind, CRN, tags, and provider. This
        endpoint is ETag enabled.

        :param str account: (optional) This changes the scope of the request
               regardless of the authorization header. Example scopes are `account` and
               `global`. `account=global` is reqired if operating with a service ID that
               has a global admin policy, for example `GET /?account=global`.
        :param str include: (optional) A GET call by default returns a basic set of
               properties. To include other properties, you must add this parameter. A
               wildcard (`*`) includes all properties for an object, for example `GET
               /?include=*`. To include specific metadata fields, separate each field with
               a colon (:), for example `GET /?include=metadata.ui:metadata.pricing`.
        :param str q: (optional) Searches the catalog entries for keywords. Add
               filters to refine your search. A query filter, for example, `q=kind:iaas
               service_name rc:true`, filters entries of kind iaas with
               metadata.service.rc_compatible set to true and  have a service name is in
               their name, display name, or description.  Valid tags are
               **kind**:<string>, **tag**:<strging>, **rc**:[true|false],
               **iam**:[true|false], **active**:[true|false], **geo**:<string>, and
               **price**:<string>.
        :param str sort_by: (optional) The field on which the output is sorted.
               Sorts by default by **name** property. Available fields are **name**,
               **displayname** (overview_ui.display_name), **kind**, **provider**
               (provider.name), **sbsindex** (metadata.ui.side_by_side_index), and the
               time **created**, and **updated**.
        :param str descending: (optional) Sets the sort order. The default is
               false, which is ascending.
        :param str languages: (optional) Return the data strings in a specified
               langauge. By default, the strings returned are of the language preferred by
               your browser through the Accept-Langauge header, which allows an override
               of the header. Languages are specified in standard form, such as `en-us`.
               To include all languages use a wildcard (*).
        :param str complete: (optional) Returns all available fields for all
               languages. Use the value `?complete=true` as shortcut for
               ?include=*&languages=*.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `EntrySearchResult` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_catalog_entries')
        headers.update(sdk_headers)

        params = {
            'account': account,
            'include': include,
            'q': q,
            'sort-by': sort_by,
            'descending': descending,
            'languages': languages,
            'complete': complete
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        url = '/'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def create_catalog_entry(self,
        name: str,
        kind: str,
        overview_ui: 'OverviewUI',
        images: 'Image',
        disabled: bool,
        tags: List[str],
        provider: 'Provider',
        id: str,
        *,
        parent_id: str = None,
        group: bool = None,
        active: bool = None,
        metadata: 'ObjectMetadataSet' = None,
        account: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Create a catalog entry.

        The created catalog entry is restricted by default. You must have an administrator
        or editor role in the scope of the provided token. This API will return an ETag
        that can be used for standard ETag processing, except when depth query is used.

        :param str name: Programmatic name for this catalog entry, which must be
               formatted like a CRN segment. See the display name in OverviewUI for a
               user-readable name.
        :param str kind: The type of catalog entry, **service**, **template**,
               **dashboard**, which determines the type and shape of the object.
        :param OverviewUI overview_ui: Overview is nested in the top level. The key
               value pair is `[_language_]overview_ui`.
        :param Image images: Image annotation for this catalog entry. The image is
               a URL.
        :param bool disabled: Boolean value that determines the global visibility
               for the catalog entry, and its children. If it is not enabled, all plans
               are disabled.
        :param List[str] tags: A list of tags. For example, IBM, 3rd Party, Beta,
               GA, and Single Tenant.
        :param Provider provider: Information related to the provider associated
               with a catalog entry.
        :param str id: Catalog entry's unique ID. It's the same across all catalog
               instances.
        :param str parent_id: (optional) The ID of the parent catalog entry if it
               exists.
        :param bool group: (optional) Boolean value that determines whether the
               catalog entry is a group.
        :param bool active: (optional) Boolean value that describes whether the
               service is active.
        :param ObjectMetadataSet metadata: (optional) Model used to describe
               metadata object that can be set.
        :param str account: (optional) This changes the scope of the request
               regardless of the authorization header. Example scopes are `account` and
               `global`. `account=global` is reqired if operating with a service ID that
               has a global admin policy, for example `GET /?account=global`.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `CatalogEntry` object
        """

        if name is None:
            raise ValueError('name must be provided')
        if kind is None:
            raise ValueError('kind must be provided')
        if overview_ui is None:
            raise ValueError('overview_ui must be provided')
        if images is None:
            raise ValueError('images must be provided')
        if disabled is None:
            raise ValueError('disabled must be provided')
        if tags is None:
            raise ValueError('tags must be provided')
        if provider is None:
            raise ValueError('provider must be provided')
        if id is None:
            raise ValueError('id must be provided')
        overview_ui = convert_model(overview_ui)
        images = convert_model(images)
        provider = convert_model(provider)
        if metadata is not None:
            metadata = convert_model(metadata)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='create_catalog_entry')
        headers.update(sdk_headers)

        params = {
            'account': account
        }

        data = {
            'name': name,
            'kind': kind,
            'overview_ui': overview_ui,
            'images': images,
            'disabled': disabled,
            'tags': tags,
            'provider': provider,
            'id': id,
            'parent_id': parent_id,
            'group': group,
            'active': active,
            'metadata': metadata
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        url = '/'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       params=params,
                                       data=data)

        response = self.send(request)
        return response


    def get_catalog_entry(self,
        id: str,
        *,
        account: str = None,
        include: str = None,
        languages: str = None,
        complete: str = None,
        depth: int = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get a specific catalog object.

        This endpoint returns a specific catalog entry using the object's unique
        identifier, for example `/_*service_name*?complete=true`. This endpoint is ETag
        enabled.

        :param str id: The catalog entry's unqiue ID.
        :param str account: (optional) This changes the scope of the request
               regardless of the authorization header. Example scopes are `account` and
               `global`. `account=global` is reqired if operating with a service ID that
               has a global admin policy, for example `GET /?account=global`.
        :param str include: (optional) A GET call by default returns a basic set of
               properties. To include other properties, you must add this parameter. A
               wildcard (`*`) includes all properties for an object, for example `GET
               /id?include=*`. To include specific metadata fields, separate each field
               with a colon (:), for example `GET
               /id?include=metadata.ui:metadata.pricing`.
        :param str languages: (optional) Return the data strings in the specified
               langauge. By default the strings returned are of the language preferred by
               your browser through the Accept-Langauge header, which allows an override
               of the header. Languages are specified in standard form, such as `en-us`.
               To include all languages use a wildcard (*).
        :param str complete: (optional) Returns all available fields for all
               languages. Use the value `?complete=true` as shortcut for
               ?include=*&languages=*.
        :param int depth: (optional) Return the children down to the requested
               depth. Use * to include the entire children tree. If there are more
               children than the maximum permitted an error will be returned. Be judicious
               with this as it can cause a large number of database accesses and can
               result in a large amount of data returned.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `CatalogEntry` object
        """

        if id is None:
            raise ValueError('id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_catalog_entry')
        headers.update(sdk_headers)

        params = {
            'account': account,
            'include': include,
            'languages': languages,
            'complete': complete,
            'depth': depth
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        url = '/{0}'.format(
            *self.encode_path_vars(id))
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def update_catalog_entry(self,
        id: str,
        name: str,
        kind: str,
        overview_ui: 'OverviewUI',
        images: 'Image',
        disabled: bool,
        tags: List[str],
        provider: 'Provider',
        *,
        parent_id: str = None,
        group: bool = None,
        active: bool = None,
        metadata: 'ObjectMetadataSet' = None,
        account: str = None,
        move: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Update a catalog entry.

        Update a catalog entry. The visibility of the catalog entry cannot be modified
        with this endpoint. You must be an administrator or editor in the scope of the
        provided token. This endpoint is ETag enabled.

        :param str id: The object's unique ID.
        :param str name: Programmatic name for this catalog entry, which must be
               formatted like a CRN segment. See the display name in OverviewUI for a
               user-readable name.
        :param str kind: The type of catalog entry, **service**, **template**,
               **dashboard**, which determines the type and shape of the object.
        :param OverviewUI overview_ui: Overview is nested in the top level. The key
               value pair is `[_language_]overview_ui`.
        :param Image images: Image annotation for this catalog entry. The image is
               a URL.
        :param bool disabled: Boolean value that determines the global visibility
               for the catalog entry, and its children. If it is not enabled, all plans
               are disabled.
        :param List[str] tags: A list of tags. For example, IBM, 3rd Party, Beta,
               GA, and Single Tenant.
        :param Provider provider: Information related to the provider associated
               with a catalog entry.
        :param str parent_id: (optional) The ID of the parent catalog entry if it
               exists.
        :param bool group: (optional) Boolean value that determines whether the
               catalog entry is a group.
        :param bool active: (optional) Boolean value that describes whether the
               service is active.
        :param ObjectMetadataSet metadata: (optional) Model used to describe
               metadata object that can be set.
        :param str account: (optional) This changes the scope of the request
               regardless of the authorization header. Example scopes are `account` and
               `global`. `account=global` is reqired if operating with a service ID that
               has a global admin policy, for example `GET /?account=global`.
        :param str move: (optional) Reparenting object. In the body set the
               parent_id to a different parent. Or remove the parent_id field to reparent
               to the root of the catalog. If this is not set to 'true' then changing the
               parent_id in the body of the request will not be permitted. If this is
               'true' and no change to parent_id then this is also error. This is to
               prevent accidental changing of parent.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `CatalogEntry` object
        """

        if id is None:
            raise ValueError('id must be provided')
        if name is None:
            raise ValueError('name must be provided')
        if kind is None:
            raise ValueError('kind must be provided')
        if overview_ui is None:
            raise ValueError('overview_ui must be provided')
        if images is None:
            raise ValueError('images must be provided')
        if disabled is None:
            raise ValueError('disabled must be provided')
        if tags is None:
            raise ValueError('tags must be provided')
        if provider is None:
            raise ValueError('provider must be provided')
        overview_ui = convert_model(overview_ui)
        images = convert_model(images)
        provider = convert_model(provider)
        if metadata is not None:
            metadata = convert_model(metadata)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='update_catalog_entry')
        headers.update(sdk_headers)

        params = {
            'account': account,
            'move': move
        }

        data = {
            'name': name,
            'kind': kind,
            'overview_ui': overview_ui,
            'images': images,
            'disabled': disabled,
            'tags': tags,
            'provider': provider,
            'parent_id': parent_id,
            'group': group,
            'active': active,
            'metadata': metadata
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        url = '/{0}'.format(
            *self.encode_path_vars(id))
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       params=params,
                                       data=data)

        response = self.send(request)
        return response


    def delete_catalog_entry(self,
        id: str,
        *,
        account: str = None,
        force: bool = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete a catalog entry.

        Delete a catalog entry. This will archive the catalog entry for a minimum of two
        weeks. While archived, it can be restored using the PUT restore API. After two
        weeks, it will be deleted and cannot be restored. You must have administrator role
        in the scope of the provided token to modify it. This endpoint is ETag enabled.

        :param str id: The object's unique ID.
        :param str account: (optional) This changes the scope of the request
               regardless of the authorization header. Example scopes are `account` and
               `global`. `account=global` is reqired if operating with a service ID that
               has a global admin policy, for example `GET /?account=global`.
        :param bool force: (optional) This will cause entry to be deleted fully. By
               default it is archived for two weeks, so that it can be restored if
               necessary.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if id is None:
            raise ValueError('id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='delete_catalog_entry')
        headers.update(sdk_headers)

        params = {
            'account': account,
            'force': force
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        url = '/{0}'.format(
            *self.encode_path_vars(id))
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def get_child_objects(self,
        id: str,
        kind: str,
        *,
        account: str = None,
        include: str = None,
        q: str = None,
        sort_by: str = None,
        descending: str = None,
        languages: str = None,
        complete: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get child catalog entries of a specific kind.

        Fetch child catalog entries for a catalog entry with a specific id. This endpoint
        is ETag enabled.

        :param str id: The parent catalog entry's ID.
        :param str kind: The **kind** of child catalog entries to search for. A
               wildcard (*) includes all child catalog entries for all kinds, for example
               `GET /service_name/_*`.
        :param str account: (optional) This changes the scope of the request
               regardless of the authorization header. Example scopes are `account` and
               `global`. `account=global` is reqired if operating with a service ID that
               has a global admin policy, for example `GET /?account=global`.
        :param str include: (optional) A colon (:) separated list of properties to
               include. A GET call by defaults return a limited set of properties. To
               include other properties, you must add the include parameter.  A wildcard
               (*) includes all properties.
        :param str q: (optional) A query filter, for example, `q=kind:iaas IBM`
               will filter on entries of **kind** iaas that has `IBM` in their name,
               display name, or description.
        :param str sort_by: (optional) The field on which to sort the output. By
               default by name. Available fields are **name**, **kind**, and **provider**.
        :param str descending: (optional) The sort order. The default is false,
               which is ascending.
        :param str languages: (optional) Return the data strings in the specified
               langauge. By default the strings returned are of the language preferred by
               your browser through the Accept-Langauge header. This allows an override of
               the header. Languages are specified in standard form, such as `en-us`. To
               include all languages use the wildcard (*).
        :param str complete: (optional) Use the value `?complete=true` as shortcut
               for ?include=*&languages=*.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `List[EntrySearchResult]` result
        """

        if id is None:
            raise ValueError('id must be provided')
        if kind is None:
            raise ValueError('kind must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_child_objects')
        headers.update(sdk_headers)

        params = {
            'account': account,
            'include': include,
            'q': q,
            'sort-by': sort_by,
            'descending': descending,
            'languages': languages,
            'complete': complete
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        url = '/{0}/{1}'.format(
            *self.encode_path_vars(id, kind))
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def restore_catalog_entry(self,
        id: str,
        *,
        account: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Restore archived catalog entry.

        Restore an archived catalog entry. You must have an administrator role in the
        scope of the provided token.

        :param str id: The catalog entry's unique ID.
        :param str account: (optional) This changes the scope of the request
               regardless of the authorization header. Example scopes are `account` and
               `global`. `account=global` is reqired if operating with a service ID that
               has a global admin policy, for example `GET /?account=global`.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if id is None:
            raise ValueError('id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='restore_catalog_entry')
        headers.update(sdk_headers)

        params = {
            'account': account
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        url = '/{0}/restore'.format(
            *self.encode_path_vars(id))
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response

    #########################
    # Visibility
    #########################


    def get_visibility(self,
        id: str,
        *,
        account: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the visibility constraints for an object.

        This endpoint returns the visibility rules for this object. Overall visibility is
        determined by the parent objects and any further restrictions on this object. You
        must have an administrator role in the scope of the provided token. This endpoint
        is ETag enabled.

        :param str id: The object's unique ID.
        :param str account: (optional) This changes the scope of the request
               regardless of the authorization header. Example scopes are `account` and
               `global`. `account=global` is reqired if operating with a service ID that
               has a global admin policy, for example `GET /?account=global`.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `Visibility` object
        """

        if id is None:
            raise ValueError('id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_visibility')
        headers.update(sdk_headers)

        params = {
            'account': account
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        url = '/{0}/visibility'.format(
            *self.encode_path_vars(id))
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def update_visibility(self,
        id: str,
        *,
        include: 'VisibilityDetail' = None,
        exclude: 'VisibilityDetail' = None,
        account: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Update visibility.

        Update an Object's Visibility. You must have an administrator role in the scope of
        the provided token. This endpoint is ETag enabled.

        :param str id: The object's unique ID.
        :param VisibilityDetail include: (optional) Visibility details related to a
               catalog entry.
        :param VisibilityDetail exclude: (optional) Visibility details related to a
               catalog entry.
        :param str account: (optional) This changes the scope of the request
               regardless of the authorization header. Example scopes are `account` and
               `global`. `account=global` is reqired if operating with a service ID that
               has a global admin policy, for example `GET /?account=global`.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if id is None:
            raise ValueError('id must be provided')
        if include is not None:
            include = convert_model(include)
        if exclude is not None:
            exclude = convert_model(exclude)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='update_visibility')
        headers.update(sdk_headers)

        params = {
            'account': account
        }

        data = {
            'include': include,
            'exclude': exclude
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        url = '/{0}/visibility'.format(
            *self.encode_path_vars(id))
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       params=params,
                                       data=data)

        response = self.send(request)
        return response

    #########################
    # Pricing
    #########################


    def get_pricing(self,
        id: str,
        *,
        account: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the pricing for an object.

        This endpoint returns the pricing for an object. Static pricing is defined in the
        catalog. Dynamic pricing is stored in Bluemix Pricing Catalog.

        :param str id: The object's unique ID.
        :param str account: (optional) This changes the scope of the request
               regardless of the authorization header. Example scopes are `account` and
               `global`. `account=global` is reqired if operating with a service ID that
               has a global admin policy, for example `GET /?account=global`.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `PricingGet` object
        """

        if id is None:
            raise ValueError('id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_pricing')
        headers.update(sdk_headers)

        params = {
            'account': account
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        url = '/{0}/pricing'.format(
            *self.encode_path_vars(id))
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response

    #########################
    # Audit
    #########################


    def get_audit_logs(self,
        id: str,
        *,
        account: str = None,
        ascending: str = None,
        startat: str = None,
        offset: int = None,
        limit: int = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get the audit logs for an object.

        This endpoint returns the audit logs for an object. Only administrators and
        editors can get logs.

        :param str id: The object's unique ID.
        :param str account: (optional) This changes the scope of the request
               regardless of the authorization header. Example scopes are `account` and
               `global`. `account=global` is reqired if operating with a service ID that
               has a global admin policy, for example `GET /?account=global`.
        :param str ascending: (optional) Sets the sort order. False is descending.
        :param str startat: (optional) Starting time for the logs. If it's
               descending then the entries will be equal or earlier. The default is
               latest. For ascending it will entries equal or later. The default is
               earliest. It can be either a number or a string. If a number then it is in
               the format of Unix timestamps. If it is a string then it is a date in the
               format YYYY-MM-DDTHH:MM:SSZ  and the time is UTC. The T and the Z are
               required. For example: 2017-12-24T12:00:00Z for Noon UTC on Dec 24, 2017.
        :param int offset: (optional) Count of number of log entries to skip before
               returning logs. The default is zero.
        :param int limit: (optional) Count of number of entries to return. The
               default is fifty. The maximum value is two hundred.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `AuditSearchResult` object
        """

        if id is None:
            raise ValueError('id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_audit_logs')
        headers.update(sdk_headers)

        params = {
            'account': account,
            'ascending': ascending,
            'startat': startat,
            '_offset': offset,
            '_limit': limit
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        url = '/{0}/logs'.format(
            *self.encode_path_vars(id))
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response

    #########################
    # Artifact
    #########################


    def list_artifacts(self,
        object_id: str,
        *,
        account: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get artifacts.

        This endpoint returns a list of artifacts for an object.

        :param str object_id: The object's unique ID.
        :param str account: (optional) This changes the scope of the request
               regardless of the authorization header. Example scopes are `account` and
               `global`. `account=global` is reqired if operating with a service ID that
               has a global admin policy, for example `GET /?account=global`.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `Artifacts` object
        """

        if object_id is None:
            raise ValueError('object_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='list_artifacts')
        headers.update(sdk_headers)

        params = {
            'account': account
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        url = '/{0}/artifacts'.format(
            *self.encode_path_vars(object_id))
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def get_artifact(self,
        object_id: str,
        artifact_id: str,
        *,
        account: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get artifact.

        This endpoint returns the binary of an artifact.

        :param str object_id: The object's unique ID.
        :param str artifact_id: The artifact's ID.
        :param str account: (optional) This changes the scope of the request
               regardless of the authorization header. Example scopes are `account` and
               `global`. `account=global` is reqired if operating with a service ID that
               has a global admin policy, for example `GET /?account=global`.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if object_id is None:
            raise ValueError('object_id must be provided')
        if artifact_id is None:
            raise ValueError('artifact_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='get_artifact')
        headers.update(sdk_headers)

        params = {
            'account': account
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        url = '/{0}/artifacts/{1}'.format(
            *self.encode_path_vars(object_id, artifact_id))
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def upload_artifact(self,
        object_id: str,
        artifact_id: str,
        *,
        artifact: BinaryIO = None,
        content_type: str = None,
        account: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Upload artifact.

        This endpoint uploads the binary for an artifact. Only administrators and editors
        can upload artifacts.

        :param str object_id: The object's unique ID.
        :param str artifact_id: The artifact's ID.
        :param BinaryIO artifact: (optional)
        :param str content_type: (optional) The type of the input.
        :param str account: (optional) This changes the scope of the request
               regardless of the authorization header. Example scopes are `account` and
               `global`. `account=global` is reqired if operating with a service ID that
               has a global admin policy, for example `GET /?account=global`.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if object_id is None:
            raise ValueError('object_id must be provided')
        if artifact_id is None:
            raise ValueError('artifact_id must be provided')
        headers = {
            'Content-Type': content_type
        }
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='upload_artifact')
        headers.update(sdk_headers)

        params = {
            'account': account
        }

        data = artifact

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        url = '/{0}/artifacts/{1}'.format(
            *self.encode_path_vars(object_id, artifact_id))
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       params=params,
                                       data=data)

        response = self.send(request)
        return response


    def delete_artifact(self,
        object_id: str,
        artifact_id: str,
        *,
        account: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete artifact.

        This endpoint deletes an artifact. Only administrators and editors can delete
        artifacts.

        :param str object_id: The object's unique ID.
        :param str artifact_id: The artifact's ID.
        :param str account: (optional) This changes the scope of the request
               regardless of the authorization header. Example scopes are `account` and
               `global`. `account=global` is reqired if operating with a service ID that
               has a global admin policy, for example `GET /?account=global`.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if object_id is None:
            raise ValueError('object_id must be provided')
        if artifact_id is None:
            raise ValueError('artifact_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V1',
                                      operation_id='delete_artifact')
        headers.update(sdk_headers)

        params = {
            'account': account
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))

        url = '/{0}/artifacts/{1}'.format(
            *self.encode_path_vars(object_id, artifact_id))
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


##############################################################################
# Models
##############################################################################


class Amount():
    """
    Country-specific pricing information.

    :attr str country: (optional) Country.
    :attr str currency: (optional) Currency.
    :attr List[Price] prices: (optional) See Price for nested fields.
    """

    def __init__(self,
                 *,
                 country: str = None,
                 currency: str = None,
                 prices: List['Price'] = None) -> None:
        """
        Initialize a Amount object.

        :param str country: (optional) Country.
        :param str currency: (optional) Currency.
        :param List[Price] prices: (optional) See Price for nested fields.
        """
        self.country = country
        self.currency = currency
        self.prices = prices

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Amount':
        """Initialize a Amount object from a json dictionary."""
        args = {}
        if 'country' in _dict:
            args['country'] = _dict.get('country')
        if 'currency' in _dict:
            args['currency'] = _dict.get('currency')
        if 'prices' in _dict:
            args['prices'] = [Price.from_dict(x) for x in _dict.get('prices')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Amount object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'country') and self.country is not None:
            _dict['country'] = self.country
        if hasattr(self, 'currency') and self.currency is not None:
            _dict['currency'] = self.currency
        if hasattr(self, 'prices') and self.prices is not None:
            _dict['prices'] = [x.to_dict() for x in self.prices]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Amount object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Amount') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Amount') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class Artifact():
    """
    Artifact Details.

    :attr str name: (optional) The name of the artifact.
    :attr str updated: (optional) The timestamp of the last update to the artifact.
    :attr str url: (optional) The url for the artifact.
    :attr str etag: (optional) The etag of the artifact.
    :attr int size: (optional) The content length of the artifact.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 updated: str = None,
                 url: str = None,
                 etag: str = None,
                 size: int = None) -> None:
        """
        Initialize a Artifact object.

        :param str name: (optional) The name of the artifact.
        :param str updated: (optional) The timestamp of the last update to the
               artifact.
        :param str url: (optional) The url for the artifact.
        :param str etag: (optional) The etag of the artifact.
        :param int size: (optional) The content length of the artifact.
        """
        self.name = name
        self.updated = updated
        self.url = url
        self.etag = etag
        self.size = size

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Artifact':
        """Initialize a Artifact object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'updated' in _dict:
            args['updated'] = _dict.get('updated')
        if 'url' in _dict:
            args['url'] = _dict.get('url')
        if 'etag' in _dict:
            args['etag'] = _dict.get('etag')
        if 'size' in _dict:
            args['size'] = _dict.get('size')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Artifact object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'updated') and self.updated is not None:
            _dict['updated'] = self.updated
        if hasattr(self, 'url') and self.url is not None:
            _dict['url'] = self.url
        if hasattr(self, 'etag') and self.etag is not None:
            _dict['etag'] = self.etag
        if hasattr(self, 'size') and self.size is not None:
            _dict['size'] = self.size
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Artifact object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Artifact') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Artifact') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class Artifacts():
    """
    Artifacts List.

    :attr int count: (optional) The total number of artifacts.
    :attr List[Artifact] resources: (optional) The list of artifacts.
    """

    def __init__(self,
                 *,
                 count: int = None,
                 resources: List['Artifact'] = None) -> None:
        """
        Initialize a Artifacts object.

        :param int count: (optional) The total number of artifacts.
        :param List[Artifact] resources: (optional) The list of artifacts.
        """
        self.count = count
        self.resources = resources

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Artifacts':
        """Initialize a Artifacts object from a json dictionary."""
        args = {}
        if 'count' in _dict:
            args['count'] = _dict.get('count')
        if 'resources' in _dict:
            args['resources'] = [Artifact.from_dict(x) for x in _dict.get('resources')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Artifacts object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'count') and self.count is not None:
            _dict['count'] = self.count
        if hasattr(self, 'resources') and self.resources is not None:
            _dict['resources'] = [x.to_dict() for x in self.resources]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Artifacts object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Artifacts') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Artifacts') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class AuditSearchResult():
    """
    The results obtained by performing a search.

    :attr str page: (optional) Returned Page Number.
    :attr str results_per_page: (optional) Results Per Page – if the page is full.
    :attr str total_results: (optional) Total number of results.
    :attr List[Message] resources: (optional) Resulting audit objects.
    """

    def __init__(self,
                 *,
                 page: str = None,
                 results_per_page: str = None,
                 total_results: str = None,
                 resources: List['Message'] = None) -> None:
        """
        Initialize a AuditSearchResult object.

        :param str page: (optional) Returned Page Number.
        :param str results_per_page: (optional) Results Per Page – if the page is
               full.
        :param str total_results: (optional) Total number of results.
        :param List[Message] resources: (optional) Resulting audit objects.
        """
        self.page = page
        self.results_per_page = results_per_page
        self.total_results = total_results
        self.resources = resources

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'AuditSearchResult':
        """Initialize a AuditSearchResult object from a json dictionary."""
        args = {}
        if 'page' in _dict:
            args['page'] = _dict.get('page')
        if 'results_per_page' in _dict:
            args['results_per_page'] = _dict.get('results_per_page')
        if 'total_results' in _dict:
            args['total_results'] = _dict.get('total_results')
        if 'resources' in _dict:
            args['resources'] = [Message.from_dict(x) for x in _dict.get('resources')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a AuditSearchResult object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'page') and self.page is not None:
            _dict['page'] = self.page
        if hasattr(self, 'results_per_page') and self.results_per_page is not None:
            _dict['results_per_page'] = self.results_per_page
        if hasattr(self, 'total_results') and self.total_results is not None:
            _dict['total_results'] = self.total_results
        if hasattr(self, 'resources') and self.resources is not None:
            _dict['resources'] = [x.to_dict() for x in self.resources]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this AuditSearchResult object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'AuditSearchResult') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'AuditSearchResult') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class Bullets():
    """
    Information related to list delimiters.

    :attr str title: (optional) The bullet title.
    :attr str description: (optional) The bullet description.
    :attr str icon: (optional) The icon to use for rendering the bullet.
    :attr str quantity: (optional) The bullet quantity.
    """

    def __init__(self,
                 *,
                 title: str = None,
                 description: str = None,
                 icon: str = None,
                 quantity: str = None) -> None:
        """
        Initialize a Bullets object.

        :param str title: (optional) The bullet title.
        :param str description: (optional) The bullet description.
        :param str icon: (optional) The icon to use for rendering the bullet.
        :param str quantity: (optional) The bullet quantity.
        """
        self.title = title
        self.description = description
        self.icon = icon
        self.quantity = quantity

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Bullets':
        """Initialize a Bullets object from a json dictionary."""
        args = {}
        if 'title' in _dict:
            args['title'] = _dict.get('title')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'icon' in _dict:
            args['icon'] = _dict.get('icon')
        if 'quantity' in _dict:
            args['quantity'] = _dict.get('quantity')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Bullets object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'title') and self.title is not None:
            _dict['title'] = self.title
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'icon') and self.icon is not None:
            _dict['icon'] = self.icon
        if hasattr(self, 'quantity') and self.quantity is not None:
            _dict['quantity'] = self.quantity
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Bullets object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Bullets') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Bullets') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class Callbacks():
    """
    Callback-related information associated with a catalog entry.

    :attr str broker_utl: (optional) The URL of the deployment broker.
    :attr str broker_proxy_url: (optional) The URL of the deployment broker SC
          proxy.
    :attr str dashboard_url: (optional) The URL of dashboard callback.
    :attr str dashboard_data_url: (optional) The URL of dashboard data.
    :attr str dashboard_detail_tab_url: (optional) The URL of the dashboard detail
          tab.
    :attr str dashboard_detail_tab_ext_url: (optional) The URL of the dashboard
          detail tab extension.
    :attr str service_monitor_api: (optional) Service monitor API URL.
    :attr str service_monitor_app: (optional) Service monitor app URL.
    :attr str service_staging_url: (optional) Service URL in staging.
    :attr str service_production_url: (optional) Service URL in production.
    """

    def __init__(self,
                 *,
                 broker_utl: str = None,
                 broker_proxy_url: str = None,
                 dashboard_url: str = None,
                 dashboard_data_url: str = None,
                 dashboard_detail_tab_url: str = None,
                 dashboard_detail_tab_ext_url: str = None,
                 service_monitor_api: str = None,
                 service_monitor_app: str = None,
                 service_staging_url: str = None,
                 service_production_url: str = None) -> None:
        """
        Initialize a Callbacks object.

        :param str broker_utl: (optional) The URL of the deployment broker.
        :param str broker_proxy_url: (optional) The URL of the deployment broker SC
               proxy.
        :param str dashboard_url: (optional) The URL of dashboard callback.
        :param str dashboard_data_url: (optional) The URL of dashboard data.
        :param str dashboard_detail_tab_url: (optional) The URL of the dashboard
               detail tab.
        :param str dashboard_detail_tab_ext_url: (optional) The URL of the
               dashboard detail tab extension.
        :param str service_monitor_api: (optional) Service monitor API URL.
        :param str service_monitor_app: (optional) Service monitor app URL.
        :param str service_staging_url: (optional) Service URL in staging.
        :param str service_production_url: (optional) Service URL in production.
        """
        self.broker_utl = broker_utl
        self.broker_proxy_url = broker_proxy_url
        self.dashboard_url = dashboard_url
        self.dashboard_data_url = dashboard_data_url
        self.dashboard_detail_tab_url = dashboard_detail_tab_url
        self.dashboard_detail_tab_ext_url = dashboard_detail_tab_ext_url
        self.service_monitor_api = service_monitor_api
        self.service_monitor_app = service_monitor_app
        self.service_staging_url = service_staging_url
        self.service_production_url = service_production_url

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Callbacks':
        """Initialize a Callbacks object from a json dictionary."""
        args = {}
        if 'broker_utl' in _dict:
            args['broker_utl'] = _dict.get('broker_utl')
        if 'broker_proxy_url' in _dict:
            args['broker_proxy_url'] = _dict.get('broker_proxy_url')
        if 'dashboard_url' in _dict:
            args['dashboard_url'] = _dict.get('dashboard_url')
        if 'dashboard_data_url' in _dict:
            args['dashboard_data_url'] = _dict.get('dashboard_data_url')
        if 'dashboard_detail_tab_url' in _dict:
            args['dashboard_detail_tab_url'] = _dict.get('dashboard_detail_tab_url')
        if 'dashboard_detail_tab_ext_url' in _dict:
            args['dashboard_detail_tab_ext_url'] = _dict.get('dashboard_detail_tab_ext_url')
        if 'service_monitor_api' in _dict:
            args['service_monitor_api'] = _dict.get('service_monitor_api')
        if 'service_monitor_app' in _dict:
            args['service_monitor_app'] = _dict.get('service_monitor_app')
        if 'service_staging_url' in _dict:
            args['service_staging_url'] = _dict.get('service_staging_url')
        if 'service_production_url' in _dict:
            args['service_production_url'] = _dict.get('service_production_url')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Callbacks object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'broker_utl') and self.broker_utl is not None:
            _dict['broker_utl'] = self.broker_utl
        if hasattr(self, 'broker_proxy_url') and self.broker_proxy_url is not None:
            _dict['broker_proxy_url'] = self.broker_proxy_url
        if hasattr(self, 'dashboard_url') and self.dashboard_url is not None:
            _dict['dashboard_url'] = self.dashboard_url
        if hasattr(self, 'dashboard_data_url') and self.dashboard_data_url is not None:
            _dict['dashboard_data_url'] = self.dashboard_data_url
        if hasattr(self, 'dashboard_detail_tab_url') and self.dashboard_detail_tab_url is not None:
            _dict['dashboard_detail_tab_url'] = self.dashboard_detail_tab_url
        if hasattr(self, 'dashboard_detail_tab_ext_url') and self.dashboard_detail_tab_ext_url is not None:
            _dict['dashboard_detail_tab_ext_url'] = self.dashboard_detail_tab_ext_url
        if hasattr(self, 'service_monitor_api') and self.service_monitor_api is not None:
            _dict['service_monitor_api'] = self.service_monitor_api
        if hasattr(self, 'service_monitor_app') and self.service_monitor_app is not None:
            _dict['service_monitor_app'] = self.service_monitor_app
        if hasattr(self, 'service_staging_url') and self.service_staging_url is not None:
            _dict['service_staging_url'] = self.service_staging_url
        if hasattr(self, 'service_production_url') and self.service_production_url is not None:
            _dict['service_production_url'] = self.service_production_url
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Callbacks object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Callbacks') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Callbacks') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CatalogEntry():
    """
    An entry in the global catalog.

    :attr str name: Programmatic name for this catalog entry, which must be
          formatted like a CRN segment. See the display name in OverviewUI for a
          user-readable name.
    :attr str kind: The type of catalog entry, **service**, **template**,
          **dashboard**, which determines the type and shape of the object.
    :attr OverviewUI overview_ui: Overview is nested in the top level. The key value
          pair is `[_language_]overview_ui`.
    :attr Image images: Image annotation for this catalog entry. The image is a URL.
    :attr str parent_id: (optional) The ID of the parent catalog entry if it exists.
    :attr bool disabled: Boolean value that determines the global visibility for the
          catalog entry, and its children. If it is not enabled, all plans are disabled.
    :attr List[str] tags: A list of tags. For example, IBM, 3rd Party, Beta, GA, and
          Single Tenant.
    :attr bool group: (optional) Boolean value that determines whether the catalog
          entry is a group.
    :attr Provider provider: Information related to the provider associated with a
          catalog entry.
    :attr bool active: (optional) Boolean value that describes whether the service
          is active.
    :attr CatalogEntryMetadata metadata: (optional) Model used to describe metadata
          object returned.
    :attr str id: (optional) Catalog entry's unique ID. It's the same across all
          catalog instances.
    :attr object catalog_crn: (optional)
    :attr object url: (optional)
    :attr object children_url: (optional)
    :attr object geo_tags: (optional)
    :attr object pricing_tags: (optional)
    :attr object created: (optional)
    :attr object updated: (optional)
    """

    def __init__(self,
                 name: str,
                 kind: str,
                 overview_ui: 'OverviewUI',
                 images: 'Image',
                 disabled: bool,
                 tags: List[str],
                 provider: 'Provider',
                 *,
                 parent_id: str = None,
                 group: bool = None,
                 active: bool = None,
                 metadata: 'CatalogEntryMetadata' = None,
                 id: str = None,
                 catalog_crn: object = None,
                 url: object = None,
                 children_url: object = None,
                 geo_tags: object = None,
                 pricing_tags: object = None,
                 created: object = None,
                 updated: object = None) -> None:
        """
        Initialize a CatalogEntry object.

        :param str name: Programmatic name for this catalog entry, which must be
               formatted like a CRN segment. See the display name in OverviewUI for a
               user-readable name.
        :param str kind: The type of catalog entry, **service**, **template**,
               **dashboard**, which determines the type and shape of the object.
        :param OverviewUI overview_ui: Overview is nested in the top level. The key
               value pair is `[_language_]overview_ui`.
        :param Image images: Image annotation for this catalog entry. The image is
               a URL.
        :param bool disabled: Boolean value that determines the global visibility
               for the catalog entry, and its children. If it is not enabled, all plans
               are disabled.
        :param List[str] tags: A list of tags. For example, IBM, 3rd Party, Beta,
               GA, and Single Tenant.
        :param Provider provider: Information related to the provider associated
               with a catalog entry.
        :param str parent_id: (optional) The ID of the parent catalog entry if it
               exists.
        :param bool group: (optional) Boolean value that determines whether the
               catalog entry is a group.
        :param bool active: (optional) Boolean value that describes whether the
               service is active.
        :param CatalogEntryMetadata metadata: (optional) Model used to describe
               metadata object returned.
        """
        self.name = name
        self.kind = kind
        self.overview_ui = overview_ui
        self.images = images
        self.parent_id = parent_id
        self.disabled = disabled
        self.tags = tags
        self.group = group
        self.provider = provider
        self.active = active
        self.metadata = metadata
        self.id = id
        self.catalog_crn = catalog_crn
        self.url = url
        self.children_url = children_url
        self.geo_tags = geo_tags
        self.pricing_tags = pricing_tags
        self.created = created
        self.updated = updated

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CatalogEntry':
        """Initialize a CatalogEntry object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        else:
            raise ValueError('Required property \'name\' not present in CatalogEntry JSON')
        if 'kind' in _dict:
            args['kind'] = _dict.get('kind')
        else:
            raise ValueError('Required property \'kind\' not present in CatalogEntry JSON')
        if 'overview_ui' in _dict:
            args['overview_ui'] = OverviewUI.from_dict(_dict.get('overview_ui'))
        else:
            raise ValueError('Required property \'overview_ui\' not present in CatalogEntry JSON')
        if 'images' in _dict:
            args['images'] = Image.from_dict(_dict.get('images'))
        else:
            raise ValueError('Required property \'images\' not present in CatalogEntry JSON')
        if 'parent_id' in _dict:
            args['parent_id'] = _dict.get('parent_id')
        if 'disabled' in _dict:
            args['disabled'] = _dict.get('disabled')
        else:
            raise ValueError('Required property \'disabled\' not present in CatalogEntry JSON')
        if 'tags' in _dict:
            args['tags'] = _dict.get('tags')
        else:
            raise ValueError('Required property \'tags\' not present in CatalogEntry JSON')
        if 'group' in _dict:
            args['group'] = _dict.get('group')
        if 'provider' in _dict:
            args['provider'] = Provider.from_dict(_dict.get('provider'))
        else:
            raise ValueError('Required property \'provider\' not present in CatalogEntry JSON')
        if 'active' in _dict:
            args['active'] = _dict.get('active')
        if 'metadata' in _dict:
            args['metadata'] = CatalogEntryMetadata.from_dict(_dict.get('metadata'))
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'catalog_crn' in _dict:
            args['catalog_crn'] = _dict.get('catalog_crn')
        if 'url' in _dict:
            args['url'] = _dict.get('url')
        if 'children_url' in _dict:
            args['children_url'] = _dict.get('children_url')
        if 'geo_tags' in _dict:
            args['geo_tags'] = _dict.get('geo_tags')
        if 'pricing_tags' in _dict:
            args['pricing_tags'] = _dict.get('pricing_tags')
        if 'created' in _dict:
            args['created'] = _dict.get('created')
        if 'updated' in _dict:
            args['updated'] = _dict.get('updated')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CatalogEntry object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'kind') and self.kind is not None:
            _dict['kind'] = self.kind
        if hasattr(self, 'overview_ui') and self.overview_ui is not None:
            _dict['overview_ui'] = self.overview_ui.to_dict()
        if hasattr(self, 'images') and self.images is not None:
            _dict['images'] = self.images.to_dict()
        if hasattr(self, 'parent_id') and self.parent_id is not None:
            _dict['parent_id'] = self.parent_id
        if hasattr(self, 'disabled') and self.disabled is not None:
            _dict['disabled'] = self.disabled
        if hasattr(self, 'tags') and self.tags is not None:
            _dict['tags'] = self.tags
        if hasattr(self, 'group') and self.group is not None:
            _dict['group'] = self.group
        if hasattr(self, 'provider') and self.provider is not None:
            _dict['provider'] = self.provider.to_dict()
        if hasattr(self, 'active') and self.active is not None:
            _dict['active'] = self.active
        if hasattr(self, 'metadata') and self.metadata is not None:
            _dict['metadata'] = self.metadata.to_dict()
        if hasattr(self, 'id') and getattr(self, 'id') is not None:
            _dict['id'] = getattr(self, 'id')
        if hasattr(self, 'catalog_crn') and getattr(self, 'catalog_crn') is not None:
            _dict['catalog_crn'] = getattr(self, 'catalog_crn')
        if hasattr(self, 'url') and getattr(self, 'url') is not None:
            _dict['url'] = getattr(self, 'url')
        if hasattr(self, 'children_url') and getattr(self, 'children_url') is not None:
            _dict['children_url'] = getattr(self, 'children_url')
        if hasattr(self, 'geo_tags') and getattr(self, 'geo_tags') is not None:
            _dict['geo_tags'] = getattr(self, 'geo_tags')
        if hasattr(self, 'pricing_tags') and getattr(self, 'pricing_tags') is not None:
            _dict['pricing_tags'] = getattr(self, 'pricing_tags')
        if hasattr(self, 'created') and getattr(self, 'created') is not None:
            _dict['created'] = getattr(self, 'created')
        if hasattr(self, 'updated') and getattr(self, 'updated') is not None:
            _dict['updated'] = getattr(self, 'updated')
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CatalogEntry object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CatalogEntry') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CatalogEntry') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class KindEnum(Enum):
        """
        The type of catalog entry, **service**, **template**, **dashboard**, which
        determines the type and shape of the object.
        """
        SERVICE = "service"
        TEMPLATE = "template"
        DASHBOARD = "dashboard"


class CatalogEntryMetadata():
    """
    Model used to describe metadata object returned.

    :attr bool rc_compatible: (optional) Boolean value that describes whether the
          service is compatible with the Resource Controller.
    :attr UIMetaData ui: (optional) Information related to the UI presentation
          associated with a catalog entry.
    :attr List[str] compliance: (optional) Compliance information for HIPAA and PCI.
    :attr ObjectMetadataBaseService service: (optional) Service-related metadata.
    :attr ObjectMetadataBasePlan plan: (optional) Plan-related metadata.
    :attr ObjectMetadataBaseTemplate template: (optional) Template-related metadata.
    :attr ObjectMetadataBaseAlias alias: (optional) Alias-related metadata.
    :attr ObjectMetadataBaseSla sla: (optional) Service Level Agreement related
          metadata.
    :attr Callbacks callbacks: (optional) Callback-related information associated
          with a catalog entry.
    :attr str version: (optional) Optional version of the object.
    :attr str original_name: (optional) The original name of the object.
    :attr object other: (optional) Additional information.
    :attr CatalogEntryMetadataPricing pricing: (optional) Pricing-related
          information.
    :attr CatalogEntryMetadataDeployment deployment: (optional) Deployment-related
          metadata.
    """

    def __init__(self,
                 *,
                 rc_compatible: bool = None,
                 ui: 'UIMetaData' = None,
                 compliance: List[str] = None,
                 service: 'ObjectMetadataBaseService' = None,
                 plan: 'ObjectMetadataBasePlan' = None,
                 template: 'ObjectMetadataBaseTemplate' = None,
                 alias: 'ObjectMetadataBaseAlias' = None,
                 sla: 'ObjectMetadataBaseSla' = None,
                 callbacks: 'Callbacks' = None,
                 version: str = None,
                 original_name: str = None,
                 other: object = None,
                 pricing: 'CatalogEntryMetadataPricing' = None,
                 deployment: 'CatalogEntryMetadataDeployment' = None) -> None:
        """
        Initialize a CatalogEntryMetadata object.

        :param bool rc_compatible: (optional) Boolean value that describes whether
               the service is compatible with the Resource Controller.
        :param UIMetaData ui: (optional) Information related to the UI presentation
               associated with a catalog entry.
        :param List[str] compliance: (optional) Compliance information for HIPAA
               and PCI.
        :param ObjectMetadataBaseService service: (optional) Service-related
               metadata.
        :param ObjectMetadataBasePlan plan: (optional) Plan-related metadata.
        :param ObjectMetadataBaseTemplate template: (optional) Template-related
               metadata.
        :param ObjectMetadataBaseAlias alias: (optional) Alias-related metadata.
        :param ObjectMetadataBaseSla sla: (optional) Service Level Agreement
               related metadata.
        :param Callbacks callbacks: (optional) Callback-related information
               associated with a catalog entry.
        :param str version: (optional) Optional version of the object.
        :param str original_name: (optional) The original name of the object.
        :param object other: (optional) Additional information.
        :param CatalogEntryMetadataPricing pricing: (optional) Pricing-related
               information.
        :param CatalogEntryMetadataDeployment deployment: (optional)
               Deployment-related metadata.
        """
        self.rc_compatible = rc_compatible
        self.ui = ui
        self.compliance = compliance
        self.service = service
        self.plan = plan
        self.template = template
        self.alias = alias
        self.sla = sla
        self.callbacks = callbacks
        self.version = version
        self.original_name = original_name
        self.other = other
        self.pricing = pricing
        self.deployment = deployment

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CatalogEntryMetadata':
        """Initialize a CatalogEntryMetadata object from a json dictionary."""
        args = {}
        if 'rc_compatible' in _dict:
            args['rc_compatible'] = _dict.get('rc_compatible')
        if 'ui' in _dict:
            args['ui'] = UIMetaData.from_dict(_dict.get('ui'))
        if 'compliance' in _dict:
            args['compliance'] = _dict.get('compliance')
        if 'service' in _dict:
            args['service'] = ObjectMetadataBaseService.from_dict(_dict.get('service'))
        if 'plan' in _dict:
            args['plan'] = ObjectMetadataBasePlan.from_dict(_dict.get('plan'))
        if 'template' in _dict:
            args['template'] = ObjectMetadataBaseTemplate.from_dict(_dict.get('template'))
        if 'alias' in _dict:
            args['alias'] = ObjectMetadataBaseAlias.from_dict(_dict.get('alias'))
        if 'sla' in _dict:
            args['sla'] = ObjectMetadataBaseSla.from_dict(_dict.get('sla'))
        if 'callbacks' in _dict:
            args['callbacks'] = Callbacks.from_dict(_dict.get('callbacks'))
        if 'version' in _dict:
            args['version'] = _dict.get('version')
        if 'original_name' in _dict:
            args['original_name'] = _dict.get('original_name')
        if 'other' in _dict:
            args['other'] = _dict.get('other')
        if 'pricing' in _dict:
            args['pricing'] = CatalogEntryMetadataPricing.from_dict(_dict.get('pricing'))
        if 'deployment' in _dict:
            args['deployment'] = CatalogEntryMetadataDeployment.from_dict(_dict.get('deployment'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CatalogEntryMetadata object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'rc_compatible') and self.rc_compatible is not None:
            _dict['rc_compatible'] = self.rc_compatible
        if hasattr(self, 'ui') and self.ui is not None:
            _dict['ui'] = self.ui.to_dict()
        if hasattr(self, 'compliance') and self.compliance is not None:
            _dict['compliance'] = self.compliance
        if hasattr(self, 'service') and self.service is not None:
            _dict['service'] = self.service.to_dict()
        if hasattr(self, 'plan') and self.plan is not None:
            _dict['plan'] = self.plan.to_dict()
        if hasattr(self, 'template') and self.template is not None:
            _dict['template'] = self.template.to_dict()
        if hasattr(self, 'alias') and self.alias is not None:
            _dict['alias'] = self.alias.to_dict()
        if hasattr(self, 'sla') and self.sla is not None:
            _dict['sla'] = self.sla.to_dict()
        if hasattr(self, 'callbacks') and self.callbacks is not None:
            _dict['callbacks'] = self.callbacks.to_dict()
        if hasattr(self, 'version') and self.version is not None:
            _dict['version'] = self.version
        if hasattr(self, 'original_name') and self.original_name is not None:
            _dict['original_name'] = self.original_name
        if hasattr(self, 'other') and self.other is not None:
            _dict['other'] = self.other
        if hasattr(self, 'pricing') and self.pricing is not None:
            _dict['pricing'] = self.pricing.to_dict()
        if hasattr(self, 'deployment') and self.deployment is not None:
            _dict['deployment'] = self.deployment.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CatalogEntryMetadata object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CatalogEntryMetadata') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CatalogEntryMetadata') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CatalogEntryMetadataDeployment():
    """
    Deployment-related metadata.

    :attr str location: (optional) Describes the region where the service is
          located.
    :attr str target_crn: (optional) A CRN that describes the deployment.
          crn:v1:[cname]:[ctype]:[location]:[scope]::[resource-type]:[resource].
    :attr CatalogEntryMetadataDeploymentBroker broker: (optional) The broker
          associated with a catalog entry.
    :attr bool supports_rc_migration: (optional) This deployment not only supports
          RC but is ready to migrate and support the RC broker for a location.
    :attr str target_network: (optional) network to use during deployment.
    :attr str location_url: (optional) Pointer to the location resource in the
          catalog.
    """

    def __init__(self,
                 *,
                 location: str = None,
                 target_crn: str = None,
                 broker: 'CatalogEntryMetadataDeploymentBroker' = None,
                 supports_rc_migration: bool = None,
                 target_network: str = None,
                 location_url: str = None) -> None:
        """
        Initialize a CatalogEntryMetadataDeployment object.

        :param str location: (optional) Describes the region where the service is
               located.
        :param str target_crn: (optional) A CRN that describes the deployment.
               crn:v1:[cname]:[ctype]:[location]:[scope]::[resource-type]:[resource].
        :param CatalogEntryMetadataDeploymentBroker broker: (optional) The broker
               associated with a catalog entry.
        :param bool supports_rc_migration: (optional) This deployment not only
               supports RC but is ready to migrate and support the RC broker for a
               location.
        :param str target_network: (optional) network to use during deployment.
        """
        self.location = location
        self.target_crn = target_crn
        self.broker = broker
        self.supports_rc_migration = supports_rc_migration
        self.target_network = target_network
        self.location_url = location_url

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CatalogEntryMetadataDeployment':
        """Initialize a CatalogEntryMetadataDeployment object from a json dictionary."""
        args = {}
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'target_crn' in _dict:
            args['target_crn'] = _dict.get('target_crn')
        if 'broker' in _dict:
            args['broker'] = CatalogEntryMetadataDeploymentBroker.from_dict(_dict.get('broker'))
        if 'supports_rc_migration' in _dict:
            args['supports_rc_migration'] = _dict.get('supports_rc_migration')
        if 'target_network' in _dict:
            args['target_network'] = _dict.get('target_network')
        if 'location_url' in _dict:
            args['location_url'] = _dict.get('location_url')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CatalogEntryMetadataDeployment object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'target_crn') and self.target_crn is not None:
            _dict['target_crn'] = self.target_crn
        if hasattr(self, 'broker') and self.broker is not None:
            _dict['broker'] = self.broker.to_dict()
        if hasattr(self, 'supports_rc_migration') and self.supports_rc_migration is not None:
            _dict['supports_rc_migration'] = self.supports_rc_migration
        if hasattr(self, 'target_network') and self.target_network is not None:
            _dict['target_network'] = self.target_network
        if hasattr(self, 'location_url') and getattr(self, 'location_url') is not None:
            _dict['location_url'] = getattr(self, 'location_url')
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CatalogEntryMetadataDeployment object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CatalogEntryMetadataDeployment') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CatalogEntryMetadataDeployment') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CatalogEntryMetadataDeploymentBroker():
    """
    The broker associated with a catalog entry.

    :attr str name: (optional) Broker name.
    :attr str guid: (optional) Broker guid.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 guid: str = None) -> None:
        """
        Initialize a CatalogEntryMetadataDeploymentBroker object.

        :param str name: (optional) Broker name.
        :param str guid: (optional) Broker guid.
        """
        self.name = name
        self.guid = guid

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CatalogEntryMetadataDeploymentBroker':
        """Initialize a CatalogEntryMetadataDeploymentBroker object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'guid' in _dict:
            args['guid'] = _dict.get('guid')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CatalogEntryMetadataDeploymentBroker object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'guid') and self.guid is not None:
            _dict['guid'] = self.guid
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CatalogEntryMetadataDeploymentBroker object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CatalogEntryMetadataDeploymentBroker') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CatalogEntryMetadataDeploymentBroker') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CatalogEntryMetadataPricing():
    """
    Pricing-related information.

    :attr str type: (optional) Type of plan. Valid values are `free`, `trial`,
          `paygo`, `bluemix-subscription`, and `ibm-subscription`.
    :attr str origin: (optional) Defines where the pricing originates.
    :attr StartingPrice starting_price: (optional) Plan-specific starting price
          information.
    :attr List[Metrics] metrics: (optional) Plan-specific cost metric structure.
    """

    def __init__(self,
                 *,
                 type: str = None,
                 origin: str = None,
                 starting_price: 'StartingPrice' = None,
                 metrics: List['Metrics'] = None) -> None:
        """
        Initialize a CatalogEntryMetadataPricing object.

        :param str type: (optional) Type of plan. Valid values are `free`, `trial`,
               `paygo`, `bluemix-subscription`, and `ibm-subscription`.
        :param str origin: (optional) Defines where the pricing originates.
        :param StartingPrice starting_price: (optional) Plan-specific starting
               price information.
        :param List[Metrics] metrics: (optional) Plan-specific cost metric
               structure.
        """
        self.type = type
        self.origin = origin
        self.starting_price = starting_price
        self.metrics = metrics

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CatalogEntryMetadataPricing':
        """Initialize a CatalogEntryMetadataPricing object from a json dictionary."""
        args = {}
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'origin' in _dict:
            args['origin'] = _dict.get('origin')
        if 'starting_price' in _dict:
            args['starting_price'] = StartingPrice.from_dict(_dict.get('starting_price'))
        if 'metrics' in _dict:
            args['metrics'] = [Metrics.from_dict(x) for x in _dict.get('metrics')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CatalogEntryMetadataPricing object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'origin') and self.origin is not None:
            _dict['origin'] = self.origin
        if hasattr(self, 'starting_price') and self.starting_price is not None:
            _dict['starting_price'] = self.starting_price.to_dict()
        if hasattr(self, 'metrics') and self.metrics is not None:
            _dict['metrics'] = [x.to_dict() for x in self.metrics]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CatalogEntryMetadataPricing object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CatalogEntryMetadataPricing') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CatalogEntryMetadataPricing') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class DeploymentBase():
    """
    Deployment-related metadata.

    :attr str location: (optional) Describes the region where the service is
          located.
    :attr str target_crn: (optional) A CRN that describes the deployment.
          crn:v1:[cname]:[ctype]:[location]:[scope]::[resource-type]:[resource].
    :attr DeploymentBaseBroker broker: (optional) The broker associated with a
          catalog entry.
    :attr bool supports_rc_migration: (optional) This deployment not only supports
          RC but is ready to migrate and support the RC broker for a location.
    :attr str target_network: (optional) network to use during deployment.
    """

    def __init__(self,
                 *,
                 location: str = None,
                 target_crn: str = None,
                 broker: 'DeploymentBaseBroker' = None,
                 supports_rc_migration: bool = None,
                 target_network: str = None) -> None:
        """
        Initialize a DeploymentBase object.

        :param str location: (optional) Describes the region where the service is
               located.
        :param str target_crn: (optional) A CRN that describes the deployment.
               crn:v1:[cname]:[ctype]:[location]:[scope]::[resource-type]:[resource].
        :param DeploymentBaseBroker broker: (optional) The broker associated with a
               catalog entry.
        :param bool supports_rc_migration: (optional) This deployment not only
               supports RC but is ready to migrate and support the RC broker for a
               location.
        :param str target_network: (optional) network to use during deployment.
        """
        self.location = location
        self.target_crn = target_crn
        self.broker = broker
        self.supports_rc_migration = supports_rc_migration
        self.target_network = target_network

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'DeploymentBase':
        """Initialize a DeploymentBase object from a json dictionary."""
        args = {}
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'target_crn' in _dict:
            args['target_crn'] = _dict.get('target_crn')
        if 'broker' in _dict:
            args['broker'] = DeploymentBaseBroker.from_dict(_dict.get('broker'))
        if 'supports_rc_migration' in _dict:
            args['supports_rc_migration'] = _dict.get('supports_rc_migration')
        if 'target_network' in _dict:
            args['target_network'] = _dict.get('target_network')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a DeploymentBase object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'target_crn') and self.target_crn is not None:
            _dict['target_crn'] = self.target_crn
        if hasattr(self, 'broker') and self.broker is not None:
            _dict['broker'] = self.broker.to_dict()
        if hasattr(self, 'supports_rc_migration') and self.supports_rc_migration is not None:
            _dict['supports_rc_migration'] = self.supports_rc_migration
        if hasattr(self, 'target_network') and self.target_network is not None:
            _dict['target_network'] = self.target_network
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this DeploymentBase object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'DeploymentBase') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'DeploymentBase') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class DeploymentBaseBroker():
    """
    The broker associated with a catalog entry.

    :attr str name: (optional) Broker name.
    :attr str guid: (optional) Broker guid.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 guid: str = None) -> None:
        """
        Initialize a DeploymentBaseBroker object.

        :param str name: (optional) Broker name.
        :param str guid: (optional) Broker guid.
        """
        self.name = name
        self.guid = guid

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'DeploymentBaseBroker':
        """Initialize a DeploymentBaseBroker object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'guid' in _dict:
            args['guid'] = _dict.get('guid')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a DeploymentBaseBroker object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'guid') and self.guid is not None:
            _dict['guid'] = self.guid
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this DeploymentBaseBroker object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'DeploymentBaseBroker') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'DeploymentBaseBroker') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class EntrySearchResult():
    """
    The Global Catalog entries obtained by performing a search.

    :attr str page: (optional) Returned Page Number.
    :attr str results_per_page: (optional) Results Per Page – if the page is full.
    :attr str total_results: (optional) Total number of results.
    :attr List[CatalogEntry] resources: (optional) Resulting objects.
    """

    def __init__(self,
                 *,
                 page: str = None,
                 results_per_page: str = None,
                 total_results: str = None,
                 resources: List['CatalogEntry'] = None) -> None:
        """
        Initialize a EntrySearchResult object.

        :param str page: (optional) Returned Page Number.
        :param str results_per_page: (optional) Results Per Page – if the page is
               full.
        :param str total_results: (optional) Total number of results.
        :param List[CatalogEntry] resources: (optional) Resulting objects.
        """
        self.page = page
        self.results_per_page = results_per_page
        self.total_results = total_results
        self.resources = resources

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'EntrySearchResult':
        """Initialize a EntrySearchResult object from a json dictionary."""
        args = {}
        if 'page' in _dict:
            args['page'] = _dict.get('page')
        if 'results_per_page' in _dict:
            args['results_per_page'] = _dict.get('results_per_page')
        if 'total_results' in _dict:
            args['total_results'] = _dict.get('total_results')
        if 'resources' in _dict:
            args['resources'] = [CatalogEntry.from_dict(x) for x in _dict.get('resources')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a EntrySearchResult object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'page') and self.page is not None:
            _dict['page'] = self.page
        if hasattr(self, 'results_per_page') and self.results_per_page is not None:
            _dict['results_per_page'] = self.results_per_page
        if hasattr(self, 'total_results') and self.total_results is not None:
            _dict['total_results'] = self.total_results
        if hasattr(self, 'resources') and self.resources is not None:
            _dict['resources'] = [x.to_dict() for x in self.resources]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this EntrySearchResult object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'EntrySearchResult') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'EntrySearchResult') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class I18N():
    """
    Language specific translation of translation properties, like label and description.

    """

    def __init__(self,
                 **kwargs) -> None:
        """
        Initialize a I18N object.

        :param **kwargs: (optional) Any additional properties.
        """
        for _key, _value in kwargs.items():
            setattr(self, _key, _value)

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'I18N':
        """Initialize a I18N object from a json dictionary."""
        return cls(**_dict)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a I18N object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        return vars(self)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this I18N object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'I18N') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'I18N') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class Image():
    """
    Image annotation for this catalog entry. The image is a URL.

    :attr str image: URL for the large, default image.
    :attr str small_image: (optional) URL for a small image.
    :attr str medium_image: (optional) URL for a medium image.
    :attr str feature_image: (optional) URL for a featured image.
    """

    def __init__(self,
                 image: str,
                 *,
                 small_image: str = None,
                 medium_image: str = None,
                 feature_image: str = None) -> None:
        """
        Initialize a Image object.

        :param str image: URL for the large, default image.
        :param str small_image: (optional) URL for a small image.
        :param str medium_image: (optional) URL for a medium image.
        :param str feature_image: (optional) URL for a featured image.
        """
        self.image = image
        self.small_image = small_image
        self.medium_image = medium_image
        self.feature_image = feature_image

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Image':
        """Initialize a Image object from a json dictionary."""
        args = {}
        if 'image' in _dict:
            args['image'] = _dict.get('image')
        else:
            raise ValueError('Required property \'image\' not present in Image JSON')
        if 'small_image' in _dict:
            args['small_image'] = _dict.get('small_image')
        if 'medium_image' in _dict:
            args['medium_image'] = _dict.get('medium_image')
        if 'feature_image' in _dict:
            args['feature_image'] = _dict.get('feature_image')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Image object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'image') and self.image is not None:
            _dict['image'] = self.image
        if hasattr(self, 'small_image') and self.small_image is not None:
            _dict['small_image'] = self.small_image
        if hasattr(self, 'medium_image') and self.medium_image is not None:
            _dict['medium_image'] = self.medium_image
        if hasattr(self, 'feature_image') and self.feature_image is not None:
            _dict['feature_image'] = self.feature_image
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Image object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Image') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Image') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class Message():
    """
    log object describing who did what.

    :attr str id: (optional) id of catalog entry.
    :attr Visibility effective: (optional) Information related to the visibility of
          a catalog entry.
    :attr str time: (optional) time of action.
    :attr str who_id: (optional) user ID of person who did action.
    :attr str who_name: (optional) name of person who did action.
    :attr str who_email: (optional) user email of person who did action.
    :attr str instance: (optional) Global catalog instance where this occured.
    :attr str gid: (optional) transaction id associatd with action.
    :attr str type: (optional) type of action taken.
    :attr str message: (optional) message describing action.
    :attr object data: (optional) JSON object containing details on changes made to
          object data.
    """

    def __init__(self,
                 *,
                 id: str = None,
                 effective: 'Visibility' = None,
                 time: str = None,
                 who_id: str = None,
                 who_name: str = None,
                 who_email: str = None,
                 instance: str = None,
                 gid: str = None,
                 type: str = None,
                 message: str = None,
                 data: object = None) -> None:
        """
        Initialize a Message object.

        :param str id: (optional) id of catalog entry.
        :param Visibility effective: (optional) Information related to the
               visibility of a catalog entry.
        :param str time: (optional) time of action.
        :param str who_id: (optional) user ID of person who did action.
        :param str who_name: (optional) name of person who did action.
        :param str who_email: (optional) user email of person who did action.
        :param str instance: (optional) Global catalog instance where this occured.
        :param str gid: (optional) transaction id associatd with action.
        :param str type: (optional) type of action taken.
        :param str message: (optional) message describing action.
        :param object data: (optional) JSON object containing details on changes
               made to object data.
        """
        self.id = id
        self.effective = effective
        self.time = time
        self.who_id = who_id
        self.who_name = who_name
        self.who_email = who_email
        self.instance = instance
        self.gid = gid
        self.type = type
        self.message = message
        self.data = data

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Message':
        """Initialize a Message object from a json dictionary."""
        args = {}
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'effective' in _dict:
            args['effective'] = Visibility.from_dict(_dict.get('effective'))
        if 'time' in _dict:
            args['time'] = _dict.get('time')
        if 'who_id' in _dict:
            args['who_id'] = _dict.get('who_id')
        if 'who_name' in _dict:
            args['who_name'] = _dict.get('who_name')
        if 'who_email' in _dict:
            args['who_email'] = _dict.get('who_email')
        if 'instance' in _dict:
            args['instance'] = _dict.get('instance')
        if 'gid' in _dict:
            args['gid'] = _dict.get('gid')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'message' in _dict:
            args['message'] = _dict.get('message')
        if 'data' in _dict:
            args['data'] = _dict.get('data')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Message object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'effective') and self.effective is not None:
            _dict['effective'] = self.effective.to_dict()
        if hasattr(self, 'time') and self.time is not None:
            _dict['time'] = self.time
        if hasattr(self, 'who_id') and self.who_id is not None:
            _dict['who_id'] = self.who_id
        if hasattr(self, 'who_name') and self.who_name is not None:
            _dict['who_name'] = self.who_name
        if hasattr(self, 'who_email') and self.who_email is not None:
            _dict['who_email'] = self.who_email
        if hasattr(self, 'instance') and self.instance is not None:
            _dict['instance'] = self.instance
        if hasattr(self, 'gid') and self.gid is not None:
            _dict['gid'] = self.gid
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'message') and self.message is not None:
            _dict['message'] = self.message
        if hasattr(self, 'data') and self.data is not None:
            _dict['data'] = self.data
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Message object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Message') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Message') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class Metrics():
    """
    Plan-specific cost metrics information.

    :attr str metric_id: (optional) The metric ID or part number.
    :attr str tier_model: (optional) The tier model.
    :attr str charge_unit_name: (optional) The charge unit name.
    :attr str charge_unit_quantity: (optional) The charge unit quantity.
    :attr str resource_display_name: (optional) Display name of the resource.
    :attr str charge_unit_display_name: (optional) Display name of the charge unit.
    :attr int usage_cap_qty: (optional) Usage limit for the metric.
    :attr List[Amount] amounts: (optional) The pricing per metric by country and
          currency.
    """

    def __init__(self,
                 *,
                 metric_id: str = None,
                 tier_model: str = None,
                 charge_unit_name: str = None,
                 charge_unit_quantity: str = None,
                 resource_display_name: str = None,
                 charge_unit_display_name: str = None,
                 usage_cap_qty: int = None,
                 amounts: List['Amount'] = None) -> None:
        """
        Initialize a Metrics object.

        :param str metric_id: (optional) The metric ID or part number.
        :param str tier_model: (optional) The tier model.
        :param str charge_unit_name: (optional) The charge unit name.
        :param str charge_unit_quantity: (optional) The charge unit quantity.
        :param str resource_display_name: (optional) Display name of the resource.
        :param str charge_unit_display_name: (optional) Display name of the charge
               unit.
        :param int usage_cap_qty: (optional) Usage limit for the metric.
        :param List[Amount] amounts: (optional) The pricing per metric by country
               and currency.
        """
        self.metric_id = metric_id
        self.tier_model = tier_model
        self.charge_unit_name = charge_unit_name
        self.charge_unit_quantity = charge_unit_quantity
        self.resource_display_name = resource_display_name
        self.charge_unit_display_name = charge_unit_display_name
        self.usage_cap_qty = usage_cap_qty
        self.amounts = amounts

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Metrics':
        """Initialize a Metrics object from a json dictionary."""
        args = {}
        if 'metric_id' in _dict:
            args['metric_id'] = _dict.get('metric_id')
        if 'tier_model' in _dict:
            args['tier_model'] = _dict.get('tier_model')
        if 'charge_unit_name' in _dict:
            args['charge_unit_name'] = _dict.get('charge_unit_name')
        if 'charge_unit_quantity' in _dict:
            args['charge_unit_quantity'] = _dict.get('charge_unit_quantity')
        if 'resource_display_name' in _dict:
            args['resource_display_name'] = _dict.get('resource_display_name')
        if 'charge_unit_display_name' in _dict:
            args['charge_unit_display_name'] = _dict.get('charge_unit_display_name')
        if 'usage_cap_qty' in _dict:
            args['usage_cap_qty'] = _dict.get('usage_cap_qty')
        if 'amounts' in _dict:
            args['amounts'] = [Amount.from_dict(x) for x in _dict.get('amounts')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Metrics object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'metric_id') and self.metric_id is not None:
            _dict['metric_id'] = self.metric_id
        if hasattr(self, 'tier_model') and self.tier_model is not None:
            _dict['tier_model'] = self.tier_model
        if hasattr(self, 'charge_unit_name') and self.charge_unit_name is not None:
            _dict['charge_unit_name'] = self.charge_unit_name
        if hasattr(self, 'charge_unit_quantity') and self.charge_unit_quantity is not None:
            _dict['charge_unit_quantity'] = self.charge_unit_quantity
        if hasattr(self, 'resource_display_name') and self.resource_display_name is not None:
            _dict['resource_display_name'] = self.resource_display_name
        if hasattr(self, 'charge_unit_display_name') and self.charge_unit_display_name is not None:
            _dict['charge_unit_display_name'] = self.charge_unit_display_name
        if hasattr(self, 'usage_cap_qty') and self.usage_cap_qty is not None:
            _dict['usage_cap_qty'] = self.usage_cap_qty
        if hasattr(self, 'amounts') and self.amounts is not None:
            _dict['amounts'] = [x.to_dict() for x in self.amounts]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Metrics object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Metrics') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Metrics') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ObjectMetadataBaseAlias():
    """
    Alias-related metadata.

    :attr str type: (optional) Type of alias.
    :attr str plan_id: (optional) Points to the plan that this object is an alias
          for.
    """

    def __init__(self,
                 *,
                 type: str = None,
                 plan_id: str = None) -> None:
        """
        Initialize a ObjectMetadataBaseAlias object.

        :param str type: (optional) Type of alias.
        :param str plan_id: (optional) Points to the plan that this object is an
               alias for.
        """
        self.type = type
        self.plan_id = plan_id

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ObjectMetadataBaseAlias':
        """Initialize a ObjectMetadataBaseAlias object from a json dictionary."""
        args = {}
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'plan_id' in _dict:
            args['plan_id'] = _dict.get('plan_id')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ObjectMetadataBaseAlias object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'plan_id') and self.plan_id is not None:
            _dict['plan_id'] = self.plan_id
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ObjectMetadataBaseAlias object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ObjectMetadataBaseAlias') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ObjectMetadataBaseAlias') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ObjectMetadataBasePlan():
    """
    Plan-related metadata.

    :attr bool bindable: (optional) Boolean value that describes whether the service
          can be bound to an application.
    :attr bool reservable: (optional) Boolean value that describes whether the
          service can be reserved.
    :attr bool allow_internal_users: (optional) Boolean value that describes whether
          the service can be used internally.
    :attr bool async_provisioning_supported: (optional) Boolean value that describes
          whether the service can be provisioned asynchronously.
    :attr bool async_unprovisioning_supported: (optional) Boolean value that
          describes whether the service can be unprovisioned asynchronously.
    :attr int test_check_interval: (optional) Test check interval.
    :attr str single_scope_instance: (optional) Single scope instance.
    :attr bool service_check_enabled: (optional) Boolean value that describes
          whether the service check is enabled.
    :attr str cf_guid: (optional) If the field is imported from Cloud Foundry, the
          Cloud Foundry region's GUID. This is a required field. For example,
          `us-south=123`.
    """

    def __init__(self,
                 *,
                 bindable: bool = None,
                 reservable: bool = None,
                 allow_internal_users: bool = None,
                 async_provisioning_supported: bool = None,
                 async_unprovisioning_supported: bool = None,
                 test_check_interval: int = None,
                 single_scope_instance: str = None,
                 service_check_enabled: bool = None,
                 cf_guid: str = None) -> None:
        """
        Initialize a ObjectMetadataBasePlan object.

        :param bool bindable: (optional) Boolean value that describes whether the
               service can be bound to an application.
        :param bool reservable: (optional) Boolean value that describes whether the
               service can be reserved.
        :param bool allow_internal_users: (optional) Boolean value that describes
               whether the service can be used internally.
        :param bool async_provisioning_supported: (optional) Boolean value that
               describes whether the service can be provisioned asynchronously.
        :param bool async_unprovisioning_supported: (optional) Boolean value that
               describes whether the service can be unprovisioned asynchronously.
        :param int test_check_interval: (optional) Test check interval.
        :param str single_scope_instance: (optional) Single scope instance.
        :param bool service_check_enabled: (optional) Boolean value that describes
               whether the service check is enabled.
        :param str cf_guid: (optional) If the field is imported from Cloud Foundry,
               the Cloud Foundry region's GUID. This is a required field. For example,
               `us-south=123`.
        """
        self.bindable = bindable
        self.reservable = reservable
        self.allow_internal_users = allow_internal_users
        self.async_provisioning_supported = async_provisioning_supported
        self.async_unprovisioning_supported = async_unprovisioning_supported
        self.test_check_interval = test_check_interval
        self.single_scope_instance = single_scope_instance
        self.service_check_enabled = service_check_enabled
        self.cf_guid = cf_guid

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ObjectMetadataBasePlan':
        """Initialize a ObjectMetadataBasePlan object from a json dictionary."""
        args = {}
        if 'bindable' in _dict:
            args['bindable'] = _dict.get('bindable')
        if 'reservable' in _dict:
            args['reservable'] = _dict.get('reservable')
        if 'allow_internal_users' in _dict:
            args['allow_internal_users'] = _dict.get('allow_internal_users')
        if 'async_provisioning_supported' in _dict:
            args['async_provisioning_supported'] = _dict.get('async_provisioning_supported')
        if 'async_unprovisioning_supported' in _dict:
            args['async_unprovisioning_supported'] = _dict.get('async_unprovisioning_supported')
        if 'test_check_interval' in _dict:
            args['test_check_interval'] = _dict.get('test_check_interval')
        if 'single_scope_instance' in _dict:
            args['single_scope_instance'] = _dict.get('single_scope_instance')
        if 'service_check_enabled' in _dict:
            args['service_check_enabled'] = _dict.get('service_check_enabled')
        if 'cf_guid' in _dict:
            args['cf_guid'] = _dict.get('cf_guid')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ObjectMetadataBasePlan object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'bindable') and self.bindable is not None:
            _dict['bindable'] = self.bindable
        if hasattr(self, 'reservable') and self.reservable is not None:
            _dict['reservable'] = self.reservable
        if hasattr(self, 'allow_internal_users') and self.allow_internal_users is not None:
            _dict['allow_internal_users'] = self.allow_internal_users
        if hasattr(self, 'async_provisioning_supported') and self.async_provisioning_supported is not None:
            _dict['async_provisioning_supported'] = self.async_provisioning_supported
        if hasattr(self, 'async_unprovisioning_supported') and self.async_unprovisioning_supported is not None:
            _dict['async_unprovisioning_supported'] = self.async_unprovisioning_supported
        if hasattr(self, 'test_check_interval') and self.test_check_interval is not None:
            _dict['test_check_interval'] = self.test_check_interval
        if hasattr(self, 'single_scope_instance') and self.single_scope_instance is not None:
            _dict['single_scope_instance'] = self.single_scope_instance
        if hasattr(self, 'service_check_enabled') and self.service_check_enabled is not None:
            _dict['service_check_enabled'] = self.service_check_enabled
        if hasattr(self, 'cf_guid') and self.cf_guid is not None:
            _dict['cf_guid'] = self.cf_guid
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ObjectMetadataBasePlan object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ObjectMetadataBasePlan') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ObjectMetadataBasePlan') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ObjectMetadataBaseService():
    """
    Service-related metadata.

    :attr str type: (optional) Type of service.
    :attr bool iam_compatible: (optional) Boolean value that describes whether the
          service is compatible with Identity and Access Management.
    :attr bool unique_api_key: (optional) Boolean value that describes whether the
          service has a unique API key.
    :attr bool provisionable: (optional) Boolean value that describes whether the
          service is provisionable or not. You may need sales or support to create this
          service.
    :attr bool async_provisioning_supported: (optional) Boolean value that describes
          whether the service supports asynchronous provisioning.
    :attr bool async_unprovisioning_supported: (optional) Boolean value that
          describes whether the service supports asynchronous unprovisioning.
    :attr str cf_guid: (optional) If the field is imported from Cloud Foundry, the
          Cloud Foundry region's GUID. This is a required field. For example,
          `us-south=123`.
    :attr bool bindable: (optional) Boolean value that describes whether you can
          create bindings for this service.
    :attr List[str] requires: (optional) Service dependencies.
    :attr bool plan_updateable: (optional) Boolean value that describes whether the
          service supports upgrade or downgrade for some plans.
    :attr str state: (optional) String that describes whether the service is active
          or inactive.
    :attr bool service_check_enabled: (optional) Boolean value that describes
          whether the service check is enabled.
    :attr int test_check_interval: (optional) Test check interval.
    :attr bool service_key_supported: (optional) Boolean value that describes
          whether the service supports service keys.
    """

    def __init__(self,
                 *,
                 type: str = None,
                 iam_compatible: bool = None,
                 unique_api_key: bool = None,
                 provisionable: bool = None,
                 async_provisioning_supported: bool = None,
                 async_unprovisioning_supported: bool = None,
                 cf_guid: str = None,
                 bindable: bool = None,
                 requires: List[str] = None,
                 plan_updateable: bool = None,
                 state: str = None,
                 service_check_enabled: bool = None,
                 test_check_interval: int = None,
                 service_key_supported: bool = None) -> None:
        """
        Initialize a ObjectMetadataBaseService object.

        :param str type: (optional) Type of service.
        :param bool iam_compatible: (optional) Boolean value that describes whether
               the service is compatible with Identity and Access Management.
        :param bool unique_api_key: (optional) Boolean value that describes whether
               the service has a unique API key.
        :param bool provisionable: (optional) Boolean value that describes whether
               the service is provisionable or not. You may need sales or support to
               create this service.
        :param bool async_provisioning_supported: (optional) Boolean value that
               describes whether the service supports asynchronous provisioning.
        :param bool async_unprovisioning_supported: (optional) Boolean value that
               describes whether the service supports asynchronous unprovisioning.
        :param str cf_guid: (optional) If the field is imported from Cloud Foundry,
               the Cloud Foundry region's GUID. This is a required field. For example,
               `us-south=123`.
        :param bool bindable: (optional) Boolean value that describes whether you
               can create bindings for this service.
        :param List[str] requires: (optional) Service dependencies.
        :param bool plan_updateable: (optional) Boolean value that describes
               whether the service supports upgrade or downgrade for some plans.
        :param str state: (optional) String that describes whether the service is
               active or inactive.
        :param bool service_check_enabled: (optional) Boolean value that describes
               whether the service check is enabled.
        :param int test_check_interval: (optional) Test check interval.
        :param bool service_key_supported: (optional) Boolean value that describes
               whether the service supports service keys.
        """
        self.type = type
        self.iam_compatible = iam_compatible
        self.unique_api_key = unique_api_key
        self.provisionable = provisionable
        self.async_provisioning_supported = async_provisioning_supported
        self.async_unprovisioning_supported = async_unprovisioning_supported
        self.cf_guid = cf_guid
        self.bindable = bindable
        self.requires = requires
        self.plan_updateable = plan_updateable
        self.state = state
        self.service_check_enabled = service_check_enabled
        self.test_check_interval = test_check_interval
        self.service_key_supported = service_key_supported

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ObjectMetadataBaseService':
        """Initialize a ObjectMetadataBaseService object from a json dictionary."""
        args = {}
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'iam_compatible' in _dict:
            args['iam_compatible'] = _dict.get('iam_compatible')
        if 'unique_api_key' in _dict:
            args['unique_api_key'] = _dict.get('unique_api_key')
        if 'provisionable' in _dict:
            args['provisionable'] = _dict.get('provisionable')
        if 'async_provisioning_supported' in _dict:
            args['async_provisioning_supported'] = _dict.get('async_provisioning_supported')
        if 'async_unprovisioning_supported' in _dict:
            args['async_unprovisioning_supported'] = _dict.get('async_unprovisioning_supported')
        if 'cf_guid' in _dict:
            args['cf_guid'] = _dict.get('cf_guid')
        if 'bindable' in _dict:
            args['bindable'] = _dict.get('bindable')
        if 'requires' in _dict:
            args['requires'] = _dict.get('requires')
        if 'plan_updateable' in _dict:
            args['plan_updateable'] = _dict.get('plan_updateable')
        if 'state' in _dict:
            args['state'] = _dict.get('state')
        if 'service_check_enabled' in _dict:
            args['service_check_enabled'] = _dict.get('service_check_enabled')
        if 'test_check_interval' in _dict:
            args['test_check_interval'] = _dict.get('test_check_interval')
        if 'service_key_supported' in _dict:
            args['service_key_supported'] = _dict.get('service_key_supported')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ObjectMetadataBaseService object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'iam_compatible') and self.iam_compatible is not None:
            _dict['iam_compatible'] = self.iam_compatible
        if hasattr(self, 'unique_api_key') and self.unique_api_key is not None:
            _dict['unique_api_key'] = self.unique_api_key
        if hasattr(self, 'provisionable') and self.provisionable is not None:
            _dict['provisionable'] = self.provisionable
        if hasattr(self, 'async_provisioning_supported') and self.async_provisioning_supported is not None:
            _dict['async_provisioning_supported'] = self.async_provisioning_supported
        if hasattr(self, 'async_unprovisioning_supported') and self.async_unprovisioning_supported is not None:
            _dict['async_unprovisioning_supported'] = self.async_unprovisioning_supported
        if hasattr(self, 'cf_guid') and self.cf_guid is not None:
            _dict['cf_guid'] = self.cf_guid
        if hasattr(self, 'bindable') and self.bindable is not None:
            _dict['bindable'] = self.bindable
        if hasattr(self, 'requires') and self.requires is not None:
            _dict['requires'] = self.requires
        if hasattr(self, 'plan_updateable') and self.plan_updateable is not None:
            _dict['plan_updateable'] = self.plan_updateable
        if hasattr(self, 'state') and self.state is not None:
            _dict['state'] = self.state
        if hasattr(self, 'service_check_enabled') and self.service_check_enabled is not None:
            _dict['service_check_enabled'] = self.service_check_enabled
        if hasattr(self, 'test_check_interval') and self.test_check_interval is not None:
            _dict['test_check_interval'] = self.test_check_interval
        if hasattr(self, 'service_key_supported') and self.service_key_supported is not None:
            _dict['service_key_supported'] = self.service_key_supported
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ObjectMetadataBaseService object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ObjectMetadataBaseService') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ObjectMetadataBaseService') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ObjectMetadataBaseSla():
    """
    Service Level Agreement related metadata.

    :attr str terms: (optional) Required Service License Agreement Terms of Use.
    :attr str tenancy: (optional) Required deployment type. Valid values are
          dedicated, local, or public. It can be Single or Multi tennancy, more
          specifically on a Server, VM, Physical, or Pod.
    :attr str provisioning: (optional) Provisioning reliability, for example, 99.95.
    :attr str responsiveness: (optional) Uptime reliability of the service, for
          example, 99.95.
    :attr ObjectMetadataBaseSlaDr dr: (optional) SLA Disaster Recovery-related
          metadata.
    """

    def __init__(self,
                 *,
                 terms: str = None,
                 tenancy: str = None,
                 provisioning: str = None,
                 responsiveness: str = None,
                 dr: 'ObjectMetadataBaseSlaDr' = None) -> None:
        """
        Initialize a ObjectMetadataBaseSla object.

        :param str terms: (optional) Required Service License Agreement Terms of
               Use.
        :param str tenancy: (optional) Required deployment type. Valid values are
               dedicated, local, or public. It can be Single or Multi tennancy, more
               specifically on a Server, VM, Physical, or Pod.
        :param str provisioning: (optional) Provisioning reliability, for example,
               99.95.
        :param str responsiveness: (optional) Uptime reliability of the service,
               for example, 99.95.
        :param ObjectMetadataBaseSlaDr dr: (optional) SLA Disaster Recovery-related
               metadata.
        """
        self.terms = terms
        self.tenancy = tenancy
        self.provisioning = provisioning
        self.responsiveness = responsiveness
        self.dr = dr

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ObjectMetadataBaseSla':
        """Initialize a ObjectMetadataBaseSla object from a json dictionary."""
        args = {}
        if 'terms' in _dict:
            args['terms'] = _dict.get('terms')
        if 'tenancy' in _dict:
            args['tenancy'] = _dict.get('tenancy')
        if 'provisioning' in _dict:
            args['provisioning'] = _dict.get('provisioning')
        if 'responsiveness' in _dict:
            args['responsiveness'] = _dict.get('responsiveness')
        if 'dr' in _dict:
            args['dr'] = ObjectMetadataBaseSlaDr.from_dict(_dict.get('dr'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ObjectMetadataBaseSla object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'terms') and self.terms is not None:
            _dict['terms'] = self.terms
        if hasattr(self, 'tenancy') and self.tenancy is not None:
            _dict['tenancy'] = self.tenancy
        if hasattr(self, 'provisioning') and self.provisioning is not None:
            _dict['provisioning'] = self.provisioning
        if hasattr(self, 'responsiveness') and self.responsiveness is not None:
            _dict['responsiveness'] = self.responsiveness
        if hasattr(self, 'dr') and self.dr is not None:
            _dict['dr'] = self.dr.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ObjectMetadataBaseSla object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ObjectMetadataBaseSla') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ObjectMetadataBaseSla') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ObjectMetadataBaseSlaDr():
    """
    SLA Disaster Recovery-related metadata.

    :attr bool dr: (optional) Required boolean value that describes whether disaster
          recovery is on.
    :attr str description: (optional) Description of the disaster recovery
          implementation.
    """

    def __init__(self,
                 *,
                 dr: bool = None,
                 description: str = None) -> None:
        """
        Initialize a ObjectMetadataBaseSlaDr object.

        :param bool dr: (optional) Required boolean value that describes whether
               disaster recovery is on.
        :param str description: (optional) Description of the disaster recovery
               implementation.
        """
        self.dr = dr
        self.description = description

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ObjectMetadataBaseSlaDr':
        """Initialize a ObjectMetadataBaseSlaDr object from a json dictionary."""
        args = {}
        if 'dr' in _dict:
            args['dr'] = _dict.get('dr')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ObjectMetadataBaseSlaDr object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'dr') and self.dr is not None:
            _dict['dr'] = self.dr
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ObjectMetadataBaseSlaDr object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ObjectMetadataBaseSlaDr') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ObjectMetadataBaseSlaDr') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ObjectMetadataBaseTemplate():
    """
    Template-related metadata.

    :attr List[str] services: (optional) List of required offering or plan IDs.
    :attr int default_memory: (optional) Cloud Foundry instance memory value.
    :attr str start_cmd: (optional) Start Command.
    :attr ObjectMetadataBaseTemplateSource source: (optional) Location of your
          applications source files.
    :attr str runtime_catalog_id: (optional) ID of the runtime.
    :attr str cf_runtime_id: (optional) ID of the Cloud Foundry runtime.
    :attr str template_id: (optional) ID of the boilerplate or template.
    :attr str executable_file: (optional) File path to the executable file for the
          template.
    :attr str buildpack: (optional) ID of the buildpack used by the template.
    :attr ObjectMetadataBaseTemplateEnvironmentVariables environment_variables:
          (optional) Environment variables for the template.
    """

    def __init__(self,
                 *,
                 services: List[str] = None,
                 default_memory: int = None,
                 start_cmd: str = None,
                 source: 'ObjectMetadataBaseTemplateSource' = None,
                 runtime_catalog_id: str = None,
                 cf_runtime_id: str = None,
                 template_id: str = None,
                 executable_file: str = None,
                 buildpack: str = None,
                 environment_variables: 'ObjectMetadataBaseTemplateEnvironmentVariables' = None) -> None:
        """
        Initialize a ObjectMetadataBaseTemplate object.

        :param List[str] services: (optional) List of required offering or plan
               IDs.
        :param int default_memory: (optional) Cloud Foundry instance memory value.
        :param str start_cmd: (optional) Start Command.
        :param ObjectMetadataBaseTemplateSource source: (optional) Location of your
               applications source files.
        :param str runtime_catalog_id: (optional) ID of the runtime.
        :param str cf_runtime_id: (optional) ID of the Cloud Foundry runtime.
        :param str template_id: (optional) ID of the boilerplate or template.
        :param str executable_file: (optional) File path to the executable file for
               the template.
        :param str buildpack: (optional) ID of the buildpack used by the template.
        :param ObjectMetadataBaseTemplateEnvironmentVariables
               environment_variables: (optional) Environment variables for the template.
        """
        self.services = services
        self.default_memory = default_memory
        self.start_cmd = start_cmd
        self.source = source
        self.runtime_catalog_id = runtime_catalog_id
        self.cf_runtime_id = cf_runtime_id
        self.template_id = template_id
        self.executable_file = executable_file
        self.buildpack = buildpack
        self.environment_variables = environment_variables

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ObjectMetadataBaseTemplate':
        """Initialize a ObjectMetadataBaseTemplate object from a json dictionary."""
        args = {}
        if 'services' in _dict:
            args['services'] = _dict.get('services')
        if 'default_memory' in _dict:
            args['default_memory'] = _dict.get('default_memory')
        if 'start_cmd' in _dict:
            args['start_cmd'] = _dict.get('start_cmd')
        if 'source' in _dict:
            args['source'] = ObjectMetadataBaseTemplateSource.from_dict(_dict.get('source'))
        if 'runtime_catalog_id' in _dict:
            args['runtime_catalog_id'] = _dict.get('runtime_catalog_id')
        if 'cf_runtime_id' in _dict:
            args['cf_runtime_id'] = _dict.get('cf_runtime_id')
        if 'template_id' in _dict:
            args['template_id'] = _dict.get('template_id')
        if 'executable_file' in _dict:
            args['executable_file'] = _dict.get('executable_file')
        if 'buildpack' in _dict:
            args['buildpack'] = _dict.get('buildpack')
        if 'environment_variables' in _dict:
            args['environment_variables'] = ObjectMetadataBaseTemplateEnvironmentVariables.from_dict(_dict.get('environment_variables'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ObjectMetadataBaseTemplate object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'services') and self.services is not None:
            _dict['services'] = self.services
        if hasattr(self, 'default_memory') and self.default_memory is not None:
            _dict['default_memory'] = self.default_memory
        if hasattr(self, 'start_cmd') and self.start_cmd is not None:
            _dict['start_cmd'] = self.start_cmd
        if hasattr(self, 'source') and self.source is not None:
            _dict['source'] = self.source.to_dict()
        if hasattr(self, 'runtime_catalog_id') and self.runtime_catalog_id is not None:
            _dict['runtime_catalog_id'] = self.runtime_catalog_id
        if hasattr(self, 'cf_runtime_id') and self.cf_runtime_id is not None:
            _dict['cf_runtime_id'] = self.cf_runtime_id
        if hasattr(self, 'template_id') and self.template_id is not None:
            _dict['template_id'] = self.template_id
        if hasattr(self, 'executable_file') and self.executable_file is not None:
            _dict['executable_file'] = self.executable_file
        if hasattr(self, 'buildpack') and self.buildpack is not None:
            _dict['buildpack'] = self.buildpack
        if hasattr(self, 'environment_variables') and self.environment_variables is not None:
            _dict['environment_variables'] = self.environment_variables.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ObjectMetadataBaseTemplate object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ObjectMetadataBaseTemplate') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ObjectMetadataBaseTemplate') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ObjectMetadataBaseTemplateEnvironmentVariables():
    """
    Environment variables for the template.

    :attr str key: (optional) Key is the editable first string in a key:value pair
          of environment variables.
    """

    def __init__(self,
                 *,
                 key: str = None) -> None:
        """
        Initialize a ObjectMetadataBaseTemplateEnvironmentVariables object.

        :param str key: (optional) Key is the editable first string in a key:value
               pair of environment variables.
        """
        self.key = key

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ObjectMetadataBaseTemplateEnvironmentVariables':
        """Initialize a ObjectMetadataBaseTemplateEnvironmentVariables object from a json dictionary."""
        args = {}
        if '_key_' in _dict:
            args['key'] = _dict.get('_key_')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ObjectMetadataBaseTemplateEnvironmentVariables object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'key') and self.key is not None:
            _dict['_key_'] = self.key
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ObjectMetadataBaseTemplateEnvironmentVariables object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ObjectMetadataBaseTemplateEnvironmentVariables') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ObjectMetadataBaseTemplateEnvironmentVariables') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ObjectMetadataBaseTemplateSource():
    """
    Location of your applications source files.

    :attr str path: (optional) Path to your application.
    :attr str type: (optional) Type of source, for example, git.
    :attr str url: (optional) URL to source.
    """

    def __init__(self,
                 *,
                 path: str = None,
                 type: str = None,
                 url: str = None) -> None:
        """
        Initialize a ObjectMetadataBaseTemplateSource object.

        :param str path: (optional) Path to your application.
        :param str type: (optional) Type of source, for example, git.
        :param str url: (optional) URL to source.
        """
        self.path = path
        self.type = type
        self.url = url

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ObjectMetadataBaseTemplateSource':
        """Initialize a ObjectMetadataBaseTemplateSource object from a json dictionary."""
        args = {}
        if 'path' in _dict:
            args['path'] = _dict.get('path')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'url' in _dict:
            args['url'] = _dict.get('url')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ObjectMetadataBaseTemplateSource object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'path') and self.path is not None:
            _dict['path'] = self.path
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'url') and self.url is not None:
            _dict['url'] = self.url
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ObjectMetadataBaseTemplateSource object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ObjectMetadataBaseTemplateSource') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ObjectMetadataBaseTemplateSource') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ObjectMetadataSet():
    """
    Model used to describe metadata object that can be set.

    :attr bool rc_compatible: (optional) Boolean value that describes whether the
          service is compatible with the Resource Controller.
    :attr UIMetaData ui: (optional) Information related to the UI presentation
          associated with a catalog entry.
    :attr List[str] compliance: (optional) Compliance information for HIPAA and PCI.
    :attr ObjectMetadataBaseService service: (optional) Service-related metadata.
    :attr ObjectMetadataBasePlan plan: (optional) Plan-related metadata.
    :attr ObjectMetadataBaseTemplate template: (optional) Template-related metadata.
    :attr ObjectMetadataBaseAlias alias: (optional) Alias-related metadata.
    :attr ObjectMetadataBaseSla sla: (optional) Service Level Agreement related
          metadata.
    :attr Callbacks callbacks: (optional) Callback-related information associated
          with a catalog entry.
    :attr str version: (optional) Optional version of the object.
    :attr str original_name: (optional) The original name of the object.
    :attr object other: (optional) Additional information.
    :attr PricingSet pricing: (optional) Pricing-related information.
    :attr DeploymentBase deployment: (optional) Deployment-related metadata.
    """

    def __init__(self,
                 *,
                 rc_compatible: bool = None,
                 ui: 'UIMetaData' = None,
                 compliance: List[str] = None,
                 service: 'ObjectMetadataBaseService' = None,
                 plan: 'ObjectMetadataBasePlan' = None,
                 template: 'ObjectMetadataBaseTemplate' = None,
                 alias: 'ObjectMetadataBaseAlias' = None,
                 sla: 'ObjectMetadataBaseSla' = None,
                 callbacks: 'Callbacks' = None,
                 version: str = None,
                 original_name: str = None,
                 other: object = None,
                 pricing: 'PricingSet' = None,
                 deployment: 'DeploymentBase' = None) -> None:
        """
        Initialize a ObjectMetadataSet object.

        :param bool rc_compatible: (optional) Boolean value that describes whether
               the service is compatible with the Resource Controller.
        :param UIMetaData ui: (optional) Information related to the UI presentation
               associated with a catalog entry.
        :param List[str] compliance: (optional) Compliance information for HIPAA
               and PCI.
        :param ObjectMetadataBaseService service: (optional) Service-related
               metadata.
        :param ObjectMetadataBasePlan plan: (optional) Plan-related metadata.
        :param ObjectMetadataBaseTemplate template: (optional) Template-related
               metadata.
        :param ObjectMetadataBaseAlias alias: (optional) Alias-related metadata.
        :param ObjectMetadataBaseSla sla: (optional) Service Level Agreement
               related metadata.
        :param Callbacks callbacks: (optional) Callback-related information
               associated with a catalog entry.
        :param str version: (optional) Optional version of the object.
        :param str original_name: (optional) The original name of the object.
        :param object other: (optional) Additional information.
        :param PricingSet pricing: (optional) Pricing-related information.
        :param DeploymentBase deployment: (optional) Deployment-related metadata.
        """
        self.rc_compatible = rc_compatible
        self.ui = ui
        self.compliance = compliance
        self.service = service
        self.plan = plan
        self.template = template
        self.alias = alias
        self.sla = sla
        self.callbacks = callbacks
        self.version = version
        self.original_name = original_name
        self.other = other
        self.pricing = pricing
        self.deployment = deployment

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ObjectMetadataSet':
        """Initialize a ObjectMetadataSet object from a json dictionary."""
        args = {}
        if 'rc_compatible' in _dict:
            args['rc_compatible'] = _dict.get('rc_compatible')
        if 'ui' in _dict:
            args['ui'] = UIMetaData.from_dict(_dict.get('ui'))
        if 'compliance' in _dict:
            args['compliance'] = _dict.get('compliance')
        if 'service' in _dict:
            args['service'] = ObjectMetadataBaseService.from_dict(_dict.get('service'))
        if 'plan' in _dict:
            args['plan'] = ObjectMetadataBasePlan.from_dict(_dict.get('plan'))
        if 'template' in _dict:
            args['template'] = ObjectMetadataBaseTemplate.from_dict(_dict.get('template'))
        if 'alias' in _dict:
            args['alias'] = ObjectMetadataBaseAlias.from_dict(_dict.get('alias'))
        if 'sla' in _dict:
            args['sla'] = ObjectMetadataBaseSla.from_dict(_dict.get('sla'))
        if 'callbacks' in _dict:
            args['callbacks'] = Callbacks.from_dict(_dict.get('callbacks'))
        if 'version' in _dict:
            args['version'] = _dict.get('version')
        if 'original_name' in _dict:
            args['original_name'] = _dict.get('original_name')
        if 'other' in _dict:
            args['other'] = _dict.get('other')
        if 'pricing' in _dict:
            args['pricing'] = PricingSet.from_dict(_dict.get('pricing'))
        if 'deployment' in _dict:
            args['deployment'] = DeploymentBase.from_dict(_dict.get('deployment'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ObjectMetadataSet object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'rc_compatible') and self.rc_compatible is not None:
            _dict['rc_compatible'] = self.rc_compatible
        if hasattr(self, 'ui') and self.ui is not None:
            _dict['ui'] = self.ui.to_dict()
        if hasattr(self, 'compliance') and self.compliance is not None:
            _dict['compliance'] = self.compliance
        if hasattr(self, 'service') and self.service is not None:
            _dict['service'] = self.service.to_dict()
        if hasattr(self, 'plan') and self.plan is not None:
            _dict['plan'] = self.plan.to_dict()
        if hasattr(self, 'template') and self.template is not None:
            _dict['template'] = self.template.to_dict()
        if hasattr(self, 'alias') and self.alias is not None:
            _dict['alias'] = self.alias.to_dict()
        if hasattr(self, 'sla') and self.sla is not None:
            _dict['sla'] = self.sla.to_dict()
        if hasattr(self, 'callbacks') and self.callbacks is not None:
            _dict['callbacks'] = self.callbacks.to_dict()
        if hasattr(self, 'version') and self.version is not None:
            _dict['version'] = self.version
        if hasattr(self, 'original_name') and self.original_name is not None:
            _dict['original_name'] = self.original_name
        if hasattr(self, 'other') and self.other is not None:
            _dict['other'] = self.other
        if hasattr(self, 'pricing') and self.pricing is not None:
            _dict['pricing'] = self.pricing.to_dict()
        if hasattr(self, 'deployment') and self.deployment is not None:
            _dict['deployment'] = self.deployment.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ObjectMetadataSet object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ObjectMetadataSet') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ObjectMetadataSet') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class Overview():
    """
    Overview is nested in the top level. The key value pair is `[_language_]overview_ui`.

    :attr str display_name: The translated display name.
    :attr str long_description: The translated long description.
    :attr str description: The translated description.
    """

    def __init__(self,
                 display_name: str,
                 long_description: str,
                 description: str) -> None:
        """
        Initialize a Overview object.

        :param str display_name: The translated display name.
        :param str long_description: The translated long description.
        :param str description: The translated description.
        """
        self.display_name = display_name
        self.long_description = long_description
        self.description = description

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Overview':
        """Initialize a Overview object from a json dictionary."""
        args = {}
        if 'display_name' in _dict:
            args['display_name'] = _dict.get('display_name')
        else:
            raise ValueError('Required property \'display_name\' not present in Overview JSON')
        if 'long_description' in _dict:
            args['long_description'] = _dict.get('long_description')
        else:
            raise ValueError('Required property \'long_description\' not present in Overview JSON')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        else:
            raise ValueError('Required property \'description\' not present in Overview JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Overview object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'display_name') and self.display_name is not None:
            _dict['display_name'] = self.display_name
        if hasattr(self, 'long_description') and self.long_description is not None:
            _dict['long_description'] = self.long_description
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Overview object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Overview') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Overview') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class OverviewUI():
    """
    Overview is nested in the top level. The key value pair is `[_language_]overview_ui`.

    """

    def __init__(self,
                 **kwargs) -> None:
        """
        Initialize a OverviewUI object.

        :param **kwargs: (optional) Any additional properties.
        """
        for _key, _value in kwargs.items():
            setattr(self, _key, _value)

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'OverviewUI':
        """Initialize a OverviewUI object from a json dictionary."""
        return cls(**_dict)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a OverviewUI object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        return vars(self)

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this OverviewUI object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'OverviewUI') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'OverviewUI') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class Price():
    """
    Pricing-related information.

    :attr int quantity_tier: (optional) Pricing tier.
    :attr float price: (optional) Price in the selected currency.
    """

    def __init__(self,
                 *,
                 quantity_tier: int = None,
                 price: float = None) -> None:
        """
        Initialize a Price object.

        :param int quantity_tier: (optional) Pricing tier.
        :param float price: (optional) Price in the selected currency.
        """
        self.quantity_tier = quantity_tier
        self.price = price

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Price':
        """Initialize a Price object from a json dictionary."""
        args = {}
        if 'quantity_tier' in _dict:
            args['quantity_tier'] = _dict.get('quantity_tier')
        if 'Price' in _dict:
            args['price'] = _dict.get('Price')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Price object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'quantity_tier') and self.quantity_tier is not None:
            _dict['quantity_tier'] = self.quantity_tier
        if hasattr(self, 'price') and self.price is not None:
            _dict['Price'] = self.price
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Price object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Price') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Price') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class PricingGet():
    """
    Pricing-related information.

    :attr str type: (optional) Type of plan. Valid values are `free`, `trial`,
          `paygo`, `bluemix-subscription`, and `ibm-subscription`.
    :attr str origin: (optional) Defines where the pricing originates.
    :attr StartingPrice starting_price: (optional) Plan-specific starting price
          information.
    :attr List[Metrics] metrics: (optional) Plan-specific cost metric structure.
    """

    def __init__(self,
                 *,
                 type: str = None,
                 origin: str = None,
                 starting_price: 'StartingPrice' = None,
                 metrics: List['Metrics'] = None) -> None:
        """
        Initialize a PricingGet object.

        :param str type: (optional) Type of plan. Valid values are `free`, `trial`,
               `paygo`, `bluemix-subscription`, and `ibm-subscription`.
        :param str origin: (optional) Defines where the pricing originates.
        :param StartingPrice starting_price: (optional) Plan-specific starting
               price information.
        :param List[Metrics] metrics: (optional) Plan-specific cost metric
               structure.
        """
        self.type = type
        self.origin = origin
        self.starting_price = starting_price
        self.metrics = metrics

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'PricingGet':
        """Initialize a PricingGet object from a json dictionary."""
        args = {}
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'origin' in _dict:
            args['origin'] = _dict.get('origin')
        if 'starting_price' in _dict:
            args['starting_price'] = StartingPrice.from_dict(_dict.get('starting_price'))
        if 'metrics' in _dict:
            args['metrics'] = [Metrics.from_dict(x) for x in _dict.get('metrics')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a PricingGet object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'origin') and self.origin is not None:
            _dict['origin'] = self.origin
        if hasattr(self, 'starting_price') and self.starting_price is not None:
            _dict['starting_price'] = self.starting_price.to_dict()
        if hasattr(self, 'metrics') and self.metrics is not None:
            _dict['metrics'] = [x.to_dict() for x in self.metrics]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this PricingGet object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'PricingGet') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'PricingGet') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class PricingSet():
    """
    Pricing-related information.

    :attr str type: (optional) Type of plan. Valid values are `free`, `trial`,
          `paygo`, `bluemix-subscription`, and `ibm-subscription`.
    :attr str origin: (optional) Defines where the pricing originates.
    :attr StartingPrice starting_price: (optional) Plan-specific starting price
          information.
    """

    def __init__(self,
                 *,
                 type: str = None,
                 origin: str = None,
                 starting_price: 'StartingPrice' = None) -> None:
        """
        Initialize a PricingSet object.

        :param str type: (optional) Type of plan. Valid values are `free`, `trial`,
               `paygo`, `bluemix-subscription`, and `ibm-subscription`.
        :param str origin: (optional) Defines where the pricing originates.
        :param StartingPrice starting_price: (optional) Plan-specific starting
               price information.
        """
        self.type = type
        self.origin = origin
        self.starting_price = starting_price

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'PricingSet':
        """Initialize a PricingSet object from a json dictionary."""
        args = {}
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'origin' in _dict:
            args['origin'] = _dict.get('origin')
        if 'starting_price' in _dict:
            args['starting_price'] = StartingPrice.from_dict(_dict.get('starting_price'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a PricingSet object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'origin') and self.origin is not None:
            _dict['origin'] = self.origin
        if hasattr(self, 'starting_price') and self.starting_price is not None:
            _dict['starting_price'] = self.starting_price.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this PricingSet object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'PricingSet') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'PricingSet') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class Provider():
    """
    Information related to the provider associated with a catalog entry.

    :attr str email: Provider's email address for this catalog entry.
    :attr str name: Provider's name, for example, IBM.
    :attr str contact: (optional) Provider's contact name.
    :attr str support_email: (optional) Provider's support email.
    :attr str phone: (optional) Provider's contact phone.
    """

    def __init__(self,
                 email: str,
                 name: str,
                 *,
                 contact: str = None,
                 support_email: str = None,
                 phone: str = None) -> None:
        """
        Initialize a Provider object.

        :param str email: Provider's email address for this catalog entry.
        :param str name: Provider's name, for example, IBM.
        :param str contact: (optional) Provider's contact name.
        :param str support_email: (optional) Provider's support email.
        :param str phone: (optional) Provider's contact phone.
        """
        self.email = email
        self.name = name
        self.contact = contact
        self.support_email = support_email
        self.phone = phone

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Provider':
        """Initialize a Provider object from a json dictionary."""
        args = {}
        if 'email' in _dict:
            args['email'] = _dict.get('email')
        else:
            raise ValueError('Required property \'email\' not present in Provider JSON')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        else:
            raise ValueError('Required property \'name\' not present in Provider JSON')
        if 'contact' in _dict:
            args['contact'] = _dict.get('contact')
        if 'support_email' in _dict:
            args['support_email'] = _dict.get('support_email')
        if 'phone' in _dict:
            args['phone'] = _dict.get('phone')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Provider object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'email') and self.email is not None:
            _dict['email'] = self.email
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'contact') and self.contact is not None:
            _dict['contact'] = self.contact
        if hasattr(self, 'support_email') and self.support_email is not None:
            _dict['support_email'] = self.support_email
        if hasattr(self, 'phone') and self.phone is not None:
            _dict['phone'] = self.phone
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Provider object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Provider') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Provider') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class StartingPrice():
    """
    Plan-specific starting price information.

    :attr str plan_id: (optional) ID of the plan the starting price is calculated.
    :attr str deployment_id: (optional) ID of the deployment the starting price is
          calculated.
    :attr List[Amount] amount: (optional) The pricing per metric by country and
          currency.
    """

    def __init__(self,
                 *,
                 plan_id: str = None,
                 deployment_id: str = None,
                 amount: List['Amount'] = None) -> None:
        """
        Initialize a StartingPrice object.

        :param str plan_id: (optional) ID of the plan the starting price is
               calculated.
        :param str deployment_id: (optional) ID of the deployment the starting
               price is calculated.
        :param List[Amount] amount: (optional) The pricing per metric by country
               and currency.
        """
        self.plan_id = plan_id
        self.deployment_id = deployment_id
        self.amount = amount

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'StartingPrice':
        """Initialize a StartingPrice object from a json dictionary."""
        args = {}
        if 'plan_id' in _dict:
            args['plan_id'] = _dict.get('plan_id')
        if 'deployment_id' in _dict:
            args['deployment_id'] = _dict.get('deployment_id')
        if 'amount' in _dict:
            args['amount'] = [Amount.from_dict(x) for x in _dict.get('amount')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a StartingPrice object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'plan_id') and self.plan_id is not None:
            _dict['plan_id'] = self.plan_id
        if hasattr(self, 'deployment_id') and self.deployment_id is not None:
            _dict['deployment_id'] = self.deployment_id
        if hasattr(self, 'amount') and self.amount is not None:
            _dict['amount'] = [x.to_dict() for x in self.amount]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this StartingPrice object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'StartingPrice') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'StartingPrice') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class Strings():
    """
    Information related to a translated text message.

    :attr List[Bullets] bullets: (optional) Presentation information related to list
          delimiters.
    :attr List[UIMetaMedia] media: (optional) Media-related metadata.
    :attr str not_creatable_msg: (optional) Warning that a message is not creatable.
    :attr str not_creatable_robot_msg: (optional) Warning that a robot message is
          not creatable.
    :attr str deprecation_warning: (optional) Warning for deprecation.
    :attr str popup_warning_message: (optional) Popup warning message.
    :attr str instruction: (optional) Instructions for UI strings.
    """

    def __init__(self,
                 *,
                 bullets: List['Bullets'] = None,
                 media: List['UIMetaMedia'] = None,
                 not_creatable_msg: str = None,
                 not_creatable_robot_msg: str = None,
                 deprecation_warning: str = None,
                 popup_warning_message: str = None,
                 instruction: str = None) -> None:
        """
        Initialize a Strings object.

        :param List[Bullets] bullets: (optional) Presentation information related
               to list delimiters.
        :param List[UIMetaMedia] media: (optional) Media-related metadata.
        :param str not_creatable_msg: (optional) Warning that a message is not
               creatable.
        :param str not_creatable_robot_msg: (optional) Warning that a robot message
               is not creatable.
        :param str deprecation_warning: (optional) Warning for deprecation.
        :param str popup_warning_message: (optional) Popup warning message.
        :param str instruction: (optional) Instructions for UI strings.
        """
        self.bullets = bullets
        self.media = media
        self.not_creatable_msg = not_creatable_msg
        self.not_creatable_robot_msg = not_creatable_robot_msg
        self.deprecation_warning = deprecation_warning
        self.popup_warning_message = popup_warning_message
        self.instruction = instruction

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Strings':
        """Initialize a Strings object from a json dictionary."""
        args = {}
        if 'bullets' in _dict:
            args['bullets'] = [Bullets.from_dict(x) for x in _dict.get('bullets')]
        if 'media' in _dict:
            args['media'] = [UIMetaMedia.from_dict(x) for x in _dict.get('media')]
        if 'not_creatable_msg' in _dict:
            args['not_creatable_msg'] = _dict.get('not_creatable_msg')
        if 'not_creatable__robot_msg' in _dict:
            args['not_creatable_robot_msg'] = _dict.get('not_creatable__robot_msg')
        if 'deprecation_warning' in _dict:
            args['deprecation_warning'] = _dict.get('deprecation_warning')
        if 'popup_warning_message' in _dict:
            args['popup_warning_message'] = _dict.get('popup_warning_message')
        if 'instruction' in _dict:
            args['instruction'] = _dict.get('instruction')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Strings object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'bullets') and self.bullets is not None:
            _dict['bullets'] = [x.to_dict() for x in self.bullets]
        if hasattr(self, 'media') and self.media is not None:
            _dict['media'] = [x.to_dict() for x in self.media]
        if hasattr(self, 'not_creatable_msg') and self.not_creatable_msg is not None:
            _dict['not_creatable_msg'] = self.not_creatable_msg
        if hasattr(self, 'not_creatable_robot_msg') and self.not_creatable_robot_msg is not None:
            _dict['not_creatable__robot_msg'] = self.not_creatable_robot_msg
        if hasattr(self, 'deprecation_warning') and self.deprecation_warning is not None:
            _dict['deprecation_warning'] = self.deprecation_warning
        if hasattr(self, 'popup_warning_message') and self.popup_warning_message is not None:
            _dict['popup_warning_message'] = self.popup_warning_message
        if hasattr(self, 'instruction') and self.instruction is not None:
            _dict['instruction'] = self.instruction
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Strings object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Strings') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Strings') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class UIMetaData():
    """
    Information related to the UI presentation associated with a catalog entry.

    :attr I18N strings: (optional) Language specific translation of translation
          properties, like label and description.
    :attr URLS urls: (optional) UI based URLs.
    :attr str embeddable_dashboard: (optional) Describes how the embeddable
          dashboard is rendered.
    :attr bool embeddable_dashboard_full_width: (optional) Describes whether the
          embeddable dashboard is rendered at the full width.
    :attr List[str] navigation_order: (optional) Defines the order of information
          presented.
    :attr bool not_creatable: (optional) Describes whether this entry is able to be
          created from the UI element or CLI.
    :attr bool reservable: (optional) Describes whether a plan or flavor is
          reservable.
    :attr str primary_offering_id: (optional) ID of the primary offering for a
          group.
    :attr bool accessible_during_provision: (optional) Alert to ACE to allow
          instance UI to be accessible while the provisioning state of instance is in
          progress.
    :attr int side_by_side_index: (optional) Specifies a side by side ordering
          weight to the UI.
    :attr datetime end_of_service_time: (optional) Date and time the service will no
          longer be available.
    """

    def __init__(self,
                 *,
                 strings: 'I18N' = None,
                 urls: 'URLS' = None,
                 embeddable_dashboard: str = None,
                 embeddable_dashboard_full_width: bool = None,
                 navigation_order: List[str] = None,
                 not_creatable: bool = None,
                 reservable: bool = None,
                 primary_offering_id: str = None,
                 accessible_during_provision: bool = None,
                 side_by_side_index: int = None,
                 end_of_service_time: datetime = None) -> None:
        """
        Initialize a UIMetaData object.

        :param I18N strings: (optional) Language specific translation of
               translation properties, like label and description.
        :param URLS urls: (optional) UI based URLs.
        :param str embeddable_dashboard: (optional) Describes how the embeddable
               dashboard is rendered.
        :param bool embeddable_dashboard_full_width: (optional) Describes whether
               the embeddable dashboard is rendered at the full width.
        :param List[str] navigation_order: (optional) Defines the order of
               information presented.
        :param bool not_creatable: (optional) Describes whether this entry is able
               to be created from the UI element or CLI.
        :param bool reservable: (optional) Describes whether a plan or flavor is
               reservable.
        :param str primary_offering_id: (optional) ID of the primary offering for a
               group.
        :param bool accessible_during_provision: (optional) Alert to ACE to allow
               instance UI to be accessible while the provisioning state of instance is in
               progress.
        :param int side_by_side_index: (optional) Specifies a side by side ordering
               weight to the UI.
        :param datetime end_of_service_time: (optional) Date and time the service
               will no longer be available.
        """
        self.strings = strings
        self.urls = urls
        self.embeddable_dashboard = embeddable_dashboard
        self.embeddable_dashboard_full_width = embeddable_dashboard_full_width
        self.navigation_order = navigation_order
        self.not_creatable = not_creatable
        self.reservable = reservable
        self.primary_offering_id = primary_offering_id
        self.accessible_during_provision = accessible_during_provision
        self.side_by_side_index = side_by_side_index
        self.end_of_service_time = end_of_service_time

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'UIMetaData':
        """Initialize a UIMetaData object from a json dictionary."""
        args = {}
        if 'strings' in _dict:
            args['strings'] = I18N.from_dict(_dict.get('strings'))
        if 'urls' in _dict:
            args['urls'] = URLS.from_dict(_dict.get('urls'))
        if 'embeddable_dashboard' in _dict:
            args['embeddable_dashboard'] = _dict.get('embeddable_dashboard')
        if 'embeddable_dashboard_full_width' in _dict:
            args['embeddable_dashboard_full_width'] = _dict.get('embeddable_dashboard_full_width')
        if 'navigation_order' in _dict:
            args['navigation_order'] = _dict.get('navigation_order')
        if 'not_creatable' in _dict:
            args['not_creatable'] = _dict.get('not_creatable')
        if 'reservable' in _dict:
            args['reservable'] = _dict.get('reservable')
        if 'primary_offering_id' in _dict:
            args['primary_offering_id'] = _dict.get('primary_offering_id')
        if 'accessible_during_provision' in _dict:
            args['accessible_during_provision'] = _dict.get('accessible_during_provision')
        if 'side_by_side_index' in _dict:
            args['side_by_side_index'] = _dict.get('side_by_side_index')
        if 'end_of_service_time' in _dict:
            args['end_of_service_time'] = string_to_datetime(_dict.get('end_of_service_time'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a UIMetaData object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'strings') and self.strings is not None:
            _dict['strings'] = self.strings.to_dict()
        if hasattr(self, 'urls') and self.urls is not None:
            _dict['urls'] = self.urls.to_dict()
        if hasattr(self, 'embeddable_dashboard') and self.embeddable_dashboard is not None:
            _dict['embeddable_dashboard'] = self.embeddable_dashboard
        if hasattr(self, 'embeddable_dashboard_full_width') and self.embeddable_dashboard_full_width is not None:
            _dict['embeddable_dashboard_full_width'] = self.embeddable_dashboard_full_width
        if hasattr(self, 'navigation_order') and self.navigation_order is not None:
            _dict['navigation_order'] = self.navigation_order
        if hasattr(self, 'not_creatable') and self.not_creatable is not None:
            _dict['not_creatable'] = self.not_creatable
        if hasattr(self, 'reservable') and self.reservable is not None:
            _dict['reservable'] = self.reservable
        if hasattr(self, 'primary_offering_id') and self.primary_offering_id is not None:
            _dict['primary_offering_id'] = self.primary_offering_id
        if hasattr(self, 'accessible_during_provision') and self.accessible_during_provision is not None:
            _dict['accessible_during_provision'] = self.accessible_during_provision
        if hasattr(self, 'side_by_side_index') and self.side_by_side_index is not None:
            _dict['side_by_side_index'] = self.side_by_side_index
        if hasattr(self, 'end_of_service_time') and self.end_of_service_time is not None:
            _dict['end_of_service_time'] = datetime_to_string(self.end_of_service_time)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this UIMetaData object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'UIMetaData') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'UIMetaData') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class UIMetaMedia():
    """
    Media-related metadata.

    :attr str caption: (optional) Caption for an image.
    :attr str thumbnail_url: (optional) URL for thumbnail image.
    :attr str type: (optional) Type of media.
    :attr str url: (optional) URL for media.
    :attr Bullets source: (optional) Information related to list delimiters.
    """

    def __init__(self,
                 *,
                 caption: str = None,
                 thumbnail_url: str = None,
                 type: str = None,
                 url: str = None,
                 source: 'Bullets' = None) -> None:
        """
        Initialize a UIMetaMedia object.

        :param str caption: (optional) Caption for an image.
        :param str thumbnail_url: (optional) URL for thumbnail image.
        :param str type: (optional) Type of media.
        :param str url: (optional) URL for media.
        :param Bullets source: (optional) Information related to list delimiters.
        """
        self.caption = caption
        self.thumbnail_url = thumbnail_url
        self.type = type
        self.url = url
        self.source = source

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'UIMetaMedia':
        """Initialize a UIMetaMedia object from a json dictionary."""
        args = {}
        if 'caption' in _dict:
            args['caption'] = _dict.get('caption')
        if 'thumbnail_url' in _dict:
            args['thumbnail_url'] = _dict.get('thumbnail_url')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'URL' in _dict:
            args['url'] = _dict.get('URL')
        if 'source' in _dict:
            args['source'] = Bullets.from_dict(_dict.get('source'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a UIMetaMedia object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'caption') and self.caption is not None:
            _dict['caption'] = self.caption
        if hasattr(self, 'thumbnail_url') and self.thumbnail_url is not None:
            _dict['thumbnail_url'] = self.thumbnail_url
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'url') and self.url is not None:
            _dict['URL'] = self.url
        if hasattr(self, 'source') and self.source is not None:
            _dict['source'] = self.source.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this UIMetaMedia object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'UIMetaMedia') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'UIMetaMedia') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class URLS():
    """
    UI based URLs.

    :attr str doc_url: (optional) URL for documentation.
    :attr str instructions_url: (optional) URL for usage instructions.
    :attr str api_url: (optional) API URL.
    :attr str create_url: (optional) URL Creation UI / API.
    :attr str sdk_download_url: (optional) URL to downlaod an SDK.
    :attr str terms_url: (optional) URL to the terms of use for your service.
    :attr str custom_create_page_url: (optional) URL to the custom create page for
          your serivce.
    :attr str catalog_details_url: (optional) URL to the catalog details page for
          your serivce.
    :attr str deprecation_doc_url: (optional) URL for deprecation documentation.
    """

    def __init__(self,
                 *,
                 doc_url: str = None,
                 instructions_url: str = None,
                 api_url: str = None,
                 create_url: str = None,
                 sdk_download_url: str = None,
                 terms_url: str = None,
                 custom_create_page_url: str = None,
                 catalog_details_url: str = None,
                 deprecation_doc_url: str = None) -> None:
        """
        Initialize a URLS object.

        :param str doc_url: (optional) URL for documentation.
        :param str instructions_url: (optional) URL for usage instructions.
        :param str api_url: (optional) API URL.
        :param str create_url: (optional) URL Creation UI / API.
        :param str sdk_download_url: (optional) URL to downlaod an SDK.
        :param str terms_url: (optional) URL to the terms of use for your service.
        :param str custom_create_page_url: (optional) URL to the custom create page
               for your serivce.
        :param str catalog_details_url: (optional) URL to the catalog details page
               for your serivce.
        :param str deprecation_doc_url: (optional) URL for deprecation
               documentation.
        """
        self.doc_url = doc_url
        self.instructions_url = instructions_url
        self.api_url = api_url
        self.create_url = create_url
        self.sdk_download_url = sdk_download_url
        self.terms_url = terms_url
        self.custom_create_page_url = custom_create_page_url
        self.catalog_details_url = catalog_details_url
        self.deprecation_doc_url = deprecation_doc_url

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'URLS':
        """Initialize a URLS object from a json dictionary."""
        args = {}
        if 'doc_url' in _dict:
            args['doc_url'] = _dict.get('doc_url')
        if 'instructions_url' in _dict:
            args['instructions_url'] = _dict.get('instructions_url')
        if 'api_url' in _dict:
            args['api_url'] = _dict.get('api_url')
        if 'create_url' in _dict:
            args['create_url'] = _dict.get('create_url')
        if 'sdk_download_url' in _dict:
            args['sdk_download_url'] = _dict.get('sdk_download_url')
        if 'terms_url' in _dict:
            args['terms_url'] = _dict.get('terms_url')
        if 'custom_create_page_url' in _dict:
            args['custom_create_page_url'] = _dict.get('custom_create_page_url')
        if 'catalog_details_url' in _dict:
            args['catalog_details_url'] = _dict.get('catalog_details_url')
        if 'deprecation_doc_url' in _dict:
            args['deprecation_doc_url'] = _dict.get('deprecation_doc_url')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a URLS object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'doc_url') and self.doc_url is not None:
            _dict['doc_url'] = self.doc_url
        if hasattr(self, 'instructions_url') and self.instructions_url is not None:
            _dict['instructions_url'] = self.instructions_url
        if hasattr(self, 'api_url') and self.api_url is not None:
            _dict['api_url'] = self.api_url
        if hasattr(self, 'create_url') and self.create_url is not None:
            _dict['create_url'] = self.create_url
        if hasattr(self, 'sdk_download_url') and self.sdk_download_url is not None:
            _dict['sdk_download_url'] = self.sdk_download_url
        if hasattr(self, 'terms_url') and self.terms_url is not None:
            _dict['terms_url'] = self.terms_url
        if hasattr(self, 'custom_create_page_url') and self.custom_create_page_url is not None:
            _dict['custom_create_page_url'] = self.custom_create_page_url
        if hasattr(self, 'catalog_details_url') and self.catalog_details_url is not None:
            _dict['catalog_details_url'] = self.catalog_details_url
        if hasattr(self, 'deprecation_doc_url') and self.deprecation_doc_url is not None:
            _dict['deprecation_doc_url'] = self.deprecation_doc_url
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this URLS object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'URLS') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'URLS') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class Visibility():
    """
    Information related to the visibility of a catalog entry.

    :attr str restrictions: (optional) This controls the overall visibility. It is
          an enum of *public*, *ibm_only*, and *private*. public means it is visible to
          all. ibm_only means it is visible to all IBM unless their account is explicitly
          excluded. private means it is visible only to the included accounts.
    :attr str owner: (optional) IAM Scope-related information associated with a
          catalog entry.
    :attr VisibilityDetail include: (optional) Visibility details related to a
          catalog entry.
    :attr VisibilityDetail exclude: (optional) Visibility details related to a
          catalog entry.
    :attr bool approved: (optional) Determines whether the owning account has full
          control over the visibility of the entry such as adding non-IBM accounts to the
          whitelist and making entries `private`, `ibm_only` or `public`.
    """

    def __init__(self,
                 *,
                 restrictions: str = None,
                 owner: str = None,
                 include: 'VisibilityDetail' = None,
                 exclude: 'VisibilityDetail' = None,
                 approved: bool = None) -> None:
        """
        Initialize a Visibility object.

        :param VisibilityDetail include: (optional) Visibility details related to a
               catalog entry.
        :param VisibilityDetail exclude: (optional) Visibility details related to a
               catalog entry.
        """
        self.restrictions = restrictions
        self.owner = owner
        self.include = include
        self.exclude = exclude
        self.approved = approved

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Visibility':
        """Initialize a Visibility object from a json dictionary."""
        args = {}
        if 'restrictions' in _dict:
            args['restrictions'] = _dict.get('restrictions')
        if 'owner' in _dict:
            args['owner'] = _dict.get('owner')
        if 'include' in _dict:
            args['include'] = VisibilityDetail.from_dict(_dict.get('include'))
        if 'exclude' in _dict:
            args['exclude'] = VisibilityDetail.from_dict(_dict.get('exclude'))
        if 'approved' in _dict:
            args['approved'] = _dict.get('approved')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Visibility object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'restrictions') and getattr(self, 'restrictions') is not None:
            _dict['restrictions'] = getattr(self, 'restrictions')
        if hasattr(self, 'owner') and getattr(self, 'owner') is not None:
            _dict['owner'] = getattr(self, 'owner')
        if hasattr(self, 'include') and self.include is not None:
            _dict['include'] = self.include.to_dict()
        if hasattr(self, 'exclude') and self.exclude is not None:
            _dict['exclude'] = self.exclude.to_dict()
        if hasattr(self, 'approved') and getattr(self, 'approved') is not None:
            _dict['approved'] = getattr(self, 'approved')
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Visibility object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Visibility') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Visibility') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class VisibilityDetail():
    """
    Visibility details related to a catalog entry.

    :attr VisibilityDetailAccounts accounts: Information related to the accounts for
          which a catalog entry is visible.
    """

    def __init__(self,
                 accounts: 'VisibilityDetailAccounts') -> None:
        """
        Initialize a VisibilityDetail object.

        :param VisibilityDetailAccounts accounts: Information related to the
               accounts for which a catalog entry is visible.
        """
        self.accounts = accounts

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'VisibilityDetail':
        """Initialize a VisibilityDetail object from a json dictionary."""
        args = {}
        if 'accounts' in _dict:
            args['accounts'] = VisibilityDetailAccounts.from_dict(_dict.get('accounts'))
        else:
            raise ValueError('Required property \'accounts\' not present in VisibilityDetail JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a VisibilityDetail object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'accounts') and self.accounts is not None:
            _dict['accounts'] = self.accounts.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this VisibilityDetail object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'VisibilityDetail') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'VisibilityDetail') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class VisibilityDetailAccounts():
    """
    Information related to the accounts for which a catalog entry is visible.

    :attr str accountid: (optional) (_accountid_) is the GUID of the account and the
          value is the scope of who set it. For setting visibility use "" as the value. It
          is replaced with the owner scope when saved.
    """

    def __init__(self,
                 *,
                 accountid: str = None) -> None:
        """
        Initialize a VisibilityDetailAccounts object.

        :param str accountid: (optional) (_accountid_) is the GUID of the account
               and the value is the scope of who set it. For setting visibility use "" as
               the value. It is replaced with the owner scope when saved.
        """
        self.accountid = accountid

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'VisibilityDetailAccounts':
        """Initialize a VisibilityDetailAccounts object from a json dictionary."""
        args = {}
        if '_accountid_' in _dict:
            args['accountid'] = _dict.get('_accountid_')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a VisibilityDetailAccounts object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'accountid') and self.accountid is not None:
            _dict['_accountid_'] = self.accountid
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this VisibilityDetailAccounts object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'VisibilityDetailAccounts') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'VisibilityDetailAccounts') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other