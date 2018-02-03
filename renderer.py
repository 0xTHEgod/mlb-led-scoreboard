from utils import refresh_scoreboard, bump_counter
from rgbmatrix import graphics
import time

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

  # Refresh the board every 15 seconds and rotate the games if the command flag is passed
  starttime = time.time()
  canvas.Fill(7, 14, 25)
  while True:
    success = refresh_scoreboard(canvas, game)
    canvas = matrix.SwapOnVSync(canvas)
    time.sleep(15.0 - ((time.time() - starttime) % 15.0))
    if args.rotate:
        game_idx = bump_counter(game_idx, games, bool(args.rotate))
        game = games[game_idx]
        canvas.Fill(7, 14, 25)

    if not success:
        # TODO https://github.com/ajbowler/mlb-led-scoreboard/issues/13
        continue

def render_standings(matrix, canvas, division):
  font = graphics.Font()
  font.LoadFont('Assets/tom-thumb.bdf')
  text_color = graphics.Color(171, 181, 170)

  canvas.Fill(37, 102, 30)

  stat = 'w'
  starttime = time.time()
  while True:
    offset = 6
    for team in division.teams:
      abbrev = '{:3s}'.format(team.team_abbrev)
      text = '%s %s' % (abbrev, getattr(team, stat))
      graphics.DrawText(canvas, font, 1, offset, text_color, text)

      for x in range(0, canvas.width):
        canvas.SetPixel(x, offset, 13, 25, 11)
      for y in range(0, canvas.height):
        canvas.SetPixel(14, y, 13, 35, 11)
      offset += 6

    matrix.SwapOnVSync(canvas)
    time.sleep(5.0 - ((time.time() - starttime) % 5.0))

    canvas.Fill(37, 102, 30)
    stat = 'w' if stat == 'l' else 'l'
