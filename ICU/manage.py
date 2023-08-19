"""Django's command-line utility for administrative tasks."""
import subprocess
import time
import sys
import os


def main():
    """Run administrative tasks."""
    current_directory = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(current_directory, "AI_Server"))
    sys.path.append(os.path.join(current_directory, "Local_Environment"))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ICU_Config.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


# 서버 부하 관리
# import time
#
# # ... 기존 코드 ...
#
# def capture_and_send():
#     # ... 기존 코드 ...
#
#     while True:
#         # ... 기존 코드 ...
#
#         # 매 프레임마다 0.1초 대기
#         time.sleep(0.1)
#
#         # ... 기존 코드 ...