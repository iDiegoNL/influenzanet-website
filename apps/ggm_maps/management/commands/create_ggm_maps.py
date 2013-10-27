from decimal import Decimal
from datetime import date, timedelta
from PIL import Image, ImageDraw
import os
from random import random

from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_models
from django.db import transaction, connection
from django.conf import settings

SHRINKING_FACTOR = Decimal('18.163')
RANDOMNESS = 2
SIZE = 1 # r of 'ellipse'

SOURCE_BASE_PATH = os.path.dirname(os.path.abspath(__file__))

SYMPTOM_COLORS = {
    'ALLERGY-or-HAY-FEVER':                         (  0, 255,   0),
    'ALLERGY-or-HAY-FEVER-and-GASTROINTESTINAL':    (  0, 255, 255),
    'COMMON-COLD':                                  (255, 255,   0),
    'COMMON-COLD-and-GASTROINTESTINAL':             (  0,  51, 255),
    'GASTROINTESTINAL':                             (  0, 128,   0),
    'ILI':                                          (255,   0,   0),
    'NON-SPECIFIC-SYMPTOMS':                        (  0,   0, 128),
    'NO-SYMPTOMS':                                  (  0,   0,   0),
}

MEASURMENT = (153, 255, 153)


@transaction.commit_on_success
class Command(BaseCommand):

    def handle(self, *args, **options):
        for i in range(356): # possibly adapt later to allow for longer ranges (recalc full year)
            day = date.today() - timedelta(days=i)
            for symptom in SYMPTOM_COLORS.keys():
                for do_all in [True, False]:
                    self.generate(day, symptom, do_all)

    def generate(self, day, symptom, do_all=False):
        image = Image.open(os.path.join(SOURCE_BASE_PATH, 'green.png'))

        if do_all:
            query, params = self._sql(day, symptom, exclude=True)
            results = self._q(query, params)
            self._draw_dots(image, results, MEASURMENT)
       
        query, params = self._sql(day, symptom)
        results = self._q(query, params)
        self._draw_dots(image, results, SYMPTOM_COLORS[symptom], white_border=True)

        directory = os.path.join(settings.MEDIA_ROOT, 'ggm_maps', self._format_date(day))
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = os.path.join(directory, symptom + ('-all' if do_all else '') + '.png')
        image.save(filename)


        if day == date.today():
            directory = os.path.join(settings.MEDIA_ROOT, 'ggm_maps', 'today')
            if not os.path.exists(directory):
                os.makedirs(directory)

            filename = os.path.join(directory, symptom + ('-all' if do_all else '') + '.png')
            image.save(filename)

    def _draw_dots(self, image, results, color, white_border=False):
        for result in results:
            pc, country, x, y = result

            # these magic numbers scale back to the map
            cx = (x - (Decimal('-5000.35'))) / SHRINKING_FACTOR
            cy = (y - (Decimal('-2327.54'))) / SHRINKING_FACTOR
            
            r = -RANDOMNESS + (RANDOMNESS * 2 * Decimal(str(random())))
            r2 = -RANDOMNESS + (RANDOMNESS * 2 * Decimal(str(random())))

            cx += r
            cy += r2
            
            if white_border:
                bbox = map(int, (cx - SIZE - 1, cy - SIZE - 1, cx + SIZE + 1, cy + SIZE + 1))
                draw = ImageDraw.Draw(image)
                draw.rectangle(bbox, fill=(255, 255, 255))
                del draw

            bbox = map(int, (cx - SIZE, cy - SIZE, cx + SIZE, cy + SIZE))
            draw = ImageDraw.Draw(image)
            draw.rectangle(bbox, fill=color)
            del draw

    def _sql(self, day, symptom, exclude=False):
        query = ("""
SELECT PC.zip_code_key, PC.zip_code_country, PC.xco, PC.yco

  FROM (
SELECT I."Q3" AS zip_code_key, I."Qcountry" AS zip_code_country
  FROM pollster_health_status AS S,
       pollster_results_intake AS I,

       -- get the last weekly submitted for each user and
       -- ensure that is not older than 7 days
      (SELECT DISTINCT ON (global_id) *
         FROM pollster_results_weekly
        WHERE timestamp BETWEEN %(date)s::date-7 AND %(date)s
        ORDER BY global_id, timestamp DESC) AS W

     WHERE S.pollster_results_weekly_id = W.id
       AND W.global_id = I.global_id
       AND S.status """ + ("!=" if exclude else "=") + """ %(status)s
      ) AS statusses
  JOIN "postcodes_rev" PC ON statusses.zip_code_key = PC.zip_code_key AND statusses.zip_code_country = PC.zip_code_country
  GROUP BY PC.zip_code_key, PC.zip_code_country, PC.xco, PC.yco
        """)

        params = {'date': self._format_date(day)}
        if symptom:
            params['status'] = symptom

        return query, params

    def _q(self, query, params):
        cursor = connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        return results


    def _format_date(self, day):
        return '%4d-%02d-%02d' % (day.year, day.month, day.day)
