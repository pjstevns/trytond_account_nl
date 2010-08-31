#!/bin/python

# convert OpenERP chart of accounts to Tryton format

import sys
import lxml.etree as ET
from lxml.builder import ElementMaker

INFILE="account_chart_netherlands.xml"
OUTFILE="account_nl.xml.new"


class Converter(object):
    """
    >>> c = Converter(INFILE)
    >>> c.intree
    <lxml.etree._ElementTree object at ...>
    
    >>> t = c.maker
    >>> x = t.tryton(t.data(t.record(model="account.account.type.template",id="nl")))
    >>> print c.render(x)
    <tryton>
      <data>
        <record model="account.account.type.template" id="nl"/>
      </data>
    </tryton>
    <BLANKLINE>
    """

    def __init__(self, infile):
        self.intree = ET.parse(infile)
        self.maker = ElementMaker()
        tree = []
        tree += self.build_account_type_template()
        tree += self.build_account_template()
        tree += self.build_tax_code_template()
        tree += self.build_tax_template()
        tree += self.build_tax_rule_template()
        tree += self.build_tax_rule_line_template()
        tree = tuple(tree)

        m = self.maker
        self.outtree = m.tryton(m.data(*tree))

    def build_account_type_template(self):
        # account.account.type -> account.account.type.template
        m = self.maker
        r = []
        seq = 10
        r.append(
            m.record(
                m.field("Dutch Account Type Chart", name='name'),
                m.field(name="sequence", eval="10"),
                model='account.account.type.template', id='nl',
            )
        )
        for e in self.intree.xpath("/openerp/data/record[@model='account.account.type']"):
            f = []
            id = e.get("id")
            name = e.xpath("field[@name='name']")[0].text
            closemethod = e.xpath("field[@name='close_method']")[0].text
            f.append(m.field(name, name='name'))
            f.append(m.field(name='sequence', eval=str(seq)))
            f.append(m.field(name='parent', ref='nl'))
            if closemethod == 'balance':
                f.append(m.field(name='balance_sheet', eval="True"))
            f = tuple(f)
            seq += 10
            r.append(m.record(*f, model='account.account.type.template', id=id))
        return r


    def build_account_template(self):
        # account.account.template
        m = self.maker
        r = []
        r.append(
            m.record(
                m.field("NEDERLANDS STANDAARD GROOTBOEKSCHEMA", name="name"),
                m.field("view", name="kind"),
                m.field(name="type", ref="nl"),
                id="a_root", 
                model="account.account.template",
            )
        )
        l = self.intree.xpath("/openerp/data/record[@model='account.account.template']")
        for e in l:
            id = e.get("id")
            if id == 'a_root':
                continue
            name = e.xpath("field[@name='name']")[0].text
            code = e.xpath("field[@name='code']")[0].text
            kind = e.xpath("field[@name='type']")[0].text
            typ = e.xpath("field[@name='user_type']")
            defer = e.xpath("field[@name='reconcile']")
            parent = e.xpath("field[@name='parent_id']")
            f = []
            f.append(m.field(name, name='name'))
            f.append(m.field(code, name='code'))
            f.append(m.field(kind, name='kind'))
            if typ:
                ref = typ[0].get("ref")
                f.append(m.field(name='type',ref=ref))
            if defer:
                defer = str(not eval(defer[0].get("eval")))
                f.append(m.field(name='deferral', eval=defer))
            if parent:
                parent = parent[0].get("ref")
                f.append(m.field(name='parent', ref=parent))
            f = tuple(f)
            r.append(m.record(*f, model='account.account.template', id=id))
        return r

    def build_tax_group(self):
        return []

    def build_tax_code_template(self):
        l = self.intree.xpath("/openerp/data/record[@model='account.tax.code.template']")
        m = self.maker
        r = []
        origroot = None
        for e in l:
            f = []
            id = e.get("id")
            name = e.xpath("field[@name='name']")[0].text
            code = e.xpath("field[@name='code']")
            parent = e.xpath("field[@name='parent_id']")
            if not parent: continue
            if parent[0].get("eval"):
                if not eval(parent[0].get("eval")):
                    origroot=id
                    r.append(
                        m.record(
                            m.field(name, name='name'),
                            m.field(name='account',ref='a_root'),
                            model="account.tax.code.template",
                            id="tax_code_nl"
                        )
                    )
                    continue

            f.append(m.field(name, name='name'))
            f.append(m.field(name='account',ref='a_root'))

            parent = parent[0].get("ref")
            if parent == origroot:
                parent = "tax_code_nl"
            f.append(m.field(name='parent', ref=parent))
        
            if code:
                code = code[0].text
                f.append(m.field(code, name='code'))

            f = tuple(f)
            r.append(m.record(*f, model='account.tax.code.template', id=id))

        return r

    def build_tax_template(self):
        return []

    def build_tax_rule_template(self):
        return []

    def build_tax_rule_line_template(self):
        return []


    def write(self, outfile=None):
        if not outfile:
            outfile = sys.stdout

        if type(outfile) == type("a"):
            outfile = open(outfile, 'w')

        outfile.write(self.render(self.outtree))
        outfile.flush()

    def render(self, e):
        return ET.tostring(e, encoding='UTF-8', pretty_print=True)


if __name__ == '__main__':
    if '--test' in sys.argv:
        import doctest
        doctest.testmod(optionflags=doctest.ELLIPSIS)
    else:
        c = Converter(INFILE)
        c.write(OUTFILE)


