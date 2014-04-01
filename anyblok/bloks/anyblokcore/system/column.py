from AnyBlok import target_registry
from AnyBlok.Model import System
from AnyBlok.Mixin import Field


@target_registry(System)
class Column(Field):

    @classmethod
    def add_field(cls, cname, column, model, table):
        c = column.property.columns[0]
        vals = dict(autoincrement=c.autoincrement,
                    code=table + '.' + cname,
                    model=model, name=cname,
                    foreign_key=c.info.get('foreign_key'),
                    label=c.info['label'],
                    nullable=c.nullable,
                    primary_key=c.primary_key,
                    ctype=str(c.type),
                    unique=c.unique)
        cls.insert(**vals)

    @classmethod
    def alter_field(cls, column, meta_column):
        c = meta_column.property.columns[0]
        for col in ('autoincrement', 'nullable', 'primary_key', 'unique'):
            if getattr(column, col) != getattr(c, col):
                setattr(column, col, getattr(c, col))

        for col in ('foreign_key', 'label'):
            if getattr(column, col) != c.info.get(col):
                setattr(column, col, c.info.get(col))

        ctype = str(c.type)
        if column.ctype != ctype:
            column.ctype = ctype
