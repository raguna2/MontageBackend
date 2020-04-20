import csv
from dataclasses import dataclass
from pathlib import Path

from apps.portraits.models import Question
from django.core.management.base import BaseCommand
from django.utils import timezone

here = Path(__file__).parents[2]
INPUT_CSV_DIR = here / 'sample_csv'


@dataclass
class InsertQuestion:
    about: str
    category_id: int
    isPersonal: bool = False


class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']
        input_path = Path(INPUT_CSV_DIR)
        input_file = input_path / filename
        inserted_list = []
        with input_file.open('r') as fp:
            # skipinitialspace: コンマの後の空白がスキップされる。
            reader = csv.reader(fp, skipinitialspace=True)
            next(reader)
            for row in reader:
                if not row:
                    continue
                try:
                    target = InsertQuestion(
                        about=row[0],
                        category_id=int(row[1]),
                    )
                except ValueError as e:
                    print('不正な値が入っています')
                    print(e)
                    return

                inserted_list.append(target)

        all_abouts = [q.about for q in Question.objects.filter(is_personal=False)]
        for item in inserted_list:
            if item.about not in all_abouts:
                Question.objects.create(
                    about=item.about,
                    category_id=item.category_id,
                    is_personal=item.isPersonal
                )
