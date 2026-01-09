from typing import Self
from enum import IntEnum


class ArmorType(IntEnum):
    CHOBHAM = 100
    COMPOSITE = 50
    CERAMIC = 50



class Tank:
    def __init__(self, armor: int, penetration: int, armor_type: ArmorType):
        if not isinstance(armor_type, ArmorType):
            raise ValueError('Invalid armor type %s' % (armor_type))

        self.name = ""
        self.armor = armor
        self.penetration = penetration
        self.armor_type = armor_type

    def set_name(self, name: str) -> Self:
        self.name = name
        return self
    
    @property
    def real_armor(self) -> int:
        return self.armor + self.armor_type.value

    def is_vunerable_to(self, other: Self) -> bool:
        return self.real_armor <= other.penetration

    def swap_armor(self, other: Self) -> None:
        tmp = other.armor
        other.armor = self.armor
        self.armor = tmp

    def __str__(self) -> str:
        return self.name.lower().replace(' ', '-')


def main():
    # Test T1 is vulnerable to T2, and vice-versa when we swap armor
    t1 = Tank(armor=500, penetration=670, armor_type=ArmorType.CHOBHAM)
    t2 = Tank(
        armor=t1.penetration + 1,  # must resist t1
        penetration=t1.real_armor + 1, # must penetrate t1
        armor_type=ArmorType.CHOBHAM
    )
    assert t1.is_vunerable_to(t2)
    assert t2.is_vunerable_to(t1) is False
    t1.swap_armor(t2)
    assert t1.is_vunerable_to(t2) is False
    assert t2.is_vunerable_to(t1)

    # Test you must specify a valid armor_type
    try:
        Tank(10, 10, "steel")
        assert False, "Expected ValueError for invalid armor type"
    except ValueError as exc:
        assert "Invalid armor type" in str(exc)

    # Test that atleast one tank is safe
    tanks = [
        Tank(400, 400, ArmorType.CERAMIC),
        Tank(300, 400, ArmorType.CERAMIC),
        Tank(600, 200, ArmorType.CERAMIC),
    ]
    
    assert all(tank.is_vunerable_to(t1) for tank in tanks), "Expected all tanks to be vulnerable"

    solid_tank = Tank(armor=1000, penetration=0, armor_type=ArmorType.CHOBHAM)
    tanks.append(solid_tank)
    assert not all(tank.is_vunerable_to(t1) for tank in tanks), "Expected atleats one tank to be safe"

    print("OK")





if __name__ == "__main__":
    main()
