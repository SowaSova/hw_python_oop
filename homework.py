M_IN_KM = 1000
MIN_IN_H = 60


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message = (f'Тип тренировки: {self.training_type};'
                   f'Длительность: {self.duration:.3f} ч.;'
                   f'Дистанция: {self.distance:.3f} км;'
                   f'\nСр. скорость: {self.speed:.3f} км/ч;'
                   f'Потрачено ккал: {self.calories:.3f}.'
                   '\n')
        return message


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP = 0.65

    def get_spent_calories(self) -> float:
        coeff_run1 = 18
        coeff_run2 = 20
        run_spent_calories = (coeff_run1 * self.get_mean_speed() - coeff_run2) * \
            self.weight / M_IN_KM * (self.duration * MIN_IN_H)
        return run_spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_wlk1 = 0.035
        coeff_wlk2 = 0.029
        wlk_spent_calories = (coeff_wlk1 * self.weight + (self.get_mean_speed()
                              ** 2 // self.height) * coeff_wlk2 * self.height) * (self.duration * MIN_IN_H)
        return wlk_spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 lenght_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        swm_mean_speed = self.lenght_pool * self.count_pool / M_IN_KM / self.duration
        return swm_mean_speed

    def get_spent_calories(self) -> float:
        coeff_swm1 = 1.1
        coeff_swm2 = 2
        swm_spent_calories = (self.get_mean_speed() + coeff_swm1) * \
            coeff_swm2 * self.weight
        return swm_spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    training_data = training[workout_type](*data)
    return training_data


def main(training: Training) -> None:
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
