class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type  # имя класса тренировки
        self.duration = duration  # длительность тренировки в часах
        self.distance = distance  # дистанция в километрах
        self.speed = speed  # средняя скорость, с которой двигался пользователь
        self.calories = calories  # количество израсходованных килокалорий

    def get_message(self) -> str:
        """ Метод возвращает строку сообщения в необходимом формате"""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {format(self.duration,".3f")} ч.; '
                f'Дистанция: {format(self.distance,".3f")} км; '
                f'Ср. скорость: {format(self.speed,".3f")} км/ч; '
                f'Потрачено ккал: {format(self.calories,".3f")}.')


class Training:
    """Базовый класс тренировки."""

    # Расстояние, которое спортсмен преодолевает за один шаг или гребок.
    # Один шаг — это 0.65 метра, один гребок при плавании — 1.38 метра.
    LEN_STEP: float = 0.65

    # Константа для перевода значений из метров в километры.
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action  # количество совершённых действий
        self.duration = duration  # длительность тренировки
        self.weight = weight  # вес спортсмена

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Возвращает информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,  # имя класса тренировки
                           self.duration,  # длительность тренировки в часах
                           self.get_distance(),  # дистанция в километрах
                           self.get_mean_speed(),  # средняя скорость
                           self.get_spent_calories())  # кол-во килокалорий


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для бега."""
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        dur_in_min: int = self.duration * 60  # Прод-ность тренировки в минутах
        return ((coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2)
                * self.weight / self.M_IN_KM * dur_in_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height  # рост спортсмена

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для спортивной ходьбы."""
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: float = 0.029
        dur_in_min: int = self.duration * 60  # Прод-ность тренировки в минутах
        return ((coeff_calorie_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * coeff_calorie_2 * self.weight) * dur_in_min)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38  # один гребок при плавании — 1.38 метра.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool  # длина бассейна в метрах
        self.count_pool = count_pool  # сколько раз польз-тель переплыл бассейн

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании"""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для плавания."""
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: int = 2
        return ((self.get_mean_speed() + coeff_calorie_1)
                * coeff_calorie_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict1 = dict()  # словарь, в котором сопостовл. коды тренировок и классы
    dict1 = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}

    # определим тип тренировки и создадим объект соответствующего класса
    if workout_type == 'SWM':
        return dict1['SWM'](data[0], data[1], data[2], data[3], data[4])
    elif workout_type == 'RUN':
        return dict1['RUN'](data[0], data[1], data[2])
    elif workout_type == 'WLK':
        return dict1['WLK'](data[0], data[1], data[2], data[3])


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()  # создаем инф. сообщение
    print(info.get_message())  # печатаем информационное сообщение


if __name__ == '__main__':
    """Тестируем свой модуль."""
    """Код выполнится когда файл запущен как самостоятельная программа."""

    # Блок датчиков фитнес-трекера передает пакеты данных в виде кортежа
    """
    Плавание:
    Код тренировки: 'SWM'
    Элементы списка: количество гребков, время в часах,
    вес пользователя, длина бассейна,
    сколько раз пользователь переплыл бассейн.

    Бег:
    Код тренировки: 'RUN'
    Элементы списка: количество шагов,
    время тренировки в часах, вес пользователя.

    Спортивная ходьба
    Код тренировки: 'WLK'
    Элементы списка: количество шагов, время тренировки в часах,
    вес пользователя, рост пользователя.
    """
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:  # перебираем список пакетов
        # читаем пакеты и создаем объект класса Training
        training = read_package(workout_type, data)
        main(training)  # Запускаем главную функцию
