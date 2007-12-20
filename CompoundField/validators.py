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
__author__ = """Eric BREHAULT <ebrehault@gmail.com>"""
__docformat__ = 'plaintext'

from Products.validation.interfaces.IValidator import IValidator

_marker = []

class CompoundValidator:
    """ Validator for CompoundField
    """

    __implements__ = (IValidator,)

    name = 'compoundfieldvalidator'
    
    def __init__(self,errormsg=None):
        self.errormsg=errormsg

    def __call__(self, value, instance, errors, field, REQUEST=None, *args, **kwargs):
        failure = None
        if REQUEST:
            form = REQUEST.form
        else:
            form = None
            
        for f in field.Schema().fields():
            if form:
                widget = f.widget
                result = widget.process_form(instance, f, form, empty_marker=_marker)
            else:
                result = None
            if result is None or result is _marker:
                accessor = f.getEditAccessor(instance) or f.getAccessor(instance)
                if accessor is not None:
                    value = accessor()
                else:
                    # can't get value to validate -- bail
                    continue
            else:
                value = result[0]

            res = f.validate(instance=instance,
                                 value=value,
                                 errors=errors,
                                 REQUEST=REQUEST)
            if res:
                errors[f.getName()] = res
        return errors