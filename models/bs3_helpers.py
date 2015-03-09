# -*- coding: utf-8 -*-

from gluon.sqlhtml import FormWidget
from gluon.html import DEFAULT_PASSWORD_DISPLAY

def mybootstrap(form, fields):
    ''' bootstrap format form layout '''
    form.add_class('form-horizontal')
    parent = FIELDSET()
    for id, label, controls, help in fields:
        # wrappers
        _help = None
        if help:
            _help = SPAN(help, _class='help-block')

        if isinstance(controls, (str, int, SPAN)):
            controls = P(controls, _class="form-control-static")

        # submit unflag by default
        _submit = False

        if isinstance(controls, INPUT):
            if controls['_type'] == 'submit':
                # flag submit button
                _submit = True
                controls['_class'] = 'btn btn-primary'
            if controls['_type'] == 'file':
                controls['_class'] = 'input-file'

        if isinstance(label, LABEL):
            label['_class'] = 'col-sm-2 control-label'

        if _submit:
            # submit button has unwrapped label and controls, different class
            parent.append(DIV(DIV(controls,_class="col-sm-offset-2 col-sm-10"),
                _class='form-group form-group-sm', _id=id))
            # unflag submit (possible side effect)
            _submit = False
        else:
            # unwrapped label
            if _help:
                parent.append(DIV(label, DIV(controls, _help, _class="col-sm-10"),
                    _class='form-group form-group-sm', _id=id))
            else:
                parent.append(DIV(label, DIV(controls, _class="col-sm-10"),
                    _class='form-group form-group-sm', _id=id))
    return parent


class BS3StringWidget(FormWidget):
    _class = 'string form-control'

    @classmethod
    def widget(cls, field, value, **attributes):

        default = dict(
            _type='text',
            value=(not value is None and str(value)) or '',
        )
        attr = cls._attributes(field, default, **attributes)

        return INPUT(**attr)


class BS3TextWidget(FormWidget):
    _class = 'text form-control'

    @classmethod
    def widget(cls, field, value, **attributes):

        default = dict(value=value)
        attr = cls._attributes(field, default, **attributes)
        return TEXTAREA(**attr)


class BS3BooleanWidget(FormWidget):
    _class = 'boolean checkbox'

    @classmethod
    def widget(cls, field, value, **attributes):

        default = dict(_type='checkbox', value=value)
        attr = cls._attributes(field, default,
                               **attributes)
        return INPUT(**attr)


class BS3TimeWidget(BS3StringWidget):
    _class = 'time form-control'


class BS3DateWidget(BS3StringWidget):
    _class = 'date form-control'


class BS3DatetimeWidget(BS3StringWidget):
    _class = 'datetime form-control'


class BS3IntegerWidget(BS3StringWidget):
    _class = 'integer form-control'


class BS3DoubleWidget(BS3StringWidget):
    _class = 'double form-control'


class BS3DecimalWidget(BS3StringWidget):
    _class = 'decimal form-control'


class BS3PasswordWidget(BS3StringWidget):
    _class = 'text password form-control'
    

    @classmethod
    def widget(cls, field, value, **attributes):
        """
        Generates a INPUT password tag.
        If a value is present it will be shown as a number of '*', not related
        to the length of the actual value.

        see also: `FormWidget.widget`
        """
        # detect if attached a IS_STRONG with entropy
        default = dict(
            _type='password',
            _value=(value and DEFAULT_PASSWORD_DISPLAY) or '',
        )
        attr = cls._attributes(field, default, **attributes)

        # deal with entropy check!
        requires = field.requires
        if not isinstance(requires, (list, tuple)):
            requires = [requires]
        is_strong = [r for r in requires if isinstance(r, IS_STRONG)]
        if is_strong:
            attr['_data-w2p_entropy'] = is_strong[0].entropy if is_strong[0].entropy else "null"
        # end entropy check
        output = INPUT(**attr)
        return output

def fixup_bs3_widgets(SQLFORM):
    SQLFORM.widgets.string = BS3StringWidget
    SQLFORM.widgets.text = BS3TextWidget
    SQLFORM.widgets.boolean = BS3BooleanWidget
    SQLFORM.widgets.date = BS3DateWidget
    SQLFORM.widgets.time = BS3TimeWidget
    SQLFORM.widgets.datetime = BS3DatetimeWidget
    SQLFORM.widgets.integer = BS3IntegerWidget
    SQLFORM.widgets.double = BS3DoubleWidget
    SQLFORM.widgets.decimal = BS3DecimalWidget
    SQLFORM.widgets.password = BS3PasswordWidget


def mymenu(menu):
    ul = UL(_class="nav navbar-nav")
    for item in menu:
        if isinstance(item,LI):
            ul.append(item)
        else:
            (name, active, link) = item[:3]
            sublevel = len(item) == 4 and item[3] or []
            if sublevel:
                subul = UL(_class="dropdown-menu", _role="menu")
                for sub in sublevel:
                    sname, sactive, slink = sub[:3]
                    if isinstance(slink, DIV):
                        li = LI(slink)
                    elif isinstance(slink, dict):
                        li = LI(A(sname, **slink))
                    elif slink:
                        li = LI(A(sname, _href=slink))
                    elif not slink and isinstance(sname, A):
                        li = LI(sname)
                    else:
                        li = LI(A(sname, _href='#',
                                  _onclick='javascript:void(0);return false;'))
                    subul.append(li)
                ul.append(LI(
                    A(name, SPAN(_class="caret"), _href='#', _class="dropdown-toggle", _role="button", data=dict(toggle="dropdown")),
                    subul,
                    _class="dropdown"))
            else:
                if isinstance(link, DIV):
                    li = LI(link)
                elif isinstance(link, dict):
                    li = LI(A(name, **link))
                elif link:
                    li = LI(A(name, _href=link))
                elif not link and isinstance(name, A):
                    li = LI(name)
                else:
                    li = LI(A(name, _href='#',
                              _onclick='javascript:void(0);return false;'))
                ul.append(li)
    return ul