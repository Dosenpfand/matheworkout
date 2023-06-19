from app.models.general import Achievement

class names:
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    PRO = "pro"
    BAD_LUCK = "bad-luck"
    BOARD = "board"
    BRAIN = "brain"
    FIRST = "first"
    THIRD = "third"
    NIGHT_OWL = "night-owl"
    NTH_ROOT = "nth-root"
    INFINITY_RAT = "infinity-rat"
    SEE_NO_EVIL = "see-no-evil"
    SPEED = "speed"
    # TODO
    # STAR = "star"
    MATH = "math"

achievements = [
    Achievement(
        name=names.BEGINNER,
        title="Anfänger(in)???",
        description="Eine Aufgabe richtig beantwortet",
    ),
    Achievement(
        name=names.INTERMEDIATE,
        title="Fortgeschritten???",
        description="100 Aufgaben richtig beantwortet",
    ),
    Achievement(
        name=names.PRO,
        title="Profi???",
        description="100 Aufgaben richtig beantwortet",
    ),
    Achievement(
        name=names.BAD_LUCK,
        title="Pechsträhne",
        description="5 Aufgaben nacheinander falsch beantwortet",
    ),
    Achievement(
        name=names.BOARD,
        title="Bereit für die Matura",
        description="Alle Aufgaben einer Matura richtig beantwortet",
    ),
    Achievement(
        name=names.BRAIN,
        title="Mathematik durchgespielt",
        description="Alle Aufgaben richtig beantwortet",
    ),
    Achievement(
        name=names.FIRST,
        title="Klassenbeste(r)",
        description="Platz 1 in deiner Klasse, gewertet nach richtig beantworteten Fragen",
    ),
    Achievement(
        name=names.THIRD,
        title="Klassenpodest",
        description="Unter den Top 3 in deiner Klasse, gewertet nach richtig beantworteten Fragen",
    ),
    Achievement(
        name=names.NIGHT_OWL,
        title="Nachteule",
        description="10 Aufgaben zu später Stunde beantwortet",
    ),
    Achievement(
        name=names.NTH_ROOT,
        title="Wurzelente",
        description="Eine Aufgabe als erstes richtig beantwortet",
    ),
    Achievement(
        name=names.INFINITY_RAT,
        title="Matheratte",
        description="Eine Frage 10 mal richtig beantwortet",
    ),
    Achievement(
        name=names.SEE_NO_EVIL,
        title="Selbstüberschätzung",
        description="5 Selbstkontrolle-Aufgaben hintereinander richtig beantwortet",
    ),
    Achievement(
        name=names.SPEED,
        title="Marathon",
        description="50 Aufgaben innerhalb von 24 Stunden richtig beantwortet",
    ),
    # TODO
    # Achievement(
    #     name=names.STAR,
    #     title="Top 1 %",
    #     description="Unter den Top 1 Prozent auf matheworkout, gewertet nach richtig beantworteten Fragen",
    # ),
    Achievement(
        name=names.MATH,
        title="Alter Hase",
        description="Benutzer für über ein Jahr",
    ),
]

achievements_map = {achievement.name: achievement for achievement in achievements}
