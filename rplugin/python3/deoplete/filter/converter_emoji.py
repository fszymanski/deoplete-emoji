# ============================================================================
# FILE: converter_emoji.py
# AUTHOR: Adam Macumber <atom.mac at gmail.com>
# License: MIT license
# ============================================================================

import re

from deoplete.filter.base import Base


class Filter(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'converter_emoji'
        self.description = 'convert candidates to unicodes'
        self._cache = {}

    def filter(self, context):
        def convert(x):
            word = x['kind'].strip()
            kind = x['word'].strip()
            return { 'word': word, 'kind': kind }

        return list(map(convert, context['candidates']))


