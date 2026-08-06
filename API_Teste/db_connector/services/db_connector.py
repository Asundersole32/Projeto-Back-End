import uuid
import json
from datetime import datetime, date
from decimal import Decimal

from sqlalchemy import create_engine, inspect, MetaData, Table, select, insert, update, delete, and_
from sqlalchemy.exc import SQLAlchemyError
from django.core.cache import cache


class DatabaseConnector:
    @staticmethod
    def get_engine(params):
        db_type = params.get('db_type')
        host = params.get('host')
        port = params.get('port')
        user = params.get('user')
        password = params.get('password')
        database = params.get('database')

        if db_type == 'postgresql':
            url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        elif db_type == 'mysql':
            url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        elif db_type == 'sqlite':
            url = f"sqlite:///{database}"   # database é o caminho do arquivo
        elif db_type == 'oracle':
            url = f"oracle+cx_oracle://{user}:{password}@{host}:{port}/{database}"
        else:
            raise ValueError("Unsupported database type")

        engine = create_engine(url, pool_pre_ping=True)
        return engine

    @staticmethod
    def connect(params):
        # Testa a conexão criando um engine e descartando-o
        engine = DatabaseConnector.get_engine(params)
        with engine.connect() as conn:
            pass

        conn_id = str(uuid.uuid4())
        # Armazena os parâmetros (não o engine)
        cache.set(f"db_conn_{conn_id}", params, timeout=3600)
        return conn_id

    @staticmethod
    def get_connection(conn_id):
        params = cache.get(f"db_conn_{conn_id}")
        if params is None:
            raise ValueError("Connection not found or expired")
        # Recria o engine a partir dos parâmetros
        return DatabaseConnector.get_engine(params)

    @staticmethod
    def get_tables(conn_id):
        engine = DatabaseConnector.get_connection(conn_id)
        inspector = inspect(engine)
        return inspector.get_table_names()

    @staticmethod
    def get_table_info(conn_id, table_name):
        engine = DatabaseConnector.get_connection(conn_id)
        inspector = inspect(engine)
        columns = inspector.get_columns(table_name)
        pk = inspector.get_pk_constraint(table_name)
        fks = inspector.get_foreign_keys(table_name)

        # 🔥 Converte os tipos para string
        for col in columns:
            if 'type' in col:
                col['type'] = str(col['type'])  # transforma VARCHAR(50) em "VARCHAR(50)"

        # Se houver outros objetos não serializáveis, trate aqui
        return {
            'columns': columns,
            'primary_key': pk,
            'foreign_keys': fks
        }

    @staticmethod
    def get_table_data(conn_id, table_name, filters=None, order_by=None, limit=100, offset=0):
        engine = DatabaseConnector.get_connection(conn_id)
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = select(table)

        # Filtros dinâmicos: suporta campo__gt, campo__lt, campo__contains, etc.
        if filters:
            conditions = []
            for key, value in filters.items():
                if '__' in key:
                    field, op = key.split('__')
                    col = table.c[field]
                    if op == 'gt':
                        conditions.append(col > value)
                    elif op == 'lt':
                        conditions.append(col < value)
                    elif op == 'gte':
                        conditions.append(col >= value)
                    elif op == 'lte':
                        conditions.append(col <= value)
                    elif op == 'contains':
                        conditions.append(col.contains(value))
                    elif op == 'startswith':
                        conditions.append(col.startswith(value))
                    elif op == 'endswith':
                        conditions.append(col.endswith(value))
                    else:
                        conditions.append(col == value)
                else:
                    col = table.c[key]
                    conditions.append(col == value)
            stmt = stmt.where(and_(*conditions))

        # Ordenação
        if order_by:
            for field in order_by:
                if field.startswith('-'):
                    stmt = stmt.order_by(table.c[field[1:]].desc())
                else:
                    stmt = stmt.order_by(table.c[field].asc())

        stmt = stmt.limit(limit).offset(offset)

        with engine.connect() as conn:
            result = conn.execute(stmt)
            rows = result.fetchall()
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in rows]
            # Serializa valores não JSON
            return json.loads(json.dumps(data, default=json_serializer))

    @staticmethod
    def insert_row(conn_id, table_name, data):
        engine = DatabaseConnector.get_connection(conn_id)
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = insert(table).values(**data)
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            pk = result.inserted_primary_key
            return {'inserted_primary_key': list(pk) if pk else None}

    @staticmethod
    def update_row(conn_id, table_name, pk_value, data, pk_column=None):
        engine = DatabaseConnector.get_connection(conn_id)
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=engine)

        if pk_column is None:
            inspector = inspect(engine)
            pk = inspector.get_pk_constraint(table_name)
            if not pk['constrained_columns']:
                raise ValueError("Table has no primary key")
            pk_column = pk['constrained_columns'][0]

        col = table.c[pk_column]
        stmt = update(table).where(col == pk_value).values(**data)
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            if result.rowcount == 0:
                raise ValueError("Row not found")
            return {'message': 'Row updated'}

    @staticmethod
    def delete_row(conn_id, table_name, pk_value, pk_column=None):
        engine = DatabaseConnector.get_connection(conn_id)
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=engine)

        if pk_column is None:
            inspector = inspect(engine)
            pk = inspector.get_pk_constraint(table_name)
            if not pk['constrained_columns']:
                raise ValueError("Table has no primary key")
            pk_column = pk['constrained_columns'][0]

        col = table.c[pk_column]
        stmt = delete(table).where(col == pk_value)
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            if result.rowcount == 0:
                raise ValueError("Row not found")
            return {'message': 'Row deleted'}


def json_serializer(obj):
    """Serializa objetos datetime, date e Decimal para JSON."""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")