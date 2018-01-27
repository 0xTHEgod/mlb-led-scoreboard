import json
from pprint import pprint
from rgbmatrix import graphics

class ScoreboardRenderer:
  def __init__(self, matrix, scoreboard):
    self.matrix = matrix
    self.scoreboard = scoreboard
    self.colors = json.load(open('Assets/colors.json'))

    self.font = graphics.Font()
    self.font.LoadFont('Assets/tom-thumb.bdf')

  def render_team_colors(self):
    away_team_color_data = self.colors[self.scoreboard.game_data['away_team'].lower()]
    away_team_color = away_team_color_data['home']

    home_team_color_data = self.colors[self.scoreboard.game_data['home_team'].lower()]
    home_team_color = home_team_color_data['home']

    for x in range(self.matrix.width):
      for y in range(14):
        color = home_team_color if y >= 7 else away_team_color
        self.matrix.SetPixel(x, y, color['r'], color['g'], color['b'])

  def render_team_text(self):
    away_team = self.scoreboard.game_data['away_team']
    away_text_color = self.colors[away_team.lower()].get('text', {'r': 255, 'g': 255, 'b': 255})
    away_text_color_graphic = graphics.Color(away_text_color['r'], away_text_color['g'], away_text_color['b'])
    away_text = away_team.upper() + ' ' + str(self.scoreboard.game_data['at_bat']['away_team_runs'])

    home_team = self.scoreboard.game_data['home_team']
    home_text_color = self.colors[home_team.lower()].get('text', {'r': 255, 'g': 255, 'b': 255})
    home_text_color_graphic = graphics.Color(home_text_color['r'], home_text_color['g'], home_text_color['b'])
    home_text = home_team.upper() + ' ' + str(self.scoreboard.game_data['at_bat']['home_team_runs'])

    graphics.DrawText(self.matrix, self.font, 1, 6, away_text_color_graphic, away_text)
    graphics.DrawText(self.matrix, self.font, 1, 13, home_text_color_graphic, home_text)

  def render_pitches(self):
    at_bat = self.scoreboard.game_data['at_bat']
    pitches_color = graphics.Color(255, 235, 59)
    graphics.DrawText(self.matrix, self.font, 1, 23, pitches_color, str(at_bat['balls']) + '-' + str(at_bat['strikes']))

  def render_outs(self):
    outs = self.scoreboard.game_data['at_bat']['outs']
    out_px = []
    out_px.append({'x': 2, 'y': 27})
    out_px.append({'x': 6, 'y': 27})
    out_px.append({'x': 10, 'y': 27})
    for out in range(len(out_px)):
      self.__render_out_circle(out_px[out])
      if (outs >= out):
        self.matrix.SetPixel(out_px[out]['x'], out_px[out]['y'], 255, 235, 59)

  def render_bases(self):
    bases = self.scoreboard.game_data['at_bat']['bases']
    base_px = []
    base_px.append({'x': 16, 'y': 27} )
    base_px.append({'x': 21, 'y': 22} )
    base_px.append({'x': 26, 'y': 27} )

    for base in base_px:
      self.__render_base_outline(base)

  def __render_out_circle(self, out):
    self.matrix.SetPixel(out['x'] - 1, out['y'] - 1, 255, 235, 59)
    self.matrix.SetPixel(out['x'] - 1, out['y'], 255, 235, 59)
    self.matrix.SetPixel(out['x'] - 1, out['y'] + 1, 255, 235, 59)
    self.matrix.SetPixel(out['x'], out['y'] - 1, 255, 235, 59)
    self.matrix.SetPixel(out['x'], out['y'] + 1, 255, 235, 59)
    self.matrix.SetPixel(out['x'] + 1, out['y'] - 1, 255, 235, 59)
    self.matrix.SetPixel(out['x'] + 1, out['y'], 255, 235, 59)
    self.matrix.SetPixel(out['x'] + 1, out['y'] + 1, 255, 235, 59)

  def __render_base_outline(self, base):
    self.matrix.SetPixel(base['x'] - 3, base['y'], 255, 235, 59)
    self.matrix.SetPixel(base['x'] - 2, base['y'] - 1, 255, 235, 59)
    self.matrix.SetPixel(base['x'] - 1, base['y'] - 2, 255, 235, 59)
    self.matrix.SetPixel(base['x'], base['y'] - 3, 255, 235, 59)
    self.matrix.SetPixel(base['x'] + 1, base['y'] - 2, 255, 235, 59)
    self.matrix.SetPixel(base['x'] + 2, base['y'] - 1, 255, 235, 59)
    self.matrix.SetPixel(base['x'] + 3, base['y'], 255, 235, 59)
    self.matrix.SetPixel(base['x'] + 2, base['y'] + 1, 255, 235, 59)
    self.matrix.SetPixel(base['x'] + 1, base['y'] + 2, 255, 235, 59)
    self.matrix.SetPixel(base['x'], base['y'] + 3, 255, 235, 59)
    self.matrix.SetPixel(base['x'] - 1, base['y'] + 2, 255, 235, 59)
    self.matrix.SetPixel(base['x'] - 2, base['y'] + 1, 255, 235, 59)
