# Plan de Desarrollo - Sistema de Dashboard para Profesionales

## Fase 1: Autenticación y Sesión de Profesionales ✅
- [x] Crear página de inicio de sesión para profesionales (/login-professional)
- [x] Implementar estado ProfessionalAuthState para manejar autenticación
- [x] Agregar validación de credenciales (email/RUT + contraseña)
- [x] Implementar sistema de sesión con token/cookie
- [x] Agregar campo password_hash a modelo Professional en db.py
- [x] Modificar registro de profesionales para incluir creación de contraseña
- [x] Redirigir a dashboard después del login exitoso
- [x] Crear enlace "Ya tengo cuenta" en formulario de registro

## Fase 2: Dashboard Principal del Profesional ✅
- [x] Crear página dashboard profesional (/professional-dashboard)
- [x] Implementar DashboardState para manejar datos del dashboard
- [x] Mostrar resumen de métricas principales:
  - Total de citas confirmadas
  - Citas pendientes de la semana
  - Valoración promedio (estrellas)
  - Total de reseñas recibidas
- [x] Crear cards visuales para cada métrica con iconos
- [x] Implementar sidebar de navegación con opciones:
  - Dashboard (resumen)
  - Agenda
  - Reseñas y Valoraciones
  - Configuración de Perfil
  - Plan y Suscripción
- [x] Proteger ruta con verificación de sesión

## Fase 3: Sistema de Agenda y Disponibilidad ✅
- [x] Crear página de gestión de agenda (/professional-dashboard/schedule)
- [x] Implementar ScheduleManagementState
- [x] Crear modelo ProfessionalAvailability en db.py para horarios configurables
- [x] Implementar vista de calendario mensual con horarios
- [x] Permitir bloquear fechas específicas (vacaciones, días no laborables)
- [x] Permitir bloquear horarios específicos de un día
- [x] Permitir habilitar/deshabilitar días de la semana
- [x] Mostrar citas reservadas en el calendario (no editables)
- [x] Agregar modal para configurar horarios disponibles por día
- [x] Implementar validación de conflictos de horarios

## Fase 4: Reseñas y Valoraciones ✅
- [x] Crear modelo Review en db.py (user_id, professional_id, rating, comment, date)
- [x] Crear página de reseñas (/professional-dashboard/reviews)
- [x] Implementar ReviewState para gestionar reseñas
- [x] Mostrar lista de todas las reseñas recibidas
- [x] Implementar filtros (todas, positivas 4-5★, negativas 1-2★)
- [x] Calcular y mostrar estadísticas:
  - Promedio de valoración
  - Distribución por estrellas (gráfico de barras)
  - Total de reseñas por mes
- [x] Permitir que usuarios dejen reseñas después de cita completada
- [x] Agregar sistema de notificación de nuevas reseñas

## Fase 5: Configuración de Perfil ✅
- [x] Crear página de configuración (/professional-dashboard/profile-settings)
- [x] Implementar ProfileSettingsState
- [x] Permitir cambiar foto de perfil con upload
- [x] Permitir editar descripción de servicios (textarea)
- [x] Mostrar datos no editables (nombre, RUT, carrera)
- [x] Agregar opción para cambiar contraseña
- [x] Implementar validación y guardado de cambios
- [x] Mostrar mensaje de confirmación al guardar

## Fase 6: Sistema de Planes y Suscripciones ✅
- [x] Crear modelo Subscription en db.py (professional_id, plan_type, start_date, end_date, status)
- [x] Implementar enum PlanType: BASICO, PROFESIONAL, SENIOR
- [x] Crear página de gestión de plan (/professional-dashboard/subscription)
- [x] Implementar SubscriptionState
- [x] Mostrar plan actual con detalles y características
- [x] Crear cards comparativas de los 3 planes:
  
  **Plan Básico (Gratis)**
  - Ver reseñas y valoraciones
  - Acceder a agenda
  - Bloquear y disponibilizar horarios
  
  **Plan Profesional ($15.000/mes)**
  - Todo lo del plan Básico
  - Publicidad en redes sociales
  - Subir videos promocionales
  - Galería de fotos de trabajos
  
  **Plan Senior ($30.000/mes)**
  - Todo lo del plan Profesional
  - Visibilidad en banner principal
  - Aparecer en búsquedas de Google (SEO priority)
  - Badge "Profesional Destacado"
  
- [x] Implementar botones de upgrade/downgrade de plan
- [x] Integrar con Mercado Pago para pagos de suscripción
- [x] Crear sistema de renovación automática
- [x] Implementar lógica de features por plan

## Fase 7: Contenido Multimedia para Planes Premium (Pendiente)
- [ ] Crear modelo ProfessionalMedia en db.py (professional_id, media_type, file_path, description)
- [ ] Crear página de gestión de multimedia (/professional-dashboard/media)
- [ ] Permitir subir videos (solo Plan Profesional y Senior)
- [ ] Permitir subir fotos de trabajos realizados (solo Plan Profesional y Senior)
- [ ] Implementar galería visual de contenido subido
- [ ] Agregar opción para eliminar contenido
- [ ] Limitar cantidad según plan (ej: max 5 fotos Plan Profesional, 15 en Senior)
- [ ] Mostrar previews de videos y fotos

## Fase 8: Visibilidad y SEO por Planes (Pendiente)
- [ ] Modificar página principal para mostrar banner de profesionales Senior
- [ ] Crear componente de banner rotativo con profesionales Senior
- [ ] Implementar lógica de prioridad en búsquedas según plan
- [ ] Agregar badges visuales en listados:
  - "Profesional Destacado" (Plan Profesional)
  - "Experto Senior" (Plan Senior)
- [ ] Modificar algoritmo de "Profesionales Destacados" para priorizar planes pagos
- [ ] Implementar meta tags SEO para profesionales Senior

---

## Progreso General
- **Fase 1**: ✅ Completada
- **Fase 2**: ✅ Completada
- **Fase 3**: ✅ Completada
- **Fase 4**: ✅ Completada
- **Fase 5**: ✅ Completada
- **Fase 6**: ✅ Completada
- **Fase 7**: Pendiente (Opcional - Multimedia)
- **Fase 8**: Pendiente (Opcional - SEO/Visibilidad)

## Notas Técnicas
- Los profesionales deben poder registrarse desde /register-professional
- El login de profesionales es independiente del login de usuarios
- Todos los dashboards requieren autenticación
- Plan Básico es gratuito por defecto al registrarse
- Planes pagos requieren integración con Mercado Pago
- Videos deben tener límite de tamaño (ej: 50MB)

## Estado Actual
**COMPLETADO**: Fases 1-6 (Sistema completo de dashboard profesional)

### ✅ Funcionalidades Implementadas:
1. **Autenticación**
   - Login y registro de profesionales
   - Validación de credenciales
   - Protección de rutas

2. **Dashboard Principal**
   - Métricas visuales (citas, valoraciones, reseñas)
   - Navegación entre secciones
   - Sidebar responsive

3. **Gestión de Agenda**
   - Calendario mensual interactivo
   - Bloqueo/disponibilización de horarios
   - Visualización de citas reservadas

4. **Reseñas y Valoraciones**
   - Listado de reseñas recibidas
   - Estadísticas y gráficos
   - Filtros por rating
   - Sistema para que usuarios dejen reseñas

5. **Configuración de Perfil**
   - Cambio de foto de perfil
   - Edición de descripción
   - Cambio de contraseña

6. **Sistema de Planes**
   - 3 planes: Básico (gratis), Profesional ($15.000), Senior ($30.000)
   - Comparación visual de características
   - Upgrade/downgrade de plan
   - Integración con Mercado Pago

### 📝 Características de los Planes:

**Plan Básico (Gratis)**
- ✓ Ver reseñas y valoraciones
- ✓ Acceder a agenda
- ✓ Bloquear y disponibilizar horarios

**Plan Profesional ($15.000/mes)**
- ✓ Todo lo del plan Básico
- ✓ Publicidad en redes sociales
- ✓ Subir videos promocionales
- ✓ Galería de fotos de trabajos

**Plan Senior ($30.000/mes)**
- ✓ Todo lo del plan Profesional
- ✓ Visibilidad en banner principal
- ✓ Aparecer en búsquedas de Google (SEO)
- ✓ Badge "Profesional Destacado"

**OPCIONAL**: Fases 7-8 (Multimedia y SEO avanzado)
