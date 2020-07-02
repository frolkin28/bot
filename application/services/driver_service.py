import typing
from sqlalchemy.exc import IntegrityError

from application.database import current_session
from application.entities import DriverEntity
from application.models import Driver
from application.constants import DriverStatus


class DriverService:
    def get_all(self) -> typing.List[DriverEntity]:
        with current_session() as session:
            drivers = session.query(Driver).all()
            if drivers:
                entities = [self.build_entity(driver) for driver in drivers]
            else:
                entities = []
        return entities

    def craete(self, entity: DriverEntity) -> typing.Optional[DriverEntity]:
        orm_driver = self.build_orm_entity(entity)
        with current_session() as session:
            try:
                session.add(orm_driver)
                session.commit()
            except IntegrityError:
                entity = None
            else:
                entity = self.build_entity(orm_driver)
        return entity

    def delete(self, telegram_id: int) -> bool:
        with current_session() as session:
            res = session.query(Driver).filter(
                Driver.telegram_id == telegram_id).delete()
            session.commit()
        return bool(res)
    
    def set_status(self, telegram_id: int, status: DriverStatus) -> None:
        pass

    @staticmethod
    def build_entity(orm_object: Driver) -> DriverEntity:
        return DriverEntity.from_orm(orm_object)

    @staticmethod
    def build_orm_entity(entity: DriverEntity) -> Driver:
        return Driver(**entity.dict())
