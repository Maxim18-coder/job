import argparse
import sys
import os

def parse_args():
    parser = argparse.ArgumentParser(description='Генерация отчетов по сотрудникам.')
    parser.add_argument('files', nargs='+', help='Пути к CSV файлам с данными сотрудников')
    parser.add_argument('--report', required=True, choices=['payout'], help='Тип отчета')
    return parser.parse_args()

def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    if not lines:
        return []

    headers = [h.strip() for h in lines[0].split(',')]
    data = []

    for line in lines[1:]:
        values = [v.strip() for v in line.split(',')]
        if len(values) != len(headers):
            continue
        row = dict(zip(headers, values))
        data.append(row)
    return data

def get_rate_column(headers):
    possible_names = ['hourly_rate', 'rate', 'salary']
    for name in possible_names:
        if name in headers:
            return name
    return None

def generate_payout_report(files):
    total_payout = 0.0
    employees_count = 0

    for file_path in files:
        data = read_csv(file_path)
        if not data:
            continue

        headers = data[0].keys()
        rate_col = get_rate_column(headers)

        for row in data:
            try:
                hours_worked = float(row.get('hours_worked', '0'))
                rate_value_str = row.get(rate_col, '0')
                rate_value = float(rate_value_str)

                payout = hours_worked * rate_value
                total_payout += payout
                employees_count += 1
            except (ValueError, TypeError):
                continue

    print(f"Общее количество сотрудников: {employees_count}")
    print(f"Общий фонд оплаты труда: {total_payout:.2f} руб.")

def main():
    args = parse_args()

    if args.report == 'payout':
        generate_payout_report(args.files)
    else:
        print(f"Отчет типа '{args.report}' не реализован.")
        sys.exit(1)

if __name__ == '__main__':
    main()