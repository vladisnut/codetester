import os

from dotenv import load_dotenv

load_dotenv()

# =============================================================================
#                                    ОБЩЕЕ
# =============================================================================

# Создавать отдельные решения для загруженных задач (в папке SOLUTIONS_DIRECTORY).
CREATE_NEW_SOLUTIONS = False

# Когда имя решения не указано, использовать то, которое было изменено последним.
LAUNCH_LAST_MODIFIED_SOLUTION = True

# Ширина шапки вывода информационных блоков (результатов тестов).
HEADER_WIDTH = 40

# Имя класса решения для тестирования метода класса.
SOLUTION_CLASS_NAME = "Solution"

# Имя функции точки входа для тестирования через поток ввода-вывода.
MAIN_FUNCTION_NAME = "main"


# =============================================================================
#                                ФАЙЛЫ И ПАПКИ
# =============================================================================

SOLUTIONS_DIRECTORY = "solutions"
ASSETS_DIRECTORY = "assets"

TEMPLATES_DIRECTORY = os.path.join(ASSETS_DIRECTORY, "templates")
SOLUTION_TEMPLATES_DIRECTORY = os.path.join(TEMPLATES_DIRECTORY, "solution")
SOLUTION_SETTINGS_TEMPLATE_NAME = "settings"
DEFAULT_SOLUTION_TEMPLATE_NAME = "stream"

SOLUTION_DEFAULT_NAME = "main"
SOLUTION_MODULE_NAME = "solution"
SOLUTION_SETTINGS_MODULE_NAME = "settings"
SOLUTION_TESTS_FILE_NAME = "tests.txt"
SOLUTION_DATA_FILE_NAME = "data.json"
SOLUTION_DESCRIPTION_FILE_NAME = "description.md"
