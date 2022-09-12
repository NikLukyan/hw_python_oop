from dataclasses import dataclass
from typing import Optional, Dict, List, Type


@dataclass
class InfoMessage:
    """
    Класс. Информационное сообщение о тренировке.

    Атрибуты
    --------
    training_type: str
        имя класса тренировки
    duration: float
        длительность тренировки в часах
    distance: float
        дистанция в км
    speed: float
        средняя скорость, с которой двигался пользователь
    calories: float
        количество израсходованных килокалорий

    Методы
    ------
    get_message(self) -> str:
        Метод возвращает строку сообщения в необходимом формате
    """

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """ Метод возвращает строку сообщения в необходимом формате"""
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {format(self.duration,".3f")} ч.; '
            f'Дистанция: {format(self.distance,".3f")} км; '
            f'Ср. скорость: {format(self.speed,".3f")} км/ч; '
            f'Потрачено ккал: {format(self.calories,".3f")}.'
        )


class Training:
    """
    Класс. Базовый класс тренировки.

    Переменные
    ----------
    LEN_STEP: float
        Hасстояние, которое спортсмен преодолевает за один шаг или гребок.
        Один шаг — это 0.65 метра, один гребок при плавании — 1.38 метра.
    M_IN_KM: int
        Константа для перевода значений из метров в километры.
        Её значение — 1000.
    HOUR_IN_MIN: int
        Константа для перевода значений из часов в минуты.
        Её значение — 60.

    Атрибуты
    --------
    action: int
        количество совершённых действий
    duration: float
        длительность тренировки
    weight: float
        вес спортсмена

    Методы
    ------
    __init__(self, action: int, duration: float, weight: float) -> None:
        Устанавливает все необходимые атрибуты для объекта Training
    get_distance(self) -> float:
        Получить дистанцию в км.
    get_mean_speed(self) -> float:
        Получить среднюю скорость движения.
    get_spent_calories(self) -> float:
        Получить количество затраченных калорий.
    show_training_info(self) -> InfoMessage:
        Возвращает информационное сообщение о выполненной тренировке.
    """

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    HOUR_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        """
        Устанавливает все необходимые атрибуты для объекта Training

        Параметры
        ---------
        action: int
            количество совершённых действий
            (число шагов при ходьбе и беге либо гребков — при плавании)
        duration: float
            длительность тренировки
        weight: float
            вес спортсмена
        """

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Возвращает информационное сообщение о выполненной тренировке.

        Возвращаемое значение
        ---------------------
        Объект класса InfoMessage в который передаются атрибуты:
        training_type: str
            имя класса тренировки
        duration: float
            длительность тренировки в часах
        distance: float
            дистанция в км
        speed: float
            средняя скорость, с которой двигался пользователь
        calories: float
            количество израсходованных килокалорий

        """

        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """
    Класс. Тренировка: бег.

    Все свойства и методы этого класса без изменений
    наследуются от базового класса Training.
    Исключение составляет только метод расчёта калорий,
    который переопределен.

    Переменные
    ----------
    COEFF_CALORIE_1: int = 18
        Константа №1 использующаяся при рассчете потраченных калорий
    COEFF_CALORIE_2: int = 20
        Константа №2 использующаяся при рассчете потраченных калорий

    Атрибуты
    --------
    action: int
        количество совершённых действий
    duration: float
        длительность тренировки
    weight: float
        вес спортсмена

    Методы
    ------
    get_spent_calories(self) -> float:
        Получить количество затраченных калорий для бега.

    """

    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для бега.

        Возвращаемое значение
        ---------------------
        Расход калорий для бега: float
            рассчитывается по такой формуле:
                (18 * средняя_скорость - 20) * вес_спортсмена
                / M_IN_KM * время_тренировки_в_минутах
        """

        return ((self.COEFF_CALORIE_1
                * self.get_mean_speed()
                - self.COEFF_CALORIE_2)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.HOUR_IN_MIN)


class SportsWalking(Training):
    """
    Класс. Тренировка: спортивная ходьба.

    Все свойства и методы этого класса без изменений
    наследуются от базового класса Training.
    Исключение составляет только метод расчёта калорий,
    который переопределен.
    Конструктор этого класса принимает дополнительный параметр
    height — рост спортсмена.

    Переменные
    ----------
    COEFF_CALORIE_1: float = 0.035
        Константа №1 использующаяся при рассчете потраченных калорий
    COEFF_CALORIE_2: float = 0.029
        Константа №2 использующаяся при рассчете потраченных калорий

    Атрибуты
    --------
    action: int
        количество совершённых действий
    duration: float
        длительность тренировки
    weight: float
        вес спортсмена
    height: int
        рост спортсмена

    Методы
    ------
    get_spent_calories(self) -> float:
        Получить количество затраченных калорий для спортивной ходьбы.
    """

    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        """
        Устанавливает все необходимые атрибуты для объекта SportWalking

        Параметры
        ---------
        action: int
            количество совершённых действий
            (число шагов при ходьбе и беге либо гребков — при плавании)
        duration: float
            длительность тренировки
        weight: float
            вес спортсмена
        height: int
            рост спортсмена
        """

        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для спортивной ходьбы.

        Возвращаемое значение
        ---------------------
        Расход калорий для спортивной ходьбы: float
            рассчитывается по такой формуле:
                (0.035 * вес + (средняя_скорость**2 // рост) * 0.029 * вес)
                * время_тренировки_в_минутах
        """

        return ((self.COEFF_CALORIE_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.COEFF_CALORIE_2 * self.weight)
                * self.duration * self.HOUR_IN_MIN)


class Swimming(Training):
    """Класс. Тренировка: плавание.

    Все свойства и методы этого класса без изменений
    наследуются от базового класса Training.
    Исключение составляет только метод расчёта калорий,
    метод определения средней скорости и
    атрибут базового класса LEN_STEP = 1.38
    (расстояние, преодолеваемое за один гребок)
    которые переопределены.
    Конструктор класса Swimming, кроме свойств базового класса,
    принимает еще два параметра:
        length_pool — длина бассейна в метрах;
        count_pool — сколько раз пользователь переплыл бассейн.

    Переменные
    ----------
    LEN_STEP = 1.38
        один гребок при плавании — 1.38 метра
    COEFF_CALORIE_1: float = 1.1
        Константа №1 использующаяся при рассчете потраченных калорий
    COEFF_CALORIE_2: int = 2
        Константа №2 использующаяся при рассчете потраченных калорий

    Атрибуты
    --------
    action: int
        количество совершённых действий
    duration: float
        длительность тренировки
    weight: float
        вес спортсмена
    length_pool: int
        длина бассейна в метрах
    count_pool: int
        сколько раз пользователь переплыл бассейн

    Методы
    ------
    get_mean_speed(self) -> float:
        Получить среднюю скорость движения при плавании
    get_spent_calories(self) -> float:
        Получить количество затраченных калорий для плавания
    """

    LEN_STEP = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        """
        Устанавливает все необходимые атрибуты для объекта Swimming

        Параметры
        ---------
        action: int
            количество совершённых действий
        duration: float
            длительность тренировки
        weight: float
            вес спортсмена
        length_pool: int
            длина бассейна в метрах
        count_pool: int
            сколько раз пользователь переплыл бассейн
        """

        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """
        Получить среднюю скорость движения при плавании

        Возвращаемое значение
        ---------------------
        Формула расчёта:
            длина_бассейна * count_pool / M_IN_KM / время_тренировки
        """

        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для плавания.

        Возвращаемое значение
        ---------------------
        Формула расчёта:
            (средняя_скорость + 1.1) * 2 * вес
        """

        return ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                * self.COEFF_CALORIE_2 * self.weight)


def read_package(workout_type: str,
                 data: List[float]
                 ) -> Optional[Training]:
    """Прочитать данные полученные от датчиков.

    Параметры
    ---------
    workout_type: str
        код тренировки
    data: Sequence[float]
        список параметров

    Переменные
    ----------
    dict1: dict
        словарь, в котором сопостовляются коды тренировок и классы

    Возвращаемое значение
    ---------------------
    None или объект класса Training в который передали
    необходимые параметры из списка data
    """

    code_class: Dict[str, Type[Training]] = {'SWM': Swimming,
                                             'RUN': Running,
                                             'WLK': SportsWalking}
    return code_class[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция. Печатает информационное сообщение.

    Параметры
    ---------
    Объект класса Training

    Переменные
    ----------
    info: InfoMessage
        создаем информационное сообщение -
        объект класса InfoMessage

    Возвращаемое значение
    ---------------------
    None
        печатаем информационное сообщение
    """

    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    """Тестируем свой модуль.
    Код выполнится когда файл запущен как самостоятельная программа.
    Блок датчиков фитнес-трекера передает пакеты данных в виде кортежа

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

    for workout_type, data in packages:
        """Перебираем в цикле список пакетов,
        распаковываем каждый кортеж
        и передаём данные в функцию read_package().
        """

        training = read_package(workout_type, data)
        main(training)
