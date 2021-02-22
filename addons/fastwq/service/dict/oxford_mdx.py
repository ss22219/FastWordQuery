#-*- coding:utf-8 -*-
import os
import re
import random
from ..base import *

DICT_PATH = u'' # u'D:\\dict\\牛津高阶英汉双解词典(第9版)_v20191111\\牛津高阶英汉双解词典(第9版)_v20191111.mdx'

@register([u'本地词典-牛津高阶英汉双解', u'MDX-OXFORD'])
class OxfordMdx(MdxService):

    def __init__(self):
        dict_path = DICT_PATH
        # if DICT_PATH is a path, stop auto detect
        if not dict_path:
            from ...service import service_manager, service_pool
            for clazz in service_manager.mdx_services:
                service = service_pool.get(clazz.__unique__)
                title = service.builder._title if service and service.support else u''
                service_pool.put(service)
                if title.startswith(u'牛津高阶英汉双解词典(第'):
                    dict_path = service.dict_path
                    break
        super(OxfordMdx, self).__init__(dict_path)

    @property
    def title(self):
        return getattr(self, '__register_label__', self.unique)

    @export('PHON')
    def fld_phonetic(self):
        return ''

    def _fld_voice(self, html, voice):
        return ''

    @export('BRE_PRON')
    def fld_voicebre(self):
        return ''

    @export('AME_PRON')
    def fld_voiceame(self):
        return ''

    @export('IMAGE')
    def fld_image(self):
        return ''

    @export('EXAMPLE')
    def fld_sentence(self):
        return ''

    @export([u'例句加音频', u'Examples with audios'])
    def fld_sentence_audio(self):
        return ''

    @export('DEF')
    def fld_definate(self):
        return ''

    @export([u'随机例句', u'Random example'])
    def fld_random_sentence(self):
        return ''

    @export([u'首2个例句', u'First 2 examples'])
    def fld_first2_sentence(self):
        return ''
    
    @export([u'随机例句加音频', u'Random example with audio'])
    def fld_random_sentence_audio(self):
        return ''

    @export([u'首2个例句加音频', u'First 2 examples with audios'])
    def fld_first2_sentence_audio(self):
        return ''

    @export([u'额外例句', u'Extra Examples'])
    def fld_extra_examples(self):
        result = ''
        html = parse_html(self.get_html())
        list = html.find_all('x-wr')
        count = 0
        for item in list:
            x = item.x
            if x == None:
                continue
            enwords = x.attrs.get('wd')
            if enwords == None:
                continue
            chn = x.chn
            if chn == None:
                continue
            cnwords = chn.text.strip()
            audios = item.find('audio-wr')
            if audios == None:
                continue
            links = audios.find_all('a')
            if links == None or len(links) == 0 or links[len(links) - 1]['href'] == None:
                continue
            url = links[len(links) - 1]['href'].replace('sound://','\\')
            result = result + '<li>' + enwords + ' ' + cnwords + self._fld_audio(url) + '</li>'
            count = count + 1
            if count == 4:
                break
        return result

    def _fld_audio(self, audio):
        name = get_hex_name('mdx-' + self.unique.lower(), audio, 'mp3')
        name = self.save_file(audio, name)
        if name:
            return self.get_anki_label(name, 'audio')
        return ''

    @with_styles(cssfile='_oxford.css')
    def _css(self, val):
        return val
    
