
from abc import abstractmethod
from dataclasses import asdict, dataclass
from typing import Dict, List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Вывод сообщения с результатами тренировки"""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    @abstractmethod
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Определение количества затраченных\
                                  калорий для {self.__class__.__name__}.'
                                  )

    def show_training_info(self) -> str:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),
                           )


class Running(Training):
    """Тренировка: бег."""
    RUN_COEFF1: int = 18
    RUN_COEFF2: int = 20

    def get_spent_calories(self) -> float:
        """Расчёт потраченных калорий для бега"""
        run_spent_calories = ((self.RUN_COEFF1 * self.get_mean_speed()
                               - self.RUN_COEFF2) * self.weight
                              / self.M_IN_KM
                              * (self.duration * self.MIN_IN_H))
        return run_spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WLK_COEFF1: float = 0.035
    WLK_COEFF2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Расчёт потраченных калорий для спортивной ходьбы"""
        wlk_spent_calories = (self.WLK_COEFF1 * self.weight
                              + (self.get_mean_speed() ** 2
                                 // self.height) * self.WLK_COEFF2
                              * self.height) * (self.duration
                                                * self.MIN_IN_H)
        return wlk_spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWM_COEFF1: float = 1.1
    SWM_COEFF2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Расчёт средней скорости плавания."""
        swm_mean_speed = ((self.length_pool * self.count_pool)
                          / self.M_IN_KM / self.duration)
        return swm_mean_speed

    def get_spent_calories(self) -> float:
        """Расчёт потраченных калорий для плавания."""

        swm_spent_calories = ((self.get_mean_speed() + self.SWM_COEFF1)
                              * self.SWM_COEFF2 * self.weight)
        return swm_spent_calories


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training: Dict[str, float] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    training_data = training[workout_type](*data)

    if workout_type not in training:
        raise ValueError('Данные ошибочны.')

    return training_data


def main(training: Training):
    """Главная функция."""
    info = Training.show_training_info(training)
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
