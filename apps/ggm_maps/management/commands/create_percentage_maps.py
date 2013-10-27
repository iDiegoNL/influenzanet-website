from decimal import Decimal
from datetime import date, timedelta
from PIL import Image, ImageDraw, ImageFont
import os
from random import random
from math import floor

from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_models
from django.db import transaction, connection
from django.conf import settings
from django.utils.translation import ugettext, activate

from apps.survey.views import _decode_person_health_status

SHRINKING_FACTOR = Decimal('18.163')
RANDOMNESS = 2
SIZE = 1 # r of 'ellipse'

STEP = 0.6 # percentages are: 0 - 0.6%; 0.6 - 1.2% etc.

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

LEGEND = (
    (1, (23, 59)),
    (2, (23, 80)),
    (3, (23, 101)),
    (4, (23, 122)),
    (5, (23, 143)),
    (6, (23, 164)),
    (7, (23, 185)),
    (8, (23, 206)),
    (9, (23, 227)),
    (10, (23, 248)),
)

FILLS = (
    (("BE", '1000'), (225, 542),),
    (("BE", '2000'), (259, 457),),
    (("BE", '3000'), (344, 500),),
    (("BE", '4000'), (378, 589),),
    (("BE", '5000'), (263, 642),),
    (("BE", '6000'), (231, 613),),
    (("BE", '6600'), (344, 694),),
    (("BE", '7000'), (149, 587),),
    (("BE", '8000'), (54, 488),),
    (("BE", '9000'), (150, 507),),

    (("NL", '1000'), (277, 237),),
    (("NL", '1200'), (285, 206),),
    (("NL", '1200'), (306, 255),),
    (("NL", '1200'), (322, 238),),
    (("NL", '1500'), (271, 97),),
    (("NL", '1500'), (281, 161),),
    (("NL", '2000'), (241, 271),),
    (("NL", '2500'), (251, 311),),
    (("NL", '3000'), (211, 328),),
    (("NL", '3200'), (193, 359),),
    (("NL", '3200'), (238, 354),),
    (("NL", '3400'), (341, 282),),
    (("NL", '3400'), (343, 242),),
    (("NL", '4000'), (168, 351),),
    (("NL", '4000'), (175, 359),),
    (("NL", '4000'), (312, 333),),
    (("NL", '4300'), (146, 404),),
    (("NL", '4300'), (170, 444),),
    (("NL", '4600'), (193, 380),),
    (("NL", '4600'), (228, 387),),
    (("NL", '5000'), (331, 363),),
    (("NL", '5500'), (390, 418),),
    (("NL", '6000'), (392, 461),),
    (("NL", '6500'), (397, 316),),
    (("NL", '7000'), (455, 281),),
    (("NL", '7500'), (456, 182),),
    (("NL", '8000'), (366, 212),),
    (("NL", '8000'), (408, 225),),
    (("NL", '8300'), (394, 162),),
    (("NL", '8500'), (286, 67),),
    (("NL", '8500'), (329, 36),),
    (("NL", '8500'), (358, 117),),
    (("NL", '9000'), (367, 26),),
    (("NL", '9000'), (412, 83),),
    (("NL", '9000'), (428, 18),),
    (("NL", '9500'), (457, 6),),
    (("NL", '9500'), (470, 5),),
    (("NL", '9500'), (476, 59),),
)

COLORS = ( 
    (255, 255, 0),
    (255, 230, 0),
    (255, 210, 0),
    (255, 180, 0),
    (255, 150, 0),
    (255, 120, 0),
    (255, 90, 0),
    (220, 60, 0),
    (128, 30, 0),
    (102, 0, 0),
)


@transaction.commit_on_success
class Command(BaseCommand):

    def handle(self, *args, **options):
        activate(settings.LANGUAGE_CODE)
        for i in range(356): # possibly adapt later to allow for longer ranges (recalc full year)
            day = date.today() - timedelta(days=i)
            for symptom in SYMPTOM_COLORS.keys():
                self.generate(day, symptom)

    def generate(self, day, symptom):
        image = Image.open(os.path.join(SOURCE_BASE_PATH, 'white.png'))

        for i, (key, (cx, cy)) in enumerate(LEGEND):
            self._draw_fill(image, LEGEND, key, i * STEP)

            font = ImageFont.truetype(os.path.join(SOURCE_BASE_PATH, 'arial.ttf'), 12)
            draw = ImageDraw.Draw(image)
            draw.text((cx + 15, cy - 5), ("%0.1f - %0.1f%%" % (i * STEP, (i + 1) * STEP)) if i < len(LEGEND) - 1 else ("%0.1f en meer" % (i * STEP)), (0, 0, 0), font=font)
            del draw


        for country, zipcode, zipcode_where, zipcode_params in self._zipcode_sql():
            total = self._count(day, None, zipcode_where, zipcode_params)
            with_symptoms = self._count(day, symptom, zipcode_where, zipcode_params)

            percentage = with_symptoms / float(total) * 100 if total else 0

            self._draw_fill(image, FILLS, (country, zipcode), percentage)

        font = ImageFont.truetype(os.path.join(SOURCE_BASE_PATH, 'arial.ttf'), 12)
        draw = ImageDraw.Draw(image)
        draw.text((15, 32), u"Percentages '%s' per regio" % (_decode_person_health_status(symptom) + u""), (0, 0, 0), font=font)
        del draw

        # save the file
        directory = os.path.join(settings.MEDIA_ROOT, 'ggm_maps', 'percentages', self._format_date(day))
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = os.path.join(directory, symptom + '.png')
        image.save(filename)

        if day == date.today():
            directory = os.path.join(settings.MEDIA_ROOT, 'ggm_maps', 'percentages', 'today')
            if not os.path.exists(directory):
                os.makedirs(directory)

            filename = os.path.join(directory, symptom + '.png')
            image.save(filename)

    def _count(self, day, symptom, extra_where, extra_params):
        query, params = self._base_sql(day, symptom)
        query = query + " AND " + extra_where
        params.update(extra_params)
        results = self._q(query, params)
        # results is a single row w/ a single count (which may be Null if no rows are found)
        return results[0][0]

    def _zipcode_sql(self):
        prev_country = None
        found = {}

        CODES = []
        for (country, lo), _ in FILLS:
            if (country, lo) not in CODES:
                CODES.append((country, lo))

        for i, (country, lo) in enumerate(CODES):
            if (country, lo) in found:
                continue

            params = {"country": country}
            country_clause = 'I."Qcountry" = %(country)s'

            if prev_country != country:
                prev_country = country
                min_clause = ""

            else:
                min_clause = ' AND I."Q3" >= %(lo)s '
                params['lo'] = lo


            if (i == len(CODES) - 1) or (CODES[i + 1][0] != country):
                max_clause = ""

            else:
                max_clause = ' AND I."Q3" < %(hi)s '
                params['hi'] = CODES[i + 1][1]
            
            found[country, lo] = 1

            yield country, lo, country_clause + min_clause + max_clause, params

    def _color(self, percentage):
        index = int(floor(percentage / STEP))
        if index >= len(COLORS):
            index = len(COLORS) - 1
        return COLORS[index]

    def _draw_fill(self, image, d, key, percentage):
        color = self._color(percentage)

        for current_key, (cx, cy) in d:
            if current_key == key:
                ImageDraw.floodfill(image, (cx, cy), color)

    def _base_sql(self, day, symptom):
        # I."Q3" == zip_code_key,
        # I."Qcountry" == zip_code_country

        query = ("""
SELECT COUNT(*)
  FROM pollster_health_status AS S,
       pollster_results_intake AS I,

       -- get the last weekly submitted for each user and
       -- ensure that is not older than 7 days
      (SELECT DISTINCT ON (global_id) *
         FROM pollster_results_weekly
        WHERE timestamp BETWEEN %(date)s::date-7 AND %(date)s
        ORDER BY global_id, timestamp DESC) AS W

     WHERE S.pollster_results_weekly_id = W.id
       AND W.global_id = I.global_id"""

       + (""" AND S.status = %(status)s """ if symptom else "")

       )

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
