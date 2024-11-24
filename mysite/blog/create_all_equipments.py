from blog.models import Equipment

def create_all_equipments():

    Equipment.objects.create(
        name="Presse à jambes",
        description="Machine de musculation pour travailler les jambes.",
        image="equipment_images/Press.jpg",  
        status="libre",
        category="musculation"
    )

    Equipment.objects.create(
        name="Banc de musculation",
        description="Banc ajustable pour effectuer divers exercices de musculation.",
        image="equipment_images/Bench.jpg",
        status="libre",
        category="musculation"
    )

    Equipment.objects.create(
        name="Chaise romaine",
        description="Appareil de musculation pour les abdominaux et les lombaires.",
        image="equipment_images/RomanChair.jpg",
        status="libre",
        category="musculation"
    )

    Equipment.objects.create(
        name="Rack à squat",
        description="Rack pour effectuer des squats en toute sécurité.",
        image="equipment_images/SquatRack.jpg",
        status="libre",
        category="musculation"
    )

    Equipment.objects.create(
        name="Machine multifonction",
        description="Appareil multifonction permettant de travailler différentes parties du corps.",
        image="equipment_images/MultifunctionMachine.jpg",
        status="libre",
        category="musculation"
    )

    Equipment.objects.create(
        name="Vélo elliptique",
        description="Appareil de cardio pour travailler l'ensemble du corps.",
        image="equipment_images/Elliptical.jpg",
        status="libre",
        category="cardio"
    )

    Equipment.objects.create(
        name="Tapis de course",
        description="Tapis de course pour la course en intérieur.",
        image="equipment_images/Treadmill.jpg",
        status="libre",
        category="cardio"
    )

create_all_equipments()
