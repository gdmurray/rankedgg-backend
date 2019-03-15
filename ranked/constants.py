ATTACKER = "attacker"
DEFENDER = "defender"

OPERATOR_TYPE_CHOICES = (
    (ATTACKER, "Attacker"),
    (DEFENDER, "Defender")
)

GLOBAL = "GLOBAL"
NA = "NA"
EU = "EU"
AS = "AS"

REGION_CHOICES = (
    (GLOBAL, "Global"),
    (NA, "America"),
    (EU, "Europe"),
    (AS, "Asia")
)

METADATA_REFRESH_HOURS = 6
PLAYER_DATA_REFRESH_HOURS = 24
