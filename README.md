# 🐸 Frogger - Python Edition

Un clon del clásico arcade **Frogger** (Konami, 1981) hecho en Python con Pygame.
Lleva la rana a salvo cruzando la carretera y el río para sumar puntos.





***

## 🎮 Capturas del juego

```
┌─────────────────────────┐
│  *** META ***  (arriba) │
│  ~~~~~~~~~~~~~~~~       │  ← Río con troncos
│  ~~~~~~~~~~~~~~~~       │
│  ─────────────          │  ← Zona segura
│  ████████████           │  ← Carretera con coches
│  ████████████           │
│  ─────────────          │  ← Inicio (tú empiezas aquí)
└─────────────────────────┘
```

***

## 🚀 Instalación rápida

### Requisitos
- **Python 3.8 o superior** → [Descargar Python](https://www.python.org/downloads/)
- **Pygame 2.x**

### Pasos

```bash
# 1. Clona o descarga el proyecto
git clone https://github.com/tuusuario/frogger-python.git
cd frogger-python

# 2. Instala pygame
pip install pygame

# 3. ¡Juega!
python frogger.py
```

> ⚠️ Si `pip` no se reconoce, prueba con: `python -m pip install pygame`

***

## 🕹️ Controles

| Tecla | Acción |
|-------|--------|
| ↑ o W | Mover arriba |
| ↓ o S | Mover abajo |
| ← o A | Mover izquierda |
| → o D | Mover derecha |
| R | Reiniciar (tras Game Over) |
| ESC | Salir del juego |

***

## 🎯 Cómo jugar

1. **Empieza** en la franja de hierba inferior.
2. **Cruza la carretera** esquivando los coches que van en ambas direcciones.
3. **Cruza el río** saltando sobre los troncos que se mueven. ¡Si caes al agua pierdes una vida!
4. **Llega a la META** (franja verde superior) para sumar **+100 puntos** y seguir jugando.
5. El juego es **infinito**: cuantas más veces llegues, más puntos acumulas.

***

## ⭐ Mecánicas del juego

- **50 vidas** para practicar sin agobios.
- **45 segundos** por intento — el tiempo restante da puntos extra al llegar.
- **Dificultad progresiva**: cada 500 puntos, los coches y troncos se mueven más rápido.
- La rana **se arrastra con los troncos** del río automáticamente.
- Si el tronco te saca fuera de la pantalla, pierdes una vida.

***

## 📁 Estructura del proyecto

```
frogger-python/
├── frogger.py      ← Código principal del juego
└── README.md       ← Este fichero
```

***

## 🔧 Tecnologías usadas

- **Python 3** — lenguaje principal
- **Pygame** — gráficos, eventos y bucle de juego
- **pygame.sprite.Sprite** — gestión de objetos del juego (rana, troncos, coches)
- **Programación orientada a objetos** — clases `Log`, `Car`, `Frog`, `Game`

***

## 📖 Arquitectura del código

```
Game
├── _build_level()    → Crea troncos y coches según el nivel
├── _draw_bg()        → Dibuja el fondo (meta, río, hierba, carretera)
├── _draw_hud()       → Muestra puntos, vidas, nivel y tiempo
├── _check_status()   → Detecta colisiones y llegada a la meta
├── _on_die()         → Gestiona la muerte de la rana
├── _on_goal()        → Suma puntos al llegar a la meta
└── run()             → Bucle principal del juego

Sprites
├── Frog    → La rana del jugador (movimiento por celdas)
├── Log     → Troncos del río (wrap-around horizontal)
└── Car     → Coches de la carretera (wrap-around horizontal)
```

***

## 🐛 Problemas frecuentes

| Error | Solución |
|-------|----------|
| `ModuleNotFoundError: No module named 'pygame'` | Ejecuta `pip install pygame` |
| `python` no se reconoce | Reinstala Python marcando ✅ "Add to PATH" |
| La ventana no abre | Asegúrate de ejecutar con `python frogger.py`, no haciendo doble clic |
| Va muy lento | Cierra otras aplicaciones o reduce `FPS = 30` en el código |

***

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Algunas ideas para mejorar el juego:

- [ ] Sonidos con `pygame.mixer`
- [ ] Pantalla de inicio con menú
- [ ] Guardado del récord en fichero
- [ ] Sprites con imágenes PNG
- [ ] Multijugador local

***

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Puedes usarlo, modificarlo y distribuirlo libremente.

***

## 🙏 Créditos

- Inspirado en el arcade original **Frogger** de Konami (1981)
- Desarrollado con **Python** y **Pygame**
- Creado como proyecto educativo para aprender programación orientada a objetos

***

> 🐸 *¿Puedes cruzar el río y llegar a la meta sin mojarte?*
