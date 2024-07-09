import time

class TrafficLight:
    def __init__(self, id, type):
        self.id = id
        self.type = type  # 'car' or 'pedestrian'
        self.queue = 0
        self.state = 'red'
        self.min_green_time = 10
        self.max_green_time = 60
        self.green_time = self.min_green_time

    def pass_traffic(self):
        # Симуляция прохождения одного автомобиля или одного пешехода
        if self.queue > 0:
            self.queue -= 1

    def update_state(self, new_state, green_time=None):
        self.state = new_state
        if green_time is not None:
            self.green_time = green_time

    def str(self):
        return f"TrafficLight(id={self.id}, type={self.type}, state={self.state}, queue={self.queue})"

class Intersection:
    def __init__(self, lights):
        self.lights = lights

    def collect_traffic_data(self, pre_defined_data):
        for light in self.lights:
            light.queue = pre_defined_data[light.id]

    def update_traffic_lights(self, control_data):
        for light in self.lights:
            if light.id in control_data:
                light.update_state(control_data[light.id]['state'], control_data[light.id].get('green_time'))

    def str(self):
        return "\n".join(str(light) for light in self.lights)

class AdaptiveTrafficControl:
    def __init__(self, intersection):
        self.intersection = intersection

    def calculate_priorities(self, traffic_data):
        total_traffic = sum(traffic_data.values())
        if total_traffic == 0:
            return {light_id: 0 for light_id in traffic_data}
        priorities = {light_id: (queue_length / total_traffic) for light_id, queue_length in traffic_data.items()}
        return priorities

    def adjust_signal_timing(self, priorities):
        control_data = {}
        for light in self.intersection.lights:
            priority = priorities.get(light.id, 0)
            green_time = int(light.min_green_time + (light.max_green_time - light.min_green_time) * priority)
            control_data[light.id] = {'state': 'green', 'green_time': green_time}
        return control_data

    def run(self, traffic_data):

        # Сбор данных из предопределенного набора
        self.intersection.collect_traffic_data(traffic_data)
        print("Collected Traffic Data:", traffic_data)

        # Анализ данных и расчет приоритетов
        priorities = self.calculate_priorities(traffic_data)
        print("Calculated Priorities:", priorities)

        # Адаптация времени сигналов
        control_data = self.adjust_signal_timing(priorities)
        print("Control Data:", control_data)

            # # Обновление состояний светофоров
            # self.intersection.update_traffic_lights(control_data)
            # print("Updated Traffic Lights:\n", self.intersection)

            # # Пропуск трафика через перекресток
            # for light in self.intersection.lights:
            #     if light.state == 'green':
            #         for _ in range(light.green_time):
            #             light.pass_traffic()
            #             print(f"Light {light.id} passing traffic. Queue: {light.queue}")
            #             time.sleep(0.1)  # Симуляция времени прохождения одного автомобиля или пешехода
            #     light.update_state('red')

            # Имитация времени ожидания до следующего цикла
            # time.sleep(1)

# Создание светофоров
traffic_lights = [
    TrafficLight('A', 'car'),
    TrafficLight('B', 'car'),
    TrafficLight('C', 'pedestrian'),
    TrafficLight('D', 'pedestrian')
]

# Создание перекрестка
intersection = Intersection(lights=traffic_lights)

# Предопределенные данные о трафике (очереди автомобилей и пешеходов)
traffic_data = {
    'A': 20,  # Очередь из 20 автомобилей
    'B': 15,  # Очередь из 15 автомобилей
    'C': 25,  # Очередь из 25 пешеходов
    'D': 10   # Очередь из 10 пешеходов
}

# Запуск адаптивного управления трафиком
adaptive_control = AdaptiveTrafficControl(intersection=intersection)
adaptive_control.run(traffic_data=traffic_data)