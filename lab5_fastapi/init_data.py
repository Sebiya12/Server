from database import SessionLocal
import models


def init_db():
    db = SessionLocal()

    # Если команд ещё нет — создаём начальные данные
    if db.query(models.Team).count() == 0:
        dinamo_players = [
            models.Player(name="Anton Shunin", position="GK"),
            models.Player(name="Eli Dasa", position="Defender"),
            models.Player(name="Vyacheslav Grulyov", position="FW"),
        ]

        dinamo = models.Team(
            location="Moscow",
            name="Dinamo",
            mascot="Gladiator",
            players=dinamo_players
        )

        cska = models.Team(
            location="Moscow",
            name="CSKA",
            mascot="Horse"
        )

        db.add(dinamo)
        db.add(cska)
        db.commit()

    db.close()