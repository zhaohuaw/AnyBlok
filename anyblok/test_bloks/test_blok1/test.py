# This file is a part of the AnyBlok project
#
#    Copyright (C) 2014 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok import Declarations
from anyblok.column import Integer, String


register = Declarations.register
Model = Declarations.Model


@register(Model)
class Test:

    id = Integer(primary_key=True)
    blok = String()
    mode = String()


@register(Model.System)
class Blok:

    def install(self):
        super(Blok, self).install()
        self.registry.Test.insert(blok=self.name, mode='install')

    def upgrade(self):
        super(Blok, self).upgrade()
        self.registry.Test.insert(blok=self.name, mode='update')

    def load(self):
        super(Blok, self).load()
        self.registry.Test.insert(blok=self.name, mode='load')
