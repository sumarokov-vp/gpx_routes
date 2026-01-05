# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Описание проекта

Репозиторий для хранения коллекции GPX-маршрутов (мотоциклетные/велосипедные треки) и QGIS проектов для их визуализации.

## Структура

- `gpx/` — GPX-файлы с GPS-треками, организованные по регионам
- `qgz/` — файлы проектов QGIS для визуализации маршрутов
- `add_metadata.py` — скрипт для добавления метаданных в GPX файлы

## Команды

```bash
uv sync                      # установить зависимости
uv run python add_metadata.py  # обновить метаданные во всех GPX
brew install --cask qgis     # установить QGIS для визуализации
```

## Формат метаданных GPX

Метаданные хранятся в `<extensions>` с namespace `route`:

```xml
<extensions>
  <route:distance>59.9</route:distance>    <!-- км, автоматически -->
  <route:elevation>245</route:elevation>   <!-- м набора, автоматически -->
  <route:stops>                            <!-- вручную -->
    <route:stop name="DB slot" url="https://maps.app.goo.gl/..."/>
    <route:stop name="Rab-a-bit" url="https://maps.app.goo.gl/..."/>
  </route:stops>
</extensions>
```

- `distance` и `elevation` — вычисляются скриптом автоматически
- `stops` — добавляются вручную, скрипт их сохраняет при обновлении
