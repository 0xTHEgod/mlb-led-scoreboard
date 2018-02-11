from rgbmatrix import graphics
from scoreboard import Scoreboard
from scoreboard_renderer import ScoreboardRenderer
from utils import bump_counter
import ledcolors.scoreboard
import ledcolors.standings
import time

FIFTEEN_MINUTES = 900

def render_games(matrix, canvas, games, args):
  # Get the game to start on. If the provided team does not have a game today,
  # or the team name isn't provided, then the first game in the list is used.
  game_idx = 0
  if args.team:
    game_idx = next(
        (i for i, game in enumerate(games) if game.away_team ==
         args.team or game.home_team == args.team), 0
    )
  game = games[game_idx]

  canvas.Fill(*ledcolors.scoreboard.fill)
  starttime = time.time()
  while True:
    endtime = time.time()
    delta = endtime - starttime
    if delta >= FIFTEEN_MINUTES:
      return

    success = __refresh_scoreboard(canvas, game)
    canvas = matrix.SwapOnVSync(canvas)
    
    # Refresh the board every 15 seconds and rotate the games
    # if the command flag is passed
    time.sleep(15.0 - ((delta) % 15.0))

    if args.rotate:
      game_idx = bump_counter(game_idx, games)
      game = games[game_idx]
      canvas.Fill(*ledcolors.scoreboard.fill)

def render_standings(matrix, canvas, division):
  font = graphics.Font()
  font.LoadFont('Assets/tom-thumb.bdf')
  text_color = graphics.Color(*ledcolors.standings.text)

  canvas.Fill(*ledcolors.standings.fill)

  stat = 'w'
  starttime = time.time()
  while True:
    offset = 6
    for team in division.teams:
      abbrev = '{:3s}'.format(team.team_abbrev)
      text = '%s %s' % (abbrev, getattr(team, stat))
      graphics.DrawText(canvas, font, 1, offset, text_color, text)

      for x in range(0, canvas.width):
        canvas.SetPixel(x, offset, *ledcolors.standings.divider)
      for y in range(0, canvas.height):
        canvas.SetPixel(14, y, *ledcolors.standings.divider)
      offset += 6

    matrix.SwapOnVSync(canvas)
    time.sleep(5.0 - ((time.time() - starttime) % 5.0))

    canvas.Fill(*ledcolors.standings.fill)
    stat = 'w' if stat == 'l' else 'l'

def render_offday(matrix, canvas):
  font = graphics.Font()
  font.LoadFont('Assets/tom-thumb.bdf')
  text_color = graphics.Color(*ledcolors.scoreboard.text)

  canvas.Fill(*ledcolors.scoreboard.fill)
  graphics.DrawText(canvas, font, 12, 8, text_color, 'No')
  graphics.DrawText(canvas, font, 6, 15, text_color, 'games')
  graphics.DrawText(canvas, font, 6, 22, text_color, 'today')
  graphics.DrawText(canvas, font, 12, 29, text_color, ':(')
  matrix.SwapOnVSync(canvas)

  while True:
    pass # I hate the offseason and off days.

def __refresh_scoreboard(canvas, game):
  scoreboard = Scoreboard(game)
  if not scoreboard.game_data:
    return False
  renderer = ScoreboardRenderer(canvas, scoreboard)
  renderer.render()
  return True
