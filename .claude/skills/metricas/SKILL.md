---
name: metricas
description: Generar e interpretar el reporte de progreso: minutos por día y semana, racha, ejercicios intentados contra resueltos sin ayuda, precisión en tarjetas y dominio por tema. Usar cuando el usuario pregunte cómo viene, cuánto estudió, cómo va la racha, si está mejorando, o pida un reporte. Triggers "cómo voy", "cómo vengo", "métricas", "reporte", "cuánto estudié", "la racha", "estoy mejorando", "dominio".
---

# Métricas

Corré el reporte y mostralo tal cual:

```bash
.venv/bin/python tools/study.py metricas
```

## Cómo interpretarlo

Escribí tres o cuatro líneas después del reporte. No repitas números que ya se ven.

Decí en cada reporte:

- El tema más frío y hace cuánto que no se toca.
- El hueco más grande entre lo que está cubierto y lo que falta en `base/temario.md`.
- Si la racha sube pero la cobertura está quieta, decilo explícitamente. El usuario pidió que se
  vigile esto.

## Qué significa cada número

- **Racha**: días seguidos con al menos una sesión cerrada con bitácora. Una sesión sin bitácora
  no cuenta y corta la racha.
- **Resueltos solo**: sin ninguna pista. Es la métrica que de verdad mide si mejora. Que suba el
  porcentaje importa más que el volumen de ejercicios.
- **Nivel de pista promedio**: si baja con el tiempo sobre el mismo tema, está internalizando el
  patrón. Si se queda en 4 o 5, el tema no está entendido y hay que volver al modelo mental.
- **Precisión en tarjetas**: por debajo de 80% sostenido, las tarjetas están mal redactadas o el
  tema se generó antes de tiempo.
- **Dominio por tema**: 0 a 100 combinando retención de tarjetas (40%), precisión en repasos
  (20%) y ratio de ejercicios resueltos solo (40%). Es una fórmula propia, no un estándar: si el
  número no coincide con la sensación del usuario, decilo y ofrecé ajustar los pesos.
- **Temas fríos**: tocados y sin actividad hace 21 días o más. Son los primeros candidatos para
  la próxima sesión.

- **Calibración**: sobreconfianza es decir que sabías una tarjeta y fallarla, o predecir que
  sacabas un ejercicio solo y no sacarlo. Por encima del 25% sostenido, el problema no es el
  temario: está confundiendo reconocer con recordar. Es el riesgo específico de su estilo.
- **Reconocimiento de patrón**: porcentaje de aciertos en el drill intercalado. Es la métrica
  más directa de su debilidad principal. Sube más lento que el resto y eso es normal.
- **Clases de error**: lo que se repite entre temas distintos. Una clase que aparece en tres
  temas es un hueco de ejecución, no de teoría, y se ataca con repeticiones cortas.

## Señales de alarma

- Muchos minutos y pocos ejercicios: está leyendo de más y practicando de menos. Es el riesgo
  conocido de su estilo de aprendizaje.
- Ejercicios que suben pero precisión de tarjetas que baja: está avanzando temas sin consolidar.
- Micro-sesiones que desplazan a las de fondo durante dos semanas: el temario se frena. Proponé
  una sesión de fondo explícitamente.
