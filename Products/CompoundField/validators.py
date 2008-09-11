# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 by Eric BREHAULT (ebrehault@gmail.com)
#
# German Free Software License (D-FSL)
#
# This Program may be used by anyone in accordance with the terms of the 
# German Free Software License
# The License may be obtained under <http://www.d-fsl.org>.
#
__author__ = """Eric BREHAULT <ebrehault@gmail.com>,
                Jens Klein <jens@bluedynamics.com>"""
__docformat__ = 'plaintext'

from Products.validation.interfaces.IValidator import IValidator
from Products.CMFPlone.utils import safeToInt

_marker = []

class CompoundValidator:
    """ Validator for CompoundField
    """

    __implements__ = (IValidator,)

    name = 'compoundfieldvalidator'
    
    def __init__(self, errormsg=None):
        self.errormsg = errormsg
        
    def _getSubfields(self, field, form):
        return field.Schema().fields()

    def __call__(self, value, instance, errors, field, REQUEST=None, 
                 *args, **kwargs):
        form = REQUEST and REQUEST.form or None
        
        for field in self._getSubfields(field, form):
            result = None
            if form:
                widget = field.widget
                result = widget.process_form(instance, field, form, 
                                             empty_marker=_marker)
            if result is None or result is _marker:
                accessor = field.getEditAccessor(instance) or \
                           field.getAccessor(instance)
                if accessor is not None:
                    value = accessor()
                else:
                    # can't get value to validate -- bail
                    continue
            else:
                value = result[0]

            res = field.validate(instance=instance,
                                 value=value,
                                 errors=errors,
                                 REQUEST=REQUEST)
            if res:
                errors[field.getName()] = res
        return errors
    
    
class ArrayValidator(CompoundValidator):
    """"""
    name = 'arrayfieldvalidator'

    def _getSubfields(self, field, form):
        sizeFieldName = field.Schema().fields()[0].getName()        
        size = safeToInt(form.get(sizeFieldName, 0))
        fields = field.Schema().fields()
        fields = fields[1:1+size]
        return fields
