import typing
from sqlalchemy.exc import IntegrityError

from application.database import current_session
from application.entities import AdminEntity
from application.models import Admin


class AdminService:
    def get(self, id: int) -> typing.Optional[AdminEntity]:
        with current_session() as session:
            admin = session.query(Admin).get(id)
            if admin:
                entity = self.build_entity(admin)
            else:
                entity = None
        return entity

    def get_by_tg_id(self, telegram_id: int) -> typing.Optional[AdminEntity]:
        with current_session() as session:
            admin = session.query(Admin).filter(
                Admin.telegram_id == telegram_id).first()
            if admin:
                entity = self.build_entity(admin)
            else:
                entity = None
        return entity

    def get_all(self) -> typing.List[AdminEntity]:
        with current_session() as session:
            admins = session.query(Admin).all()
            if admins:
                entities = [self.build_entity(admin) for admin in admins]
            else:
                entities = []
        return entities

    def create(self, entity: AdminEntity) -> typing.Optional[AdminEntity]:
        orm_admin = self.build_orm_entity(entity)
        with current_session() as session:
            try:
                session.add(orm_admin)
                session.commit()
            except IntegrityError:
                entity = None
            else:
                entity = self.build_entity(orm_admin)
        return entity

    def delete(self, telegram_id: int) -> bool:
        with current_session() as session:
            res = session.query(Admin).filter(Admin.telegram_id==telegram_id).delete()
            session.commit()
        return bool(res)

    @staticmethod
    def build_entity(orm_object: Admin) -> AdminEntity:
        return AdminEntity.from_orm(orm_object)

    @staticmethod
    def build_orm_entity(entity: AdminEntity) -> Admin:
        return Admin(**entity.dict())
