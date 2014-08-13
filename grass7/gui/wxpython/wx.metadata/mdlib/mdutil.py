#!/usr/bin/env python
# -*- coding: utf-8
"""
@package mdgrass
@module  v.info.iso, r.info.iso, g.gui.metadata
@brief   Global methods for metadata management

Methods:
-mdutil::removeNonAscii
-mdutil::yesNo
-mdutil::findBetween
-mdutil::replaceXMLReservedChar
-mdutil::pathToMapset
-mdutil::grassProfileValidator
-mdutil::isnpireValidator

(C) 2014 by the GRASS Development Team
This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author Matej Krejci <matejkrejci gmail.com> (GSoC 2014)
"""

import string
import os
from grass.script import core as grass
import wx


def removeNonAscii(s):
    '''Removed non ascii char
    '''
    s = filter(lambda x: x in string.printable, s)
    return s


def yesNo(parent, question, caption='Yes or no?'):

    dlg = wx.MessageDialog(parent, question, caption, wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal() == wx.ID_YES
    dlg.Destroy()
    return result


def findBetween(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except:
        return ""


def replaceXMLReservedChar(inp):
    if inp:
        import re

        inp = re.sub('<', '&lt;', inp)
        inp = re.sub('>', '&gt;', inp)
        inp = re.sub('&', '&amp;', inp)
        inp = re.sub('%', '&#37;', inp)
    return inp


def pathToMapset():
    gisenvDict = grass.gisenv()
    return os.path.join(gisenvDict['GISDBASE'], gisenvDict['LOCATION_NAME'], gisenvDict['MAPSET'])


def grassProfileValidator(md):
    '''function for validation GRASS BASIC XML-OWSLib  file-object'''

    result = {}
    result["status"] = "succeded"
    result["errors"] = []
    result["num_of_errors"] = "0"
    errors = 0

    if md.identification is None:
        result["errors"].append("gmd:CI_ResponsibleParty: Organization missing")
        result["errors"].append("gmd:CI_ResponsibleParty: E-mail missing")
        result["errors"].append("gmd:CI_ResponsibleParty: Role missing")
        result["errors"].append("gmd:md_DataIdentification: Title is missing")
        result["errors"].append("gmd:md_DataIdentification: Abstract is missing")
        result["errors"].append("gmd:md_ScopeCode: Resource Type is missing")
        result["errors"].append("gmd:RS_Identifier: Unique Resource Identifier is missing")
        result["errors"].append("gmd:EX_Extent: extent element is missing")
        result["errors"].append("gmd:EX_GeographicBoundingBox: bbox is missing")
        result["errors"].append("Both gmd:EX_TemporalExtent and gmd:CI_Date are missing")
        result["errors"].append("gmd:useLimitation is missing")
        errors += 20
    else:
        if len(md.identification.contact) < 1 or md.identification.contact is None:
            result["errors"].append("gmd:CI_ResponsibleParty: Organization missing")
            result["errors"].append("gmd:CI_ResponsibleParty: E-mail missing")
            result["errors"].append("gmd:CI_ResponsibleParty: Role missing")
            errors += 3
        else:
                if md.identification.contact[0].organization is (None or ''):
                    result["errors"].append("gmd:CI_ResponsibleParty: Organization missing")
                    errors += 1

                if md.identification.contact[0].email is (None or ''):
                    result["errors"].append("gmd:CI_ResponsibleParty: E-mail missing")
                    errors += 1

                if md.identification.contact[0].role is (None or ''):
                    result["errors"].append("gmd:CI_ResponsibleParty: Role missing")
                    errors += 1

        if md.identification.title is (None or ''):
            result["errors"].append("gmd:md_DataIdentification: Title is missing")
            errors += 1
        if md.identification.abstract is (None or ''):
            result["errors"].append("gmd:md_DataIdentification: Abstract is missing")
            errors += 1
        if md.identification.identtype is '':
            result["errors"].append("gmd:md_ScopeCode: Resource Type is missing")
            errors += 1

        if md.identification.extent is None:
            result["errors"].append("gmd:EX_Extent: extent element is missing")
            errors += 4
        else:
            if md.identification.extent.boundingBox is None:
                result["errors"].append("gmd:EX_GeographicBoundingBox: bbox is missing")
                errors += 4
            else:
                if md.identification.extent.boundingBox.minx is (None or ''):
                    result["errors"].append("gmd:westBoundLongitude: minx is missing")
                    errors += 1
                if md.identification.extent.boundingBox.maxx is (None or ''):
                    result["errors"].append("gmd:eastBoundLongitude: maxx is missing")
                    errors += 1
                if md.identification.extent.boundingBox.miny is (None or ''):
                    result["errors"].append("gmd:southBoundLatitude: miny is missing")
                    errors += 1
                if md.identification.extent.boundingBox.maxy is (None or ''):
                    result["errors"].append("gmd:northBoundLatitude: maxy is missing")
                    errors += 1

        if len(md.identification.date) < 1 or (md.identification.temporalextent_start is (
                None or '') or md.identification.temporalextent_end is (None or '')):
            result["errors"].append("Both gmd:EX_TemporalExtent and gmd:CI_Date are missing")
            errors += 1

    if md.datestamp is (None or ''):
        result["errors"].append("gmd:dateStamp: Date is missing")
        errors += 1

    if md.identifier is (None or ''):
        result["errors"].append("gmd:identifier: Identifier is missing")
        errors += 1

    if md.contact is None:
        result["errors"].append("gmd:contact: Organization name is missing")
        result["errors"].append("gmd:contact: e-mail is missing")
        result["errors"].append("gmd:role: role is missing")
        errors += 3
    else:
            if md.contact[0].organization is (None or ''):
                result["errors"].append("gmd:contact: Organization name is missing")
                errors += 1

            if md.contact[0].email is (None or ''):
                result["errors"].append("gmd:contact: e-mail is missing")
                errors += 1

            if md.contact[0].role is (None or ''):
                result["errors"].append("gmd:role: role is missing")
                errors += 1

    if errors > 0:
        result["status"] = "failed"
        result["num_of_errors"] = str(errors)
    return result


def isnpireValidator(md):
    '''function for validation INSPIRE  XML-OWSLib  file-object'''

    result = {}
    result["status"] = "succeded"
    result["errors"] = []
    result["num_of_errors"] = "0"
    errors = 0

    if md.identification is None:
        result["errors"].append("gmd:CI_ResponsibleParty: Organization missing")
        result["errors"].append("gmd:CI_ResponsibleParty: E-mail missing")
        result["errors"].append("gmd:CI_ResponsibleParty: Role missing")
        result["errors"].append("gmd:md_DataIdentification: Title is missing")
        result["errors"].append("gmd:md_DataIdentification: Abstract is missing")
        result["errors"].append("gmd:md_ScopeCode: Resource Type is missing")
        result["errors"].append("gmd:language: Resource Language is missing")
        result["errors"].append("gmd:RS_Identifier: Unique Resource Identifier is missing")
        result["errors"].append("gmd:topicCategory: TopicCategory is missing")
        result["errors"].append("gmd:md_Keywords: Keywords are missing")
        result["errors"].append("gmd:thesaurusName: Thesaurus Title is missing")
        result["errors"].append("gmd:thesaurusName: Thesaurus Date is missing")
        result["errors"].append("gmd:thesaurusName: Thesaurus Date Type is missing")
        result["errors"].append("gmd:EX_Extent: extent element is missing")
        result["errors"].append("gmd:EX_GeographicBoundingBox: bbox is missing")
        result["errors"].append("Both gmd:EX_TemporalExtent and gmd:CI_Date are missing")
        result["errors"].append("gmd:useLimitation is missing")
        result["errors"].append("gmd:accessConstraints is missing")
        result["errors"].append("gmd:otherConstraints is missing")
        errors += 20
    else:
        if md.identification.contact is None or len(md.identification.contact) < 1:
            result["errors"].append("gmd:CI_ResponsibleParty: Organization missing")
            result["errors"].append("gmd:CI_ResponsibleParty: E-mail missing")
            result["errors"].append("gmd:CI_ResponsibleParty: Role missing")
            errors += 3
        else:

                if md.identification.contact[0].organization is (None or ''):
                    result["errors"].append("gmd:CI_ResponsibleParty: Organization missing")
                    errors += 1

                if md.identification.contact[0].email is (None or ''):
                    result["errors"].append("gmd:CI_ResponsibleParty: E-mail missing")
                    errors += 1

                if md.identification.contact[0].role is (None or ''):
                    result["errors"].append("gmd:CI_ResponsibleParty: Role missing")
                    errors += 1

        if md.identification.title is (None or ''):
            result["errors"].append("gmd:md_DataIdentification: Title is missing")
            errors += 1
        if md.identification.abstract is (None or ''):
            result["errors"].append("gmd:md_DataIdentification: Abstract is missing")
            errors += 1
        if md.identification.identtype is (None or ''):
            result["errors"].append("gmd:md_ScopeCode: Resource Type is missing")
            errors += 1

        if md.identification.resourcelanguage is None:
            errors += 1
            result["errors"].append("gmd:language: Resource Language is missing")
        else:
            if len(md.identification.resourcelanguage) < 1 or md.identification.resourcelanguage[0] == '':
                    result["errors"].append("gmd:language: Resource Language is missing")
                    errors += 1

        if md.identification.uricode is None:
            result["errors"].append("gmd:RS_Identifier: Unique Resource Identifier is missing")
            errors += 1
        else:
            if len(md.identification.uricode) < 1 or md.identification.uricode[0] == '':
                result["errors"].append("gmd:RS_Identifier: Unique Resource Identifier is missing")
                errors += 1

        if md.identification.topiccategory is None:
            result["errors"].append("gmd:topicCategory: TopicCategory is missing")
            errors += 1
        else:
            if len(md.identification.topiccategory) < 1 or md.identification.topiccategory[0] == '':
                result["errors"].append("gmd:topicCategory: TopicCategory is missing")
                errors += 1

        if md.identification.keywords is None or len(md.identification.keywords) < 1:
                result["errors"].append("gmd:MD_Keywords: Keywords are missing")
                result["errors"].append("gmd:thesaurusName: Thesaurus Title is missing")
                result["errors"].append("gmd:thesaurusName: Thesaurus Date is missing")
                result["errors"].append("gmd:thesaurusName: Thesaurus Date Type is missing")
                errors += 4
        else:
                if md.identification.keywords[0]['keywords'] is None or len(md.identification.keywords[0]['keywords']) < 1 \
                        or str(md.identification.keywords[0]['keywords']) == "[u'']":
                    result["errors"].append("gmd:MD_Keywords: Keywords are missing")
                    errors += 1
                if md.identification.keywords[0]['thesaurus'] is None:
                    result["errors"].append("gmd:thesaurusName: Thesaurus Title is missing")
                    result["errors"].append("gmd:thesaurusName: Thesaurus Date is missing")
                    result["errors"].append("gmd:thesaurusName: Thesaurus Date Type is missing")
                    errors += 3
                else:
                    if md.identification.keywords[0]['thesaurus']['title'] is None \
                            or len(md.identification.keywords[0]['thesaurus']['title']) < 1:
                        result["errors"].append("gmd:thesaurusName: Thesaurus Title is missing")
                        errors += 1
                    if md.identification.keywords[0]['thesaurus']['date'] is None \
                            or len(md.identification.keywords[0]['thesaurus']['date']) < 1:
                        result["errors"].append("gmd:thesaurusName: Thesaurus Date is missing")
                        errors += 1
                    if md.identification.keywords[0]['thesaurus']['datetype'] is None \
                            or len(md.identification.keywords[0]['thesaurus']['datetype']) < 1:
                        result["errors"].append("gmd:thesaurusName: Thesaurus Date Type is missing")
                        errors += 1

        if md.identification.extent is None:
            result["errors"].append("gmd:EX_Extent: extent element is missing")
            errors += 1
        else:
            if md.identification.extent.boundingBox is None:
                result["errors"].append(
                    "gmd:EX_GeographicBoundingBox: bbox is missing")
                errors += 1
            else:
                if md.identification.extent.boundingBox.minx is (None or ''):
                    result["errors"].append("gmd:westBoundLongitude: minx is missing")
                    errors += 1
                if md.identification.extent.boundingBox.maxx is (None or ''):
                    result["errors"].append("gmd:eastBoundLongitude: maxx is missing")
                    errors += 1
                if md.identification.extent.boundingBox.miny is (None or ''):
                    result["errors"].append("gmd:southBoundLatitude: miny is missing")
                    errors += 1
                if md.identification.extent.boundingBox.maxy is (None or ''):
                    result["errors"].append("gmd:northBoundLatitude: maxy is missing")
                    errors += 1

        if len(md.identification.date) < 1 or (md.identification.temporalextent_start is (
                None or '') or md.identification.temporalextent_end is (None or '')):
            result["errors"].append("Both gmd:EX_TemporalExtent and gmd:CI_Date are missing")
            errors += 1

        if len(md.identification.uselimitation) < 1 or md.identification.uselimitation[0] == '':
            result["errors"].append("gmd:useLimitation is missing")
            errors += 1
        if len(md.identification.accessconstraints) < 1 or md.identification.accessconstraints[0] == '':
            result["errors"].append("gmd:accessConstraints is missing")
            errors += 1
        if len(md.identification.otherconstraints) < 1 or md.identification.otherconstraints[0] == '':
            result["errors"].append("gmd:otherConstraints is missing")
            errors += 1

    if md.languagecode is (None or ''):
        result["errors"].append("gmd:LanguageCode: Language code missing")
        errors += 1
    if md.datestamp is (None or ''):
        result["errors"].append("gmd:dateStamp: Date is missing")
        errors += 1
    if md.identifier is (None or ''):
        result["errors"].append("gmd:identifier: Identifier is missing")
        errors += 1
    if md.dataquality is (None or ''):
        result["errors"].append("gmd:LI_Lineage is missing")
        result["errors"].append("gmd:DQ_ConformanceResult: date is missing")
        result["errors"].append("gmd:DQ_ConformanceResult: date type is missing")
        # result["errors"].append("gmd:DQ_ConformanceResult: degree is missing")
        result["errors"].append("gmd:DQ_ConformanceResult: title is missing")
        errors += 4
    else:

        if md.dataquality.lineage is (None or ''):
            result["errors"].append("gmd:LI_Lineage is missing")
            errors += 1
        if len(md.dataquality.conformancedate) < 1 or md.dataquality.conformancedate[0] == '':
            result["errors"].append("gmd:DQ_ConformanceResult: date is missing")
            errors += 1
        if len(md.dataquality.conformancedatetype) < 1 or md.dataquality.conformancedatetype[0] == '':
            result["errors"].append("gmd:DQ_ConformanceResult: date type is missing")
            errors += 1
        # if len(md.dataquality.conformancedegree) < 1:
        #     result["errors"].append("gmd:DQ_ConformanceResult: degree is missing")
        #     errors += 1
        if len(md.dataquality.conformancetitle) < 1 or md.dataquality.conformancetitle[0] == '':
            result["errors"].append("gmd:DQ_ConformanceResult: title is missing")
            errors += 1

    if md.contact is None or len(md.contact) < 1:
        result["errors"].append("gmd:contact: Organization name is missing")
        result["errors"].append("gmd:contact: e-mail is missing")
        result["errors"].append("gmd:role: role is missing")
        errors += 3
    else:

            if md.contact[0].organization is (None or ''):
                result["errors"].append("gmd:contact: Organization name is missing")
                errors += 1

            if md.contact[0].email is (None or ''):
                result["errors"].append("gmd:contact: e-mail is missing")
                errors += 1

            if md.contact[0].role is (None or ''):
                result["errors"].append("gmd:role: role is missing")
                errors += 1

    if errors > 0:
        result["status"] = "failed"
        result["num_of_errors"] = str(errors)

    return result