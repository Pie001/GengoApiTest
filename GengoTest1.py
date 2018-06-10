#!/usr/bin/env PYTHONIOENCODING=UTF-8 python3
# -*- coding: utf-8 -*-
from gengo import Gengo

gengo = Gengo(
    public_key='public_key',
    private_key='private_key',
    sandbox=True,
    debug=True)

print(gengo.getServiceLanguagePairs(lc_src='ja'))
