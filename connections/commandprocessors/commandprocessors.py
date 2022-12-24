from abc import abstractmethod

from connections.connector import Connector


class CommandProcessor:
    def __init__(self, connector: Connector):
        self.__connector = connector

    @property
    def connector(self):
        return self.__connector

    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, id: int, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass


class MakerCommandProcessor(CommandProcessor):
    def create(self, name: str):
        if not name:
            raise ValueError("Name cannot be empty")
        query = "BEGIN MAKERCR(:name); END;"
        self.connector.execute_without_return(query,
                                              name=name)

    def update(self, id: int, *args, **kwargs):
        if "name" not in kwargs:
            raise ValueError("Name cannot be empty")
        self.connector.execute_without_return("UPDATE MAKERS SET NAME=:name WHERE ID=:id",
                                              name=kwargs["name"],
                                              id=id)

    def delete(self, id: int):
        self.connector.execute_without_return("DELETE FROM MAKERS WHERE ID=:id",
                                              id=id)


class TakerCommandProcessor(CommandProcessor):
    def create(self, name: str, weapon: str):
        if not name:
            raise ValueError("Name cannot be empty")
        query = "BEGIN TAKERCR(:name, :weapon); END;"
        self.connector.execute_without_return(query,
                                              name=name,
                                              weapon=weapon)

    def update(self, id: int, *args, **kwargs):
        if "name" not in kwargs:
            raise ValueError("Name cannot be empty")
        self.connector.execute_without_return("UPDATE TAKERS SET NAME=:name WHERE ID=:id",
                                              name=kwargs["name"],
                                              id=id)

    def delete(self, id: int):
        self.connector.execute_without_return("DELETE FROM TAKERS WHERE ID=:id",
                                              id=id)


class VictimCommandProcessor(CommandProcessor):
    def create(self, name: str):
        self.connector.execute_without_return("INSERT INTO VICTIMS (NAME) VALUES (:name)",
                                              name=name)

    def update(self, id: int, *args, **kwargs):
        if "name" not in kwargs:
            raise ValueError("Name cannot be empty")
        self.connector.execute_without_return("UPDATE VICTIMS SET NAME=:name WHERE ID=:id",
                                              name=kwargs["name"],
                                              id=id)

    def delete(self, id: int):
        self.connector.execute_without_return("DELETE FROM VICTIMS WHERE ID=:id",
                                              id=id)


class OrderCommandProcessor(CommandProcessor):
    def create(self, maker: str,
               victim: str,
               cost: int,
               location: str = None,
               weapon: str = None):
        if maker is None:
            raise ValueError("Maker cannot be empty")
        if victim is None:
            raise ValueError("Victim cannot be empty")
        if cost is None:
            raise ValueError("Cost cannot be empty")
        query = "BEGIN ORDERING(:maker, :victim, :location, :weapon, :cost); END;"
        self.connector.execute_without_return(query,
                                              maker=maker,
                                              victim=victim,
                                              location=location,
                                              weapon=weapon,
                                              cost=cost)

    def update(self, id: int, *args, **kwargs):
        if 0 > len(kwargs.values()) or len(kwargs.values()) >= 5:
            raise ValueError("Invalid number of arguments")
        if set(kwargs.keys()) - {"maker_id", "victim_id", "cost", "taker_id", "requirement_id"}:
            raise ValueError("Invalid arguments")
        query = "UPDATE ORDERS SET "
        if "maker_id" in kwargs:
            query += "MAKER_ID=:maker_id, "
        if "victim_id" in kwargs:
            query += "VICTIM_ID=:victim_id, "
        if "cost" in kwargs:
            query += "COST=:cost, "
        if "taker_id" in kwargs:
            query += "TAKER_ID=:taker_id, "
        if "requirement_id" in kwargs:
            query += "REQUIREMENT_ID=:requirement_id"
        query += " WHERE ID=:id"
        self.connector.execute_without_return(query,
                                              id=id,
                                              **kwargs)

    def delete(self, id: int):
        self.connector.execute_without_return("DELETE FROM ORDERS WHERE ID=:id", id=id)


class RequirementCommandProcessor(CommandProcessor):
    def create(self, location_id: int, weapon_type_id: int):
        if not location_id:
            raise ValueError("Location cannot be empty")
        if not weapon_type_id:
            raise ValueError("Weapon type cannot be empty")
        self.connector.execute_without_return(
            "INSERT INTO REQUIREMENTS (LOCATION_ID, WEAPON_TYPE_ID) "
            "VALUES (:location_id, :weapon_type_id)",
            location_id=location_id,
            weapon_type_id=weapon_type_id)

    def update(self, id: int, *args, **kwargs):
        if 0 > len(kwargs.values()) or len(kwargs.values()) >= 3:
            raise ValueError("Invalid number of arguments")
        if set(kwargs.keys()) - {"location_id", "weapon_type_id"}:
            raise ValueError("Invalid arguments")
        query = "UPDATE REQUIREMENTS SET "
        if "location_id" in kwargs:
            query += "LOCATION_ID=:location_id, "
        if "weapon_type_id" in kwargs:
            query += "WEAPON_TYPE_ID=:weapon_type_id"
        query += " WHERE ID=:id"
        self.connector.execute_without_return(query, id=id, **kwargs)

    def delete(self, id: int):
        self.connector.execute_without_return("DELETE FROM REQUIREMENTS WHERE ID=:id", id=id)


class WeaponCommandProcessor(CommandProcessor):
    def create(self, killer_id: int, weapon_type: int, **kwargs):
        if not killer_id:
            raise ValueError("Killer cannot be empty")
        if not weapon_type:
            raise ValueError("Weapon type cannot be empty")
        self.connector.execute_without_return(
            "INSERT INTO WEAPONS (KILLER_ID, TYPE_ID) "
            "VALUES (:killer_id, :weapon_type)",
            killer_id=killer_id,
            weapon_type=weapon_type)

    def update(self, id: int, *args, **kwargs):
        if 0 > len(kwargs.values()) or len(kwargs.values()) >= 3:
            raise ValueError("Invalid number of arguments")
        if set(kwargs.keys()) - {"killer_id", "weapon_type"}:
            raise ValueError("Invalid arguments")
        query = "UPDATE WEAPONS SET "
        if "killer_id" in kwargs:
            query += "KILLER_ID=:killer_id, "
        if "weapon_type" in kwargs:
            query += "TYPE_ID=:weapon_type"
        query += " WHERE ID=:id"
        self.__connector.execute_without_return(query, id=id, **kwargs)

    def delete(self, id: int):
        self.connector.execute_without_return("DELETE FROM WEAPONS WHERE ID=:id", id=id)


class LocationCommandProcessor(CommandProcessor):
    def create(self, name: str):
        self.connector.execute_without_return("INSERT INTO LOCATIONS (NAME) VALUES (:name)", name=name)

    def update(self, id: int, *args, **kwargs):
        if "name" not in kwargs:
            raise ValueError("Name cannot be empty")
        self.connector.execute_without_return("UPDATE LOCATIONS SET NAME=:name WHERE ID=:id",
                                              name=kwargs["name"],
                                              id=id)

    def delete(self, id: int):
        self.connector.execute_without_return("DELETE FROM LOCATIONS WHERE ID=:id", id=id)
