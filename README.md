# Краткое описание

Данный пакет позволяет производить запуск и менеджмент сценариев в симуляторах Carla и Apollo. Каждый сценарий задается в отдельном xml-файле из директории **data**, параметры запуска содерджатся в директории **config** в отдельных xml-файлах. В процессе запуска сценария создается управляемый агент и подвижный трафик. Если запуск происходит в Apollo -- движение трафика контролируется пользвователем. В случае запуска в Carla -- автомобили могут управляться встроенным автопилотом, либо также осуществлять движение по прдеписанным пользователем траектории. В процессе работы сценария ведется запись движения агента, по которой впоследствии можно посчитать разнообразные метрики. Лог-файлы с траекторией агента и результатом метрик записываются в директорю **log**.

# Подготовка

TODO

# Использование

- Запустите Carla
- Запустите Apollo

TODO

# Конфигурация

Для запуска пакета требуется указать конфиг-файл из директории **config**. В нем содержатся основные параметры запуска симулятора и сценария. Стандартный конфиг запуска содержит следующие параметры:

- simulator - (str) название симлуятора [Carla/Apollo]
- host - (IP) ip-адрес симулятора
- port - (int) порт симулятора
- timeout - (float) timeout симулятора
- fps - (int) частота обновления сценария, а именно частота обновления положения машин трафика в случае ручного управления, и частота фиксации метрик
- traffic_filter - (str) фильтр модели машин трафика в Carla
- traffic_autopilot - (bool) переключатель автопилота трафика
- ego_filter - (str) фильтр модели управляемого авто
- autostart - (bool) переключатель автоматического запуска сценария 
- prefix - (str) префикс записи эксперимента в лог-файл - **outdated**

# Описание

TODO
