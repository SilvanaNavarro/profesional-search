import reflex as rx
import asyncio
from typing import TypedDict


class Professional(TypedDict):
    id: int
    name: str
    photo: str
    area: str
    title: str
    description: str
    city: str
    available_hours: list[str]


professionals_data: list[Professional] = [
    {
        "id": 1,
        "name": "Lucia Fernandez",
        "photo": "/architect-1.jpg",
        "area": "Arquitectura",
        "title": "Arquitecta Senior",
        "description": "Más de 15 años de experiencia en diseño sostenible y planificación urbana.",
        "city": "Santiago",
        "available_hours": ["09:00", "11:00", "14:00"],
    },
    {
        "id": 2,
        "name": "Ricardo Morales",
        "photo": "/architect-2.jpg",
        "area": "Arquitectura",
        "title": "Especialista en Interiores",
        "description": "Creatividad y funcionalidad en cada espacio. Proyectos residenciales y comerciales.",
        "city": "Valparaíso",
        "available_hours": ["10:00", "12:00", "16:00"],
    },
    {
        "id": 3,
        "name": "Sofia Vargas",
        "photo": "/architect-3.jpg",
        "area": "Arquitectura",
        "title": "Urbanista",
        "description": "Planificación de ciudades inteligentes y desarrollo comunitario.",
        "city": "Concepción",
        "available_hours": ["09:30", "11:30", "15:00"],
    },
    {
        "id": 4,
        "name": "Carlos Pinto",
        "photo": "/social-1.jpg",
        "area": "Trabajo Social",
        "title": "Trabajador Social Clínico",
        "description": "Apoyo emocional y terapia para individuos y familias. Especializado en salud mental.",
        "city": "Santiago",
        "available_hours": ["08:00", "10:00", "13:00"],
    },
    {
        "id": 5,
        "name": "Elena Torres",
        "photo": "/social-2.jpg",
        "area": "Trabajo Social",
        "title": "Consejero Familiar",
        "description": "Mediación y resolución de conflictos en el ámbito familiar y de pareja.",
        "city": "La Serena",
        "available_hours": ["14:00", "16:00", "18:00"],
    },
    {
        "id": 6,
        "name": "Javier Acosta",
        "photo": "/social-3.jpg",
        "area": "Trabajo Social",
        "title": "Especialista en Adicciones",
        "description": "Programas de intervención y prevención para superar adicciones.",
        "city": "Antofagasta",
        "available_hours": ["09:00", "11:00", "17:00"],
    },
    {
        "id": 7,
        "name": "Mariana Diaz",
        "photo": "/accountant-1.jpg",
        "area": "Contadores",
        "title": "Contadora Póblica Certificada",
        "description": "Asesoría fiscal y financiera para pequeñas y medianas empresas. Optimización de impuestos.",
        "city": "Santiago",
        "available_hours": ["10:00", "13:00", "15:00"],
    },
    {
        "id": 8,
        "name": "Fernando Vega",
        "photo": "/accountant-2.jpg",
        "area": "Contadores",
        "title": "Auditor Financiero",
        "description": "Auditorías internas y externas para garantizar la transparencia y el cumplimiento.",
        "city": "Concepción",
        "available_hours": ["09:00", "12:00", "14:00"],
    },
    {
        "id": 9,
        "name": "Gabriela Soto",
        "photo": "/accountant-3.jpg",
        "area": "Contadores",
        "title": "Consultora Fiscal",
        "description": "Estrategias fiscales personalizadas para individuos y corporaciones.",
        "city": "Valparaíso",
        "available_hours": ["11:00", "14:00", "16:00"],
    },
    {
        "id": 10,
        "name": "Andrés Ramirez",
        "photo": "/lawyer-1.jpg",
        "area": "Abogados",
        "title": "Abogado Corporativo",
        "description": "Experto en derecho mercantil, fusiones, adquisiciones y contratos complejos.",
        "city": "Santiago",
        "available_hours": ["10:30", "12:30", "15:30"],
    },
    {
        "id": 11,
        "name": "Isabela Guerrero",
        "photo": "/lawyer-2.jpg",
        "area": "Abogados",
        "title": "Abogada de Familia",
        "description": "Representación legal en casos de divorcio, custodia y herencias.",
        "city": "Concepción",
        "available_hours": ["09:00", "11:00", "14:00"],
    },
    {
        "id": 12,
        "name": "Martín Castillo",
        "photo": "/lawyer-3.jpg",
        "area": "Abogados",
        "title": "Abogado Penalista",
        "description": "Defensa legal en casos penales, con un alto índice de éxito.",
        "city": "Antofagasta",
        "available_hours": ["13:00", "15:00", "17:00"],
    },
]
AREAS = ["Arquitectura", "Trabajo Social", "Contadores", "Abogados"]


def map_professional_to_dict(prof) -> Professional:
    return {
        "id": prof.id,
        "name": prof.name,
        "photo": prof.photo_profile_path or "/placeholder.svg",
        "area": prof.career,
        "title": prof.career,
        "description": prof.description_services,
        "city": prof.city or "N/A",
        "available_hours": [],
    }


class State(rx.State):
    professionals_by_area: dict[str, list[Professional]] = {}
    current_area_index: int = 0
    all_professionals_db: list[dict] = []

    def _load_professionals_from_db(self):
        from app.db import Professional as ProfessionalDB
        from sqlmodel import select

        with rx.session() as session:
            db_professionals = session.exec(
                select(ProfessionalDB).where(ProfessionalDB.verified == True)
            ).all()
            if db_professionals:
                self.all_professionals_db = [
                    map_professional_to_dict(p) for p in db_professionals
                ]
            else:
                self.all_professionals_db = professionals_data
            self.professionals_by_area = {
                area: [p for p in self.all_professionals_db if p["area"] == area]
                for area in AREAS
            }

    @rx.var
    def current_area(self) -> str:
        return AREAS[self.current_area_index]

    @rx.var
    def featured_professionals(self) -> list[Professional]:
        if not self.professionals_by_area:
            self._load_professionals_from_db()
        return self.professionals_by_area.get(self.current_area, [])[:3]

    @rx.event(background=True)
    async def rotate_area(self):
        async with self:
            self._load_professionals_from_db()
        while True:
            await asyncio.sleep(5)
            async with self:
                self.current_area_index = (self.current_area_index + 1) % len(AREAS)