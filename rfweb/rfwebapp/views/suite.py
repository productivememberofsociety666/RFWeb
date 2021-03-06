import re

from django.shortcuts import render_to_response, get_object_or_404

from django.http import HttpResponse
from rfweb.rfwebapp.models import Suite
from rfweb.rfwebapp import utils
from django.middleware.gzip import GZipMiddleware
from django.template import loader, Context

gzip_middleware = GZipMiddleware()

def suite(request, suitename):
    def _raw(request):
        suite = get_object_or_404(Suite, name=suitename)
        suitedoc = SuiteDoc(suite)
        return render_to_response('suite.html', {'suite': suitedoc })
    response = _raw(request)
    return gzip_middleware.process_response(request, response)
    return suite

def suite_csv(request, suitename):
    def _raw(request):
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=suite_%s.csv' % suitename
        t = loader.get_template('suite.csv')
        suite = get_object_or_404(Suite, name=suitename)
        suitedoc = SuiteDoc(suite)
        c = Context({'suite': suitedoc,})
        response.write(t.render(c))
        return response
    response = _raw(request)
    return gzip_middleware.process_response(request, response)
    return suite_csv

def suite_md(request, suitename):
    def _raw(request):
        response = HttpResponse(mimetype='text/markdown')
        response['Content-Disposition'] = 'attachment; filename=suite_%s.md' % suitename
        t = loader.get_template('suite.md')
        suite = get_object_or_404(Suite, name=suitename)
        suitedoc = SuiteDoc(suite)
        c = Context({'suite': suitedoc,})
        response.write(t.render(c))
        return response
    response = _raw(request)
    return gzip_middleware.process_response(request, response)
    return suite_md

class _DocHelper:
    # This code is adapted from libdoc.py, see
    # http://code.google.com/p/robotframework/wiki/LibraryDocumentationTool

    _name_regexp = re.compile("`(.+?)`")

    def _get_htmldoc(self):
        doc = utils.html_escape(self._doc, formatting=True)
        return self._name_regexp.sub(self._link_keywords, doc)

    def _link_keywords(self, res):
        name = res.group(1)
        keywords = self.keywords if isinstance(self, SuiteDoc) else self._suite.keywords
        for kw in keywords:
            if utils.eq(name, kw.name):
                return '<a href="#%s" class="name">%s</a>' % (kw.name, name)
        if utils.eq_any(name, ['introduction', 'suite introduction']):
            return '<a href="#introduction" class="name">%s</a>' % name
        if utils.eq_any(name, ['importing', 'suite importing']):
            return '<a href="#importing" class="name">%s</a>' % name
        return '<span class="name">%s</span>' % name

    doc = property(_get_htmldoc)

class SuiteDoc(_DocHelper):
    def __init__(self, suitedata):
        self.name = suitedata.name
        self.path = suitedata.path
        self._doc = suitedata.doc
        self.version = suitedata.version
        self.keywords = [ KeywordDoc(kwdata, self)
                          for kwdata in suitedata.keyword_set.all() ]
        self.tests = [ TestDoc(tcdata, self)
                          for tcdata in suitedata.test_set.all() ]
        self.variables = [ VariableDoc(vrdata, self)
                          for vrdata in suitedata.variable_set.all() ]

class VariableDoc(_DocHelper):
    def __init__(self, vrdata, suite):
        self.name = vrdata.name
        self.value = vrdata.value
        self.comment = vrdata.comment
        self._suite = suite
 
class KeywordDoc(_DocHelper):
    def __init__(self, kwdata, suite):
        self.name = kwdata.name
        self.args = kwdata.args
        self._doc = kwdata.doc
        self.shortdoc = self._doc.split('\n')[0]
        self._suite = suite
 
class TestDoc(_DocHelper):
    def __init__(self, tcdata, suite):
        self.name = tcdata.name
        self._doc = tcdata.doc
        self.shortdoc = self._doc.split('\n')[0]
        self._suite = suite

