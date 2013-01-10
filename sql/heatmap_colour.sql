DROP FUNCTION heatmap_colour(float);

CREATE FUNCTION heatmap_colour (f float) RETURNS varchar AS $$
DECLARE
  max integer := 30;
  num_colours integer := 2;
  colours integer[2][3] = '{{0,0,255},{255,0,0}}';
/*  num_colours integer := 3;
  colours integer[3][3] = '{{0,0,255},{255,155,0},{255,0,0}}';*/
/*  num_colours integer := 4;
  colours integer[4][3] = '{{0,0,255},{0,255,0},{255,255,0},{255,0,0}}'; */
  idx1 integer;
  idx2 integer;
  fraction_between float = 0;
  colour integer; 
  red integer;
  blue integer;
  green integer;
BEGIN 
  IF f <= 0
  THEN
    idx1 = 1;
    idx2 = 1;
  ELSE
    IF f >= max
    THEN
      idx1 = num_colours;
      idx2 = num_colours;
    ELSE
      f = f * (num_colours - 1);
      idx1 = ceil(f/max);
      idx2 = idx1 + 1;
      fraction_between = f/max::float + 1 - idx1;
    END IF;
  END IF;

  red = round((colours[idx2][1] - colours[idx1][1]) * fraction_between + colours[idx1][1]);
  green = round((colours[idx2][2] - colours[idx1][2]) * fraction_between + colours[idx1][2]);
  blue = round((colours[idx2][3] - colours[idx1][3]) * fraction_between + colours[idx1][3]);
   
  RETURN '#' || lpad(to_hex(red), 2, '0') || lpad(to_hex(green), 2, '0') || lpad(to_hex(blue), 2, '0');
END;

$$ LANGUAGE plpgsql;
