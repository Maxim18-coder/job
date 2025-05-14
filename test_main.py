import pytest
import tempfile
import os
from main import read_csv, generate_payout_report


# Вспомогательная функция для создания временного файла с содержимым
def create_temp_csv(content_lines):
    tmp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv', encoding='utf-8')
    tmp_file.write('\n'.join(content_lines))
    tmp_file.close()
    return tmp_file.name


def test_read_csv_basic():
    content = [
        "id,email,name,department,hours_worked,hourly_rate",
        "1,alice@example.com,Alice Johnson,Marketing,160,50",
        "2,bob@example.com,Bob Smith,Design,150,40"
    ]
    filename = create_temp_csv(content)

    data = read_csv(filename)

    assert len(data) == 2
    assert data[0]['name'] == 'Alice Johnson'

    os.remove(filename)


def test_get_rate_column():
    headers1 = ['id', 'email', 'name', 'department', 'hours_worked', 'hourly_rate']
    headers2 = ['id', 'email', 'name', 'department', 'hours_worked', 'rate']
    headers3 = ['id', 'email', 'name', 'department', 'hours_worked', 'salary']

    assert get_rate_column(headers1) == 'hourly_rate'
    assert get_rate_column(headers2) == 'rate'
    assert get_rate_column(headers3) == 'salary'


def test_generate_payout_report(capsys):
    content1 = [
        "id,email,name,department,hours_worked,hourly_rate",
        "1,alice@example.com,Alice Johnson,Marketing,160,50",
        "2,bob@example.com,Bob Smith,Design,150,40"
    ]

    content2 = [
        "id,email,name,department,hours_worked,salary",
        "3,carol@example.com,Carol Williams,Design,170,60"
    ]

    file1 = create_temp_csv(content1)
    file2 = create_temp_csv(content2)

    generate_payout_report([file1, file2])

    captured = capsys.readouterr()
    output_lines = captured.out.strip().split('\n')

    # Проверка наличия общего количества сотрудников и суммы выплат
    assert any("Общее количество сотрудников" in line for line in output_lines)
    assert any("Общий фонд оплаты труда" in line for line in output_lines)

    os.remove(file1)
    os.remove(file2)
