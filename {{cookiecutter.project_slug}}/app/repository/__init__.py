import abc

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Query
from loguru import logger

from app.utils import render_query


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session, model):
        self.session = session
        self.model = model

    def add(self, model_obj):
        self.session.add(model_obj)

    def add_and_commit(self, model_obj):
        self.session.add(model_obj)
        self.session.commit()

    def get(self, **kwargs):
        return self.session.query(self.model).filter_by(**kwargs).one()

    def list(self, **kwargs):
        _query = self.session.query(self.model)
        _limit = kwargs.pop('limit', None)
        _offset = kwargs.pop('offset', None)

        _query = _query.filter_by(**kwargs)
        if _limit:
            _query = _query.limit(_limit)
        if _offset:
            _query = _query.offset(_offset)

        logger.debug(f'query statement: {_query.statement}')
        return _query.all()

    def list_query(self, query: Query, **kwargs):
        _limit = kwargs.pop('limit', None)
        _offset = kwargs.pop('offset', None)

        if _limit:
            query = query.limit(_limit)
        if _offset:
            query = query.offset(_offset)

        logger.debug(f'list_query query: {render_query(query, self.session)}')
        return query.all()

    def update(self, model_obj, obj_in):
        obj_data = jsonable_encoder(model_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                logger.debug(f'SqlAlchemyRepository update: {model_obj}.{field} = {update_data[field]}')
                setattr(model_obj, field, update_data[field])
        self.session.add(model_obj)
        self.session.commit()
        self.session.refresh(model_obj)
        return model_obj

    def delete(self, model_obj):
        self.session.delete(model_obj)
        self.session.commit()
        return model_obj
