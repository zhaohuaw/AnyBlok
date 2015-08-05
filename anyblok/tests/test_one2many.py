# -*- coding: utf-8 -*-
# This file is a part of the AnyBlok project
#
#    Copyright (C) 2014 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.tests.testcase import DBTestCase
from anyblok import Declarations
from anyblok.column import Integer, String
from anyblok.relationship import One2Many


register = Declarations.register
Model = Declarations.Model
Mixin = Declarations.Mixin


def _complete_one2many(**kwargs):
    primaryjoin = "address.id == person.address_id"

    @register(Model)
    class Address:

        id = Integer(primary_key=True)
        street = String()
        zip = String()
        city = String()

    @register(Model)
    class Person:

        name = String(primary_key=True)
        address_id = Integer(foreign_key=(Model.Address, 'id'))

    @register(Model)  # noqa
    class Address:

        persons = One2Many(model=Model.Person,
                           remote_columns="address_id",
                           primaryjoin=primaryjoin,
                           many2one="address")


def _minimum_one2many(**kwargs):

    @register(Model)
    class Address:

        id = Integer(primary_key=True)
        street = String()
        zip = String()
        city = String()

    @register(Model)
    class Person:

        name = String(primary_key=True)
        address_id = Integer(foreign_key=(Model.Address, 'id'))

    @register(Model)  # noqa
    class Address:

        persons = One2Many(model=Model.Person)


def _minimum_one2many_remote_field_in_mixin(**kwargs):

    @register(Model)
    class Address:

        id = Integer(primary_key=True)
        street = String()
        zip = String()
        city = String()

    @register(Mixin)
    class MPerson:
        address_id = Integer(foreign_key=(Model.Address, 'id'))

    @register(Model)
    class Person(Mixin.MPerson):

        name = String(primary_key=True)

    @register(Model)  # noqa
    class Address:

        persons = One2Many(model=Model.Person)


def _one2many_with_str_model(**kwargs):

    @register(Model)
    class Address:

        id = Integer(primary_key=True)
        street = String()
        zip = String()
        city = String()

    @register(Model)
    class Person:

        name = String(primary_key=True)
        address_id = Integer(foreign_key=(Model.Address, 'id'))

    @register(Model)  # noqa
    class Address:

        persons = One2Many(model='Model.Person')


def _autodetect_two_foreign_key(**kwargs):

    @register(Model)
    class Address:

        id = Integer(primary_key=True)
        street = String()
        zip = String()
        city = String()

    @register(Model)
    class Person:

        name = String(primary_key=True)
        address_id = Integer(foreign_key=(Model.Address, 'id'))
        address2_id = Integer(foreign_key=(Model.Address, 'id'))

    @register(Model)  # noqa
    class Address:

        persons = One2Many(model=Model.Person)


class TestOne2Many(DBTestCase):

    def test_complete_one2many(self):
        self.reload_registry_with(_complete_one2many)

        address = self.registry.Address.insert(
            street='14-16 rue soleillet', zip='75020', city='Paris')

        person = self.registry.Person.insert(name="Jean-sébastien SUZANNE")
        address.persons.append(person)

        self.assertEqual(person.address, address)

    def test_minimum_one2many(self):
        self.reload_registry_with(_minimum_one2many)

        address = self.registry.Address.insert(
            street='14-16 rue soleillet', zip='75020', city='Paris')

        person = self.registry.Person.insert(name="Jean-sébastien SUZANNE")
        address.persons.append(person)

    def test_minimum_one2many_remote_field_in_mixin(self):
        self.reload_registry_with(_minimum_one2many)

        address = self.registry.Address.insert(
            street='14-16 rue soleillet', zip='75020', city='Paris')

        person = self.registry.Person.insert(name="Jean-sébastien SUZANNE")
        address.persons.append(person)

    def test_one2many_with_str_model(self):
        self.reload_registry_with(_one2many_with_str_model)

        address = self.registry.Address.insert(
            street='14-16 rue soleillet', zip='75020', city='Paris')

        person = self.registry.Person.insert(name="Jean-sébastien SUZANNE")
        address.persons.append(person)

    def test_same_model_backref(self):

        def add_in_registry():

            @register(Model)
            class Test:

                id = Integer(primary_key=True)
                parent_id = Integer(foreign_key=('Model.Test', 'id'))
                children = One2Many(model='Model.Test', many2one='parent')

        self.reload_registry_with(add_in_registry)
        t1 = self.registry.Test.insert()
        t2 = self.registry.Test.insert(parent=t1)
        self.assertIs(t1.children[0], t2)
        self.assertIs(t2.parent, t1)

    def test_complet_with_multi_foreign_key(self):

        def add_in_registry():
            primaryjoin = "test.id == test2.test_id and "
            primaryjoin += "test.id2 == test2.test_id2"

            @register(Model)
            class Test:

                id = Integer(primary_key=True, unique=True)
                id2 = String(primary_key=True, unique=True)

            @register(Model)
            class Test2:

                id = Integer(primary_key=True)
                test_id = Integer(foreign_key=(Model.Test, 'id'))
                test_id2 = String(foreign_key=(Model.Test, 'id2'))

            @register(Model)  # noqa
            class Test:

                test2 = One2Many(model=Model.Test2,
                                 remote_columns=['test_id', 'test_id2'],
                                 primaryjoin=primaryjoin,
                                 many2one="test")

        self.reload_registry_with(add_in_registry)
        t1 = self.registry.Test.insert(id2="test")
        t2 = self.registry.Test2.insert(test=t1)
        self.assertEqual(len(t1.test2), 1)
        self.assertIs(t1.test2[0], t2)

    def test_with_multi_foreign_key(self):

        def add_in_registry():

            @register(Model)
            class Test:

                id = Integer(primary_key=True, unique=True)
                id2 = String(primary_key=True, unique=True)

            @register(Model)
            class Test2:

                id = Integer(primary_key=True)
                test_id = Integer(foreign_key=(Model.Test, 'id'))
                test_id2 = String(foreign_key=(Model.Test, 'id2'))

            @register(Model)  # noqa
            class Test:

                test2 = One2Many(model=Model.Test2, many2one="test")

        self.reload_registry_with(add_in_registry)
        t1 = self.registry.Test.insert(id2="test")
        t2 = self.registry.Test2.insert(test=t1)
        self.assertEqual(len(t1.test2), 1)
        self.assertIs(t1.test2[0], t2)
