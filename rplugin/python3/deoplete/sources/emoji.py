# Copyright (c) 2018 Filip Szymański. All rights reserved.
# Use of this source code is governed by an MIT license that can be
# found in the LICENSE file.

import re

from .base import Base
from deoplete.util import load_external_module

load_external_module(__file__, 'sources/emoji')
from data import EMOJI_CODES


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)

        self.__pattern = re.compile(r':[^:\s]+$')

        self.filetypes = ['gitcommit', 'markdown']
        self.mark = '[emoji]'
        self.matchers = ['matcher_length', 'matcher_full_fuzzy']
        self.name = 'emoji'
        self.max_candidates = 0

    def gather_candidates(self, context):
        return [{'word': k, 'kind': ' {} '.format(v)} for (k, v) in EMOJI_CODES.items()]

    def get_complete_position(self, context):
        match = self.__pattern.search(context['input'])
        return match.start() if match is not None else -1
